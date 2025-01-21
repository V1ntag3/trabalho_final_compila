# Compilador de LPMS

Este projeto foi desenvolvido em Python e inclui um arquivo `requirements.txt` para instalar as dependências necessárias. Siga as etapas abaixo para configurar o ambiente, instalar as dependências e executar o programa principal.

## Requisitos

- Python 3.13
- `pip`

## Configuração do Ambiente

1. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   ```

2. Ative o ambiente virtual:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Executando o Projeto

Com o ambiente configurado e as dependências instaladas, execute o arquivo principal:

```bash
python3 main.py input.lps
```

## Desativando o Ambiente Virtual

Quando terminar, desative o ambiente virtual:

```bash
deactivate
```

## OBS:

Os arquivos input.lps e input2.lps tem operações que estão funcionando quando executados, o main.py mostra o código de três endereços e gera o arquivo assembly_code.s que contém o código em assembly. O site que utilizamos para executar o código assembly é o https://www.mycompiler.io/pt/new/asm-x86_64.
Além disso foi feita a modificação na etapa 2 que está no main_etapa_2.py, já que somente essa semana consegui implementar AST com foi solicitado.
