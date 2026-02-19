"""
test_lexer.py

Unit tests for lexer
Run with: pytest tests/
"""

import pytest
from lexer.lexer import Lexer
from lexer.token import TokenType


def test_variable_declaration():
    source = "int x = 5;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.INT
    assert tokens[1].value == "x"
    assert tokens[2].type == TokenType.ASSIGN
    assert tokens[3].value == 5        # ✅ number is int
    assert tokens[4].type == TokenType.SEMICOLON


def test_arithmetic_expression():
    source = "x = 10 + 20;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert tokens[0].value == "x"
    assert tokens[1].type == TokenType.ASSIGN
    assert tokens[2].value == 10       # ✅ int not string
    assert tokens[3].type == TokenType.PLUS
    assert tokens[4].value == 20       # ✅ int


def test_if_statement():
    source = "if (x > 0) { print(x); }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.IF
    assert tokens[1].type == TokenType.LPAREN
    assert tokens[2].value == "x"
    assert tokens[3].type == TokenType.GREATER
    assert tokens[4].value == 0        # ✅ int


def test_while_statement():
    source = "while (x > 0) { x = x - 1; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.WHILE
    assert tokens[1].type == TokenType.LPAREN
    assert tokens[2].value == "x"
    assert tokens[3].type == TokenType.GREATER
    assert tokens[4].value == 0        # ✅ int
