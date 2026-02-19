"""
Semantic analysis package

Exposes:
- SemanticAnalyzer
- SymbolTable
"""

from .semantic_analyzer import SemanticAnalyzer
from .symbol_table import SymbolTable

__all__ = ["SemanticAnalyzer", "SymbolTable"]
