#!/usr/bin/env python3
"""
Example usage of the HyperTree library.

This script demonstrates the main features of the HyperTree library
extracted from the HyperTree Planning research project.
"""

import sys
import os

# Add the parent directory to the path to import the hypertree module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hypertree import HyperTree, TravelHyperTree


def demo_basic_hypertree():
    """Demonstrate basic HyperTree functionality."""
    print("=== Basic HyperTree Demo ===")
    
    # Create a simple planning tree
    root = HyperTree("Project Plan")
    
    # Add main phases
    planning = root.add_child("Planning Phase")
    development = root.add_child("Development Phase")
    testing = root.add_child("Testing Phase")
    
    # Add sub-tasks to each phase
    planning.add_children([
        "Define Requirements",
        "Create Architecture",
        "Estimate Timeline"
    ])
    
    development.add_children([
        "Setup Environment",
        "Implement Core Features",
        "Code Review"
    ])
    
    testing.add_children([
        "Unit Tests",
        "Integration Tests",
        "User Acceptance Testing"
    ])
    
    print("Project structure:")
    print(root.show())
    
    print(f"Total nodes: {root.size()}")
    print(f"Tree depth: {root.depth()}")
    print(f"Number of leaves: {len(root.get_leaves())}")
    
    # Find specific node
    requirements = root.find_node("Define Requirements")
    if requirements:
        print(f"Found node: {requirements.value}")
    
    print()


def demo_travel_hypertree():
    """Demonstrate TravelHyperTree with travel planning."""
    print("=== Travel Planning Demo ===")
    
    # Create a travel plan
    trip = TravelHyperTree("[Plan]")
    
    # Add main categories
    transportation = trip.add_child("[Transportation]")
    accommodation = trip.add_child("[Accommodation]")
    activities = trip.add_child("[Attraction]")
    dining = trip.add_child("[Dining]")
    
    # Add specific transportation
    flight = transportation.add_child("[transportation from New York to Tokyo]")
    local_transport = transportation.add_child("[transportation from Airport to Hotel]")
    
    # Add accommodation details
    hotel = accommodation.add_child("[accommodation for Tokyo]")
    
    # Add terminal details
    flight_cost = flight.add_child("[cost]")
    hotel_preference = hotel.add_child("[preference]")
    room_type = hotel.add_child("[room type]")
    
    print("Travel plan structure:")
    print(trip.show())
    
    # Demonstrate category analysis
    print("Travel categories found:")
    categories = ["transportation", "accommodation", "attraction", "dining"]
    for category in categories:
        nodes = trip.get_nodes_by_category(category)
        print(f"  {category}: {len(nodes)} nodes")
    
    # Check terminal status
    print("\nTerminal status:")
    print(f"  Trip plan: {trip.is_terminal()}")
    print(f"  Flight: {flight.is_terminal()}")
    print(f"  Flight cost: {flight_cost.is_terminal()}")
    print(f"  Hotel preference: {hotel_preference.is_terminal()}")
    
    # Get structured representation
    structure = trip.get_travel_plan_structure()
    print(f"\nStructured plan has {len(structure['children'])} main categories")
    
    print()


def demo_branching():
    """Demonstrate branching functionality."""
    print("=== Branching Demo ===")
    
    # Create a decision point
    decision = HyperTree("Choose Restaurant")
    
    # Add multiple possible choices
    decision.add_children_set(["Italian", "Japanese", "Mexican"])
    decision.add_children_set(["Fast Food", "Fine Dining"])
    decision.add_children_set(["Vegetarian", "Seafood", "Steakhouse", "Sushi"])
    
    print("Available choice sets:")
    for i, choices in enumerate(decision.all):
        print(f"  Set {i + 1}: {choices}")
    
    # Try different branches
    for branch_idx in range(len(decision.all)):
        success = decision.set_current_branch(branch_idx)
        if success:
            choices = [child.value for child in decision.children]
            print(f"\nBranch {branch_idx + 1} activated: {choices}")
    
    # Demonstrate post-order traversal
    decision.set_current_branch(0)  # Reset to first branch
    print(f"\nCurrent children: {[child.value for child in decision.children]}")
    
    # Try to expand to next branch
    expanded = decision.postorder_traversal()
    if expanded:
        print(f"Expanded to: {[child.value for child in decision.children]}")
    
    print()


def demo_compatibility():
    """Demonstrate compatibility with original usage patterns."""
    print("=== Compatibility Demo ===")
    
    # Original pattern from natural_plan/response.py
    print("Natural plan pattern:")
    leaf = HyperTree("root")
    city, days = "Paris", "3"
    leaf.children.append(HyperTree(f"{city}: {days}"))
    print(f"  Added: {leaf.children[0].value}")
    
    # Original pattern from travelplanner/tools/planner/apis.py
    print("\nTravelplanner pattern:")
    current_tree = TravelHyperTree('[Plan]')
    node = current_tree
    node.all = [["[Transportation]", "[Accommodation]", "[Dining]"]]
    node.branch = 0
    children_value_list = node.all[node.branch]
    
    for value in children_value_list:
        if value != node.value:
            node.children.append(TravelHyperTree(value))
    
    print(f"  Created {len(node.children)} children:")
    for child in node.children:
        print(f"    - {child.value}")
    
    print()


if __name__ == "__main__":
    print("HyperTree Library Examples")
    print("=" * 50)
    print()
    
    demo_basic_hypertree()
    demo_travel_hypertree()
    demo_branching()
    demo_compatibility()
    
    print("🎉 All demos completed successfully!")
    print("\nThe HyperTree library provides a flexible foundation for")
    print("hierarchical planning and reasoning tasks.")