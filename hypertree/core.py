"""
Core HyperTree implementation.

This module provides the base HyperTree class with common functionality
extracted from the existing implementations in the repository.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional, Union


class HyperTreeNode(ABC):
    """Abstract base class for HyperTree nodes."""
    
    def __init__(self, value: Any):
        """Initialize a HyperTree node with a value."""
        self.value = value
        self.all: List[List[Any]] = []  # Store all possible children sets
        self.branch: Optional[int] = None  # Current branch index
        self.children: List['HyperTreeNode'] = []  # Current children
    
    def show(self, depth: int = 0) -> str:
        """
        Display the tree structure with indentation.
        
        Args:
            depth: Current depth in the tree for indentation
            
        Returns:
            String representation of the tree structure
        """
        result = '<Tab>' * depth + str(self.value) + '\n'
        for child in self.children:
            result += child.show(depth + 1)
        return result
    
    def is_leaf(self) -> bool:
        """Check if this node is a leaf (has no children)."""
        return len(self.children) == 0
    
    def get_leaves(self) -> List['HyperTreeNode']:
        """
        Get all leaf nodes in the subtree rooted at this node.
        
        Returns:
            List of leaf nodes
        """
        leaves = []
        if self.is_leaf():
            leaves.append(self)
        else:
            for child in self.children:
                leaves.extend(child.get_leaves())
        return leaves
    
    def postorder_traversal(self) -> bool:
        """
        Perform post-order traversal and try to expand to next branch.
        
        Returns:
            True if expansion was successful, False otherwise
        """
        # First try to expand children
        for child in self.children:
            is_found = child.postorder_traversal()
            if is_found:
                return True
        
        # If no children can expand, try to expand this node
        if self.branch is None:
            return False
        
        if self.branch + 1 < len(self.all):
            self.branch = self.branch + 1
            children_value_list = self.all[self.branch]
            self.children = [self._create_child(value) for value in children_value_list]
            return True
        
        return False
    
    def add_children_set(self, children_values: List[Any]) -> None:
        """
        Add a set of possible children values.
        
        Args:
            children_values: List of values for potential children
        """
        self.all.append(children_values)
    
    def set_current_branch(self, branch_index: int) -> bool:
        """
        Set the current branch and create children.
        
        Args:
            branch_index: Index of the branch to activate
            
        Returns:
            True if branch was set successfully, False otherwise
        """
        if 0 <= branch_index < len(self.all):
            self.branch = branch_index
            children_value_list = self.all[self.branch]
            self.children = [self._create_child(value) for value in children_value_list]
            return True
        return False
    
    @abstractmethod
    def _create_child(self, value: Any) -> 'HyperTreeNode':
        """
        Create a child node with the given value.
        This method must be implemented by subclasses.
        
        Args:
            value: Value for the new child node
            
        Returns:
            New child node instance
        """
        pass
    
    @abstractmethod
    def is_terminal(self) -> bool:
        """
        Check if this node is terminal (cannot be expanded further).
        This method must be implemented by subclasses.
        
        Returns:
            True if node is terminal, False otherwise
        """
        pass


class HyperTree(HyperTreeNode):
    """
    Basic implementation of HyperTree with minimal functionality.
    
    This is the simplest concrete implementation that can be used directly
    or extended for specific use cases.
    """
    
    def _create_child(self, value: Any) -> 'HyperTree':
        """Create a child HyperTree node."""
        return HyperTree(value)
    
    def is_terminal(self) -> bool:
        """
        Basic terminal check - always returns False.
        Override this method for domain-specific terminal conditions.
        """
        return False
    
    def add_child(self, value: Any) -> 'HyperTree':
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
    
    def add_children(self, values: List[Any]) -> List['HyperTree']:
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
    
    def find_node(self, value: Any) -> Optional['HyperTree']:
        """
        Find a node with the given value in the subtree.
        
        Args:
            value: Value to search for
            
        Returns:
            First node found with the value, or None if not found
        """
        if self.value == value:
            return self
        
        for child in self.children:
            result = child.find_node(value)
            if result:
                return result
        
        return None
    
    def get_path_to_root(self) -> List['HyperTree']:
        """
        Get the path from this node to the root.
        Note: This requires parent references which are not maintained by default.
        """
        # This would need parent references to be properly implemented
        return [self]
    
    def depth(self) -> int:
        """Get the maximum depth of the subtree rooted at this node."""
        if self.is_leaf():
            return 0
        return 1 + max(child.depth() for child in self.children)
    
    def size(self) -> int:
        """Get the total number of nodes in the subtree rooted at this node."""
        size = 1  # Count this node
        for child in self.children:
            size += child.size()
        return size