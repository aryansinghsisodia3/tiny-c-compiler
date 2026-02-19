# semantic/symbol_table.py


class Symbol:
    def __init__(self, name, symbol_type):
        self.name = name
        self.type = symbol_type

    def __repr__(self):
        return f"Symbol(name={self.name}, type={self.type})"


class SymbolTable:
    def __init__(self):
        self.table = {}

    # Declare a new variable
    def declare(self, name, symbol_type):
        if name in self.table:
            raise Exception(f"Semantic Error: Variable '{name}' already declared.")
        self.table[name] = Symbol(name, symbol_type)

    # Lookup variable
    def lookup(self, name):
        if name not in self.table:
            raise Exception(f"Semantic Error: Variable '{name}' not declared.")
        return self.table[name]

    def __repr__(self):
        return str(self.table)
