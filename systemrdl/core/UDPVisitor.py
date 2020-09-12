from typing import List, Type, TYPE_CHECKING

from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor
from .helpers import get_ID_text

from . import properties
from . import expressions

from ..source_ref import src_ref_from_antlr
from .. import component as comp
from .. import rdltypes

if TYPE_CHECKING:
    from typing import Optional, Union, Any, Set
    from ..compiler import RDLCompiler

class UDPVisitor(BaseVisitor):
    def __init__(self, compiler: 'RDLCompiler') -> None:
        super().__init__(compiler)

        self._constr_componentwidth = None # type: Optional[bool]
        self._default = None # type: Any
        self._valid_types = None # type: Optional[List[Type[Union[int, str, bool, rdltypes.BuiltinEnum, rdltypes.UserEnum, rdltypes.UserStruct, comp.Component]]]]
        self._bindable_to = None # type: Optional[Set[Type[comp.Component]]]

    def visitUdp_def(self, ctx: SystemRDLParser.Udp_defContext) -> None:
        udp_name = get_ID_text(ctx.ID())

        # Collect all attributes
        for attr_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Udp_attrContext):
            self.visit(attr_ctx)

        # Check attribute rules
        # 15.1.1.b: A user-defined property definition shall include the
        #   component property specification.
        if self._valid_types is None:
            self.msg.fatal(
                "User-defined property '%s' does not specify the 'type' attribute"
                % udp_name,
                src_ref_from_antlr(ctx.ID())
            )

        # 15.1.1.c: A user-defined property definition shall include its type definition
        if self._bindable_to is None:
            self.msg.fatal(
                "User-defined property '%s' does not specify the 'component' attribute"
                % udp_name,
                src_ref_from_antlr(ctx.ID())
            )

        # 15.1 Table 30: Currently limited to componentwidth for type bit
        if self._constr_componentwidth:
            if int not in self._valid_types:
                self.msg.fatal(
                    "Constraint 'componentwidth' is only valid for properties of type 'bit'",
                    src_ref_from_antlr(ctx.ID())
                )

        # Evaluate default value, if any
        if self._default is not None:
            expr_ctx = self._default

            visitor = ExprVisitor(self.compiler)
            expr = visitor.visit(expr_ctx)
            expr_type = expr.predict_type()

            # 15.1.1-e: The default value shall be assignment compatible with
            # the property type
            for valid_type in self._valid_types:
                if expressions.is_castable(expr_type, valid_type):
                    if isinstance(expr, expressions.Expr):
                        # Found a type-compatible match. (first match is best match)
                        # Wrap the expression with an explicit assignment cast
                        expr = expressions.AssignmentCast(
                            self.compiler.env, src_ref_from_antlr(expr_ctx),
                            expr, valid_type
                        )
                    break
            else:
                self.msg.fatal(
                    "Property default is incompatible with property type",
                    src_ref_from_antlr(expr_ctx)
                )

            # OK to immediately evaluate the expression since there is no way that it
            # can depend on any post-elaborate references (parameters)
            self._default = expr.get_value()

        # Create and register the new property rule
        udp = properties.UserProperty(
            self.compiler.env, udp_name,
            self._bindable_to, self._valid_types, self._default,
            self._constr_componentwidth
        )
        self.compiler.env.property_rules.register_udp(udp, src_ref_from_antlr(ctx.ID()))


    def visitUdp_type(self, ctx: SystemRDLParser.Udp_typeContext) -> None:
        # Determine which type this property can hold
        if self._valid_types is not None:
            self.msg.fatal(
                "More than one 'type' attribute specified for user-defined property",
                src_ref_from_antlr(ctx.TYPE_kw())
            )

        token = self.visit(ctx.udp_data_type())

        if token.type == SystemRDLParser.REF_kw:
            valid_types = [
                comp.Field,
                comp.Reg,
                comp.Regfile,
                comp.Addrmap,
                comp.Mem
            ] # type: List[Type[Union[int, str, bool, rdltypes.BuiltinEnum, rdltypes.UserEnum, rdltypes.UserStruct, comp.Component]]]
        else:
            valid_types = [self.datatype_from_token(token)]

        is_array = (ctx.array_type_suffix() is not None)
        if is_array:
            # arrayify each entry in the list of valid types
            for i, valid_type in enumerate(valid_types):
                valid_types[i] = rdltypes.ArrayPlaceholder(valid_type) # type: ignore

        self._valid_types = valid_types


    _UDPUsage_Map = {
        SystemRDLParser.FIELD_kw    : comp.Field,
        SystemRDLParser.REG_kw      : comp.Reg,
        SystemRDLParser.REGFILE_kw  : comp.Regfile,
        SystemRDLParser.ADDRMAP_kw  : comp.Addrmap,
        SystemRDLParser.MEM_kw      : comp.Mem,
        SystemRDLParser.SIGNAL_kw   : comp.Signal,
        #SystemRDLParser.CONSTRAINT_kw   : TODO,
    }
    def visitUdp_usage(self, ctx: SystemRDLParser.Udp_usageContext) -> None:
        # Determine which components the UDP can be bound to
        if self._bindable_to is not None:
            self.msg.fatal(
                "More than one 'component' attribute specified for user-defined property",
                src_ref_from_antlr(ctx.COMPONENT_kw())
            )

        comp_types = [] # type: List[Type[comp.Component]]
        for token_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Udp_comp_typeContext):
            token = self.visit(token_ctx)
            if token.type == SystemRDLParser.ALL_kw:
                comp_types.extend(list(self._UDPUsage_Map.values()))
            else:
                comp_types.append(self._UDPUsage_Map[token.type])

        self._bindable_to = set(comp_types)


    def visitUdp_default(self, ctx: SystemRDLParser.Udp_defaultContext) -> None:
        if self._default is not None:
            self.msg.fatal(
                "More than one 'default' attribute specified for user-defined property",
                src_ref_from_antlr(ctx.DEFAULT_kw())
            )

        # defer expr evaluation until later
        self._default = ctx.expr()


    def visitUdp_constraint(self, ctx: SystemRDLParser.Udp_constraintContext) -> None:
        # There is only one type of constraint even allowed by the grammar
        # no need to explore further
        if self._constr_componentwidth is not None:
            self.msg.fatal(
                "More than one 'constraint' attribute specified for user-defined property",
                src_ref_from_antlr(ctx.CONSTRAINT_kw())
            )

        self._constr_componentwidth = True
