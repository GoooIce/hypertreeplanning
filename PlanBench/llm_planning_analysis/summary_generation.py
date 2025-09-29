#!/usr/bin/env python3
"""
PlanBench Summary Generation Module

This module provides functionality to generate comprehensive summaries
of PlanBench evaluation results, including individual task summaries,
domain-level aggregations, and overall benchmark reports.
"""

import json
import os
import glob
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from datetime import datetime

# Optional imports for enhanced functionality
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Warning: pandas not available. Some functionality will be limited.")

class PlanBenchSummarizer:
    """
    A comprehensive summarizer for PlanBench evaluation results.
    
    This class provides methods to:
    1. Generate individual task summaries
    2. Create domain-level aggregated reports
    3. Produce overall benchmark summaries
    4. Export results in various formats (JSON, CSV, markdown)
    """
    
    def __init__(self, results_dir: str = "results"):
        """
        Initialize the summarizer.
        
        Args:
            results_dir: Path to the directory containing result files
        """
        self.results_dir = results_dir
        self.domains = [
            "blocksworld", "mystery_blocksworld", "obfuscated_randomized_blocksworld",
            "logistics", "obfuscated_randomized_logistics", "sokoban",
            "unsolvable_blocksworld", "unsolvable_obfuscated_randomized_blocksworld"
        ]
        self.models = [
            "o1-preview_chat", "o1-mini_chat", "llama-3.1-405b_aws",
            "gpt-4o_chat", "gpt-4o-mini-2024-07-18_chat", "gpt-4-turbo_chat", "gpt-4_chat",
            "gemini-1.5-pro", "gemini-1.5-flash", "claude-3.5-sonnet_aws", "claude-3-opus"
        ]
        self.task_types = [
            "task_1_plan_generation_zero_shot.json",
            "task_1_plan_generation.json",
            "task_1_plan_generation_zero_shot_pddl.json"
        ]
        
    def load_result_file(self, file_path: str) -> Optional[Dict]:
        """Load and return the contents of a result file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load {file_path}: {e}")
            return None
    
    def analyze_task_results(self, data: Dict) -> Dict:
        """
        Analyze results from a single task file.
        
        Returns:
            Dictionary containing summary statistics for the task
        """
        if not data or "instances" not in data:
            return {}
            
        instances = data["instances"]
        total_instances = len(instances)
        
        # Count correct instances
        correct_count = 0
        evaluated_count = 0
        plan_length_stats = defaultdict(list)
        
        for instance in instances:
            # Check if instance was evaluated
            has_correct = "llm_correct" in instance or "correct" in instance
            if not has_correct:
                continue
                
            evaluated_count += 1
            
            # Get correctness
            is_correct = instance.get("llm_correct", instance.get("correct", False))
            if is_correct:
                correct_count += 1
                
            # Analyze plan length if available
            if "ground_truth_plan" in instance:
                gt_plan = instance["ground_truth_plan"]
                if isinstance(gt_plan, list):
                    gt_plan = '\n'.join(gt_plan)
                elif isinstance(gt_plan, dict):
                    # Skip if ground_truth_plan is a dict (unexpected format)
                    continue
                elif gt_plan is None:
                    continue
                else:
                    gt_plan = str(gt_plan)
                plan_length = len([line for line in gt_plan.split('\n') if line.strip()])
                plan_length_stats[plan_length].append(1 if is_correct else 0)
        
        # Calculate statistics
        accuracy = correct_count / evaluated_count if evaluated_count > 0 else 0
        
        # Plan length analysis
        plan_length_analysis = {}
        for length, results in plan_length_stats.items():
            plan_length_analysis[length] = {
                "instances": len(results),
                "correct": sum(results),
                "accuracy": sum(results) / len(results) if results else 0
            }
        
        return {
            "total_instances": total_instances,
            "evaluated_instances": evaluated_count,
            "correct_instances": correct_count,
            "accuracy": round(accuracy, 4),
            "accuracy_percentage": round(accuracy * 100, 2),
            "plan_length_analysis": plan_length_analysis
        }
    
    def generate_task_summary(self, domain: str, model: str, task: str) -> Dict:
        """Generate summary for a specific task."""
        file_patterns = [
            f"{self.results_dir}/{domain}/{model}/{task}",
            f"{self.results_dir}/{domain}_3/{model}/{task}"
        ]
        
        combined_results = {"instances": []}
        
        for pattern in file_patterns:
            data = self.load_result_file(pattern)
            if data and "instances" in data:
                combined_results["instances"].extend(data["instances"])
                combined_results.update({k: v for k, v in data.items() if k != "instances"})
        
        analysis = self.analyze_task_results(combined_results)
        
        return {
            "domain": domain,
            "model": model,
            "task": task,
            "timestamp": datetime.now().isoformat(),
            **analysis
        }
    
    def generate_domain_summary(self, domain: str) -> Dict:
        """Generate summary for all models and tasks in a domain."""
        domain_results = {}
        
        for model in self.models:
            model_results = {}
            for task in self.task_types:
                task_summary = self.generate_task_summary(domain, model, task)
                if task_summary.get("evaluated_instances", 0) > 0:
                    model_results[task] = task_summary
            
            if model_results:
                domain_results[model] = model_results
        
        return {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "models": domain_results
        }
    
    def generate_overall_summary(self) -> Dict:
        """Generate overall summary across all domains and models."""
        overall_results = {}
        
        for domain in self.domains:
            domain_summary = self.generate_domain_summary(domain)
            if domain_summary.get("models"):
                overall_results[domain] = domain_summary
        
        return {
            "summary_type": "overall_benchmark",
            "timestamp": datetime.now().isoformat(),
            "domains": overall_results
        }
    
    def generate_leaderboard_data(self) -> List[Dict]:
        """Generate leaderboard data in a format suitable for tables."""
        leaderboard = []
        
        for domain in self.domains:
            for model in self.models:
                model_entry = {
                    "model": model,
                    "domain": domain
                }
                
                for task in self.task_types:
                    task_summary = self.generate_task_summary(domain, model, task)
                    task_key = task.replace(".json", "")
                    model_entry[f"{task_key}_accuracy"] = task_summary.get("accuracy_percentage", 0)
                    model_entry[f"{task_key}_instances"] = task_summary.get("evaluated_instances", 0)
                
                # Only add if model has results for this domain
                if any(model_entry[key] > 0 for key in model_entry if "instances" in key):
                    leaderboard.append(model_entry)
        
        return leaderboard
    
    def export_summary_json(self, summary: Dict, output_path: str):
        """Export summary to JSON file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Summary exported to {output_path}")
    
    def export_leaderboard_csv(self, output_path: str):
        """Export leaderboard data to CSV."""
        if not HAS_PANDAS:
            print("Warning: pandas not available. Cannot export to CSV.")
            return
            
        leaderboard_data = self.generate_leaderboard_data()
        df = pd.DataFrame(leaderboard_data)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Leaderboard exported to {output_path}")
    
    def generate_markdown_report(self, summary: Dict) -> str:
        """Generate a markdown report from summary data."""
        report = []
        report.append("# PlanBench Evaluation Summary Report")
        report.append(f"\nGenerated on: {summary.get('timestamp', 'Unknown')}")
        report.append("\n## Overview")
        
        if "domains" in summary:
            # Overall summary
            total_evaluations = 0
            total_correct = 0
            
            for domain_name, domain_data in summary["domains"].items():
                report.append(f"\n### {domain_name}")
                
                for model_name, model_data in domain_data.get("models", {}).items():
                    report.append(f"\n#### Model: {model_name}")
                    
                    for task_name, task_data in model_data.items():
                        eval_instances = task_data.get("evaluated_instances", 0)
                        correct_instances = task_data.get("correct_instances", 0)
                        accuracy = task_data.get("accuracy_percentage", 0)
                        
                        total_evaluations += eval_instances
                        total_correct += correct_instances
                        
                        report.append(f"- **{task_name}**: {correct_instances}/{eval_instances} correct ({accuracy:.2f}%)")
            
            if total_evaluations > 0:
                overall_accuracy = (total_correct / total_evaluations) * 100
                report.append(f"\n## Overall Statistics")
                report.append(f"- Total Evaluations: {total_evaluations}")
                report.append(f"- Total Correct: {total_correct}")
                report.append(f"- Overall Accuracy: {overall_accuracy:.2f}%")
        
        return "\n".join(report)
    
    def export_markdown_report(self, output_path: str):
        """Export a comprehensive markdown report."""
        summary = self.generate_overall_summary()
        markdown_content = self.generate_markdown_report(summary)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(markdown_content)
        print(f"Markdown report exported to {output_path}")
    
    def print_quick_summary(self):
        """Print a quick summary to console."""
        print("\n" + "="*60)
        print("PlanBench Quick Summary")
        print("="*60)
        
        for domain in self.domains:
            domain_has_results = False
            
            for model in self.models:
                model_results = []
                
                for task in self.task_types:
                    task_summary = self.generate_task_summary(domain, model, task)
                    if task_summary.get("evaluated_instances", 0) > 0:
                        model_results.append(task_summary)
                        domain_has_results = True
                
                if model_results:
                    print(f"\n{domain} - {model}:")
                    for result in model_results:
                        accuracy = result.get("accuracy_percentage", 0)
                        instances = result.get("evaluated_instances", 0)
                        correct = result.get("correct_instances", 0)
                        task = result.get("task", "").replace(".json", "")
                        print(f"  {task}: {correct}/{instances} ({accuracy:.1f}%)")
            
            if not domain_has_results:
                print(f"\n{domain}: No results found")


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate PlanBench summaries")
    parser.add_argument("--results-dir", default="results", help="Path to results directory")
    parser.add_argument("--output-dir", default="summaries", help="Output directory for summaries")
    parser.add_argument("--format", choices=["json", "csv", "markdown", "all"], default="all",
                       help="Output format")
    parser.add_argument("--domain", help="Specific domain to summarize")
    parser.add_argument("--model", help="Specific model to summarize")
    parser.add_argument("--quick", action="store_true", help="Print quick summary to console")
    
    args = parser.parse_args()
    
    summarizer = PlanBenchSummarizer(args.results_dir)
    
    if args.quick:
        summarizer.print_quick_summary()
        return
    
    # Generate outputs based on format selection
    if args.format in ["json", "all"]:
        if args.domain and args.model:
            # Single task summary
            for task in summarizer.task_types:
                summary = summarizer.generate_task_summary(args.domain, args.model, task)
                if summary.get("evaluated_instances", 0) > 0:
                    output_path = f"{args.output_dir}/task_summaries/{args.domain}_{args.model}_{task}.json"
                    summarizer.export_summary_json(summary, output_path)
        elif args.domain:
            # Domain summary
            summary = summarizer.generate_domain_summary(args.domain)
            output_path = f"{args.output_dir}/domain_summaries/{args.domain}_summary.json"
            summarizer.export_summary_json(summary, output_path)
        else:
            # Overall summary
            summary = summarizer.generate_overall_summary()
            output_path = f"{args.output_dir}/overall_summary.json"
            summarizer.export_summary_json(summary, output_path)
    
    if args.format in ["csv", "all"]:
        output_path = f"{args.output_dir}/leaderboard.csv"
        summarizer.export_leaderboard_csv(output_path)
    
    if args.format in ["markdown", "all"]:
        output_path = f"{args.output_dir}/summary_report.md"
        summarizer.export_markdown_report(output_path)


if __name__ == "__main__":
    main()