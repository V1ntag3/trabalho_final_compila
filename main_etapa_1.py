import argparse
from antlr4 import *
from gen.LPMSLexer import LPMSLexer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("arquivo", type=str)
    args = parser.parse_args()

    try:
        input_stream = FileStream(args.arquivo)
        
        lexer = LPMSLexer(input_stream)
        fluxo_de_tokens = CommonTokenStream(lexer)
        fluxo_de_tokens.fill()

        for token in fluxo_de_tokens.tokens:
            token_name = lexer.symbolicNames[token.type]
            print(f"<{token_name}, {token.text}>")
            
    except FileNotFoundError:
        print(f"Erro: Arquivo '{args.arquivo}' não encontrado.")
        
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

if __name__ == '__main__':
    main()
