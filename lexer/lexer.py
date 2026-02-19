# lexer/lexer.py

from lexer.token import Token, TokenType


class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None
        self.line = 1

        self.keywords = {
            "int": TokenType.INT,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "print": TokenType.PRINT,
        }

    # --------------------------
    # Utility Methods
    # --------------------------

    def advance(self):
        self.position += 1
        if self.position < len(self.text):
            self.current_char = self.text[self.position]
        else:
            self.current_char = None

    def peek(self):
        peek_pos = self.position + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == "\n":
                self.line += 1
            self.advance()

    def skip_comment(self):
        # Handles // single-line comments
        while self.current_char is not None and self.current_char != "\n":
            self.advance()

    # --------------------------
    # Token Generators
    # --------------------------

    def number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, int(result), self.line)

    def identifier(self):
        result = ""
        while (
            self.current_char is not None
            and (self.current_char.isalnum() or self.current_char == "_")
        ):
            result += self.current_char
            self.advance()

        token_type = self.keywords.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result, self.line)

    # --------------------------
    # Main Tokenizer
    # --------------------------

    def tokenize(self):
        tokens = []

        while self.current_char is not None:

            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Skip comments
            if self.current_char == "/" and self.peek() == "/":
                self.advance()
                self.advance()
                self.skip_comment()
                continue

            # Numbers
            if self.current_char.isdigit():
                tokens.append(self.number())
                continue

            # Identifiers / Keywords
            if self.current_char.isalpha() or self.current_char == "_":
                tokens.append(self.identifier())
                continue

            # Operators
            if self.current_char == "+":
                tokens.append(Token(TokenType.PLUS, "+", self.line))
                self.advance()
                continue

            if self.current_char == "-":
                tokens.append(Token(TokenType.MINUS, "-", self.line))
                self.advance()
                continue

            if self.current_char == "*":
                tokens.append(Token(TokenType.MULTIPLY, "*", self.line))
                self.advance()
                continue

            if self.current_char == "/":
                tokens.append(Token(TokenType.DIVIDE, "/", self.line))
                self.advance()
                continue

            if self.current_char == "=":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.EQUAL, "==", self.line))
                else:
                    tokens.append(Token(TokenType.ASSIGN, "=", self.line))
                    self.advance()
                continue

            if self.current_char == "!":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.NOT_EQUAL, "!=", self.line))
                    continue
                else:
                    raise Exception(f"Unexpected character '!' at line {self.line}")

            if self.current_char == "<":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.LESS_EQUAL, "<=", self.line))
                else:
                    tokens.append(Token(TokenType.LESS, "<", self.line))
                    self.advance()
                continue

            if self.current_char == ">":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.GREATER_EQUAL, ">=", self.line))
                else:
                    tokens.append(Token(TokenType.GREATER, ">", self.line))
                    self.advance()
                continue

            # Symbols
            if self.current_char == ";":
                tokens.append(Token(TokenType.SEMICOLON, ";", self.line))
                self.advance()
                continue

            if self.current_char == "(":
                tokens.append(Token(TokenType.LPAREN, "(", self.line))
                self.advance()
                continue

            if self.current_char == ")":
                tokens.append(Token(TokenType.RPAREN, ")", self.line))
                self.advance()
                continue

            if self.current_char == "{":
                tokens.append(Token(TokenType.LBRACE, "{", self.line))
                self.advance()
                continue

            if self.current_char == "}":
                tokens.append(Token(TokenType.RBRACE, "}", self.line))
                self.advance()
                continue
            
            if self.current_char == '%':
                tokens.append(Token(TokenType.MOD, '%', self.line))
                self.advance()
                continue

            # Unknown character
            raise Exception(f"Illegal character '{self.current_char}' at line {self.line}")

        tokens.append(Token(TokenType.EOF, line=self.line))
        return tokens
