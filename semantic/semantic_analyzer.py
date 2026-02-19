# semantic/semantic_analyzer.py

from semantic.symbol_table import SymbolTable
from myparser.ast_nodes import *


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    # ---------------------------
    # Visitor Dispatcher
    # ---------------------------

    def visit(self, node):
        """
        Main visitor entry (used by main.py)
        """
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    # Optional compatibility method
    def analyze(self, node):
        return self.visit(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    # ---------------------------
    # Program
    # ---------------------------

    def visit_Program(self, node):
        for decl in node.declarations:
            self.visit(decl)

        for stmt in node.statements:
            self.visit(stmt)

    # ---------------------------
    # Declarations
    # ---------------------------

    def visit_Declaration(self, node):
        if getattr(node, "initializer", None):
            self.visit(node.initializer)
        self.symbol_table.declare(node.var_name, "int")

    # ---------------------------
    # Statements
    # ---------------------------

    def visit_Assignment(self, node):
        # Ensure variable is declared
        self.symbol_table.lookup(node.var_name)

        # Check expression
        self.visit(node.expression)

    def visit_PrintStatement(self, node):
        self.visit(node.expression)

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        self.visit(node.true_block)

        if node.false_block:
            self.visit(node.false_block)

    def visit_WhileStatement(self, node):
        self.visit(node.condition)
        self.visit(node.body)

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    # ---------------------------
    # Expressions
    # ---------------------------

    def visit_BinaryOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Number(self, node):
        pass  # Numbers are always valid

    def visit_Identifier(self, node):
        self.symbol_table.lookup(node.name)
