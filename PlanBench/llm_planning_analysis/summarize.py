#!/usr/bin/env python3
"""
PlanBench Summary CLI

Simple command-line interface for generating PlanBench summaries.
Usage: python summarize.py [options]
"""

import sys
import os
import argparse

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from summary_generation import PlanBenchSummarizer
    HAS_SUMMARIZER = True
except ImportError as e:
    print(f"Error importing summarizer: {e}")
    HAS_SUMMARIZER = False

def basic_summary():
    """Generate a basic summary without dependencies."""
    print("\n" + "="*60)
    print("BASIC PLANBENCH SUMMARY")
    print("="*60)
    
    domains = ["mystery_blocksworld", "blocksworld", "obfuscated_randomized_blocksworld"]
    models = ["o1-preview_chat", "o1-mini_chat", "llama-3.1-405b_aws", "gpt-4o_chat"]
    tasks = ["task_1_plan_generation_zero_shot.json", "task_1_plan_generation.json"]
    
    for domain in domains:
        domain_has_results = False
        print(f"\n{domain.upper()}:")
        for model in models:
            for task in tasks:
                file_path = f"results/{domain}/{model}/{task}"
                try:
                    import json
                    with open(file_path) as f:
                        data = json.load(f)
                    
                    total = len(data["instances"])
                    correct = sum(1 for inst in data["instances"] 
                                if inst.get("llm_correct", inst.get("correct", False)))
                    accuracy = correct / total if total > 0 else 0
                    
                    print(f"  {model} - {task}: {correct}/{total} ({accuracy*100:.1f}%)")
                    domain_has_results = True
                except FileNotFoundError:
                    continue
        if not domain_has_results:
            print(f"  No results found")

def main():
    parser = argparse.ArgumentParser(description="Generate PlanBench summaries")
    parser.add_argument("--quick", action="store_true", 
                       help="Display quick summary to console only")
    parser.add_argument("--comprehensive", action="store_true", 
                       help="Generate comprehensive summary with all output formats")
    parser.add_argument("--basic", action="store_true",
                       help="Generate basic summary without dependencies")
    parser.add_argument("--domain", help="Specific domain to summarize")
    parser.add_argument("--model", help="Specific model to summarize")
    parser.add_argument("--output-dir", default="summaries", 
                       help="Output directory for summary files")
    parser.add_argument("--results-dir", default="results",
                       help="Directory containing result files")
    
    args = parser.parse_args()
    
    if args.basic or not HAS_SUMMARIZER:
        basic_summary()
        return
    
    if args.quick:
        summarizer = PlanBenchSummarizer(args.results_dir)
        summarizer.print_quick_summary()
    elif args.comprehensive:
        try:
            from stats_generation import generate_comprehensive_summary
            generate_comprehensive_summary()
        except ImportError:
            print("Warning: Could not import stats_generation. Using basic functionality.")
            summarizer = PlanBenchSummarizer(args.results_dir)
            summarizer.print_quick_summary()
    elif args.domain or args.model:
        summarizer = PlanBenchSummarizer(args.results_dir)
        
        if args.domain and args.model:
            print(f"Generating summaries for {args.domain} with {args.model}")
            for task in summarizer.task_types:
                summary = summarizer.generate_task_summary(args.domain, args.model, task)
                if summary.get("evaluated_instances", 0) > 0:
                    output_path = f"{args.output_dir}/task_summaries/{args.domain}_{args.model}_{task}.json"
                    summarizer.export_summary_json(summary, output_path)
        elif args.domain:
            print(f"Generating summary for domain: {args.domain}")
            summary = summarizer.generate_domain_summary(args.domain)
            output_path = f"{args.output_dir}/domain_summaries/{args.domain}_summary.json"
            summarizer.export_summary_json(summary, output_path)
        else:
            print("Please specify both --domain and --model, or just --domain")
    else:
        # Default: try comprehensive, fall back to quick
        if HAS_SUMMARIZER:
            summarizer = PlanBenchSummarizer(args.results_dir)
            summarizer.print_quick_summary()
        else:
            basic_summary()

if __name__ == "__main__":
    main()