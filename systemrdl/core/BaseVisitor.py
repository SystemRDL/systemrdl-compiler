from typing import TYPE_CHECKING, Any

from .helpers import get_ID_text

from ..parser.SystemRDLParser import SystemRDLParser
from ..parser.SystemRDLVisitor import SystemRDLVisitor
from ..source_ref import src_ref_from_antlr

from .. import rdltypes

if TYPE_CHECKING:
    from ..compiler import RDLCompiler
    from antlr4.Token import CommonToken
    from antlr4 import ParserRuleContext
    from typing import Union, Type

class BaseVisitor(SystemRDLVisitor):

    def __init__(self, compiler: 'RDLCompiler') -> None:
        self.compiler = compiler
        self.msg = compiler.env.msg

    #---------------------------------------------------------------------------
    # Type Handling
    #---------------------------------------------------------------------------
    _DataType_Map = {
        SystemRDLParser.BIT_kw              : int,
        SystemRDLParser.NUMBER_kw           : int,
        SystemRDLParser.LONGINT_kw          : int,
        SystemRDLParser.ACCESSTYPE_kw       : rdltypes.AccessType,
        SystemRDLParser.ADDRESSINGTYPE_kw   : rdltypes.AddressingType,
        SystemRDLParser.ONREADTYPE_kw       : rdltypes.OnReadType,
        SystemRDLParser.ONWRITETYPE_kw      : rdltypes.OnWriteType,
        SystemRDLParser.STRING_kw           : str,
        SystemRDLParser.BOOLEAN_kw          : bool,
        SystemRDLParser.REF_kw              : rdltypes.references.RefType,
    }
    def datatype_from_token(self, token):
        # type: ('CommonToken') -> Type[Union[int, str, bool, rdltypes.BuiltinEnum, rdltypes.UserEnum, rdltypes.UserStruct, rdltypes.references.RefType]]
        """
        Given a SystemRDLParser token, lookup the type
        This only includes types under the "data_type" grammar rule
        """

        if token.type == SystemRDLParser.ID:
            # Is an identifier for either an enum or struct type

            typ = self.compiler.namespace.lookup_type(get_ID_text(token))
            if typ is None:
                self.msg.fatal(
                    "Type '%s' is not defined" % get_ID_text(token),
                    src_ref_from_antlr(token)
                )

            if rdltypes.is_user_enum(typ) or rdltypes.is_user_struct(typ):
                return typ # type: ignore
            else:
                self.msg.fatal(
                    "Type '%s' is not a struct or enum" % get_ID_text(token),
                    src_ref_from_antlr(token)
                )

        return self._DataType_Map[token.type]

    #---------------------------------------------------------------------------
    # Keyword passthrough visitors
    #---------------------------------------------------------------------------

    # It is convenient to be able to group commonly-used sets of tokens in the
    # grammar.
    # These visitors propagate the original tokens all the way back up to the
    # visitor that actually needs to know which keyword was used.

    def passthru_kw_token(self, ctx: 'ParserRuleContext') -> Any:
        if ctx.kw is not None:
            return ctx.kw
        else:
            return self.visitChildren(ctx)

    def visitComponent_inst_type(self, ctx: SystemRDLParser.Component_inst_typeContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitComponent_type(self, ctx: SystemRDLParser.Component_typeContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitComponent_type_primary(self, ctx: SystemRDLParser.Component_type_primaryContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitData_type(self, ctx: SystemRDLParser.Data_typeContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitBasic_data_type(self, ctx: SystemRDLParser.Basic_data_typeContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitProp_keyword(self, ctx: SystemRDLParser.Prop_keywordContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitProp_mod(self, ctx: SystemRDLParser.Prop_modContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitUdp_data_type(self, ctx: SystemRDLParser.Udp_data_typeContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitUdp_comp_type(self, ctx: SystemRDLParser.Udp_comp_typeContext) -> Any:
        return self.passthru_kw_token(ctx)

    def visitEval_expr_root(self, ctx:SystemRDLParser.Eval_expr_rootContext) -> Any:
        return self.visit(ctx.expr()) # type: ignore
