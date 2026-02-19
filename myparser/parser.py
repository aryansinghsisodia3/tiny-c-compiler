from lexer.token import TokenType
from .ast_nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.position += 1
            if self.position < len(self.tokens):
                self.current_token = self.tokens[self.position]
        else:
            raise Exception(
                f"Unexpected token {self.current_token.type}, expected {token_type}"
            )

    # Entry point
    def parse(self):
        declarations = []
        statements = []

        while self.current_token.type == TokenType.INT:
            declarations.append(self.declaration())

        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())

        return Program(declarations, statements)

    # Declarations
    def declaration(self):
        self.eat(TokenType.INT)
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        initializer = None
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            initializer = self.expression()

        self.eat(TokenType.SEMICOLON)
        return Declaration(var_name, initializer)

    # Statements
    def statement(self):
        if self.current_token.type == TokenType.IDENTIFIER:
            return self.assignment()
        elif self.current_token.type == TokenType.PRINT:
            return self.print_statement()
        elif self.current_token.type == TokenType.IF:
            return self.if_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.while_statement()
        elif self.current_token.type == TokenType.LBRACE:
            return self.block()
        else:
            raise Exception(f"Invalid statement at token {self.current_token}")

    def assignment(self):
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        self.eat(TokenType.SEMICOLON)
        return Assignment(var_name, expr)

    def print_statement(self):
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        expr = self.expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        return PrintStatement(expr)

    def if_statement(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)

        true_block = self.block()

        false_block = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            false_block = self.block()

        return IfStatement(condition, true_block, false_block)

    def while_statement(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        body = self.block()
        return WhileStatement(condition, body)

    def block(self):
        self.eat(TokenType.LBRACE)
        statements = []

        while self.current_token.type != TokenType.RBRACE:
            statements.append(self.statement())

        self.eat(TokenType.RBRACE)
        return Block(statements)

    # Expression parsing with precedence:
    # equality -> relational -> additive -> multiplicative -> factor

    def expression(self):
        return self.equality()

    def equality(self):
        node = self.relational()
        while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self.current_token.value
            if self.current_token.type == TokenType.EQUAL:
                self.eat(TokenType.EQUAL)
            else:
                self.eat(TokenType.NOT_EQUAL)
            node = BinaryOp(node, operator, self.relational())
        return node

    def relational(self):
        node = self.additive()
        while self.current_token.type in (
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.current_token.value
            if self.current_token.type == TokenType.GREATER:
                self.eat(TokenType.GREATER)
            elif self.current_token.type == TokenType.GREATER_EQUAL:
                self.eat(TokenType.GREATER_EQUAL)
            elif self.current_token.type == TokenType.LESS:
                self.eat(TokenType.LESS)
            else:
                self.eat(TokenType.LESS_EQUAL)
            node = BinaryOp(node, operator, self.additive())
        return node

    def additive(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            if self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            node = BinaryOp(node, operator, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MOD):
            operator = self.current_token.value
            if self.current_token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif self.current_token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            else:
                self.eat(TokenType.MOD)
            node = BinaryOp(node, operator, self.factor())
        return node

    def factor(self):
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node
        else:
            raise Exception(f"Invalid expression at token {token}")
