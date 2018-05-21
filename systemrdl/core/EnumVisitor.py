from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor
from . import expressions

from .. import rdltypes

class EnumVisitor(BaseVisitor):
    def __init__(self, compiler):
        super().__init__(compiler)
    
    def visitEnum_def(self, ctx:SystemRDLParser.Enum_defContext):
        self.compiler.namespace.enter_scope()
        
        enum_name = ctx.ID().getText()
        
        # Collect entries
        entry_values = []
        entries = {}
        for enum_entry_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Enum_entryContext):
            name_token, value_expr_ctx, rdl_name, rdl_desc = self.visit(enum_entry_ctx)
            
            entry_name = name_token.getText()
            if(entry_name in entries):
                self.msg.fatal(
                    "Entry '%s' has already been defined in this enum" % entry_name,
                    name_token
                )
            
            if(value_expr_ctx is not None):
                # explicit enumerator assignment
                
                visitor = ExprVisitor(self.compiler, None)
                expr = visitor.visit(value_expr_ctx)
                expr = expressions.AssignmentCast(self.compiler, value_expr_ctx, expr, int)
                expr.predict_type()
                
                # OK to immediately evaluate the expression since there is no way that it
                # can depend on any external references
                expr.resolve_expr_width()
                entry_value = expr.get_value()
            else:
                # automatic enumerator assignment
                if(len(entry_values) == 0):
                    entry_value = 0
                else:
                    entry_value = entry_values[-1] + 1
            
            if(entry_value in entry_values):
                # Value was already assigned
                self.msg.fatal(
                    "Enumeration encoding values must be unique",
                    name_token
                )
            
            entry_values.append(entry_value)
            entries[entry_name] = (entry_value, rdl_name, rdl_desc)
        
        
        # Create Enum type
        enum_type = rdltypes.UserEnum(enum_name, entries)
        
        self.compiler.namespace.exit_scope()
        return(enum_type, ctx.ID())

    def visitEnum_entry(self, ctx:SystemRDLParser.Enum_entryContext):
        name_token = ctx.ID()
        value_expr_ctx = ctx.expr()
        
        rdl_name = None
        rdl_desc = None
        
        for pa_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Enum_prop_assignContext):
            prop_token, prop_value = self.visit(pa_ctx)
            prop_name = prop_token.getText()
            
            if(prop_name == "desc"):
                if(rdl_desc is not None):
                    self.msg.error(
                        "Property 'desc' was already assigned in this scope",
                        prop_token
                    )
                    continue
                rdl_desc = prop_value
            elif(prop_name == "name"):
                if(rdl_name is not None):
                    self.msg.error(
                        "Property 'name' was already assigned in this scope",
                        prop_token
                    )
                    continue
                rdl_name = prop_value
            else:
                self.msg.fatal(
                    "Illegal enum property assignment '%s'" % prop_name,
                    prop_token
                )
        
        return(name_token, value_expr_ctx, rdl_name, rdl_desc)

    def visitEnum_prop_assign(self, ctx:SystemRDLParser.Enum_prop_assignContext):
        prop_token = ctx.ID()
        
        visitor = ExprVisitor(self.compiler, None)
        prop_expr = visitor.visit(ctx.expr())
        prop_expr = expressions.AssignmentCast(self.compiler, ctx.expr(), prop_expr, str)
        prop_expr.predict_type()
        
        # OK to immediately evaluate the expression since there is no way that it
        # can depend on any external references
        prop_expr.resolve_expr_width()
        prop_value = prop_expr.get_value()
        
        return(prop_token, prop_value)
