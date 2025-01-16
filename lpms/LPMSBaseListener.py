from gen.LPMSParser import LPMSParser
from gen.LPMSVisitor import LPMSVisitor
from antlr4 import TerminalNode


class SemanticAnalyzer(LPMSVisitor):
    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def evaluateExpression(self, ctx: LPMSParser.ExpressionContext):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.FLOAT():
            return float(ctx.FLOAT().getText())
        elif ctx.ID():
            var_name = ctx.ID().getText()
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]["value"]
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
            left_value = self.evaluateExpression(ctx.expression(0))
            right_value = self.evaluateExpression(ctx.expression(1))

            if left_value is None or right_value is None:
                return None

            if ctx.SOMA_OPERADOR():
                return left_value + right_value
            elif ctx.MINUS_OPERADOR():
                return left_value - right_value
            elif ctx.MUL_DIV_OPERADOR():
                return left_value * right_value
            elif ctx.MODULO_OPERADOR():
                return left_value % right_value
        elif ctx.E_PARAN() and ctx.D_PARAN():
            return self.evaluateExpression(ctx.expression(0))
        elif ctx.MINUS_OPERADOR() and ctx.expression(0):
            value = self.evaluateExpression(ctx.expression(0))

            if value is None:
                return None

            if isinstance(value, (int, float)):
                return -value
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - O operador '-' só pode ser aplicado a números, mas foi aplicado a '{value}'."
                )
                return None

        return None

    def evaluateLogicExpression(self, ctx: LPMSParser.Logic_exprContext):
        if ctx.BOOLEAN():
            return bool(ctx.BOOLEAN().getText())
        elif ctx.ID():  
            var_name = ctx.ID().getText()
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]["value"]
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - Variável '{var_name}' não declarada."
                )
                return None
        elif ctx.NOT_OPERADOR() and ctx.logic_expr(0):
            value = self.evaluateLogicalExpression(ctx.logic_expr(0))

            if value is None:
                return None

            if isinstance(value, bool):
                return not value
            else:
                self.errors.append(
                    f"Erro semântico na linha {ctx.start.line} - O operador '!' só pode ser aplicado a valores booleanos, mas foi aplicado a '{value}'."
                )
                return None
        elif ctx.E_PARAN() and ctx.D_PARAN():
            return self.evaluateLogicalExpression(ctx.logic_expr())
        elif ctx.IGUALDADE_OPERADOR() and ctx.expression(0) and ctx.expression(1):
            left_value = self.evaluateAlgebraicExpression(ctx.expression(0))
            right_value = self.evaluateAlgebraicExpression(ctx.expression(1))

            if left_value is None or right_value is None:
                return None
            if left_value == right_value:
                return True
            else:
                return False

        elif ctx.IGUALDADE_OPERADOR() and ctx.logic_expr(0) and ctx.logic_expr(1):
            left_value = self.evaluateLogicExpression(ctx.logic_expr(0))
            right_value = self.evaluateLogicExpression(ctx.logic_expr(1))

            if left_value is None or right_value is None:
                return None

            if left_value == right_value:
                return True
            else:
                return False

        elif ctx.RELACIONAL_OPERADOR() and ctx.expression(0) and ctx.expression(1):

            left_value = self.evaluateAlgebraicExpression(ctx.expression(0))
            right_value = self.evaluateAlgebraicExpression(ctx.expression(1))

            if left_value is None or right_value is None:
                return None

            if ctx.RELACIONAL_OPERADOR().getText() == ">":
                return left_value > right_value
            elif ctx.RELACIONAL_OPERADOR().getText() == "<":
                return left_value < right_value
            elif ctx.RELACIONAL_OPERADOR().getText() == ">=":
                return left_value >= right_value
            elif ctx.RELACIONAL_OPERADOR().getText() == "<=":
                return left_value <= right_value
            elif ctx.RELACIONAL_OPERADOR().getText() == "!=":
                return left_value != right_value

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

                    self.symbol_table[var_name] = {
                        "type": var_type,
                        "value": default_value,
                        "is_const": is_const,
                    }

    # Atribuir valores as variaveis
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
                    self.symbol_table[var_name]["value"] = value

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

    def visitOutput(self, ctx: LPMSParser.OutputContext):
        value_list = ctx.valueList()

        for value in value_list.children:
            if isinstance(value, TerminalNode):
                if value.symbol.type == LPMSParser.STRING:
                    continue
                elif value.symbol.type == LPMSParser.ID:
                    continue
            elif isinstance(value, LPMSParser.ExpressionContext):
                self.inferExpressionType(value)
            elif isinstance(value, LPMSParser.LogicExprContext):
                self.inferLogicExpressionType(value)

    def visitWhileStatement(self, ctx: LPMSParser.WhileStatementContext):
        condition = ctx.logic_expr()

        condition_type = self.inferLogicExpressionType(condition)
        if condition_type != "bool":
            self.errors.append(
                f"Erro semântico na linha {ctx.start.line} - Condição do 'while' deve ser do tipo 'bool', mas é '{condition_type}'."
            )

        self.visit(ctx.block())

    def visitIfStatement(self, ctx: LPMSParser.IfStatementContext):
        condition = ctx.logic_expr()

        condition_type = self.inferLogicExpressionType(condition)

        if condition_type != "bool":
            self.errors.append(
                f"Erro semântico na linha {ctx.start.line} - Condição do 'if' deve ser do tipo 'bool', mas é '{condition_type}'."
            )
        self.visit(ctx.block(0))

        if ctx.ELSE_CONDICIONAL():
            self.visit(ctx.block(1))

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors
