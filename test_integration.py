"""
Integration test to verify that the new HyperTree library works with existing usage patterns.
"""

import sys
import os

# Add the parent directory to the path to import the hypertree module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hypertree import HyperTree, TravelHyperTree


def test_natural_plan_usage():
    """Test usage patterns from natural_plan/response.py"""
    print("Testing natural_plan usage patterns...")
    
    # Simulate usage from natural_plan/response.py line 163
    leaf = HyperTree("root")
    city = "Paris"
    days = "3"
    leaf.children.append(HyperTree(f"{city}: {days}"))
    
    assert len(leaf.children) == 1
    assert leaf.children[0].value == "Paris: 3"
    
    # Simulate usage from line 198
    root = HyperTree(f"{city}: {days}")
    assert root.value == "Paris: 3"
    
    print("✓ Natural plan usage patterns work correctly")


def test_travelplanner_usage():
    """Test usage patterns from travelplanner/tools/planner/apis.py"""
    print("Testing travelplanner usage patterns...")
    
    # Simulate usage from travelplanner - line 548
    node = TravelHyperTree("[Plan]")
    value = "[Transportation]"
    if value != node.value:
        node.children.append(TravelHyperTree(value))
    
    assert len(node.children) == 1
    assert node.children[0].value == "[Transportation]"
    
    # Simulate usage from line 552
    current_tree = TravelHyperTree('[Plan]')
    assert current_tree.value == '[Plan]'
    
    # Test the all/branch pattern from lines 450, 547-548
    node = TravelHyperTree("[Plan]")
    node.all = [["[Transportation]", "[Accommodation]", "[Dining]"]]
    node.branch = 0
    children_value_list = node.all[node.branch]
    
    for value in children_value_list:
        if value != node.value:
            node.children.append(TravelHyperTree(value))
    
    assert len(node.children) == 3
    assert node.children[0].value == "[Transportation]"
    assert node.children[1].value == "[Accommodation]"
    assert node.children[2].value == "[Dining]"
    
    # Test is_terminal functionality
    assert not current_tree.is_terminal()  # [Plan] should not be terminal
    
    cost_node = TravelHyperTree("[cost]")
    assert cost_node.is_terminal()  # [cost] should be terminal
    
    print("✓ Travelplanner usage patterns work correctly")


def test_backward_compatibility():
    """Test that all original methods still work as expected"""
    print("Testing backward compatibility...")
    
    # Test basic functionality
    tree = TravelHyperTree("root")
    assert tree.is_leaf()
    
    child = TravelHyperTree("child")
    tree.children.append(child)
    assert not tree.is_leaf()
    
    # Test show method
    output = tree.show()
    assert "root" in output
    assert "child" in output
    
    # Test get_leaves
    leaves = tree.get_leaves()
    assert len(leaves) == 1
    assert leaves[0] == child
    
    # Test postorder_traversal with branching
    tree.all = [["branch1", "branch2"]]
    tree.branch = 0
    
    success = tree.postorder_traversal()
    # Should return False since there are no more branches to expand
    
    print("✓ Backward compatibility tests passed")


if __name__ == "__main__":
    print("Running integration tests for HyperTree library...\n")
    
    try:
        test_natural_plan_usage()
        test_travelplanner_usage()
        test_backward_compatibility()
        
        print("\n🎉 All integration tests passed! The library is compatible with existing code.")
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)