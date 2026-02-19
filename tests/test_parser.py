"""
test_parser.py

Unit tests for parser
Run with: pytest tests/
"""

import pytest
from lexer.lexer import Lexer
from myparser.parser import Parser
from myparser.ast_nodes import (
    Program,
    Declaration,
    Assignment,
    PrintStatement,
    WhileStatement,
    IfStatement,
)


def parse_source(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


# ---------------------------
# Declarations
# ---------------------------

def test_parse_variable_declaration():
    source = "int x;"
    ast = parse_source(source)

    assert isinstance(ast, Program)
    assert len(ast.declarations) == 1
    assert isinstance(ast.declarations[0], Declaration)
    assert ast.declarations[0].var_name == "x"


# ---------------------------
# Assignment
# ---------------------------

def test_parse_assignment():
    source = "int x; x = 10;"
    ast = parse_source(source)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], Assignment)
    assert ast.statements[0].var_name == "x"


# ---------------------------
# Print
# ---------------------------

def test_parse_print():
    source = "int x; print(x);"
    ast = parse_source(source)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], PrintStatement)


# ---------------------------
# While
# ---------------------------

def test_parse_while():
    source = """
    int x;
    while (x > 0) {
        x = x - 1;
    }
    """
    ast = parse_source(source)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], WhileStatement)


# ---------------------------
# If-Else
# ---------------------------

def test_parse_if_else():
    source = """
    int x;
    if (x > 0) {
        print(x);
    } else {
        print(0);
    }
    """
    ast = parse_source(source)

    assert len(ast.statements) == 1
    assert isinstance(ast.statements[0], IfStatement)
