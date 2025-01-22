import argparse
from antlr4 import *
from gen.LPMSLexer import LPMSLexer
from gen.LPMSParser import LPMSParser
from lpms.LPMSErrorListener import LPMSErrorListener
from lpms.LPMSBaseListener import SemanticAnalyzer
import script_exe 
def write_to_files(three_address_code, assembly_code):
    with open('three_address_code.txt', 'w') as f:
        for line in three_address_code:
            f.write(f"{line}\n")
    
    with open('assembly_code.s', 'w') as f:
        f.write(assembly_code)

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
            write_to_files(analyzer.three_address_code, analyzer.generate_assembly_code())

            for i in analyzer.three_address_code:
                print(i)

if __name__ == "__main__":
    main()
