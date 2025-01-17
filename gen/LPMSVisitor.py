# Generated from /Users/marcosviniciusribeiroalencar/Documents/Workspace/workspace-universidade/trabalho_final_compila/LPMS.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LPMSParser import LPMSParser
else:
    from LPMSParser import LPMSParser

# This class defines a complete generic visitor for a parse tree produced by LPMSParser.

class LPMSVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LPMSParser#program.
    def visitProgram(self, ctx:LPMSParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#programSection.
    def visitProgramSection(self, ctx:LPMSParser.ProgramSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#block.
    def visitBlock(self, ctx:LPMSParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#blockWhile.
    def visitBlockWhile(self, ctx:LPMSParser.BlockWhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#statement.
    def visitStatement(self, ctx:LPMSParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#declarations.
    def visitDeclarations(self, ctx:LPMSParser.DeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:LPMSParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#ifStatement.
    def visitIfStatement(self, ctx:LPMSParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#whileStatement.
    def visitWhileStatement(self, ctx:LPMSParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#expression.
    def visitExpression(self, ctx:LPMSParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#logic_expr.
    def visitLogic_expr(self, ctx:LPMSParser.Logic_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#input.
    def visitInput(self, ctx:LPMSParser.InputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#varList.
    def visitVarList(self, ctx:LPMSParser.VarListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#output.
    def visitOutput(self, ctx:LPMSParser.OutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LPMSParser#valueList.
    def visitValueList(self, ctx:LPMSParser.ValueListContext):
        return self.visitChildren(ctx)



del LPMSParser