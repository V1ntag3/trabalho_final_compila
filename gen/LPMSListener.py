# Generated from /Users/marcosviniciusribeiroalencar/Documents/Workspace/workspace-universidade/trabalho_final_compila/LPMS.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LPMSParser import LPMSParser
else:
    from LPMSParser import LPMSParser

# This class defines a complete listener for a parse tree produced by LPMSParser.
class LPMSListener(ParseTreeListener):

    # Enter a parse tree produced by LPMSParser#program.
    def enterProgram(self, ctx:LPMSParser.ProgramContext):
        pass

    # Exit a parse tree produced by LPMSParser#program.
    def exitProgram(self, ctx:LPMSParser.ProgramContext):
        pass


    # Enter a parse tree produced by LPMSParser#programSection.
    def enterProgramSection(self, ctx:LPMSParser.ProgramSectionContext):
        pass

    # Exit a parse tree produced by LPMSParser#programSection.
    def exitProgramSection(self, ctx:LPMSParser.ProgramSectionContext):
        pass


    # Enter a parse tree produced by LPMSParser#declarations.
    def enterDeclarations(self, ctx:LPMSParser.DeclarationsContext):
        pass

    # Exit a parse tree produced by LPMSParser#declarations.
    def exitDeclarations(self, ctx:LPMSParser.DeclarationsContext):
        pass


    # Enter a parse tree produced by LPMSParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:LPMSParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by LPMSParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:LPMSParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by LPMSParser#block.
    def enterBlock(self, ctx:LPMSParser.BlockContext):
        pass

    # Exit a parse tree produced by LPMSParser#block.
    def exitBlock(self, ctx:LPMSParser.BlockContext):
        pass


    # Enter a parse tree produced by LPMSParser#statement.
    def enterStatement(self, ctx:LPMSParser.StatementContext):
        pass

    # Exit a parse tree produced by LPMSParser#statement.
    def exitStatement(self, ctx:LPMSParser.StatementContext):
        pass


    # Enter a parse tree produced by LPMSParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:LPMSParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by LPMSParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:LPMSParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by LPMSParser#ifStatement.
    def enterIfStatement(self, ctx:LPMSParser.IfStatementContext):
        pass

    # Exit a parse tree produced by LPMSParser#ifStatement.
    def exitIfStatement(self, ctx:LPMSParser.IfStatementContext):
        pass


    # Enter a parse tree produced by LPMSParser#whileStatement.
    def enterWhileStatement(self, ctx:LPMSParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by LPMSParser#whileStatement.
    def exitWhileStatement(self, ctx:LPMSParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by LPMSParser#expressionStatement.
    def enterExpressionStatement(self, ctx:LPMSParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by LPMSParser#expressionStatement.
    def exitExpressionStatement(self, ctx:LPMSParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by LPMSParser#expression.
    def enterExpression(self, ctx:LPMSParser.ExpressionContext):
        pass

    # Exit a parse tree produced by LPMSParser#expression.
    def exitExpression(self, ctx:LPMSParser.ExpressionContext):
        pass


    # Enter a parse tree produced by LPMSParser#logic_expr.
    def enterLogic_expr(self, ctx:LPMSParser.Logic_exprContext):
        pass

    # Exit a parse tree produced by LPMSParser#logic_expr.
    def exitLogic_expr(self, ctx:LPMSParser.Logic_exprContext):
        pass


    # Enter a parse tree produced by LPMSParser#values_permitidos.
    def enterValues_permitidos(self, ctx:LPMSParser.Values_permitidosContext):
        pass

    # Exit a parse tree produced by LPMSParser#values_permitidos.
    def exitValues_permitidos(self, ctx:LPMSParser.Values_permitidosContext):
        pass


    # Enter a parse tree produced by LPMSParser#input.
    def enterInput(self, ctx:LPMSParser.InputContext):
        pass

    # Exit a parse tree produced by LPMSParser#input.
    def exitInput(self, ctx:LPMSParser.InputContext):
        pass


    # Enter a parse tree produced by LPMSParser#varList.
    def enterVarList(self, ctx:LPMSParser.VarListContext):
        pass

    # Exit a parse tree produced by LPMSParser#varList.
    def exitVarList(self, ctx:LPMSParser.VarListContext):
        pass


    # Enter a parse tree produced by LPMSParser#output.
    def enterOutput(self, ctx:LPMSParser.OutputContext):
        pass

    # Exit a parse tree produced by LPMSParser#output.
    def exitOutput(self, ctx:LPMSParser.OutputContext):
        pass


    # Enter a parse tree produced by LPMSParser#valueList.
    def enterValueList(self, ctx:LPMSParser.ValueListContext):
        pass

    # Exit a parse tree produced by LPMSParser#valueList.
    def exitValueList(self, ctx:LPMSParser.ValueListContext):
        pass



del LPMSParser