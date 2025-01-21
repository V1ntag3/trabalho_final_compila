from gen.LPMSVisitor import LPMSVisitor
from gen.LPMSParser import LPMSParser


class CustomASTVisitor(LPMSVisitor):

    def visitProgram(self, ctx: LPMSParser.ProgramContext):
        program_name = ctx.programSection().ID().getText()
        statements = [
            self.visit(statement)
            for statement in ctx.programSection().block().statement()
        ]
        return ("Program", program_name, statements)

    def visitProgramSection(self, ctx: LPMSParser.ProgramSectionContext):
        return self.visitChildren(ctx)
    

    def visitBlock(self, ctx: LPMSParser.BlockContext):
        statements = [self.visit(statement) for statement in ctx.statement()]
        return statements

    def visitDeclarations(self, ctx: LPMSParser.DeclarationsContext):
        var_type = ctx.TYPE().getText() if ctx.TYPE() else ctx.TYPE_CONST().getText()
        variables = [var.getText() for var in ctx.ID()]

        if ctx.ATRIBUICAO_OPERADOR():
            if ctx.expression():
                expression = self.visit(ctx.expression())
                return ("Declaration:", var_type, variables, expression)
            elif ctx.logic_expr():
                logic_expr = self.visit(ctx.logic_expr())
                return ("Declaration:", var_type, variables, logic_expr)
            else:
                return ("Declaration:", var_type, variables)

        else:
            return ("Declaration:", var_type, variables)

    def visitAssignmentStatement(self, ctx: LPMSParser.AssignmentStatementContext):
        var_name = ctx.ID().getText()
        expression = (
            self.visit(ctx.expression())
            if ctx.expression()
            else self.visit(ctx.logic_expr())
        )
        return ("Assignment:", var_name, expression)

    def visitIfStatement(self, ctx: LPMSParser.IfStatementContext):
        condition = self.visit(ctx.logic_expr())
        if_body = self.visit(ctx.block())

        else_body = self.visit(ctx.block()) if ctx.ELSE_CONDICIONAL() else None

        return (
            "If:",
            condition,
            if_body,
            ("Else:", else_body) if else_body else None,
        )

    def visitWhileStatement(self, ctx: LPMSParser.WhileStatementContext):
        condition = self.visit(ctx.logic_expr())
        block =  self.visit(ctx.blockWhile())
        return ("While:", condition, block)
    
    def visitBlockWhile(self, ctx: LPMSParser.BlockWhileContext):
        statements = []

        for child in ctx.children:
            if isinstance(child, LPMSParser.StatementContext):
                statements.append(self.visit(child))
            elif child.getText() == "break":
                statements.append("break")
        
        return statements

    def visitInput(self, ctx: LPMSParser.InputContext):
        variables = [var.getText() for var in ctx.varList().ID()]
        return ("Input:", variables)

    def visitOutput(self, ctx: LPMSParser.OutputContext):
        values = []

        for string in ctx.valueList().STRING():
            values.append(string.getText())

        for expression in ctx.valueList().expression():
            values.append(self.visit(expression))

        return ("Print:", values)

    def visitExpression(self, ctx: LPMSParser.ExpressionContext):
        if ctx.ID():
            return ctx.ID().getText()
        elif ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.FLOAT():
            return float(ctx.FLOAT().getText())

        elif ctx.E_PARAN() and ctx.D_PARAN():
            return f"'('{self.visit(ctx.expression(0))}')'"
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
           
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            return (ctx.getChild(1).getText(), left, right)
        elif ctx.MINUS_OPERADOR() and not ctx.expression(1):
            return f"-{self.visit(ctx.expression())}"

        return self.visitChildren(ctx)

    def visitLogic_expr(self, ctx: LPMSParser.Logic_exprContext):
        if ctx.BOOLEAN():
            return ctx.BOOLEAN().getText()
        elif ctx.RELACIONAL_OPERADOR():
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            return (ctx.RELACIONAL_OPERADOR().getText(), left, right)
        elif ctx.IGUALDADE_OPERADOR():
            left = self.visit(ctx.expression(0))
            right = self.visit(ctx.expression(1))
            return (ctx.IGUALDADE_OPERADOR().getText(), left, right)
        elif ctx.NEG_OPERADOR():
            return (ctx.NEG_OPERADOR().getText(), self.visit(ctx.logic_expr()))
        return self.visitChildren(ctx)
