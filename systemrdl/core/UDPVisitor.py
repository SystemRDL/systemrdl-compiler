from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor
from .helpers import get_ID_text

from . import properties
from . import expressions

from .. import component as comp

class UDPVisitor(BaseVisitor):
    def __init__(self, compiler, current_component):
        super().__init__(compiler)
        self.current_component = current_component
        
        # Attributes
        self.attr = {}
    
    def visitUdp_def(self, ctx:SystemRDLParser.Udp_defContext):
        udp_name = get_ID_text(ctx.ID())
        
        # Collect all attributes
        for attr_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Udp_attrContext):
            self.visit(attr_ctx)
        
        # Check attribute rules
        # 15.1.1.b: A user-defined property definition shall include the
        #   component property specification.
        if('valid_types' not in self.attr):
            self.msg.fatal(
                "User-defined property '%s' does not specify the 'type' attribute"
                % udp_name,
                ctx.ID()
            )
            
        # 15.1.1.c: A user-defined property definition shall include its type definition
        if('bindable_to' not in self.attr):
            self.msg.fatal(
                "User-defined property '%s' does not specify the 'component' attribute"
                % udp_name,
                ctx.ID()
            )
        
        # 15.1 Table 30: Currently limited to componentwidth for type bit
        if(self.attr.get('constr_componentwidth', False)):
            if(int not in self.attr['valid_types']):
                self.msg.fatal(
                    "Constraint 'componentwidth' is only valid for properties of type 'bit'",
                    ctx.ID()
                )
        
        # Evaluate default value, if any
        if('default' in self.attr):
            expr_ctx = self.attr['default']
            
            visitor = ExprVisitor(self.compiler, self.current_component)
            expr = visitor.visit(expr_ctx)
            expr_type = expr.predict_type()
        
            # 15.1.1-e: The default value shall be assignment compatible with
            # the property type
            for valid_type in self.attr['valid_types']:
                if(expressions.is_castable(expr_type, valid_type)):
                    break
            else:
                self.msg.fatal(
                    "Property default is incompatible with property type",
                    expr_ctx
                )
            
            # OK to immediately evaluate the expression since there is no way that it
            # can depend on any post-elaborate references (parameters)
            expr.resolve_expr_width()
            self.attr['default'] = expr.get_value()
        
        # Create and register the new property rule
        udp = properties.UserProperty(self.compiler, udp_name, **self.attr)
        self.compiler.property_rules.register_udp(udp, ctx.ID())
        
    
    def visitUdp_type(self, ctx:SystemRDLParser.Udp_typeContext):
        # Determine which type this property can hold
        if('valid_types' in self.attr):
            self.msg.fatal(
                "More than one 'type' attribute specified for user-defined property",
                ctx.TYPE_kw()
            )
        
        token = self.visit(ctx.udp_data_type())
        
        if(token.type == SystemRDLParser.REF_kw):
            valid_types = [
                comp.Field,
                comp.Reg,
                comp.Regfile,
                comp.Addrmap,
                comp.Mem
            ]
        else:
            valid_types = [self.datatype_from_token(token)]
        
        is_array = (ctx.array_type_suffix() is not None)
        if(is_array):
            # TODO: arrayify each entry in the list of valid types
            raise NotImplementedError
        
        
        self.attr['valid_types'] = valid_types
        
    
    _UDPUsage_Map = {
        SystemRDLParser.FIELD_kw    : comp.Field,
        SystemRDLParser.REG_kw      : comp.Reg,
        SystemRDLParser.REGFILE_kw  : comp.Regfile,
        SystemRDLParser.ADDRMAP_kw  : comp.Addrmap,
        SystemRDLParser.MEM_kw      : comp.Mem,
        SystemRDLParser.SIGNAL_kw   : comp.Signal,
        #SystemRDLParser.CONSTRAINT_kw   : TODO,
    }
    def visitUdp_usage(self, ctx:SystemRDLParser.Udp_usageContext):
        # Determine which components the UDP can be bound to
        if('bindable_to' in self.attr):
            self.msg.fatal(
                "More than one 'component' attribute specified for user-defined property",
                ctx.COMPONENT_kw()
            )
        
        comp_types = []
        for token_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Udp_comp_typeContext):
            token = self.visit(token_ctx)
            if(token.type == SystemRDLParser.ALL_kw):
                comp_types.extend(self._UDPUsage_Map.values())
            else:
                comp_types.append(self._UDPUsage_Map[token.type])
        
        comp_types = list(set(comp_types))
        
        
        self.attr['bindable_to'] = comp_types


    def visitUdp_default(self, ctx:SystemRDLParser.Udp_defaultContext):
        if('default' in self.attr):
            self.msg.fatal(
                "More than one 'default' attribute specified for user-defined property",
                ctx.DEFAULT_kw()
            )
        
        # defer expr evaluation until later
        self.attr['default'] = ctx.expr()
        

    def visitUdp_constraint(self, ctx:SystemRDLParser.Udp_constraintContext):
        # There is only one type of constraint even allowed by the grammar
        # no need to explore further
        if('constr_componentwidth' in self.attr):
            self.msg.fatal(
                "More than one 'constraint' attribute specified for user-defined property",
                ctx.CONSTRAINT_kw()
            )
        
        self.attr['constr_componentwidth'] = True
