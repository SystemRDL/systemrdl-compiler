from .helpers import get_ID_text

from ..messages import SourceRef
from ..parser.SystemRDLParser import SystemRDLParser
from ..parser.SystemRDLVisitor import SystemRDLVisitor

from .. import rdltypes

class BaseVisitor(SystemRDLVisitor):
    
    def __init__(self, compiler):
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
        SystemRDLParser.BOOLEAN_kw          : bool
    }
    def datatype_from_token(self, token):
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
                    SourceRef.from_antlr(token)
                )
            
            if rdltypes.is_user_enum(typ) or rdltypes.is_user_struct(typ):
                return typ
            else:
                self.msg.fatal(
                    "Type '%s' is not a struct or enum" % get_ID_text(token),
                    SourceRef.from_antlr(token)
                )
            
        else:
            return self._DataType_Map[token.type]
    
    #---------------------------------------------------------------------------
    # Keyword passthrough visitors
    #---------------------------------------------------------------------------
    
    # It is convenient to be able to group commonly-used sets of tokens in the
    # grammar.
    # These visitors propagate the original tokens all the way back up to the
    # visitor that actually needs to know which keyword was used.
    
    def passthru_kw_token(self, ctx):
        if ctx.kw is not None:
            return ctx.kw
        else:
            return self.visitChildren(ctx)
        
    def visitComponent_inst_type(self, ctx:SystemRDLParser.Component_inst_typeContext):
        return self.passthru_kw_token(ctx)

    def visitComponent_type(self, ctx:SystemRDLParser.Component_typeContext):
        return self.passthru_kw_token(ctx)

    def visitComponent_type_primary(self, ctx:SystemRDLParser.Component_type_primaryContext):
        return self.passthru_kw_token(ctx)
    
    def visitData_type(self, ctx:SystemRDLParser.Data_typeContext):
        return self.passthru_kw_token(ctx)

    def visitBasic_data_type(self, ctx:SystemRDLParser.Basic_data_typeContext):
        return self.passthru_kw_token(ctx)
    
    def visitProp_keyword(self, ctx:SystemRDLParser.Prop_keywordContext):
        return self.passthru_kw_token(ctx)
    
    def visitProp_mod(self, ctx:SystemRDLParser.Prop_modContext):
        return self.passthru_kw_token(ctx)
        
    def visitUdp_data_type(self, ctx:SystemRDLParser.Udp_data_typeContext):
        return self.passthru_kw_token(ctx)
    
    def visitUdp_comp_type(self, ctx:SystemRDLParser.Udp_comp_typeContext):
        return self.passthru_kw_token(ctx)
