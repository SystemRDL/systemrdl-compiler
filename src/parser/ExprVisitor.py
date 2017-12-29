import re

from antlr4 import *

from .SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from . import expressions as e

class ExprVisitor(BaseVisitor):
    
    #---------------------------------------------------------------------------
    # Numerical Expressions
    #---------------------------------------------------------------------------
    _BinaryExpr_map = {
        SystemRDLParser.EXP     : e.Exponent,
        SystemRDLParser.MULT    : e.Mult,
        SystemRDLParser.DIV     : e.Div,
        SystemRDLParser.MOD     : e.Mod,
        SystemRDLParser.PLUS    : e.Add,
        SystemRDLParser.MINUS   : e.Sub,
        SystemRDLParser.LSHIFT  : e.LShift,
        SystemRDLParser.RSHIFT  : e.RShift,
        SystemRDLParser.LT      : e.Lt,
        SystemRDLParser.LEQ     : e.Leq,
        SystemRDLParser.GT      : e.Gt,
        SystemRDLParser.GEQ     : e.Geq,
        SystemRDLParser.EQ      : e.Eq,
        SystemRDLParser.NEQ     : e.Neq,
        SystemRDLParser.AND     : e.BitwiseAnd,
        SystemRDLParser.XOR     : e.BitwiseXor,
        SystemRDLParser.XNOR    : e.BitwiseXnor,
        SystemRDLParser.OR      : e.BitwiseOr,
        SystemRDLParser.BAND    : e.BoolAnd,
        SystemRDLParser.BOR     : e.BoolOr
    }
    
    _UnaryExpr_map = {
        SystemRDLParser.PLUS    : e.UnaryPlus,
        SystemRDLParser.MINUS   : e.UnaryMinus,
        SystemRDLParser.BNOT    : e.BoolNot,
        SystemRDLParser.NOT     : e.BitwiseInvert,
        SystemRDLParser.AND     : e.AndReduce,
        SystemRDLParser.NAND    : e.NandReduce,
        SystemRDLParser.OR      : e.OrReduce,
        SystemRDLParser.NOR     : e.NorReduce,
        SystemRDLParser.XOR     : e.XorReduce,
        SystemRDLParser.XNOR    : e.XnorReduce
    }
    
    # Visit a parse tree produced by SystemRDLParser#BinaryExpr.
    def visitBinaryExpr(self, ctx:SystemRDLParser.BinaryExprContext):
        l = self.visit(ctx.expr(0))
        r = self.visit(ctx.expr(1))
        expr_class = self._BinaryExpr_map[ctx.op.type]
        return(expr_class(l,r))


    # Visit a parse tree produced by SystemRDLParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:SystemRDLParser.UnaryExprContext):
        n = self.visit(ctx.expr_primary())
        expr_class = self._UnaryExpr_map[ctx.op.type]
        return(expr_class(n))


    # Visit a parse tree produced by SystemRDLParser#TernaryExpr.
    def visitTernaryExpr(self, ctx:SystemRDLParser.TernaryExprContext):
        i = self.visit(ctx.expr(0))
        j = self.visit(ctx.expr(1))
        k = self.visit(ctx.expr(2))
        return(e.TernaryExpr(i,j,k))
    
    
    # Visit a parse tree produced by SystemRDLParser#paren_expr.
    def visitParen_expr(self, ctx:SystemRDLParser.Paren_exprContext):
        return(self.visit(ctx.expr()))
    
    #---------------------------------------------------------------------------
    # Numeric Literals
    #---------------------------------------------------------------------------
    # Visit a parse tree produced by SystemRDLParser#NumberInt.
    def visitNumberInt(self, ctx:SystemRDLParser.NumberIntContext):
        s = ctx.INT().getText()
        s.replace("_","")
        return(e.IntLiteral(int(s)))
    
    
    # Visit a parse tree produced by SystemRDLParser#NumberHex.
    def visitNumberHex(self, ctx:SystemRDLParser.NumberHexContext):
        s = ctx.HEX_INT().getText()
        s.replace("_","")
        return(e.IntLiteral(int(s,16)))
    
    
    # Visit a parse tree produced by SystemRDLParser#NumberVerilog.
    def visitNumberVerilog(self, ctx:SystemRDLParser.NumberVerilogContext):
        s = ctx.VLOG_INT().getText()
        
        m = re.fullmatch(r"(\d+)'(b|d|h)([\da-f_]+)", s, re.IGNORECASE)
        width = int(m.group(1))
        basechar = m.group(2).lower()
        if(basechar == "b"):
            base = 2
        elif(basechar == "d"):
            base = 10
        else:
            base = 16
        
        val = int(m.group(3), base)
        return(e.IntLiteral(val, width))
        
    
    # Visit a parse tree produced by SystemRDLParser#boolean_literal.
    def visitBoolean_literal(self, ctx:SystemRDLParser.Boolean_literalContext):
        if(ctx.val.type == SystemRDLParser.TRUE_kw):
            return(e.IntLiteral(1, 1))
        else:
            return(e.IntLiteral(0, 1))
        
    #---------------------------------------------------------------------------
    # Cast
    #---------------------------------------------------------------------------
    _CastWidth_map = {
        SystemRDLParser.BOOLEAN_kw  : 1,
        SystemRDLParser.BIT_kw      : 1,
        SystemRDLParser.LONGINT_kw  : 64,
    }
    # Visit a parse tree produced by SystemRDLParser#CastType.
    def visitCastType(self, ctx:SystemRDLParser.CastTypeContext):
        w = _CastWidth_map[ctx.typ.type]
        return(e.WidthCast(self.visit(ctx.expr()), w_int=w))


    # Visit a parse tree produced by SystemRDLParser#CastWidth.
    def visitCastWidth(self, ctx:SystemRDLParser.CastWidthContext):
        w = self.visit(ctx.cast_width_expr())
        return(e.WidthCast(self.visit(ctx.expr()), w_expr=w))
    
    
    #---------------------------------------------------------------------------
    # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
    #---------------------------------------------------------------------------
    # Visit a parse tree produced by SystemRDLParser#string_literal.
    def visitString_literal(self, ctx:SystemRDLParser.String_literalContext):
        raise NotImplementedError
    

    # Visit a parse tree produced by SystemRDLParser#array_literal.
    def visitArray_literal(self, ctx:SystemRDLParser.Array_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#struct_literal.
    def visitStruct_literal(self, ctx:SystemRDLParser.Struct_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#enum_literal.
    def visitEnum_literal(self, ctx:SystemRDLParser.Enum_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#accesstype_literal.
    def visitAccesstype_literal(self, ctx:SystemRDLParser.Accesstype_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#onreadtype_literal.
    def visitOnreadtype_literal(self, ctx:SystemRDLParser.Onreadtype_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#onwritetype_literal.
    def visitOnwritetype_literal(self, ctx:SystemRDLParser.Onwritetype_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#addressingtype_literal.
    def visitAddressingtype_literal(self, ctx:SystemRDLParser.Addressingtype_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#precedencetype_literal.
    def visitPrecedencetype_literal(self, ctx:SystemRDLParser.Precedencetype_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#reference.
    def visitReference(self, ctx:SystemRDLParser.ReferenceContext):
        raise NotImplementedError
    

    # Visit a parse tree produced by SystemRDLParser#concatenate.
    def visitConcatenate(self, ctx:SystemRDLParser.ConcatenateContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#replicate.
    def visitReplicate(self, ctx:SystemRDLParser.ReplicateContext):
        raise NotImplementedError
    
    
