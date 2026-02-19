class ASTNode:
    pass


# Program Structure
class Program(ASTNode):
    def __init__(self, declarations, statements):
        self.declarations = declarations
        self.statements = statements

    def __repr__(self):
        return f"Program(declarations={self.declarations}, statements={self.statements})"


class Declaration(ASTNode):
    def __init__(self, var_name, initializer=None):
        self.var_name = var_name
        self.initializer = initializer

    def __repr__(self):
        return f"Declaration({self.var_name}, init={self.initializer})"


# Statements
class Assignment(ASTNode):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

    def __repr__(self):
        return f"Assignment({self.var_name}, {self.expression})"


class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Print({self.expression})"


class IfStatement(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def __repr__(self):
        return f"If({self.condition}, {self.true_block}, else={self.false_block})"


class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"


# Expressions
class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.operator}, {self.right})"


class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"
