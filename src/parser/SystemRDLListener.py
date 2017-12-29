# Generated from SystemRDL.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SystemRDLParser import SystemRDLParser
else:
    from SystemRDLParser import SystemRDLParser

# This class defines a complete listener for a parse tree produced by SystemRDLParser.
class SystemRDLListener(ParseTreeListener):

    # Enter a parse tree produced by SystemRDLParser#prog.
    def enterProg(self, ctx:SystemRDLParser.ProgContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#prog.
    def exitProg(self, ctx:SystemRDLParser.ProgContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#dummy.
    def enterDummy(self, ctx:SystemRDLParser.DummyContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#dummy.
    def exitDummy(self, ctx:SystemRDLParser.DummyContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#BinaryExpr.
    def enterBinaryExpr(self, ctx:SystemRDLParser.BinaryExprContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#BinaryExpr.
    def exitBinaryExpr(self, ctx:SystemRDLParser.BinaryExprContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#UnaryExpr.
    def enterUnaryExpr(self, ctx:SystemRDLParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#UnaryExpr.
    def exitUnaryExpr(self, ctx:SystemRDLParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#NOP.
    def enterNOP(self, ctx:SystemRDLParser.NOPContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#NOP.
    def exitNOP(self, ctx:SystemRDLParser.NOPContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#TernaryExpr.
    def enterTernaryExpr(self, ctx:SystemRDLParser.TernaryExprContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#TernaryExpr.
    def exitTernaryExpr(self, ctx:SystemRDLParser.TernaryExprContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#expr_primary.
    def enterExpr_primary(self, ctx:SystemRDLParser.Expr_primaryContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#expr_primary.
    def exitExpr_primary(self, ctx:SystemRDLParser.Expr_primaryContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#concatenate.
    def enterConcatenate(self, ctx:SystemRDLParser.ConcatenateContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#concatenate.
    def exitConcatenate(self, ctx:SystemRDLParser.ConcatenateContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#replicate.
    def enterReplicate(self, ctx:SystemRDLParser.ReplicateContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#replicate.
    def exitReplicate(self, ctx:SystemRDLParser.ReplicateContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#paren_expr.
    def enterParen_expr(self, ctx:SystemRDLParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#paren_expr.
    def exitParen_expr(self, ctx:SystemRDLParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#CastType.
    def enterCastType(self, ctx:SystemRDLParser.CastTypeContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#CastType.
    def exitCastType(self, ctx:SystemRDLParser.CastTypeContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#CastWidth.
    def enterCastWidth(self, ctx:SystemRDLParser.CastWidthContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#CastWidth.
    def exitCastWidth(self, ctx:SystemRDLParser.CastWidthContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#cast_width_expr.
    def enterCast_width_expr(self, ctx:SystemRDLParser.Cast_width_exprContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#cast_width_expr.
    def exitCast_width_expr(self, ctx:SystemRDLParser.Cast_width_exprContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#literal.
    def enterLiteral(self, ctx:SystemRDLParser.LiteralContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#literal.
    def exitLiteral(self, ctx:SystemRDLParser.LiteralContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#NumberInt.
    def enterNumberInt(self, ctx:SystemRDLParser.NumberIntContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#NumberInt.
    def exitNumberInt(self, ctx:SystemRDLParser.NumberIntContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#NumberHex.
    def enterNumberHex(self, ctx:SystemRDLParser.NumberHexContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#NumberHex.
    def exitNumberHex(self, ctx:SystemRDLParser.NumberHexContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#NumberVerilog.
    def enterNumberVerilog(self, ctx:SystemRDLParser.NumberVerilogContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#NumberVerilog.
    def exitNumberVerilog(self, ctx:SystemRDLParser.NumberVerilogContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#string_literal.
    def enterString_literal(self, ctx:SystemRDLParser.String_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#string_literal.
    def exitString_literal(self, ctx:SystemRDLParser.String_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#boolean_literal.
    def enterBoolean_literal(self, ctx:SystemRDLParser.Boolean_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#boolean_literal.
    def exitBoolean_literal(self, ctx:SystemRDLParser.Boolean_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#array_literal.
    def enterArray_literal(self, ctx:SystemRDLParser.Array_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#array_literal.
    def exitArray_literal(self, ctx:SystemRDLParser.Array_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#struct_literal.
    def enterStruct_literal(self, ctx:SystemRDLParser.Struct_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#struct_literal.
    def exitStruct_literal(self, ctx:SystemRDLParser.Struct_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#struct_kv.
    def enterStruct_kv(self, ctx:SystemRDLParser.Struct_kvContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#struct_kv.
    def exitStruct_kv(self, ctx:SystemRDLParser.Struct_kvContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#enum_literal.
    def enterEnum_literal(self, ctx:SystemRDLParser.Enum_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#enum_literal.
    def exitEnum_literal(self, ctx:SystemRDLParser.Enum_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#accesstype_literal.
    def enterAccesstype_literal(self, ctx:SystemRDLParser.Accesstype_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#accesstype_literal.
    def exitAccesstype_literal(self, ctx:SystemRDLParser.Accesstype_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#onreadtype_literal.
    def enterOnreadtype_literal(self, ctx:SystemRDLParser.Onreadtype_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#onreadtype_literal.
    def exitOnreadtype_literal(self, ctx:SystemRDLParser.Onreadtype_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#onwritetype_literal.
    def enterOnwritetype_literal(self, ctx:SystemRDLParser.Onwritetype_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#onwritetype_literal.
    def exitOnwritetype_literal(self, ctx:SystemRDLParser.Onwritetype_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#addressingtype_literal.
    def enterAddressingtype_literal(self, ctx:SystemRDLParser.Addressingtype_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#addressingtype_literal.
    def exitAddressingtype_literal(self, ctx:SystemRDLParser.Addressingtype_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#precedencetype_literal.
    def enterPrecedencetype_literal(self, ctx:SystemRDLParser.Precedencetype_literalContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#precedencetype_literal.
    def exitPrecedencetype_literal(self, ctx:SystemRDLParser.Precedencetype_literalContext):
        pass


    # Enter a parse tree produced by SystemRDLParser#reference.
    def enterReference(self, ctx:SystemRDLParser.ReferenceContext):
        pass

    # Exit a parse tree produced by SystemRDLParser#reference.
    def exitReference(self, ctx:SystemRDLParser.ReferenceContext):
        pass


