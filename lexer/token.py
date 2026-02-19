# lexer/token.py

from enum import Enum, auto


class TokenType(Enum):
    INT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()

    IDENTIFIER = auto()
    NUMBER = auto()

    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MOD = auto()
    ASSIGN = auto()

    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    SEMICOLON = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()

    EOF = auto()


class Token:
    def __init__(self, token_type, value=None, line=1):
        self.type = token_type
        self.value = value
        self.line = line

    def __repr__(self):
        # Safe handling for both Enum and string token types
        type_name = self.type.name if hasattr(self.type, "name") else self.type

        if self.value is not None:
            return f"{type_name}({self.value})"
        return f"{type_name}"
