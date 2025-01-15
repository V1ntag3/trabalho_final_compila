from gen.LPMSParser import LPMSParser
from gen.LPMSVisitor import LPMSVisitor


class SemanticAnalyzer(LPMSVisitor):
    def __init__(self):
        self.symbol_table = {}  # Tabela de símbolos
        self.errors = []

    def visitDeclarations(self, ctx: LPMSParser.DeclarationsContext):
        variable_declaration_ctx = ctx.variableDeclaration()
        if variable_declaration_ctx:
            for var in variable_declaration_ctx.ID():
                var_name = var.getText()
                var_type = variable_declaration_ctx.getChild(
                    0
                ).getText()  # O tipo da variável

                # Verificando se a variável já foi declarada
                if var_name in self.symbol_table:
                    self.errors.append(
                        f"Erro semântico na linha {var.symbol.line}:{var.symbol.column} - Variável '{var_name}' já declarada."
                    )
                else:
                    # Inicializa a variável com o valor padrão baseado no tipo
                    if var_type == "int":
                        self.symbol_table[var_name] = {"value": 0, "type": "int"}
                    elif var_type == "float":
                        self.symbol_table[var_name] = {"value": 0.0, "type": "float"}
                    elif var_type == "bool":
                        self.symbol_table[var_name] = {"value": False, "type": "bool"}
                    elif var_type == "str":
                        self.symbol_table[var_name] = {"value": "", "type": "str"}
                    else:
                        self.symbol_table[var_name] = {
                            "value": None,
                            "type": "undefined",
                        }

    def visitAssignmentStatement(self, ctx: LPMSParser.AssignmentStatementContext):
        var_name = ctx.ID().getText()

        # Verifica se a variável foi declarada
        if var_name not in self.symbol_table:
            self.errors.append(
                f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável '{var_name}' não declarada."
            )
        else:
            expected_type = self.symbol_table[var_name]["type"]  # Obtém o tipo esperado
            actual_type = self.inferExpressionType(ctx.expression())
            if actual_type == "undefined":
                actual_type = self.inferExpressionType(ctx.logic_expr())

            # Verificar se o tipo da expressão é compatível com o tipo da variável
            if expected_type != actual_type:
                self.errors.append(
                    f"Erro semântico na linha {ctx.ID().symbol.line} - Atribuição incompatível. Variável '{var_name}' é do tipo '{expected_type}', "
                    f"mas recebeu expressão do tipo '{actual_type}'."
                )

    def inferExpressionType(self, ctx):
        """Inferir o tipo de uma expressão."""
        print(isinstance(ctx, LPMSParser.ExpressionContext))
        if isinstance(ctx, LPMSParser.ExpressionContext):
            # Para expressões numéricas
            if ctx.INT():
                return "int"
            elif ctx.FLOAT():
                return "float"
            elif ctx.STRING():
                return "str"
            elif ctx.ID():
                var_name = ctx.ID().getText()
                return self.symbol_table.get(var_name, "undefined")
            elif ctx.expression():  # Verifica operadores e subexpressões
                left_type = self.inferExpressionType(ctx.expression(0))
                right_type = self.inferExpressionType(ctx.expression(1))
                operator = ctx.getChild(1).getText()  # Operador entre as expressões

                if operator in ["+", "-", "*", "/", "%"]:
                    if left_type == "int" and right_type == "int":
                        return "int"
                    elif left_type == "float" or right_type == "float":
                        return "float"
                    else:
                        return "undefined"
                elif operator in ["<", ">", "<=", ">=", "==", "!="]:
                    if left_type == right_type:
                        return "bool"
                    else:
                        return "undefined"

        elif isinstance(ctx, LPMSParser.Logic_exprContext):
            # Para expressões lógicas
            if ctx.BOOLEAN():
                return "bool"
            elif ctx.ID():
                var_name = ctx.ID().getText()
                return self.symbol_table.get(var_name, "undefined")
            elif ctx.expression():  # Lógica que envolve expressões
                left_type = self.inferExpressionType(ctx.expression(0))
                right_type = self.inferExpressionType(ctx.expression(1))
                operator = ctx.getChild(1).getText()  # Operador lógico

                if operator in ["and", "or"]:
                    if left_type == "bool" and right_type == "bool":
                        return "bool"
                    else:
                        return "undefined"
                elif operator in ["!", "not"]:
                    if left_type == "bool":
                        return "bool"
                    else:
                        return "undefined"

        return "undefined"

    def visitIfStatement(self, ctx: LPMSParser.IfStatementContext):
        logic_expr = ctx.logic_expr()
        if logic_expr:
            self.visit(logic_expr)

    def visit(self, ctx):
        super().visit(ctx)

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors
