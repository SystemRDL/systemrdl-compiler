# Generated from SystemRDL.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SystemRDLParser import SystemRDLParser
else:
    from SystemRDLParser import SystemRDLParser

# This class defines a complete generic visitor for a parse tree produced by SystemRDLParser.

class SystemRDLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SystemRDLParser#root.
    def visitRoot(self, ctx:SystemRDLParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#root_elem.
    def visitRoot_elem(self, ctx:SystemRDLParser.Root_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_def.
    def visitComponent_def(self, ctx:SystemRDLParser.Component_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_named_def.
    def visitComponent_named_def(self, ctx:SystemRDLParser.Component_named_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_anon_def.
    def visitComponent_anon_def(self, ctx:SystemRDLParser.Component_anon_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_body.
    def visitComponent_body(self, ctx:SystemRDLParser.Component_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_body_elem.
    def visitComponent_body_elem(self, ctx:SystemRDLParser.Component_body_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_insts.
    def visitComponent_insts(self, ctx:SystemRDLParser.Component_instsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_inst.
    def visitComponent_inst(self, ctx:SystemRDLParser.Component_instContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#field_inst_reset.
    def visitField_inst_reset(self, ctx:SystemRDLParser.Field_inst_resetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#inst_addr_fixed.
    def visitInst_addr_fixed(self, ctx:SystemRDLParser.Inst_addr_fixedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#inst_addr_stride.
    def visitInst_addr_stride(self, ctx:SystemRDLParser.Inst_addr_strideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#inst_addr_align.
    def visitInst_addr_align(self, ctx:SystemRDLParser.Inst_addr_alignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_inst_type.
    def visitComponent_inst_type(self, ctx:SystemRDLParser.Component_inst_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_type.
    def visitComponent_type(self, ctx:SystemRDLParser.Component_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#component_type_primary.
    def visitComponent_type_primary(self, ctx:SystemRDLParser.Component_type_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#param_def.
    def visitParam_def(self, ctx:SystemRDLParser.Param_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#param_def_elem.
    def visitParam_def_elem(self, ctx:SystemRDLParser.Param_def_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#param_inst.
    def visitParam_inst(self, ctx:SystemRDLParser.Param_instContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#param_assignment.
    def visitParam_assignment(self, ctx:SystemRDLParser.Param_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#BinaryExpr.
    def visitBinaryExpr(self, ctx:SystemRDLParser.BinaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:SystemRDLParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#NOP.
    def visitNOP(self, ctx:SystemRDLParser.NOPContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#TernaryExpr.
    def visitTernaryExpr(self, ctx:SystemRDLParser.TernaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#expr_primary.
    def visitExpr_primary(self, ctx:SystemRDLParser.Expr_primaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#concatenate.
    def visitConcatenate(self, ctx:SystemRDLParser.ConcatenateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#replicate.
    def visitReplicate(self, ctx:SystemRDLParser.ReplicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#paren_expr.
    def visitParen_expr(self, ctx:SystemRDLParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#CastType.
    def visitCastType(self, ctx:SystemRDLParser.CastTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#CastWidth.
    def visitCastWidth(self, ctx:SystemRDLParser.CastWidthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#cast_width_expr.
    def visitCast_width_expr(self, ctx:SystemRDLParser.Cast_width_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#range_suffix.
    def visitRange_suffix(self, ctx:SystemRDLParser.Range_suffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#array_suffix.
    def visitArray_suffix(self, ctx:SystemRDLParser.Array_suffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#array_type_suffix.
    def visitArray_type_suffix(self, ctx:SystemRDLParser.Array_type_suffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#data_type.
    def visitData_type(self, ctx:SystemRDLParser.Data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#basic_data_type.
    def visitBasic_data_type(self, ctx:SystemRDLParser.Basic_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#literal.
    def visitLiteral(self, ctx:SystemRDLParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#NumberInt.
    def visitNumberInt(self, ctx:SystemRDLParser.NumberIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#NumberHex.
    def visitNumberHex(self, ctx:SystemRDLParser.NumberHexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#NumberVerilog.
    def visitNumberVerilog(self, ctx:SystemRDLParser.NumberVerilogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#string_literal.
    def visitString_literal(self, ctx:SystemRDLParser.String_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#boolean_literal.
    def visitBoolean_literal(self, ctx:SystemRDLParser.Boolean_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#array_literal.
    def visitArray_literal(self, ctx:SystemRDLParser.Array_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#struct_literal.
    def visitStruct_literal(self, ctx:SystemRDLParser.Struct_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#struct_kv.
    def visitStruct_kv(self, ctx:SystemRDLParser.Struct_kvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#enum_literal.
    def visitEnum_literal(self, ctx:SystemRDLParser.Enum_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#accesstype_literal.
    def visitAccesstype_literal(self, ctx:SystemRDLParser.Accesstype_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#onreadtype_literal.
    def visitOnreadtype_literal(self, ctx:SystemRDLParser.Onreadtype_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#onwritetype_literal.
    def visitOnwritetype_literal(self, ctx:SystemRDLParser.Onwritetype_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#addressingtype_literal.
    def visitAddressingtype_literal(self, ctx:SystemRDLParser.Addressingtype_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#precedencetype_literal.
    def visitPrecedencetype_literal(self, ctx:SystemRDLParser.Precedencetype_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SystemRDLParser#reference.
    def visitReference(self, ctx:SystemRDLParser.ReferenceContext):
        return self.visitChildren(ctx)



del SystemRDLParser