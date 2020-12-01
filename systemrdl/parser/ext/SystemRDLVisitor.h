
// Generated from SystemRDL.g4 by ANTLR 4.9

#pragma once


#include "antlr4-runtime.h"
#include "SystemRDLParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by SystemRDLParser.
 */
class  SystemRDLVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by SystemRDLParser.
   */
    virtual antlrcpp::Any visitRoot(SystemRDLParser::RootContext *context) = 0;

    virtual antlrcpp::Any visitRoot_elem(SystemRDLParser::Root_elemContext *context) = 0;

    virtual antlrcpp::Any visitComponent_def(SystemRDLParser::Component_defContext *context) = 0;

    virtual antlrcpp::Any visitExplicit_component_inst(SystemRDLParser::Explicit_component_instContext *context) = 0;

    virtual antlrcpp::Any visitComponent_inst_alias(SystemRDLParser::Component_inst_aliasContext *context) = 0;

    virtual antlrcpp::Any visitComponent_named_def(SystemRDLParser::Component_named_defContext *context) = 0;

    virtual antlrcpp::Any visitComponent_anon_def(SystemRDLParser::Component_anon_defContext *context) = 0;

    virtual antlrcpp::Any visitComponent_body(SystemRDLParser::Component_bodyContext *context) = 0;

    virtual antlrcpp::Any visitComponent_body_elem(SystemRDLParser::Component_body_elemContext *context) = 0;

    virtual antlrcpp::Any visitComponent_insts(SystemRDLParser::Component_instsContext *context) = 0;

    virtual antlrcpp::Any visitComponent_inst(SystemRDLParser::Component_instContext *context) = 0;

    virtual antlrcpp::Any visitField_inst_reset(SystemRDLParser::Field_inst_resetContext *context) = 0;

    virtual antlrcpp::Any visitInst_addr_fixed(SystemRDLParser::Inst_addr_fixedContext *context) = 0;

    virtual antlrcpp::Any visitInst_addr_stride(SystemRDLParser::Inst_addr_strideContext *context) = 0;

    virtual antlrcpp::Any visitInst_addr_align(SystemRDLParser::Inst_addr_alignContext *context) = 0;

    virtual antlrcpp::Any visitComponent_inst_type(SystemRDLParser::Component_inst_typeContext *context) = 0;

    virtual antlrcpp::Any visitComponent_type(SystemRDLParser::Component_typeContext *context) = 0;

    virtual antlrcpp::Any visitComponent_type_primary(SystemRDLParser::Component_type_primaryContext *context) = 0;

    virtual antlrcpp::Any visitParam_def(SystemRDLParser::Param_defContext *context) = 0;

    virtual antlrcpp::Any visitParam_def_elem(SystemRDLParser::Param_def_elemContext *context) = 0;

    virtual antlrcpp::Any visitParam_inst(SystemRDLParser::Param_instContext *context) = 0;

    virtual antlrcpp::Any visitParam_assignment(SystemRDLParser::Param_assignmentContext *context) = 0;

    virtual antlrcpp::Any visitBinaryExpr(SystemRDLParser::BinaryExprContext *context) = 0;

    virtual antlrcpp::Any visitUnaryExpr(SystemRDLParser::UnaryExprContext *context) = 0;

    virtual antlrcpp::Any visitNOP(SystemRDLParser::NOPContext *context) = 0;

    virtual antlrcpp::Any visitTernaryExpr(SystemRDLParser::TernaryExprContext *context) = 0;

    virtual antlrcpp::Any visitExpr_primary(SystemRDLParser::Expr_primaryContext *context) = 0;

    virtual antlrcpp::Any visitConcatenate(SystemRDLParser::ConcatenateContext *context) = 0;

    virtual antlrcpp::Any visitReplicate(SystemRDLParser::ReplicateContext *context) = 0;

    virtual antlrcpp::Any visitParen_expr(SystemRDLParser::Paren_exprContext *context) = 0;

    virtual antlrcpp::Any visitCastType(SystemRDLParser::CastTypeContext *context) = 0;

    virtual antlrcpp::Any visitCastWidth(SystemRDLParser::CastWidthContext *context) = 0;

    virtual antlrcpp::Any visitCast_width_expr(SystemRDLParser::Cast_width_exprContext *context) = 0;

    virtual antlrcpp::Any visitRange_suffix(SystemRDLParser::Range_suffixContext *context) = 0;

    virtual antlrcpp::Any visitArray_suffix(SystemRDLParser::Array_suffixContext *context) = 0;

    virtual antlrcpp::Any visitArray_type_suffix(SystemRDLParser::Array_type_suffixContext *context) = 0;

    virtual antlrcpp::Any visitData_type(SystemRDLParser::Data_typeContext *context) = 0;

    virtual antlrcpp::Any visitBasic_data_type(SystemRDLParser::Basic_data_typeContext *context) = 0;

    virtual antlrcpp::Any visitLiteral(SystemRDLParser::LiteralContext *context) = 0;

    virtual antlrcpp::Any visitNumberInt(SystemRDLParser::NumberIntContext *context) = 0;

    virtual antlrcpp::Any visitNumberHex(SystemRDLParser::NumberHexContext *context) = 0;

    virtual antlrcpp::Any visitNumberVerilog(SystemRDLParser::NumberVerilogContext *context) = 0;

    virtual antlrcpp::Any visitString_literal(SystemRDLParser::String_literalContext *context) = 0;

    virtual antlrcpp::Any visitBoolean_literal(SystemRDLParser::Boolean_literalContext *context) = 0;

    virtual antlrcpp::Any visitArray_literal(SystemRDLParser::Array_literalContext *context) = 0;

    virtual antlrcpp::Any visitStruct_literal(SystemRDLParser::Struct_literalContext *context) = 0;

    virtual antlrcpp::Any visitStruct_kv(SystemRDLParser::Struct_kvContext *context) = 0;

    virtual antlrcpp::Any visitEnum_literal(SystemRDLParser::Enum_literalContext *context) = 0;

    virtual antlrcpp::Any visitAccesstype_literal(SystemRDLParser::Accesstype_literalContext *context) = 0;

    virtual antlrcpp::Any visitOnreadtype_literal(SystemRDLParser::Onreadtype_literalContext *context) = 0;

    virtual antlrcpp::Any visitOnwritetype_literal(SystemRDLParser::Onwritetype_literalContext *context) = 0;

    virtual antlrcpp::Any visitAddressingtype_literal(SystemRDLParser::Addressingtype_literalContext *context) = 0;

    virtual antlrcpp::Any visitPrecedencetype_literal(SystemRDLParser::Precedencetype_literalContext *context) = 0;

    virtual antlrcpp::Any visitInstance_ref(SystemRDLParser::Instance_refContext *context) = 0;

    virtual antlrcpp::Any visitInstance_ref_element(SystemRDLParser::Instance_ref_elementContext *context) = 0;

    virtual antlrcpp::Any visitProp_ref(SystemRDLParser::Prop_refContext *context) = 0;

    virtual antlrcpp::Any visitLocal_property_assignment(SystemRDLParser::Local_property_assignmentContext *context) = 0;

    virtual antlrcpp::Any visitDynamic_property_assignment(SystemRDLParser::Dynamic_property_assignmentContext *context) = 0;

    virtual antlrcpp::Any visitNormal_prop_assign(SystemRDLParser::Normal_prop_assignContext *context) = 0;

    virtual antlrcpp::Any visitEncode_prop_assign(SystemRDLParser::Encode_prop_assignContext *context) = 0;

    virtual antlrcpp::Any visitProp_mod_assign(SystemRDLParser::Prop_mod_assignContext *context) = 0;

    virtual antlrcpp::Any visitProp_assignment_rhs(SystemRDLParser::Prop_assignment_rhsContext *context) = 0;

    virtual antlrcpp::Any visitProp_keyword(SystemRDLParser::Prop_keywordContext *context) = 0;

    virtual antlrcpp::Any visitProp_mod(SystemRDLParser::Prop_modContext *context) = 0;

    virtual antlrcpp::Any visitUdp_def(SystemRDLParser::Udp_defContext *context) = 0;

    virtual antlrcpp::Any visitUdp_attr(SystemRDLParser::Udp_attrContext *context) = 0;

    virtual antlrcpp::Any visitUdp_type(SystemRDLParser::Udp_typeContext *context) = 0;

    virtual antlrcpp::Any visitUdp_data_type(SystemRDLParser::Udp_data_typeContext *context) = 0;

    virtual antlrcpp::Any visitUdp_usage(SystemRDLParser::Udp_usageContext *context) = 0;

    virtual antlrcpp::Any visitUdp_comp_type(SystemRDLParser::Udp_comp_typeContext *context) = 0;

    virtual antlrcpp::Any visitUdp_default(SystemRDLParser::Udp_defaultContext *context) = 0;

    virtual antlrcpp::Any visitUdp_constraint(SystemRDLParser::Udp_constraintContext *context) = 0;

    virtual antlrcpp::Any visitEnum_def(SystemRDLParser::Enum_defContext *context) = 0;

    virtual antlrcpp::Any visitEnum_entry(SystemRDLParser::Enum_entryContext *context) = 0;

    virtual antlrcpp::Any visitEnum_prop_assign(SystemRDLParser::Enum_prop_assignContext *context) = 0;

    virtual antlrcpp::Any visitStruct_def(SystemRDLParser::Struct_defContext *context) = 0;

    virtual antlrcpp::Any visitStruct_elem(SystemRDLParser::Struct_elemContext *context) = 0;

    virtual antlrcpp::Any visitStruct_type(SystemRDLParser::Struct_typeContext *context) = 0;

    virtual antlrcpp::Any visitConstraint_def(SystemRDLParser::Constraint_defContext *context) = 0;

    virtual antlrcpp::Any visitConstraint_named_def(SystemRDLParser::Constraint_named_defContext *context) = 0;

    virtual antlrcpp::Any visitConstraint_anon_def(SystemRDLParser::Constraint_anon_defContext *context) = 0;

    virtual antlrcpp::Any visitConstraint_body(SystemRDLParser::Constraint_bodyContext *context) = 0;

    virtual antlrcpp::Any visitConstraint_body_elem(SystemRDLParser::Constraint_body_elemContext *context) = 0;

    virtual antlrcpp::Any visitConstraint_insts(SystemRDLParser::Constraint_instsContext *context) = 0;

    virtual antlrcpp::Any visitConstr_relational(SystemRDLParser::Constr_relationalContext *context) = 0;

    virtual antlrcpp::Any visitConstr_prop_assign(SystemRDLParser::Constr_prop_assignContext *context) = 0;

    virtual antlrcpp::Any visitConstr_inside_values(SystemRDLParser::Constr_inside_valuesContext *context) = 0;

    virtual antlrcpp::Any visitConstr_inside_enum(SystemRDLParser::Constr_inside_enumContext *context) = 0;

    virtual antlrcpp::Any visitConstr_lhs(SystemRDLParser::Constr_lhsContext *context) = 0;

    virtual antlrcpp::Any visitConstr_inside_value(SystemRDLParser::Constr_inside_valueContext *context) = 0;


};

