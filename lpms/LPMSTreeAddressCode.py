from gen.LPMSParser import LPMSParser
from gen.LPMSVisitor import LPMSVisitor
from antlr4 import TerminalNode


class ThreeAddressCodeGenerator(LPMSVisitor):
    def __init__(self):
        self.symbol_table = {}
        self.errors = []
        self.three_address_code = []
        self.temp_counter = 0

    def new_temp(self):
        temp_var = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_var

    def emit(self, code):
        self.three_address_code.append(code)

    def evaluateExpression(self, ctx: LPMSParser.ExpressionContext):
        if ctx.INT():
            return ctx.INT().getText()
        elif ctx.FLOAT():
            return ctx.FLOAT().getText()
        elif ctx.ID():
            return ctx.ID().getText()
        elif (
            ctx.MUL_DIV_OPERADOR()
            or ctx.SOMA_OPERADOR()
            or ctx.MINUS_OPERADOR()
            or ctx.MODULO_OPERADOR()
        ):
            left = self.evaluateExpression(ctx.expression(0))
            right = self.evaluateExpression(ctx.expression(1))
            operator = ctx.getChild(1).getText()
            temp_var = self.new_temp()
            self.emit(f"{temp_var} = {left} {operator} {right}")
            return temp_var
        elif ctx.E_PARAN() and ctx.D_PARAN():
            return self.evaluateExpression(ctx.expression(0))
        elif ctx.MINUS_OPERADOR():
            operand = self.evaluateExpression(ctx.expression(0))
            temp_var = self.new_temp()
            self.emit(f"{temp_var} = -{operand}")
            return temp_var

    def evaluateLogicExpression(self, ctx: LPMSParser.Logic_exprContext):
        if ctx.BOOLEAN():
            return ctx.BOOLEAN().getText()
        elif ctx.ID():
            return ctx.ID().getText()
        elif ctx.NOT_OPERADOR():
            operand = self.evaluateLogicExpression(ctx.logic_expr(0))
            temp_var = self.new_temp()
            self.emit(f"{temp_var} = NOT {operand}")
            return temp_var
        elif ctx.IGUALDADE_OPERADOR() or ctx.RELACIONAL_OPERADOR():
            left = self.evaluateExpression(ctx.expression(0))
            right = self.evaluateExpression(ctx.expression(1))
            operator = ctx.getChild(1).getText()
            temp_var = self.new_temp()
            self.emit(f"{temp_var} = {left} {operator} {right}")
            return temp_var

    def visitDeclarations(self, ctx: LPMSParser.DeclarationsContext):
        for var in ctx.ID():
            var_name = var.getText()
            var_type = ctx.TYPE().getText()
            is_const = ctx.TYPE_CONST() is not None

            if var_name in self.symbol_table:
                self.errors.append(
                    f"Erro semântico: Variável '{var_name}' já declarada."
                )
            else:
                default_value = (
                    0
                    if var_type in ["int", "float"]
                    else "False" if var_type == "bool" else ""
                )
                self.symbol_table[var_name] = {
                    "type": var_type,
                    "value": default_value,
                    "is_const": is_const,
                }
                self.emit(f"DECLARE {var_name} : {var_type}")

    def visitAssignmentStatement(self, ctx: LPMSParser.AssignmentStatementContext):
        var_name = ctx.ID().getText()

        if var_name not in self.symbol_table:
            self.errors.append(f"Erro semântico: Variável '{var_name}' não declarada.")
        else:
            value = None
            if ctx.expression():
                value = self.evaluateExpression(ctx.expression())
            elif ctx.logic_expr():
                value = self.evaluateLogicExpression(ctx.logic_expr())

            if value:
                self.emit(f"{var_name} = {value}")

    def visitInput(self, ctx: LPMSParser.InputContext):
        for var in ctx.varList().ID():
            var_name = var.getText()
            if var_name not in self.symbol_table:
                self.errors.append(
                    f"Erro semântico: Variável '{var_name}' não declarada no 'input'."
                )
            else:
                self.emit(f"READ {var_name}")

    def visitOutput(self, ctx: LPMSParser.OutputContext):
        for value in ctx.valueList().children:
            if isinstance(value, TerminalNode):
                if value.symbol.type == LPMSParser.STRING:
                    self.emit(f"PRINT {value.getText()}")
                elif value.symbol.type == LPMSParser.ID:
                    self.emit(f"PRINT {value.getText()}")
            elif isinstance(value, LPMSParser.ExpressionContext):
                expr = self.evaluateExpression(value)
                self.emit(f"PRINT {expr}")

    def visitWhileStatement(self, ctx: LPMSParser.WhileStatementContext):
        condition = self.evaluateLogicExpression(ctx.logic_expr())
        self.emit(f"LABEL_WHILE:")
        self.emit(f"IF NOT {condition} GOTO END_WHILE")
        self.visit(ctx.block())
        self.emit(f"GOTO LABEL_WHILE")
        self.emit(f"END_WHILE:")

    def visitIfStatement(self, ctx: LPMSParser.IfStatementContext):
        condition = self.evaluateLogicExpression(ctx.logic_expr())
        self.emit(f"IF NOT {condition} GOTO ELSE")
        self.visit(ctx.block(0))
        if ctx.ELSE_CONDICIONAL():
            self.emit(f"GOTO END_IF")
            self.emit(f"ELSE:")
            self.visit(ctx.block(1))
        self.emit(f"END_IF:")

    def get_three_address_code(self):
        return self.three_address_code

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors
