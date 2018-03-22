import re

from antlr4 import *

from ..parser.SystemRDLParser import SystemRDLParser
from .. import rdltypes

from .BaseVisitor import BaseVisitor
from . import expressions as e
from ..errors import RDLCompileError, RDLNotSupportedYet
from .parameter import Parameter
from .. import component as comp

class ExprVisitor(BaseVisitor):
    
    def __init__(self, ns, pr, current_component, target_depth=0):
        super().__init__(ns=ns, pr=pr)
        
        # Reference to the current component that this expression was found in.
        # This is used for context when constructing hierarchical references
        self.current_component = current_component
        
        # Nonzero if target of an expression assignment is not within the 
        # current_component instance. (i.e. dynamic property assignments)
        # Number denotes how many instance levels deep the dynamic property
        # assignment "reaches in"
        self.target_depth = target_depth
        
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
        s = s.replace("_","")
        return(e.IntLiteral(ctx.INT(), int(s)))
    
    
    # Visit a parse tree produced by SystemRDLParser#NumberHex.
    def visitNumberHex(self, ctx:SystemRDLParser.NumberHexContext):
        s = ctx.HEX_INT().getText()
        s = s.replace("_","")
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
        return(e.BuiltinEnumLiteral(ctx.kw, rdltypes.AccessType[ctx.kw.text]))

    def visitOnreadtype_literal(self, ctx:SystemRDLParser.Onreadtype_literalContext):
        return(e.BuiltinEnumLiteral(ctx.kw, rdltypes.OnReadType[ctx.kw.text]))

    def visitOnwritetype_literal(self, ctx:SystemRDLParser.Onwritetype_literalContext):
        return(e.BuiltinEnumLiteral(ctx.kw, rdltypes.OnWriteType[ctx.kw.text]))

    def visitAddressingtype_literal(self, ctx:SystemRDLParser.Addressingtype_literalContext):
        return(e.BuiltinEnumLiteral(ctx.kw, rdltypes.AddressingType[ctx.kw.text]))

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
    # Visit a parse tree produced by SystemRDLParser#CastType.
    def visitCastType(self, ctx:SystemRDLParser.CastTypeContext):
        if(ctx.typ.type == SystemRDLParser.LONGINT_kw):
            # Longint gets truncated to 64-bits
            return(e.WidthCast(ctx.op, self.visit(ctx.expr()), w_int=64))
        elif(ctx.typ.type == SystemRDLParser.BIT_kw):
            # Cast to bit remains unaffected, but in self-determined context
            # Use assignment cast to isolate evaluation
            return(e.AssignmentCast(ctx.op, self.visit(ctx.expr()), int))
        elif(ctx.typ.type == SystemRDLParser.BOOLEAN_kw):
            return(e.BoolCast(ctx.op, self.visit(ctx.expr())))
        else:
            raise RuntimeError

    # Visit a parse tree produced by SystemRDLParser#CastWidth.
    def visitCastWidth(self, ctx:SystemRDLParser.CastWidthContext):
        w = self.visit(ctx.cast_width_expr())
        return(e.WidthCast(ctx.op, self.visit(ctx.expr()), w_expr=w))
    
    #---------------------------------------------------------------------------
    # References
    #---------------------------------------------------------------------------
    def visitInstance_ref(self, ctx:SystemRDLParser.Instance_refContext):
        
        # Get each ref element in a hierarchical chain. Each element is a tuple:
        #   (name_token, [index_expr, ...])
        ref_elements = []
        for ref_elem in ctx.getTypedRuleContexts(SystemRDLParser.Instance_ref_elementContext):
            ref_elements.append(self.visit(ref_elem))
        
        # Resolve reference of first element, since it is in the local scope
        first_name_token, first_array_suffixes = ref_elements[0]
        first_name = first_name_token.getText()
        first_elem = self.NS.lookup_element(first_name)
        if(first_elem is None):
            raise RDLCompileError(
                "Reference to '%s' not found" % first_name,
                first_name_token
            )
        
        if(type(first_elem) == Parameter):
            # Reference is to a local parameter
            ref_expr = e.ParameterRef(first_name_token, first_elem)
            
            if(len(first_array_suffixes) != 0):
                raise RDLNotSupportedYet(
                    "Index or bit-slice of a parameter is not supported yet. Coming soon!",
                    first_array_suffixes[0].err_ctx
                )
            if(len(ref_elements) > 1):
                raise RDLNotSupportedYet(
                    "Referencing child elements of a parameter is not supported yet. Coming soon!",
                    ctx.instance_ref_element(1)
                )
        elif(type(first_elem) == comp.Signal):
            # TODO: Need to handle signals differently. They are non-hierarchical (or something)
            raise NotImplementedError
        elif(issubclass(type(first_elem), comp.Component)):
            # Reference is to a component instance
            ref_expr = e.InstRef(
                ref_inst=self.current_component,
                uplevels_to_ref=self.target_depth,
                ref_elements=ref_elements
            )
        else:
            raise RuntimeError
        
        return(ref_expr)

    def visitInstance_ref_element(self, ctx:SystemRDLParser.Instance_ref_elementContext):
        name_token = ctx.ID()
        
        array_suffixes = []
        for as_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Array_suffixContext):
            array_suffixes.append(self.visit(as_ctx))
        
        return(name_token, array_suffixes)

    def visitProp_ref(self, ctx:SystemRDLParser.Prop_refContext):
        ref_expr = self.visit(ctx.instance_ref())
        
        if(ctx.prop_keyword() is not None):
            prop_token = self.visit(ctx.prop_keyword())
        else:
            prop_token = ctx.ID()
        
        raise RDLNotSupportedYet(
            "Property references in expressions are not supported.",
            prop_token
        )
    
    def visitArray_suffix(self, ctx:SystemRDLParser.Array_suffixContext):
        expr = self.visit(ctx.expr())
        expr = e.AssignmentCast(ctx.expr(), expr, int)
        expr.predict_type()
        return(expr)
    
    #---------------------------------------------------------------------------
    # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
    #---------------------------------------------------------------------------

    def visitArray_literal(self, ctx:SystemRDLParser.Array_literalContext):
        raise NotImplementedError

    def visitStruct_literal(self, ctx:SystemRDLParser.Struct_literalContext):
        raise NotImplementedError

    def visitEnum_literal(self, ctx:SystemRDLParser.Enum_literalContext):
        raise NotImplementedError

    def visitConcatenate(self, ctx:SystemRDLParser.ConcatenateContext):
        raise NotImplementedError

    def visitReplicate(self, ctx:SystemRDLParser.ReplicateContext):
        raise NotImplementedError
