from antlr4 import *
from gen.LPMSLexer import LPMSLexer
from gen.LPMSParser import LPMSParser
from lpms.LPMSErrorListener import LPMSErrorListener
from lpms.LPMSBaseListener import SemanticAnalyzer
from lpms.LPMSTreeAddressCode import ThreeAddressCodeGenerator
import argparse


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
    parser = argparse.ArgumentParser(
        description="Compilador LPMS: Análise semântica e geração de código intermediário."
    )
    parser.add_argument(
        "arquivo", type=str, help="Caminho para o arquivo de código-fonte LPMS."
    )
    args = parser.parse_args()

    input_stream = FileStream(args.arquivo)

    lexer = LPMSLexer(input_stream)
    fluxo_de_tokens = CommonTokenStream(lexer)

    parser = LPMSParser(fluxo_de_tokens)

    error_listener = LPMSErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.program()

    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)

    if analyzer.has_errors():
        print("Erros Semânticos Encontrados:")
        for error in analyzer.get_errors():
            print(error)
        return

    print("Análise semântica concluída com sucesso!")

    try:
        code_generator = ThreeAddressCodeGenerator()
        code_generator.visit(tree)
        code = code_generator.get_three_address_code()

        print("Código de Três Endereços Gerado:")
        for quad in code:
            print(quad)
    except AttributeError as e:
        print("Erro ao gerar o código intermediário:", e)
    except Exception as e:
        print("Erro inesperado:", e)


if __name__ == "__main__":
    main()
