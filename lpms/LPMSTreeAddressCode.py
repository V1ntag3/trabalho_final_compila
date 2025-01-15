from antlr4 import TerminalNode
from gen.LPMSParser import LPMSParser
from lpms.LPMSBaseListener import SemanticAnalyzer


class ThreeAddressCodeGenerator(SemanticAnalyzer):
    def __init__(self):
        super().__init__()
        self.temp_count = 0  # Para gerar nomes de variáveis temporárias
        self.quadruples = []  # Lista para armazenar o código gerado
        self.label_count = 0  # Contador para rótulos de saltos

    def new_temp(self):
        """Gera uma nova variável temporária."""
        temp_name = f"T{self.temp_count}"
        self.temp_count += 1
        return temp_name

    def new_label(self):
        """Gera um novo rótulo para salto."""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

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
                    if var_type == "int":
                        default_value = 0
                    elif var_type == "float":
                        default_value = 0.0
                    elif var_type == "bool":
                        default_value = False
                    elif var_type == "str":
                        default_value = ""
                    else:
                        default_value = None

                    self.symbol_table[var_name] = {
                        "type": var_type,
                        "value": default_value,
                        "is_const": is_const,
                    }

                    # Gerar declaração no código de 3 endereços (apenas se não for const)
                    if not is_const:
                        self.quadruples.append(f"{var_name} = {default_value}")

    def visitAssignmentStatement(self, ctx: LPMSParser.AssignmentStatementContext):
        var_name = ctx.ID().getText()
        if var_name not in self.symbol_table:
            self.errors.append(
                f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável '{var_name}' não declarada usada."
            )
        else:
            var_info = self.symbol_table[var_name]
            expected_type = var_info["type"]
            is_const = var_info["is_const"]

            if is_const:
                self.errors.append(
                    f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável constante '{var_name}' não pode ser reatribuída."
                )
            else:
                actual_type = self.inferExpressionType(ctx.expression())
                if actual_type is None:
                    actual_type = self.inferLogicExpressionType(ctx.logic_expr())

                if str(expected_type) != str(actual_type):
                    self.errors.append(
                        f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Atribuição incompatível. Variável '{var_name}' é do tipo '{expected_type}', "
                        f"mas recebeu expressão do tipo '{actual_type}'."
                    )
                else:
                    # Gerar código de 3 endereços para a atribuição
                    expr_result = self.visit(ctx.expression())
                    self.quadruples.append(f"{var_name} = {expr_result}")

    def inferExpressionType(self, ctx):
        if ctx.INT():
            return "int"
        elif ctx.FLOAT():
            return "float"
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]["type"]
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável '{var_name}' não declarada."
                )
                return None
        # Outras verificações de expressões
        return None

    def visitExpression(self, ctx):
        """Visita uma expressão e retorna um valor que representa a operação em código de 3 endereços."""
        if ctx.INT():
            return ctx.INT().getText()
        elif ctx.FLOAT():
            return ctx.FLOAT().getText()
        elif ctx.ID():
            return ctx.ID().getText()
        elif ctx.MINUS_OPERADOR():
            operand = self.visit(ctx.expression())  # Pode ser uma expressão recursiva
            temp_var = self.new_temp()
            self.quadruples.append(f"{temp_var} = -{operand}")
            return temp_var
        elif ctx.MUL_DIV_OPERADOR():
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            temp_var = self.new_temp()
            if ctx.MUL_DIV_OPERADOR().getText() == "*":
                self.quadruples.append(f"{temp_var} = {left} * {right}")
            else:
                self.quadruples.append(f"{temp_var} = {left} / {right}")
            return temp_var
        # Lógica adicional para outros tipos de expressões

    def visitOutput(self, ctx: LPMSParser.OutputContext):
        value_list = ctx.valueList()
        for value in value_list.children:
            if isinstance(value, TerminalNode):
                if value.symbol.type == LPMSParser.STRING:
                    self.quadruples.append(f"print {value.getText()}")
                elif value.symbol.type == LPMSParser.ID:
                    var_name = value.getText()
                    self.quadruples.append(f"print {var_name}")
            elif isinstance(value, LPMSParser.ExpressionContext):
                expr_result = self.visit(value)
                self.quadruples.append(f"print {expr_result}")
            elif isinstance(value, LPMSParser.LogicExprContext):
                expr_result = self.inferLogicExpressionType(value)
                self.quadruples.append(f"print {expr_result}")

    def get_code(self):
        return "\n".join(self.quadruples)
