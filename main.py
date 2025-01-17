import argparse
from antlr4 import *
from gen.LPMSLexer import LPMSLexer
from gen.LPMSParser import LPMSParser
from lpms.LPMSErrorListener import LPMSErrorListener
from lpms.LPMSBaseListener import SemanticAnalyzer
from antlr4.tree.Trees import Trees

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("arquivo", type=str)
    args = parser.parse_args()

    input_stream = FileStream(args.arquivo, encoding="utf-8")

    lexer = LPMSLexer(input_stream)
    fluxo_de_tokens = CommonTokenStream(lexer)

    parser = LPMSParser(fluxo_de_tokens)

    error_listener = LPMSErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.program()

    if error_listener.has_errors():
        print(error_listener.get_errors()[0])
    else:
        analyzer = SemanticAnalyzer()
        analyzer.visit(tree)

        if analyzer.has_errors():
            print(analyzer.get_errors()[0])
        else:
            tree_dot = Trees.toStringTree(tree, None, parser)
            print(tree_dot)


if __name__ == "__main__":
    main()
