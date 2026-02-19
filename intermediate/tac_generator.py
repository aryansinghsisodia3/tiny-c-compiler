"""
tac_generator.py

Generates Three Address Code (TAC) from AST
"""

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.code = []

    # ==============================
    # Utility Functions
    # ==============================

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instruction):
        self.code.append(instruction)

    # ==============================
    # Main Entry
    # ==============================

    def generate(self, node):
        method_name = f"gen_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_gen)
        return method(node)

    def generic_gen(self, node):
        raise Exception(f"No TAC generator for {type(node).__name__}")

    # ==============================
    # AST Node Generators
    # ==============================

    def gen_Program(self, node):
        for stmt in node.statements:
            self.generate(stmt)
        return self.code

    # ------------------------------
    # Declarations
    # ------------------------------

    def gen_Declaration(self, node):
        # No TAC needed for simple int declaration
        pass

    # ------------------------------
    # Statements
    # ------------------------------

    def gen_Assignment(self, node):
        value = self.generate(node.expression)
        self.emit(f"{node.var_name} = {value}")

    def gen_PrintStatement(self, node):
        value = self.generate(node.expression)
        self.emit(f"print {value}")

    def gen_IfStatement(self, node):
        condition = self.generate(node.condition)

        label_else = self.new_label()
        label_end = self.new_label()

        self.emit(f"ifFalse {condition} goto {label_else}")

        # True block
        self.generate(node.true_block)

        self.emit(f"goto {label_end}")
        self.emit(f"{label_else}:")

        # False block
        if node.false_block:
            self.generate(node.false_block)

        self.emit(f"{label_end}:")

    def gen_WhileStatement(self, node):
        label_start = self.new_label()
        label_end = self.new_label()

        self.emit(f"{label_start}:")

        condition = self.generate(node.condition)
        self.emit(f"ifFalse {condition} goto {label_end}")

        self.generate(node.body)

        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")

    def gen_Block(self, node):
        for stmt in node.statements:
            self.generate(stmt)

    # ==============================
    # Expressions
    # ==============================

    def gen_BinaryOp(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)

        temp = self.new_temp()
        self.emit(f"{temp} = {left} {node.operator} {right}")
        return temp

    def gen_Number(self, node):
        return node.value

    def gen_Identifier(self, node):
        return node.name
