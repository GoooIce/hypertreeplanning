# PlanBench Summary Functionality

This directory now includes comprehensive summary generation capabilities for PlanBench evaluation results.

## Features

- **Individual Task Summaries**: Generate detailed summaries for specific domain/model/task combinations
- **Domain-level Aggregations**: Summarize results across all models for a specific domain  
- **Overall Benchmark Reports**: Comprehensive summaries across all domains and models
- **Multiple Output Formats**: JSON, CSV, and Markdown reports
- **Command-line Interface**: Easy-to-use CLI for generating summaries

## Usage

### Quick Summary (Console Output)
```bash
python summarize.py --quick
```

### Basic Summary (No Dependencies)
```bash
python summarize.py --basic
```

### Comprehensive Summary (All Formats)
```bash
python summarize.py --comprehensive
```

### Domain-specific Summary
```bash
python summarize.py --domain blocksworld
```

### Task-specific Summary
```bash
python summarize.py --domain blocksworld --model o1-preview_chat
```

## Output Files

When generating comprehensive summaries, the following files are created:

- `summaries/overall_summary.json` - Complete results in JSON format
- `summaries/leaderboard.csv` - Tabular data suitable for leaderboards  
- `summaries/comprehensive_report.md` - Human-readable markdown report
- `summaries/domain_summaries/` - Individual domain summaries
- `summaries/task_summaries/` - Individual task summaries

## Integration with Existing Code

The summary functionality is integrated with existing PlanBench code:

- **response_evaluation.py**: Enhanced to always display task summaries after evaluation
- **stats_generation.py**: Enhanced with comprehensive summary generation
- **summary_generation.py**: New module providing core summary functionality  
- **summarize.py**: Command-line interface for easy access

## Example Output

### Console Summary
```
==================================================
TASK SUMMARY: task_1_plan_generation_zero_shot.json
==================================================
Total instances: 600
Correct instances: 587
Accuracy: 0.9783 (97.83%)
==================================================
```

### Markdown Report
The markdown reports include:
- Overview by domain and model
- Detailed accuracy statistics  
- Overall benchmark statistics
- Plan length analysis (where available)

## Dependencies

- **Core functionality**: Works with Python standard library only
- **Enhanced features**: Requires `pandas` for CSV export
- **Plotting**: Requires `matplotlib`, `seaborn` for advanced visualizations

## Files Added/Modified

### New Files:
- `summary_generation.py` - Core summary functionality
- `summarize.py` - Command-line interface
- `summaries/` - Output directory for generated summaries

### Modified Files:
- `response_evaluation.py` - Enhanced with summary output
- `stats_generation.py` - Added comprehensive summary generation

This addresses the issue "PlanBench 没有总结" (PlanBench has no summary) by providing comprehensive summary generation capabilities.