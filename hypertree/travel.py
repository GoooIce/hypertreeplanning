"""
Travel-specific HyperTree implementation.

This module provides travel planning specific extensions to the HyperTree class,
including terminal node detection for travel planning domains.
"""

import re
from typing import Any, List
from .core import HyperTreeNode


class TravelHyperTree(HyperTreeNode):
    """
    Travel planning specific HyperTree implementation.
    
    This class includes domain-specific knowledge for travel planning,
    such as terminal node detection based on travel categories.
    """
    
    def __init__(self, value: Any):
        """Initialize a TravelHyperTree node."""
        super().__init__(value)
        
        # Define travel planning categories
        self.non_terminals = [
            "[Plan]", "[Transportation]", "[Taxi]", "[Self-driving]", "[Flight]",
            "[Accommodation]", "[Attraction]", "[Dining]"
        ]
        
        self.terminals = [
            "[environment]", "[preference]", "[cost]", "[consistency]", 
            "[house rule]", "[room type]", "[minimum stay]", "[cuisine]"
        ]
        
        # Compile regex patterns for dynamic categories
        self.wrong_pattern = re.compile(r'\[(.*?)\]\s*(.*?)\s*\[(.*?)\]')
        self.transportation_pattern = re.compile(
            r'\[transportation from [\w\s.]+ to [\w\s.]+\]', re.IGNORECASE
        )
        self.accommodation_pattern = re.compile(
            r'\[accommodation for [\w\s.]+\]', re.IGNORECASE
        )
        self.dining_pattern = re.compile(
            r'\[dining for [\w\s.]+\]', re.IGNORECASE
        )
        self.attraction_pattern = re.compile(
            r'\[attraction for [\w\s.]+\]', re.IGNORECASE
        )
    
    def _create_child(self, value: Any) -> 'TravelHyperTree':
        """Create a child TravelHyperTree node."""
        return TravelHyperTree(value)
    
    def add_child(self, value: Any) -> 'TravelHyperTree':
        """
        Add a single child with the given value.
        
        Args:
            value: Value for the new child
            
        Returns:
            The newly created child node
        """
        child = self._create_child(value)
        self.children.append(child)
        return child
    
    def add_children(self, values: List[Any]) -> List['TravelHyperTree']:
        """
        Add multiple children with the given values.
        
        Args:
            values: List of values for new children
            
        Returns:
            List of newly created child nodes
        """
        children = []
        for value in values:
            child = self.add_child(value)
            children.append(child)
        return children
    
    def is_terminal(self) -> bool:
        """
        Check if this node is terminal based on travel planning rules.
        
        Returns:
            True if node is terminal, False otherwise
        """
        node = str(self.value).lower()
        
        # Check against predefined non-terminal categories
        if any(nt.lower() == node for nt in self.non_terminals):
            return False
        
        # Check against predefined terminal categories
        if any(t.lower() == node for t in self.terminals):
            return True
        
        # Check against regex patterns for malformed nodes
        if self.wrong_pattern.match(node):
            return True
        
        # Check specific travel category patterns
        if self.transportation_pattern.match(node):
            return False
        elif self.accommodation_pattern.match(node):
            return False
        elif self.dining_pattern.match(node):
            return False
        elif self.attraction_pattern.match(node):
            return True
        
        # Default to terminal if no pattern matches
        return True
    
    def is_transportation_node(self) -> bool:
        """Check if this node represents transportation."""
        return self.transportation_pattern.match(str(self.value).lower()) is not None
    
    def is_accommodation_node(self) -> bool:
        """Check if this node represents accommodation."""
        return self.accommodation_pattern.match(str(self.value).lower()) is not None
    
    def is_dining_node(self) -> bool:
        """Check if this node represents dining."""
        return self.dining_pattern.match(str(self.value).lower()) is not None
    
    def is_attraction_node(self) -> bool:
        """Check if this node represents an attraction."""
        return self.attraction_pattern.match(str(self.value).lower()) is not None
    
    def get_category(self) -> str:
        """
        Get the category of this travel node.
        
        Returns:
            String indicating the category of this node
        """
        node_str = str(self.value).lower()
        
        if any(nt.lower() == node_str for nt in self.non_terminals):
            # Find the matching non-terminal
            for nt in self.non_terminals:
                if nt.lower() == node_str:
                    return nt.strip('[]').lower()
        
        if self.is_transportation_node():
            return "transportation"
        elif self.is_accommodation_node():
            return "accommodation"
        elif self.is_dining_node():
            return "dining"
        elif self.is_attraction_node():
            return "attraction"
        
        return "unknown"
    
    def get_nodes_by_category(self, category: str) -> List['TravelHyperTree']:
        """
        Get all nodes in the subtree that belong to a specific category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of nodes matching the category
        """
        nodes = []
        
        if self.get_category() == category:
            nodes.append(self)
        
        for child in self.children:
            nodes.extend(child.get_nodes_by_category(category))
        
        return nodes
    
    def get_travel_plan_structure(self) -> dict:
        """
        Get the structure of the travel plan as a nested dictionary.
        
        Returns:
            Dictionary representing the travel plan structure
        """
        structure = {
            'value': self.value,
            'category': self.get_category(),
            'is_terminal': self.is_terminal(),
            'children': []
        }
        
        for child in self.children:
            structure['children'].append(child.get_travel_plan_structure())
        
        return structure