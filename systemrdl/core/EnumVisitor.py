from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor
from .helpers import get_ID_text
from . import expressions

from ..messages import SourceRef
from .. import rdltypes

class EnumVisitor(BaseVisitor):
    
    def visitEnum_def(self, ctx:SystemRDLParser.Enum_defContext):
        self.compiler.namespace.enter_scope()
        
        enum_name = get_ID_text(ctx.ID())
        
        # Collect entries
        entry_values = []
        entries = {}
        for enum_entry_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Enum_entryContext):
            name_token, value_expr_ctx, rdl_name, rdl_desc = self.visit(enum_entry_ctx)
            
            entry_name = get_ID_text(name_token)
            if entry_name in entries:
                self.msg.fatal(
                    "Entry '%s' has already been defined in this enum" % entry_name,
                    SourceRef.from_antlr(name_token)
                )
            
            if value_expr_ctx is not None:
                # explicit enumerator assignment
                
                visitor = ExprVisitor(self.compiler)
                expr = visitor.visit(value_expr_ctx)
                expr = expressions.AssignmentCast(self.compiler.env, value_expr_ctx, expr, int)
                expr.predict_type()
                
                # OK to immediately evaluate the expression since there is no way that it
                # can depend on any external references
                entry_value = expr.get_value()
            else:
                # automatic enumerator assignment
                if len(entry_values) == 0:
                    entry_value = 0
                else:
                    entry_value = entry_values[-1] + 1
            
            if entry_value in entry_values:
                # Value was already assigned
                self.msg.fatal(
                    "Enumeration encoding values must be unique",
                    SourceRef.from_antlr(name_token)
                )
            
            entry_values.append(entry_value)
            entries[entry_name] = (entry_value, rdl_name, rdl_desc)
        
        
        # Create Enum type
        enum_type = rdltypes.UserEnum(enum_name, entries) #pylint: disable=no-value-for-parameter
        
        self.compiler.namespace.exit_scope()
        return enum_type, get_ID_text(ctx.ID()), SourceRef.from_antlr(ctx.ID())

    def visitEnum_entry(self, ctx:SystemRDLParser.Enum_entryContext):
        name_token = ctx.ID()
        value_expr_ctx = ctx.expr()
        
        rdl_name = None
        rdl_desc = None
        
        for pa_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Enum_prop_assignContext):
            prop_token, prop_value = self.visit(pa_ctx)
            prop_name = get_ID_text(prop_token)
            
            if prop_name == "desc":
                if rdl_desc is not None:
                    self.msg.error(
                        "Property 'desc' was already assigned in this scope",
                        SourceRef.from_antlr(prop_token)
                    )
                    continue
                rdl_desc = prop_value
            elif prop_name == "name":
                if rdl_name is not None:
                    self.msg.error(
                        "Property 'name' was already assigned in this scope",
                        SourceRef.from_antlr(prop_token)
                    )
                    continue
                rdl_name = prop_value
            else:
                self.msg.fatal(
                    "Illegal enum property assignment '%s'" % prop_name,
                    SourceRef.from_antlr(prop_token)
                )
        
        return name_token, value_expr_ctx, rdl_name, rdl_desc

    def visitEnum_prop_assign(self, ctx:SystemRDLParser.Enum_prop_assignContext):
        prop_token = ctx.ID()
        
        visitor = ExprVisitor(self.compiler)
        prop_expr = visitor.visit(ctx.expr())
        prop_expr = expressions.AssignmentCast(self.compiler.env, ctx.expr(), prop_expr, str)
        prop_expr.predict_type()
        
        # OK to immediately evaluate the expression since there is no way that it
        # can depend on any external references
        prop_value = prop_expr.get_value()
        
        return prop_token, prop_value
