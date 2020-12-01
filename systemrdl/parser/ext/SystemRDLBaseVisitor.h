
// Generated from SystemRDL.g4 by ANTLR 4.9

#pragma once


#include "antlr4-runtime.h"
#include "SystemRDLVisitor.h"


/**
 * This class provides an empty implementation of SystemRDLVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  SystemRDLBaseVisitor : public SystemRDLVisitor {
public:

  virtual antlrcpp::Any visitRoot(SystemRDLParser::RootContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitRoot_elem(SystemRDLParser::Root_elemContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_def(SystemRDLParser::Component_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitExplicit_component_inst(SystemRDLParser::Explicit_component_instContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_inst_alias(SystemRDLParser::Component_inst_aliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_named_def(SystemRDLParser::Component_named_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_anon_def(SystemRDLParser::Component_anon_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_body(SystemRDLParser::Component_bodyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_body_elem(SystemRDLParser::Component_body_elemContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_insts(SystemRDLParser::Component_instsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_inst(SystemRDLParser::Component_instContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitField_inst_reset(SystemRDLParser::Field_inst_resetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitInst_addr_fixed(SystemRDLParser::Inst_addr_fixedContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitInst_addr_stride(SystemRDLParser::Inst_addr_strideContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitInst_addr_align(SystemRDLParser::Inst_addr_alignContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_inst_type(SystemRDLParser::Component_inst_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_type(SystemRDLParser::Component_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitComponent_type_primary(SystemRDLParser::Component_type_primaryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitParam_def(SystemRDLParser::Param_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitParam_def_elem(SystemRDLParser::Param_def_elemContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitParam_inst(SystemRDLParser::Param_instContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitParam_assignment(SystemRDLParser::Param_assignmentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitBinaryExpr(SystemRDLParser::BinaryExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUnaryExpr(SystemRDLParser::UnaryExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitNOP(SystemRDLParser::NOPContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitTernaryExpr(SystemRDLParser::TernaryExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitExpr_primary(SystemRDLParser::Expr_primaryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConcatenate(SystemRDLParser::ConcatenateContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitReplicate(SystemRDLParser::ReplicateContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitParen_expr(SystemRDLParser::Paren_exprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitCastType(SystemRDLParser::CastTypeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitCastWidth(SystemRDLParser::CastWidthContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitCast_width_expr(SystemRDLParser::Cast_width_exprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitRange_suffix(SystemRDLParser::Range_suffixContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitArray_suffix(SystemRDLParser::Array_suffixContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitArray_type_suffix(SystemRDLParser::Array_type_suffixContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitData_type(SystemRDLParser::Data_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitBasic_data_type(SystemRDLParser::Basic_data_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitLiteral(SystemRDLParser::LiteralContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitNumberInt(SystemRDLParser::NumberIntContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitNumberHex(SystemRDLParser::NumberHexContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitNumberVerilog(SystemRDLParser::NumberVerilogContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitString_literal(SystemRDLParser::String_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitBoolean_literal(SystemRDLParser::Boolean_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitArray_literal(SystemRDLParser::Array_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitStruct_literal(SystemRDLParser::Struct_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitStruct_kv(SystemRDLParser::Struct_kvContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitEnum_literal(SystemRDLParser::Enum_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitAccesstype_literal(SystemRDLParser::Accesstype_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitOnreadtype_literal(SystemRDLParser::Onreadtype_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitOnwritetype_literal(SystemRDLParser::Onwritetype_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitAddressingtype_literal(SystemRDLParser::Addressingtype_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitPrecedencetype_literal(SystemRDLParser::Precedencetype_literalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitInstance_ref(SystemRDLParser::Instance_refContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitInstance_ref_element(SystemRDLParser::Instance_ref_elementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitProp_ref(SystemRDLParser::Prop_refContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitLocal_property_assignment(SystemRDLParser::Local_property_assignmentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitDynamic_property_assignment(SystemRDLParser::Dynamic_property_assignmentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitNormal_prop_assign(SystemRDLParser::Normal_prop_assignContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitEncode_prop_assign(SystemRDLParser::Encode_prop_assignContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitProp_mod_assign(SystemRDLParser::Prop_mod_assignContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitProp_assignment_rhs(SystemRDLParser::Prop_assignment_rhsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitProp_keyword(SystemRDLParser::Prop_keywordContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitProp_mod(SystemRDLParser::Prop_modContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUdp_def(SystemRDLParser::Udp_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUdp_attr(SystemRDLParser::Udp_attrContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUdp_type(SystemRDLParser::Udp_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUdp_data_type(SystemRDLParser::Udp_data_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUdp_usage(SystemRDLParser::Udp_usageContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUdp_comp_type(SystemRDLParser::Udp_comp_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUdp_default(SystemRDLParser::Udp_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUdp_constraint(SystemRDLParser::Udp_constraintContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitEnum_def(SystemRDLParser::Enum_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitEnum_entry(SystemRDLParser::Enum_entryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitEnum_prop_assign(SystemRDLParser::Enum_prop_assignContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitStruct_def(SystemRDLParser::Struct_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitStruct_elem(SystemRDLParser::Struct_elemContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitStruct_type(SystemRDLParser::Struct_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstraint_def(SystemRDLParser::Constraint_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstraint_named_def(SystemRDLParser::Constraint_named_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstraint_anon_def(SystemRDLParser::Constraint_anon_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstraint_body(SystemRDLParser::Constraint_bodyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstraint_body_elem(SystemRDLParser::Constraint_body_elemContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstraint_insts(SystemRDLParser::Constraint_instsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstr_relational(SystemRDLParser::Constr_relationalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstr_prop_assign(SystemRDLParser::Constr_prop_assignContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstr_inside_values(SystemRDLParser::Constr_inside_valuesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstr_inside_enum(SystemRDLParser::Constr_inside_enumContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstr_lhs(SystemRDLParser::Constr_lhsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConstr_inside_value(SystemRDLParser::Constr_inside_valueContext *ctx) override {
    return visitChildren(ctx);
  }


};

