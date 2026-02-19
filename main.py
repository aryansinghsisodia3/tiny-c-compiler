import sys
from lexer import Lexer
from myparser.parser import Parser
from semantic import SemanticAnalyzer
from intermediate import TACGenerator


def compile_file(filepath):
    with open(filepath, "r") as f:
        source = f.read()

    print("===== SOURCE CODE =====")
    print(source)

    # Lexing
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    print("\n===== TOKENS =====")
    for token in tokens:
        print(token)

    # Parsing
    parser = Parser(tokens)
    ast = parser.parse()

    print("\n===== AST GENERATED =====")

    # Semantic Analysis
    semantic = SemanticAnalyzer()
    semantic.visit(ast)

    print("Semantic Analysis Passed")

    # TAC Generation
    tac_gen = TACGenerator()
    tac_code = tac_gen.generate(ast)

    print("\n===== THREE ADDRESS CODE =====")
    for line in tac_code:
        print(line)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        sys.exit(1)

    compile_file(sys.argv[1])
