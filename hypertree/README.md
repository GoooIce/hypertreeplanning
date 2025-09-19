# HyperTree Library

A generic tree structure for hierarchical planning and reasoning, extracted from the HyperTree Planning research project.

## Overview

The HyperTree library provides a flexible tree data structure that supports:

- **Hierarchical representation**: Build complex tree structures with arbitrary depth
- **Branching support**: Maintain multiple possible expansion paths for each node
- **Domain-specific extensions**: Specialized implementations for specific use cases
- **Traversal methods**: Various ways to navigate and manipulate the tree structure

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/GoooIce/hypertreeplanning.git
cd hypertreeplanning

# Install the library
pip install -e .
```

### Usage in the Repository

```python
from hypertree import HyperTree, TravelHyperTree
```

## Quick Start

### Basic HyperTree

```python
from hypertree import HyperTree

# Create a root node
root = HyperTree("My Plan")

# Add children
step1 = root.add_child("Step 1")
step2 = root.add_child("Step 2")

# Add sub-steps
step1.add_child("Sub-step 1.1")
step1.add_child("Sub-step 1.2")

# Display the tree
print(root.show())
```

### Travel Planning with TravelHyperTree

```python
from hypertree import TravelHyperTree

# Create a travel plan
plan = TravelHyperTree("[Plan]")

# Add travel components
transportation = plan.add_child("[Transportation]")
accommodation = plan.add_child("[Accommodation]")
dining = plan.add_child("[Dining]")

# Add specific details
flight = transportation.add_child("[transportation from New York to Paris]")
hotel = accommodation.add_child("[accommodation for Paris]")

# Check terminal status
print(f"Plan is terminal: {plan.is_terminal()}")  # False
print(f"Flight is terminal: {flight.is_terminal()}")  # False

# Add terminal details
cost = hotel.add_child("[cost]")
print(f"Cost is terminal: {cost.is_terminal()}")  # True
```

### Branching Support

```python
from hypertree import HyperTree

root = HyperTree("Decision Point")

# Add multiple possible expansion sets
root.add_children_set(["Option 1A", "Option 1B"])
root.add_children_set(["Option 2A", "Option 2B", "Option 2C"])

# Activate first branch
root.set_current_branch(0)
print(f"Children: {[child.value for child in root.children]}")
# Output: ['Option 1A', 'Option 1B']

# Switch to second branch
root.set_current_branch(1)
print(f"Children: {[child.value for child in root.children]}")
# Output: ['Option 2A', 'Option 2B', 'Option 2C']
```

## Core Classes

### HyperTree

The base implementation with essential tree functionality:

- `__init__(value)`: Create a node with a value
- `add_child(value)`: Add a single child
- `add_children(values)`: Add multiple children
- `is_leaf()`: Check if node has no children
- `get_leaves()`: Get all leaf nodes in subtree
- `show(depth=0)`: Display tree structure
- `find_node(value)`: Find node with specific value
- `depth()`: Get maximum depth of subtree
- `size()`: Get total number of nodes

### TravelHyperTree

Specialized for travel planning with domain-specific knowledge:

- `is_terminal()`: Check if node can be expanded further (travel-specific rules)
- `get_category()`: Get the travel category (transportation, accommodation, etc.)
- `is_transportation_node()`: Check if node represents transportation
- `is_accommodation_node()`: Check if node represents accommodation
- `is_dining_node()`: Check if node represents dining
- `is_attraction_node()`: Check if node represents attractions
- `get_nodes_by_category(category)`: Filter nodes by travel category
- `get_travel_plan_structure()`: Get structured representation of travel plan

## Advanced Features

### Branching and Expansion

HyperTree supports maintaining multiple possible expansion paths:

```python
node = HyperTree("expandable")
node.all = [
    ["path1_child1", "path1_child2"],
    ["path2_child1", "path2_child2", "path2_child3"]
]

# Set active branch
node.branch = 0
children_values = node.all[node.branch]
node.children = [HyperTree(value) for value in children_values]

# Use post-order traversal to expand
success = node.postorder_traversal()
```

### Travel Category Detection

TravelHyperTree automatically categorizes nodes based on patterns:

```python
transport = TravelHyperTree("[transportation from NYC to LAX]")
print(transport.get_category())  # "transportation"
print(transport.is_transportation_node())  # True

hotel = TravelHyperTree("[accommodation for Los Angeles]")
print(hotel.get_category())  # "accommodation"
print(hotel.is_terminal())  # False (can be expanded further)

cost = TravelHyperTree("[cost]")
print(cost.is_terminal())  # True (terminal node)
```

## Integration with Existing Code

This library was extracted from the original HyperTree Planning codebase and maintains full backward compatibility. The original implementations in:

- `natural_plan/response.py`
- `travelplanner/tools/planner/apis.py`

Have been updated to use this library while preserving all existing functionality.

## API Reference

### Core Methods

All HyperTree nodes support these essential methods:

- **Navigation**: `get_leaves()`, `find_node()`, `get_path_to_root()`
- **Structure**: `depth()`, `size()`, `is_leaf()`
- **Display**: `show()`, `get_travel_plan_structure()` (TravelHyperTree only)
- **Modification**: `add_child()`, `add_children()`, `add_children_set()`
- **Branching**: `set_current_branch()`, `postorder_traversal()`

### Domain-Specific Methods (TravelHyperTree)

- **Terminal Detection**: `is_terminal()`
- **Category Analysis**: `get_category()`, `get_nodes_by_category()`
- **Type Checking**: `is_transportation_node()`, `is_accommodation_node()`, etc.

## License

This library is part of the HyperTree Planning research project. Please refer to the main repository license for usage terms.

## Citation

If you use this library in your research, please cite the original HyperTree Planning paper:

```bibtex
@inproceedings{gui2025hypertree,
  title={HyperTree Planning: Enhancing LLM Reasoning via Hierarchical Thinking},
  author={Gui, Runquan and Wang, Zhihai and Wang, Jie and Ma, Chi and Zhen, Huiling and Yuan, Mingxuan and Hao, Jianye and Lian, Defu and Chen, Enhong and Wu, Feng},
  booktitle={Proceedings of the 42nd International Conference on Machine Learning},
  year={2025}
}
```