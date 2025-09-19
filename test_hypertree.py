"""
Tests for the HyperTree library.

This module contains tests for both the core HyperTree functionality
and the travel-specific extensions.
"""

import sys
import os

# Add the parent directory to the path to import the hypertree module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hypertree import HyperTree, TravelHyperTree


def test_basic_hypertree():
    """Test basic HyperTree functionality."""
    print("Testing basic HyperTree functionality...")
    
    # Create a root node
    root = HyperTree("Root")
    assert root.value == "Root"
    assert root.is_leaf() == True
    assert len(root.children) == 0
    
    # Add children
    child1 = root.add_child("Child1")
    child2 = root.add_child("Child2")
    
    assert root.is_leaf() == False
    assert len(root.children) == 2
    assert child1.value == "Child1"
    assert child2.value == "Child2"
    
    # Test tree display
    tree_str = root.show()
    assert "Root" in tree_str
    assert "Child1" in tree_str
    assert "Child2" in tree_str
    
    # Test leaf collection
    leaves = root.get_leaves()
    assert len(leaves) == 2
    assert child1 in leaves
    assert child2 in leaves
    
    # Test find node
    found = root.find_node("Child1")
    assert found == child1
    
    found = root.find_node("NonExistent")
    assert found is None
    
    # Test depth and size
    assert root.depth() == 1
    assert root.size() == 3
    
    print("✓ Basic HyperTree tests passed")


def test_travel_hypertree():
    """Test TravelHyperTree functionality."""
    print("Testing TravelHyperTree functionality...")
    
    # Create a travel plan root
    root = TravelHyperTree("[Plan]")
    assert root.value == "[Plan]"
    assert root.is_terminal() == False
    assert root.get_category() == "plan"
    
    # Add travel components
    transportation = root.add_child("[Transportation]")
    accommodation = root.add_child("[Accommodation]")
    dining = root.add_child("[Dining]")
    
    assert transportation.is_terminal() == False
    assert accommodation.is_terminal() == False
    assert dining.is_terminal() == False
    
    # Add specific transportation details
    flight = transportation.add_child("[transportation from New York to Paris]")
    assert flight.is_transportation_node() == True
    assert flight.is_terminal() == False
    
    # Add specific accommodation details
    hotel = accommodation.add_child("[accommodation for Paris]")
    assert hotel.is_accommodation_node() == True
    assert hotel.is_terminal() == False
    
    # Add terminal nodes
    cost = hotel.add_child("[cost]")
    preference = hotel.add_child("[preference]")
    
    assert cost.is_terminal() == True
    assert preference.is_terminal() == True
    
    # Test category filtering
    transport_nodes = root.get_nodes_by_category("transportation")
    assert len(transport_nodes) >= 1
    
    # Test travel plan structure
    structure = root.get_travel_plan_structure()
    assert structure['value'] == "[Plan]"
    assert structure['category'] == "plan"
    assert len(structure['children']) == 3
    
    print("✓ TravelHyperTree tests passed")


def test_branching_functionality():
    """Test the branching functionality of HyperTree."""
    print("Testing branching functionality...")
    
    root = HyperTree("Root")
    
    # Add multiple possible children sets
    root.add_children_set(["Option1A", "Option1B"])
    root.add_children_set(["Option2A", "Option2B", "Option2C"])
    
    # Set first branch
    success = root.set_current_branch(0)
    assert success == True
    assert len(root.children) == 2
    assert root.children[0].value == "Option1A"
    assert root.children[1].value == "Option1B"
    
    # Switch to second branch
    success = root.set_current_branch(1)
    assert success == True
    assert len(root.children) == 3
    assert root.children[0].value == "Option2A"
    assert root.children[1].value == "Option2B"
    assert root.children[2].value == "Option2C"
    
    # Test post-order traversal
    success = root.postorder_traversal()
    assert success == False  # No more branches to expand
    
    print("✓ Branching functionality tests passed")


def test_compatibility_with_original():
    """Test that the new library is compatible with original usage patterns."""
    print("Testing compatibility with original implementations...")
    
    # Test original usage pattern from natural_plan/response.py
    tree = HyperTree("Paris: 3 days")
    assert tree.value == "Paris: 3 days"
    assert tree.is_leaf() == True
    
    # Test original usage pattern from travelplanner
    travel_tree = TravelHyperTree("[Plan]")
    travel_tree.all = [["[Transportation]", "[Accommodation]", "[Dining]"]]
    travel_tree.branch = 0
    children_value_list = travel_tree.all[travel_tree.branch]
    
    for value in children_value_list:
        if value != travel_tree.value:
            travel_tree.children.append(TravelHyperTree(value))
    
    assert len(travel_tree.children) == 3
    assert travel_tree.children[0].value == "[Transportation]"
    
    print("✓ Compatibility tests passed")


if __name__ == "__main__":
    print("Running HyperTree library tests...\n")
    
    try:
        test_basic_hypertree()
        test_travel_hypertree()
        test_branching_functionality()
        test_compatibility_with_original()
        
        print("\n🎉 All tests passed! The HyperTree library is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)