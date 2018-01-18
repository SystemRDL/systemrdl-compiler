import re

from antlr4 import *

from ..parser.SystemRDLParser import SystemRDLParser
from ..model import rdl_types

from .BaseVisitor import BaseVisitor
from .namespace import NamespaceRegistry
from . import expressions as e
from .errors import RDLCompileError

class ExprVisitor(BaseVisitor):
    
    def __init__(self, ns=None):
        if(ns is None):
            self.NS = NamespaceRegistry()
        else:
            self.NS = ns
        
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
        return(expr_class(ctx.op,l,r))


    # Visit a parse tree produced by SystemRDLParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:SystemRDLParser.UnaryExprContext):
        n = self.visit(ctx.expr_primary())
        expr_class = self._UnaryExpr_map[ctx.op.type]
        return(expr_class(ctx.op,n))


    # Visit a parse tree produced by SystemRDLParser#TernaryExpr.
    def visitTernaryExpr(self, ctx:SystemRDLParser.TernaryExprContext):
        i = self.visit(ctx.expr(0))
        j = self.visit(ctx.expr(1))
        k = self.visit(ctx.expr(2))
        return(e.TernaryExpr(ctx.op,i,j,k))
    
    
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
        return(e.IntLiteral(ctx.INT(), int(s)))
    
    
    # Visit a parse tree produced by SystemRDLParser#NumberHex.
    def visitNumberHex(self, ctx:SystemRDLParser.NumberHexContext):
        s = ctx.HEX_INT().getText()
        s.replace("_","")
        return(e.IntLiteral(ctx.HEX_INT(), int(s,16)))
    
    
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
        
        if(val >= (1 << width)):
            raise RDLCompileError(
                "Value of integer literal exceeds the specified width",
                ctx.VLOG_INT()
            )
        
        return(e.IntLiteral(ctx.VLOG_INT(), val, width))
        
    
    # Visit a parse tree produced by SystemRDLParser#boolean_literal.
    def visitBoolean_literal(self, ctx:SystemRDLParser.Boolean_literalContext):
        if(ctx.val.type == SystemRDLParser.TRUE_kw):
            return(e.IntLiteral(ctx.val, 1, 1))
        else:
            return(e.IntLiteral(ctx.val, 0, 1))
        
    #---------------------------------------------------------------------------
    # Built-in RDL Enumeration literals
    #---------------------------------------------------------------------------
    def visitAccesstype_literal(self, ctx:SystemRDLParser.Accesstype_literalContext):
        return(e.BuiltinEnumLiteral(ctx.kw, rdl_types.AccessType[ctx.kw.text]))

    def visitOnreadtype_literal(self, ctx:SystemRDLParser.Onreadtype_literalContext):
        return(e.BuiltinEnumLiteral(ctx.kw, rdl_types.OnReadType[ctx.kw.text]))

    def visitOnwritetype_literal(self, ctx:SystemRDLParser.Onwritetype_literalContext):
        return(e.BuiltinEnumLiteral(ctx.kw, rdl_types.OnWriteType[ctx.kw.text]))

    def visitAddressingtype_literal(self, ctx:SystemRDLParser.Addressingtype_literalContext):
        return(e.BuiltinEnumLiteral(ctx.kw, rdl_types.AddressingType[ctx.kw.text]))

    def visitPrecedencetype_literal(self, ctx:SystemRDLParser.Precedencetype_literalContext):
        return(e.BuiltinEnumLiteral(ctx.kw, rdl_types.PrecedenceType[ctx.kw.text]))
    
    #---------------------------------------------------------------------------
    # Misc other literals
    #---------------------------------------------------------------------------
    def visitString_literal(self, ctx:SystemRDLParser.String_literalContext):
        string = ctx.STRING().getText()
        
        # Remove leading and trailing quotes (guaranteed to exist)
        string = string [1:-1]
        
        # Remove backslashes from any escaped characters
        string = re.sub(r'\\(.)', r'\1', string)
        
        return(e.StringLiteral(ctx.STRING(), string))
        
    
    #---------------------------------------------------------------------------
    # Cast
    #---------------------------------------------------------------------------
    _CastWidth_map = {
        SystemRDLParser.BIT_kw      : 1,
        SystemRDLParser.LONGINT_kw  : 64,
    }
    # Visit a parse tree produced by SystemRDLParser#CastType.
    def visitCastType(self, ctx:SystemRDLParser.CastTypeContext):
        if(ctx.typ.type in _CastWidth_map):
            w = _CastWidth_map[ctx.typ.type]
            return(e.WidthCast(ctx.op, self.visit(ctx.expr()), w_int=w))
        elif(ctx.typ.type == SystemRDLParser.BOOLEAN_kw):
            return(e.BoolCast(ctx.op, self.visit(ctx.expr())))
        else:
            raise RuntimeError

    # Visit a parse tree produced by SystemRDLParser#CastWidth.
    def visitCastWidth(self, ctx:SystemRDLParser.CastWidthContext):
        w = self.visit(ctx.cast_width_expr())
        return(e.WidthCast(ctx.op, self.visit(ctx.expr()), w_expr=w))
    
    #---------------------------------------------------------------------------
    # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
    #---------------------------------------------------------------------------

    # Visit a parse tree produced by SystemRDLParser#array_literal.
    def visitArray_literal(self, ctx:SystemRDLParser.Array_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#struct_literal.
    def visitStruct_literal(self, ctx:SystemRDLParser.Struct_literalContext):
        raise NotImplementedError


    # Visit a parse tree produced by SystemRDLParser#enum_literal.
    def visitEnum_literal(self, ctx:SystemRDLParser.Enum_literalContext):
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
    
    
