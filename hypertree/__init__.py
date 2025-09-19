"""
HyperTree Library - A generic tree structure for hierarchical planning and reasoning.

This library provides a flexible tree data structure that supports branching,
traversal, and domain-specific extensions.
"""

from .core import HyperTree, HyperTreeNode
from .travel import TravelHyperTree

__version__ = "1.0.0"
__all__ = ["HyperTree", "HyperTreeNode", "TravelHyperTree"]