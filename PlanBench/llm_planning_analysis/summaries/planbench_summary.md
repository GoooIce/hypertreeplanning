# PlanBench Evaluation Summary Report

Generated on: 2025-09-19T13:12:07.455035

## Overview

### blocksworld

#### Model: o1-preview_chat
- **task_1_plan_generation_zero_shot.json**: 587/600 correct (97.83%)

#### Model: o1-mini_chat
- **task_1_plan_generation_zero_shot.json**: 340/600 correct (56.67%)

#### Model: llama-3.1-405b_aws
- **task_1_plan_generation_zero_shot.json**: 387/600 correct (64.50%)
- **task_1_plan_generation.json**: 284/600 correct (47.33%)

#### Model: gpt-4o_chat
- **task_1_plan_generation_zero_shot.json**: 213/600 correct (35.50%)
- **task_1_plan_generation.json**: 170/600 correct (28.33%)

#### Model: gpt-4-turbo_chat
- **task_1_plan_generation_zero_shot.json**: 241/600 correct (40.17%)
- **task_1_plan_generation.json**: 138/600 correct (23.00%)

#### Model: gpt-4_chat
- **task_1_plan_generation_zero_shot.json**: 210/600 correct (35.00%)
- **task_1_plan_generation.json**: 206/600 correct (34.33%)
- **task_1_plan_generation_zero_shot_pddl.json**: 106/600 correct (17.67%)

#### Model: gemini-1.5-pro
- **task_1_plan_generation_zero_shot.json**: 143/600 correct (23.83%)
- **task_1_plan_generation.json**: 101/600 correct (16.83%)

#### Model: gemini-1.5-flash
- **task_1_plan_generation_zero_shot.json**: 44/600 correct (7.33%)
- **task_1_plan_generation.json**: 77/600 correct (12.83%)

#### Model: claude-3.5-sonnet_aws
- **task_1_plan_generation_zero_shot.json**: 329/600 correct (54.83%)
- **task_1_plan_generation.json**: 346/600 correct (57.67%)

#### Model: claude-3-opus
- **task_1_plan_generation_zero_shot.json**: 356/600 correct (59.33%)
- **task_1_plan_generation.json**: 289/600 correct (48.17%)

### mystery_blocksworld

#### Model: o1-preview_chat
- **task_1_plan_generation_zero_shot.json**: 317/600 correct (52.83%)
- **task_1_plan_generation.json**: 247/600 correct (41.17%)

#### Model: o1-mini_chat
- **task_1_plan_generation_zero_shot.json**: 115/601 correct (19.13%)

#### Model: llama-3.1-405b_aws
- **task_1_plan_generation_zero_shot.json**: 5/601 correct (0.83%)
- **task_1_plan_generation.json**: 21/600 correct (3.50%)

#### Model: gpt-4o_chat
- **task_1_plan_generation_zero_shot.json**: 0/601 correct (0.00%)
- **task_1_plan_generation.json**: 5/600 correct (0.83%)

#### Model: gpt-4-turbo_chat
- **task_1_plan_generation_zero_shot.json**: 1/601 correct (0.17%)
- **task_1_plan_generation.json**: 5/600 correct (0.83%)

#### Model: gpt-4_chat
- **task_1_plan_generation_zero_shot.json**: 0/600 correct (0.00%)
- **task_1_plan_generation.json**: 26/600 correct (4.33%)
- **task_1_plan_generation_zero_shot_pddl.json**: 3/600 correct (0.50%)

#### Model: gemini-1.5-pro
- **task_1_plan_generation_zero_shot.json**: 1/16 correct (6.25%)
- **task_1_plan_generation.json**: 0/6 correct (0.00%)

#### Model: gemini-1.5-flash
- **task_1_plan_generation_zero_shot.json**: 0/2 correct (0.00%)
- **task_1_plan_generation.json**: 0/4 correct (0.00%)

#### Model: claude-3.5-sonnet_aws
- **task_1_plan_generation_zero_shot.json**: 0/601 correct (0.00%)
- **task_1_plan_generation.json**: 19/600 correct (3.17%)

#### Model: claude-3-opus
- **task_1_plan_generation_zero_shot.json**: 0/601 correct (0.00%)
- **task_1_plan_generation.json**: 8/600 correct (1.33%)

### obfuscated_randomized_blocksworld

#### Model: o1-preview_chat
- **task_1_plan_generation_zero_shot.json**: 224/600 correct (37.33%)
- **task_1_plan_generation_zero_shot_pddl.json**: 110/230 correct (47.83%)

#### Model: o1-mini_chat
- **task_1_plan_generation_zero_shot.json**: 21/600 correct (3.50%)

### logistics

#### Model: o1-preview_chat
- **task_1_plan_generation_zero_shot_pddl.json**: 188/200 correct (94.00%)

#### Model: llama-3.1-405b_aws
- **task_1_plan_generation_zero_shot_pddl.json**: 19/200 correct (9.50%)

#### Model: gpt-4_chat
- **task_1_plan_generation.json**: 28/200 correct (14.00%)

### obfuscated_randomized_logistics

#### Model: o1-preview_chat
- **task_1_plan_generation_zero_shot_pddl.json**: 104/200 correct (52.00%)

### sokoban

#### Model: o1-preview_chat
- **task_1_plan_generation_zero_shot_pddl.json**: 4/30 correct (13.33%)

#### Model: llama-3.1-405b_aws
- **task_1_plan_generation_zero_shot_pddl.json**: 0/55 correct (0.00%)

### unsolvable_blocksworld

#### Model: o1-preview_chat
- **task_1_plan_generation_zero_shot.json**: 0/21 correct (0.00%)
- **task_1_plan_generation_zero_shot_pddl.json**: 0/100 correct (0.00%)

#### Model: gpt-4o-mini-2024-07-18_chat
- **task_1_plan_generation_zero_shot.json**: 0/100 correct (0.00%)
- **task_1_plan_generation_zero_shot_pddl.json**: 0/20 correct (0.00%)

### unsolvable_obfuscated_randomized_blocksworld

#### Model: o1-preview_chat
- **task_1_plan_generation_zero_shot_pddl.json**: 0/100 correct (0.00%)

## Overall Statistics
- Total Evaluations: 23690
- Total Correct: 6038
- Overall Accuracy: 25.49%