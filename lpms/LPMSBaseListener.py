from gen.LPMSParser import LPMSParser
from gen.LPMSVisitor import LPMSVisitor


class SemanticAnalyzer(LPMSVisitor):
    def __init__(self):
        self.symbol_table = {}  # Tabela de símbolos
        self.errors = []

    def visitDeclarations(self, ctx: LPMSParser.DeclarationsContext):

        if ctx:
            for var in ctx.ID():
                var_name = var.getText()
                var_type = ctx.TYPE().getText()  # Obtendo o tipo da variável
                if var_name in self.symbol_table:
                    self.errors.append(
                        f"Erro semântico na linha {var.symbol.line}:{var.symbol.column} - Variável '{var_name}' já declarada."
                    )
                else:
                    self.symbol_table[var_name] = {
                        "type": var_type,
                        "value": None,  # Inicializa o valor da variável como None
                    }

    def visitAssignmentStatement(self, ctx: LPMSParser.AssignmentStatementContext):
        var_name = ctx.ID().getText()
        if var_name not in self.symbol_table:
            self.errors.append(
                f"Erro semântico na linha {ctx.ID().symbol.line}:{ctx.ID().symbol.column} - Variável '{var_name}' não declarada usada."
            )
        else:
            expected_type = self.symbol_table[var_name]["type"]
            actual_type = self.inferExpressionType(ctx.expression())

            # Verificar se o tipo da expressão é compatível com o tipo da variável
            if expected_type != actual_type:
                self.errors.append(
                    f"Erro semântico na linha {ctx.ID().symbol.line} - Atribuição incompatível. Variável '{var_name}' é do tipo '{expected_type}', "
                    f"mas recebeu expressão do tipo '{actual_type}'."
                )

    def inferExpressionType(self, ctx):
        """Inferir o tipo de uma expressão."""
        # Caso a expressão seja um parêntese (subexpressão)
        if isinstance(ctx, LPMSParser.ExpressionContext) and ctx.E_PARAN():
            return self.inferExpressionType(ctx.expression(0))

        # Caso a expressão seja um valor negativo (unário)
        elif isinstance(ctx, LPMSParser.ExpressionContext) and ctx.MINUS_OPERADOR():
            return self.inferExpressionType(ctx.expression(0))

        # Caso a expressão seja uma operação aritmética (binária)
        elif (
            isinstance(ctx, LPMSParser.ExpressionContext) and len(ctx.expression()) == 2
        ):
            left_type = self.inferExpressionType(ctx.expression(0))
            right_type = self.inferExpressionType(ctx.expression(1))
            operator = ctx.getChild(1).getText()  # Pega o operador (+, -, *, /, %)

            # Verifica as operações aritméticas
            if operator in ["+", "-", "*", "/", "%"]:
                if left_type == "int" and right_type == "int":
                    return "int"
                elif left_type == "float" or right_type == "float":
                    return "float"
                return "undefined"  # Se os tipos não são compatíveis

        # Caso a expressão seja uma operação de soma ou subtração
        elif (
            isinstance(ctx, LPMSParser.ExpressionContext) and len(ctx.expression()) == 3
        ):
            left_type = self.inferExpressionType(ctx.expression(0))
            right_type = self.inferExpressionType(ctx.expression(1))
            operator = ctx.getChild(1).getText()  # Pega o operador (+ ou -)

            # Verifica as operações de soma e subtração
            if operator in ["+", "-"]:
                if left_type == "int" and right_type == "int":
                    return "int"
                elif left_type == "float" or right_type == "float":
                    return "float"
                return "undefined"  # Se os tipos não são compatíveis

        # Caso a expressão seja um valor literal INT
        elif ctx.INT():
            return "int"

        # Caso a expressão seja um valor literal FLOAT
        elif ctx.FLOAT():
            return "float"

        # Caso a expressão seja um ou mais identificadores
        elif ctx.ID():
            # ctx.ID() retorna uma lista, então precisamos iterar sobre ela
            types = []
            for id_node in ctx.ID():
                var_name = id_node.getText()
                var_type = self.symbol_table.get(var_name, {}).get("type", "undefined")
                types.append(var_type)

            # Se você quiser garantir que todos os IDs sejam do mesmo tipo:
            if len(set(types)) == 1:
                return types[0]  # Todos os tipos são iguais
            else:
                return "undefined"  # Tipos conflitantes entre os IDs

        # Caso a expressão seja uma operação lógica
        elif isinstance(ctx, LPMSParser.Logic_exprContext):
            return self.inferLogicExpressionType(ctx)

        # Se não for nenhuma das opções acima, o tipo é indefinido
        return "undefined"

    def inferLogicExpressionType(self, ctx):
        """Inferir o tipo de uma expressão lógica."""
        # Caso a expressão lógica seja uma operação de negação (unário)
        if isinstance(ctx, LPMSParser.Logic_exprContext) and ctx.NEG_OPERADOR():
            return "bool"

        # Caso a expressão lógica seja uma comparação (relacional ou igualdade)
        elif (
            isinstance(ctx, LPMSParser.Logic_exprContext) and len(ctx.logic_expr()) == 2
        ):
            left_type = self.inferExpressionType(ctx.logic_expr(0))
            right_type = self.inferExpressionType(ctx.logic_expr(1))
            operator = ctx.getChild(
                1
            ).getText()  # Pega o operador relacional ou de igualdade

            if operator in ["<", ">", "<=", ">=", "==", "!="]:
                if (
                    left_type in ["int", "float"] and right_type in ["int", "float"]
                ) or (left_type == right_type and left_type in ["bool"]):
                    return "bool"
                return "undefined"

        # Caso a expressão lógica seja um valor booleano
        elif ctx.BOOLEAN():
            return "bool"

        # Se a expressão for uma variável booleana
        elif ctx.ID():
            var_name = ctx.ID().getText()
            return self.symbol_table.get(var_name, {}).get("type", "undefined")

        # Se não for nenhuma das opções acima, o tipo é indefinido
        return "undefined"

    def visitIfStatement(self, ctx: LPMSParser.IfStatementContext):
        logic_expr = ctx.logic_expr()
        if logic_expr:
            logic_type = self.inferExpressionType(logic_expr)
            if logic_type != "bool":
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Condição do if deve ser do tipo 'bool'."
                )

    def visitWhileStatement(self, ctx: LPMSParser.WhileStatementContext):
        logic_expr = ctx.logic_expr()
        if logic_expr:
            logic_type = self.inferExpressionType(logic_expr)
            if logic_type != "bool":
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Condição do while deve ser do tipo 'bool'."
                )

    def visit(self, ctx):
        super().visit(ctx)

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors
