from gen.LPMSParser import LPMSParser
from gen.LPMSVisitor import LPMSVisitor
from antlr4 import TerminalNode


class SemanticAnalyzer(LPMSVisitor):
    def __init__(self):
        self.symbol_table = {}
        self.errors = []
        self.three_address_code = []
        self.three_address_code_assembly = []
        self.temp_counter = 0

    def new_temp(self):
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name

    def add_three_address_code(self, code):
        self.three_address_code.append(code)
        self.three_address_code_assembly.append(code)

    def only_assembly_add_three_address_code(self, code):
        self.three_address_code_assembly.append(code)

    def generate_assembly_code(self):
        bss_code = []
        text_code = []
        data_code = []

        variables = set()
        strings = {}
        defined_variables = []
        for code in self.three_address_code_assembly:
            if code.startswith("print"):
                value_list = code[6:].strip()
                if value_list.startswith('"') and value_list.endswith('"'):
                    if value_list not in strings:
                        label = f"msg{len(strings)}"
                        strings[value_list] = label

                        data_code.append(f"{label} db {value_list}, 0xA, 0")
                else:
                    variables.add(value_list)
            else:
                parts = code.split(" = ")
                if len(parts) == 2:
                    var, expression = parts
                    variables.add(var)
        bss_code.append("section .bss")
        bss_code.append(f"    num resb 20")
        bss_code.append(f"    num_len resb 1")

        for var in variables:
            bss_code.append(f"    {var} resq 1")

        if strings:
            text_code.insert(0, "section .data")
            for string, label in strings.items():
                text_code.append(f"{label}: db {string}, 0xA, 0")

        text_code.append("section .text")
        text_code.append("    global _start")
        text_code.append("\n_start:")

        for index, code in enumerate(self.three_address_code_assembly):
            label_next = ""

            if index + 1 < len(self.three_address_code_assembly) - 1:
                if self.three_address_code_assembly[index + 1].startswith("if"):
                    if len(self.three_address_code_assembly[index + 1].split()) == 4:
                        label_next = self.three_address_code_assembly[
                            index + 1
                        ].split()[3]
                    else:
                        label_next = self.three_address_code_assembly[
                            index + 1
                        ].split()[4]

            parts = code.split(" = ")

            if len(parts) == 2:
                var, expression = parts
                if " " in expression:
                    operator_index = expression.index(" ")
                    left_operand = expression[:operator_index]
                    operator = expression[operator_index + 1 : operator_index + 2]
                    right_operand = expression[operator_index + 3 :]
                    if not left_operand.isdigit():
                        left_operand = f"[{left_operand}]"
                    if not right_operand.isdigit():
                        right_operand = f"[{right_operand}]"

                    if left_operand == "True":
                        left_operand = "1"
                    elif left_operand == "False":
                        left_operand = "0"

                    if right_operand == "True":
                        right_operand = "1"
                    elif right_operand == "False":
                        right_operand = "0"

                    # Comparações
                    if operator == ">":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    cmp rax, {right_operand}")
                        text_code.append(f"    jl {label_next}")
                    elif operator == "<":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    cmp rax, {right_operand}")
                        text_code.append(f"    jg {label_next}")
                    elif operator == "==":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    cmp rax, {right_operand}")
                        text_code.append(f"    je {label_next}")
                    elif operator == "!=":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    cmp rax, {right_operand}")
                        text_code.append(f"    jne {label_next}")
                    elif operator == ">=":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    cmp rax, {right_operand}")
                        text_code.append(f"    jle {label_next}")
                    elif operator == "<=":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    cmp rax, {right_operand}")
                        text_code.append(f"    jge {label_next}")

                    # Operações Aritméticas
                    elif operator == "+":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    add rax, {right_operand}")
                        text_code.append(f"    mov [{var}], rax")
                    elif operator == "-":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    sub rax, {right_operand}")
                        text_code.append(f"    mov [{var}], rax")
                    elif operator == "*":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    imul rax, {right_operand}")
                        text_code.append(f"    mov [{var}], rax")
                    elif operator == "/":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    mov rbx, {right_operand}")
                        text_code.append(f"    xor rdx, rdx")

                        text_code.append(f"    idiv rbx")

                        text_code.append(f"    mov [{var}], rax")
                    elif operator == "%":
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    mov rbx, {right_operand}")
                        text_code.append(f"    xor rdx, rdx")
                        text_code.append(f"    div rbx")
                        text_code.append(f"    mov [{var}], rdx")
                        text_code.append(f"    mov rax, {left_operand}")
                        text_code.append(f"    mov rbx, {right_operand}")
                        text_code.append(f"    xor rdx, rdx")
                        text_code.append(f"    div rbx")
                        text_code.append(f"    mov [{var}], rax")

                else:
                    print(code)
                    if var in defined_variables and not expression.isdigit():
                        text_code.append(f"    mov [{var}], rax")
                    else:
                        text_code.append(f"    mov qword [{var}], {expression}")
                        defined_variables.append(var)
            elif code.startswith("goto"):
                label = code.split()[1]
                text_code.append(f"    jmp {label}")
            elif code.startswith("if"):
                parts = code.split(" ")
                label = parts[3]
                if len(parts) == 4 or len(parts) == 5:
                    if parts[1] == "True":
                        text_code.append(f"    jmp {parts[-1]}")

            elif code.startswith("input"):
                variable = code.split()[1]

                text_code.append(f"    mov rax, 0")
                text_code.append(f"    mov rdi, 0")
                text_code.append(f"    lea rsi, [{variable}]")
                text_code.append(f"    mov rdx, 20")
                text_code.append(f"    syscall")

                text_code.append(f"    xor rax, rax")
                text_code.append(f"    mov rbx, 10")
                text_code.append(f"    call input_wait")

            elif code.startswith("print"):
                value_list = code[6:].strip()
                if value_list.startswith('"') and value_list.endswith('"'):  #
                    label = strings[value_list]
                    text_code.append(f"    mov rax, 1")
                    text_code.append(f"    mov rdi, 1")
                    text_code.append(f"    mov rsi, {label}")
                    text_code.append(f"    mov rdx, {len(value_list) - 2 + 1}")
                    text_code.append(f"    syscall")
                else:
                    text_code.append(f"    mov rax, [{value_list}]")
                    text_code.append(f"    call print_int")

            else:
                text_code.append(f"{code}")

        text_code.append("    mov rax, 60")
        text_code.append("    xor rdi, rdi")
        text_code.append("    syscall")
        text_code.append(
            """
print_int:
    mov rcx, num        ; Ponteiro para o buffer num
    mov rbx, 10         ; Divisor para obter dígitos
    xor rdx, rdx        ; Limpa rdx para a divisão

decimal_loop:
    xor rdx, rdx        ; Limpa rdx
    div rbx             ; Divide rax por 10: quociente em rax, resto em rdx
    add dl, '0'         ; Converte o dígito (resto) em ASCII
    dec rcx             ; Move o ponteiro para trás
    mov [rcx], dl       ; Armazena o dígito no buffer
    test rax, rax       ; Verifica se o quociente é 0
    jnz decimal_loop    ; Continua se ainda há dígitos para processar

    ; Calcula o comprimento do número
    mov rbx, num
    sub rbx, rcx        ; Comprimento = endereço inicial - ponteiro atual
    mov [num_len], bl   ; Armazena o comprimento

    ; Imprime o número
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; stdout
    mov rsi, rcx        ; Ponteiro para o início do número
    mov rdx, rbx        ; Comprimento do número
    syscall
    ret

string_to_int:
    ; rsi = endereço da string de entrada
    xor rax, rax       ; Limpa rax (acumulador do número)
    xor rcx, rcx       ; Limpa rcx (contador)
string_to_int_loop:
    movzx rdx, byte [rsi + rcx]  ; Pega o byte atual da string
    test rdx, rdx               ; Verifica se é o final da string
    jz string_to_int_done       ; Se for zero (fim), sai
    sub rdx, '0'                ; Converte de ASCII para valor numérico
    imul rax, rax, 10           ; Multiplica o acumulador por 10
    add rax, rdx                ; Adiciona o dígito ao acumulador
    inc rcx                     ; Incrementa o contador
    jmp string_to_int_loop      ; Repete o loop
string_to_int_done:
    ret
    
input_wait:
    ; Preparando para ler a entrada
    mov rax, 0          ; Syscall para leitura (0 - read)
    mov rdi, 0          ; stdin (entrada padrão)
    lea rsi, [num]      ; Endereço de armazenamento da entrada
    mov rdx, 20         ; Máximo de 20 bytes
    syscall             ; Executa a leitura

    ; Agora o código aguarda a entrada, o programa só continua quando pressionar "Enter"
    ; O código vai parar aqui até a entrada ser fornecida
    ret

                        """
        )
        return "\n".join(bss_code + text_code)

    # dar valor de expressoes algebricas
    def evaluateExpression(self, ctx: LPMSParser.ExpressionContext):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.symbol_table:
                return var_name
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Variável '{var_name}' não declarada."
                )
                return None
        elif (
            (
                ctx.MUL_DIV_OPERADOR()
                or ctx.SOMA_OPERADOR()
                or ctx.MINUS_OPERADOR()
                or ctx.MODULO_OPERADOR()
            )
            and ctx.expression(0)
            and ctx.expression(1)
        ):
            left_temp = self.evaluateExpression(ctx.expression(0))
            right_temp = self.evaluateExpression(ctx.expression(1))

            if left_temp is None or right_temp is None:
                return None

            operator = ctx.getChild(1).getText()
            result_temp = self.new_temp()
            self.add_three_address_code(
                f"{result_temp} = {left_temp} {operator} {right_temp}"
            )
            return result_temp

        elif ctx.E_PARAN() and ctx.D_PARAN():
            return self.evaluateExpression(ctx.expression(0))
        elif ctx.MINUS_OPERADOR() and ctx.expression(0):
            value_temp = self.evaluateExpression(ctx.expression(0))
            if value_temp is None:
                return None

            result_temp = self.new_temp()
            self.add_three_address_code(f"{result_temp} = -{value_temp}")
            return result_temp

        return None

    # dar valor de expressoes logicas
    def evaluateLogicExpression(self, ctx: LPMSParser.Logic_exprContext):
        if ctx.BOOLEAN():
            return ctx.BOOLEAN().getText()
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.symbol_table:
                return var_name
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Variável '{var_name}' não declarada."
                )
                return None
        elif ctx.NEG_OPERADOR and ctx.logic_expr(0):
            temp = self.evaluateLogicExpression(ctx.logic_expr(0))
            if temp is None:
                return None

            result_temp = self.new_temp()
            self.add_three_address_code(f"{result_temp} = !{temp}")
            return result_temp

        elif ctx.E_PARAN() and ctx.D_PARAN():
            return self.evaluateLogicalExpression(ctx.logic_expr())
        elif ctx.IGUALDADE_OPERADOR() and ctx.expression(0) and ctx.expression(1):
            left_value = self.evaluateExpression(ctx.expression(0))
            right_value = self.evaluateExpression(ctx.expression(1))

            if left_value is None or right_value is None:
                return None

            operator = ctx.IGUALDADE_OPERADOR().getText()
            result_temp = self.new_temp()
            self.add_three_address_code(
                f"{result_temp} = {left_value} {operator} {right_value}"
            )
            return result_temp

        elif ctx.IGUALDADE_OPERADOR() and ctx.logic_expr(0) and ctx.logic_expr(1):
            left_value = self.evaluateLogicExpression(ctx.logic_expr(0))
            right_value = self.evaluateLogicExpression(ctx.logic_expr(1))

            if left_value is None or right_value is None:
                return None

            operator = ctx.IGUALDADE_OPERADOR().getText()
            result_temp = self.new_temp()
            self.add_three_address_code(
                f"{result_temp} = {left_value} {operator} {right_value}"
            )
            return result_temp

            # if left_value == right_value:
            #     operator = ctx.RELACIONAL_OPERADOR().getText()
            #     result_temp = self.new_temp()
            #     self.add_three_address_code(
            #         f"{result_temp} = {left_value} {operator} {right_value}"
            #     )
            #     return True
            # else:
            #     return False

        elif ctx.RELACIONAL_OPERADOR() and ctx.expression(0) and ctx.expression(1):

            left_value = self.evaluateExpression(ctx.expression(0))
            right_value = self.evaluateExpression(ctx.expression(1))

            operator = ctx.RELACIONAL_OPERADOR().getText()
            result_temp = self.new_temp()
            self.add_three_address_code(
                f"{result_temp} = {left_value} {operator} {right_value}"
            )
            return result_temp
            # operator = ctx.RELACIONAL_OPERADOR().getText()
            # result_temp = self.new_temp()
            # self.add_three_address_code(
            #     f"{result_temp} = {left_value} {operator} {right_value}"
            # )

            # if left_value is None or right_value is None:
            #     return None

            # if ctx.RELACIONAL_OPERADOR().getText() == ">":
            #     return left_value > right_value
            # elif ctx.RELACIONAL_OPERADOR().getText() == "<":
            #     return left_value < right_value
            # elif ctx.RELACIONAL_OPERADOR().getText() == ">=":
            #     return left_value >= right_value
            # elif ctx.RELACIONAL_OPERADOR().getText() == "<=":
            #     return left_value <= right_value
            # elif ctx.RELACIONAL_OPERADOR().getText() == "!=":
            #     return left_value != right_value

        return None

    # inferir tipos de expressoes algebricas
    def inferExpressionType(self, ctx: LPMSParser.ExpressionContext):

        if (
            ctx.MUL_DIV_OPERADOR()
            or ctx.SOMA_OPERADOR()
            or ctx.MINUS_OPERADOR()
            or ctx.MODULO_OPERADOR()
        ):
            left_type = self.inferExpressionType(ctx.expression(0))
            right_type = self.inferExpressionType(ctx.expression(1))
            if str(left_type) in ["int", "float"] and str(right_type) in [
                "int",
                "float",
            ]:
                return left_type
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Operação entre tipos incompatíveis: '{left_type}' e '{right_type}'."
                )
                return None
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]["type"]
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável '{var_name}' não declarada."
                )
                return None

        elif ctx.MINUS_OPERADOR():
            return self.inferExpressionType(ctx.expression())
        elif ctx.E_PARAN() and ctx.D_PARAN():
            return self.inferExpressionType(ctx.expression(0))
        elif ctx.INT():
            return "int"
        elif ctx.FLOAT():
            return "float"
        return None

    # inferir tipos de expressoes logicas
    def inferLogicExpressionType(self, ctx: LPMSParser.Logic_exprContext):
        if ctx.BOOLEAN():
            return "bool"
        elif ctx.RELACIONAL_OPERADOR():

            left_type = self.inferExpressionType(ctx.expression(0))
            right_type = self.inferExpressionType(ctx.expression(1))

            if (
                (str(left_type) in ["int", "float"])
                and (str(right_type) in ["int", "float"])
            ) or (
                str(left_type) == "bool"
                and str(right_type) == "bool"
                and ctx.IGUALDADE_OPERADOR()
            ):
                return "bool"
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Operação relacional entre tipos incompatíveis: '{left_type}' e '{right_type}'."
                )
                return None

        elif ctx.IGUALDADE_OPERADOR() and ctx.expression():

            left_type = self.inferExpressionType(ctx.expression(0))
            right_type = self.inferExpressionType(ctx.expression(1))

            if (
                (str(left_type) in ["int", "float"])
                and (str(right_type) in ["int", "float"])
            ) or (
                str(left_type) == "bool"
                and str(right_type) == "bool"
                and ctx.IGUALDADE_OPERADOR()
            ):
                return "bool"
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Operação relacional entre tipos incompatíveis: '{left_type}' e '{right_type}'."
                )
                return None
        elif ctx.IGUALDADE_OPERADOR() and ctx.logic_expr():

            left_type = self.inferLogicExpressionType(ctx.logic_expr(0))
            right_type = self.inferLogicExpressionType(ctx.logic_expr(1))

            if (
                (str(left_type) in ["int", "float"])
                and (str(right_type) in ["int", "float"])
            ) or (
                str(left_type) == "bool"
                and str(right_type) == "bool"
                and ctx.IGUALDADE_OPERADOR()
            ):
                return "bool"
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Operação relacional entre tipos incompatíveis: '{left_type}' e '{right_type}'."
                )
                return None
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]["type"]
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável '{var_name}' não declarada."
                )
                return None
        elif ctx.E_PARAN() and ctx.D_PARAN():
            return self.inferLogicExpressionType(ctx.logic_expr())

        elif ctx.NEG_OPERADOR():
            logic_type = self.inferLogicExpressionType(ctx.logic_expr())
            if logic_type != "bool":
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Operador '!' só pode ser aplicado em expressões do tipo 'bool'."
                )
            return "bool"
        return None

    # atribui aos IDs tipos e valores iniciais
    def visitDeclarations(self, ctx: LPMSParser.DeclarationsContext):
        if ctx:
            for var in ctx.ID():
                var_name = var.getText()
                var_type = ctx.TYPE()
                is_const = ctx.TYPE_CONST() is not None

                if var_name in self.symbol_table:
                    self.errors.append(
                        f"Erro semântico na linha {var.symbol.line}:{var.symbol.column} - Variável '{var_name}' já declarada."
                    )
                else:
                    if str(var_type) == "int":
                        default_value = 0
                    elif str(var_type) == "float":
                        default_value = 0.0
                    elif str(var_type) == "bool":
                        default_value = False
                    elif str(var_type) == "str":
                        default_value = ""
                    else:
                        default_value = None

                    if is_const:
                        if ctx.expression():
                            var_type = self.inferExpressionType(ctx.expression())
                            default_value = self.evaluateExpression(ctx.expression())
                        elif ctx.logic_expr:
                            var_type = self.inferLogicExpressionType(ctx.logic_expr())
                            default_value = self.evaluateLogicExpression(
                                ctx.logic_expr()
                            )
                        else:
                            self.errors.append(
                                f"Erro semântico na linha {var.symbol.line}:{var.symbol.column} - Constante '{var_name}' deve ser inicializada com um valor."
                            )

                    self.add_three_address_code(f"{var_name} = {default_value}")

                    self.symbol_table[var_name] = {
                        "type": var_type,
                        "value": default_value,
                        "is_const": is_const,
                    }

    # atribuir valores as variaveis
    def visitAssignmentStatement(self, ctx: LPMSParser.AssignmentStatementContext):
        var_name = ctx.ID().getText()
        # Verificar reatribuiçao
        if var_name not in self.symbol_table:
            self.errors.append(
                f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável '{var_name}' não declarada usada."
            )
        else:
            var_info = self.symbol_table[var_name]
            expected_type = var_info["type"]
            is_const = var_info["is_const"]
            # Verificar se nao foi atribuido const novamente
            if is_const:
                self.errors.append(
                    f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável constante '{var_name}' não pode ser reatribuída."
                )
            else:
                actual_type = self.inferExpressionType(ctx.expression())
                value = None
                if actual_type is None and ctx.logic_expr():
                    actual_type = self.inferLogicExpressionType(ctx.logic_expr())
                    value = self.evaluateLogicExpression(ctx.logic_expr())
                else:
                    value = self.evaluateExpression(ctx.expression())
                # Verifica se o tipo atribuido é igual ao da variavel
                if str(expected_type) != str(actual_type):
                    self.errors.append(
                        f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Atribuição incompatível. Variável '{var_name}' é do tipo '{expected_type}', "
                        f"mas recebeu expressão do tipo '{actual_type}'."
                    )
                else:
                    self.add_three_address_code(f"{var_name} = {value}")
                    self.symbol_table[var_name]["value"] = value

    # verificar bloco de input
    def visitInput(self, ctx: LPMSParser.InputContext):
        var_list = ctx.varList()
        for var in var_list.ID():
            var_name = var.getText()
            if var_name not in self.symbol_table:
                self.errors.append(
                    f"Erro semântico na linha {var.symbol.line}:{var.symbol.column} - Variável '{var_name}' não declarada no 'input'."
                )
            else:
                var_type = self.symbol_table[var_name]["type"]

                if str(var_type) not in ["int", "float", "str", "bool"]:
                    self.errors.append(
                        f"Erro semântico na linha {var.symbol.line}:{var.symbol.column} - Tipo '{var_type}' da variável '{var_name}' não é compatível com o 'input'."
                    )
                self.only_assembly_add_three_address_code(f"input {var_name}")

    # verificar bloco de print
    def visitOutput(self, ctx: LPMSParser.OutputContext):
        value_list = ctx.valueList()

        for value in value_list.children:
            if isinstance(value, TerminalNode):
                value_type = value.symbol.type
                if value_type == LPMSParser.STRING:
                    self.only_assembly_add_three_address_code(
                        f"print {value.getText()}"
                    )
                elif value_type == LPMSParser.ID:
                    # Aqui retornamos o nome da variável (getText() fornece o nome)
                    variable_name = value.getText()
                    self.only_assembly_add_three_address_code(f"print {variable_name}")

            elif isinstance(value, LPMSParser.ExpressionContext):
                inferred_value = self.inferExpressionType(value)

                self.only_assembly_add_three_address_code(f"print {value.getText()}")

            elif isinstance(value, LPMSParser.LogicExprContext):
                inferred_value = self.inferLogicExpressionType(value)
                self.only_assembly_add_three_address_code(f"print {inferred_value}")

    # verificar bloco while
    def visitWhileStatement(self, ctx: LPMSParser.WhileStatementContext):
        label_start = f"L{self.temp_counter}"
        self.temp_counter += 1
        label_end = f"L{self.temp_counter}"
        self.temp_counter += 1

        self.add_three_address_code(f"{label_start}:")

        value = self.evaluateLogicExpression(ctx.logic_expr())
        type = self.inferLogicExpressionType(ctx.logic_expr())

        if type != "bool":
            self.errors.append(
                f"Erro semântico na linha {ctx.start.line} - Condição do 'while' deve ser do tipo 'bool', mas é '{type}'."
            )
        self.add_three_address_code(f"if not {value} goto {label_end}")

        self.visitBlockWhile(ctx.blockWhile(), label_start, label_end)

        self.add_three_address_code(f"goto {label_start}")
        self.add_three_address_code(f"{label_end}:")

    def visitBlockWhile(
        self, ctx: LPMSParser.BlockWhileContext, label_start, label_end
    ):
        for child in ctx.children:
            if isinstance(child, LPMSParser.StatementContext):
                self.visit(child)
            elif child.getText() == "break":
                self.add_three_address_code(f"goto {label_end}")

    # verificar bloco if e else se existir
    def visitIfStatement(self, ctx: LPMSParser.IfStatementContext):
        value = self.evaluateLogicExpression(ctx.logic_expr())
        type = self.inferLogicExpressionType(ctx.logic_expr())
        if value is None:
            return

        label_true = f"L{self.temp_counter}"
        self.temp_counter += 1
        label_end = f"L{self.temp_counter}"
        self.temp_counter += 1

        if type != "bool":
            self.errors.append(
                f"Erro semântico na linha {ctx.start.line} - Condição do 'if' deve ser do tipo 'bool', mas é '{type}'."
            )
        self.add_three_address_code(f"if {value} goto {label_true}")
        self.add_three_address_code(f"goto {label_end}")
        self.add_three_address_code(f"{label_true}:")

        self.visit(ctx.block(0))

        if ctx.ELSE_CONDICIONAL():
            label_else = f"L{self.temp_counter}"
            self.temp_counter += 1

            self.add_three_address_code(f"goto {label_else}")
            self.add_three_address_code(f"{label_end}:")

            self.visit(ctx.block(1))

            self.add_three_address_code(f"goto L{self.temp_counter - 1}")
            self.add_three_address_code(f"{label_else}:")
        else:
            self.add_three_address_code(f"goto L{self.temp_counter - 1}")

            self.add_three_address_code(f"{label_end}:")

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors
