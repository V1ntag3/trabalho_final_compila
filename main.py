import argparse
from antlr4 import *
from gen.LPMSLexer import LPMSLexer
from gen.LPMSParser import LPMSParser
from lpms.LPMSErrorListener import LPMSErrorListener
from lpms.LPMSBaseListener import SemanticAnalyzer


def print_ast(tree, parser, indent=0):
    def recursive_print(node, level):
        if node.getChildCount() == 0:
            return "  " * level + node.getText()

        children = [recursive_print(child, level + 1) for child in node.getChildren()]
        rule_name = parser.ruleNames[node.getRuleIndex()]
        return (
            "  " * level
            + f"({rule_name}\n"
            + "\n".join(children)
            + f"\n{'  ' * level})"
        )

    return recursive_print(tree, indent)


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
            print(print_ast(tree, parser))


if __name__ == "__main__":
    main()
