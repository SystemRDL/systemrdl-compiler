from collections import OrderedDict

from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .helpers import get_ID_text

from .. import component as comp
from ..messages import SourceRef
from .. import rdltypes

class StructVisitor(BaseVisitor):
    
    def visitStruct_def(self, ctx:SystemRDLParser.Struct_defContext):
        self.compiler.namespace.enter_scope()
        
        is_abstract = (ctx.ABSTRACT_kw() is not None)
        struct_name = get_ID_text(ctx.name)
        
        if ctx.base is not None:
            # Get the base struct type
            base_name = get_ID_text(ctx.base)
            base_type = self.compiler.namespace.lookup_type(base_name)
            if base_type is None:
                self.msg.fatal(
                    "Type '%s' is not defined" % base_name,
                    SourceRef.from_antlr(ctx.base)
                )
            if not rdltypes.is_user_struct(base_type):
                self.msg.fatal(
                    "Base type '%s' is not a struct" % base_name,
                    SourceRef.from_antlr(ctx.base)
                )
        else:
            base_type = rdltypes.UserStruct
        
        
        # Collect struct member elements
        members = OrderedDict()
        for struct_elem_ctx in ctx.getTypedRuleContexts(SystemRDLParser.Struct_elemContext):
            member_type, member_name, member_src_ref = self.visit(struct_elem_ctx)
            
            if member_name in members:
                self.msg.error(
                    "Struct member '%s' has already been defined" % member_name,
                    member_src_ref
                )
                continue
            
            if member_name in base_type._members:
                self.msg.error(
                    "Struct member '%s' has already been defined in base struct '%s'"
                    % (member_name, base_type.__name__),
                    member_src_ref
                )
                continue
            
            members[member_name] = member_type
        
        
        # Create Struct type
        struct_type = base_type.define_new(struct_name, members, is_abstract)
        
        self.compiler.namespace.exit_scope()
        return struct_type, struct_name, SourceRef.from_antlr(ctx.name)


    def visitStruct_elem(self, ctx:SystemRDLParser.Struct_elemContext):
        
        member_name = get_ID_text(ctx.ID())
        member_src_ref = SourceRef.from_antlr(ctx.ID())
        
        member_type = self.visit(ctx.struct_type())
        
        if ctx.array_type_suffix() is not None:
            member_type = rdltypes.ArrayPlaceholder(member_type)
        
        return member_type, member_name, member_src_ref


    _CompType_Map = {
        SystemRDLParser.FIELD_kw    : comp.Field,
        SystemRDLParser.REG_kw      : comp.Reg,
        SystemRDLParser.REGFILE_kw  : comp.Regfile,
        SystemRDLParser.ADDRMAP_kw  : comp.Addrmap,
        SystemRDLParser.SIGNAL_kw   : comp.Signal,
        SystemRDLParser.MEM_kw      : comp.Mem
    }
    def visitStruct_type(self, ctx:SystemRDLParser.Struct_typeContext):
        if ctx.data_type() is not None:
            data_type_token = self.visit(ctx.data_type())
            member_type = self.datatype_from_token(data_type_token)
        elif ctx.component_type() is not None:
            type_token = self.visit(ctx.component_type())
            member_type = self._CompType_Map[type_token.type]
        else:
            raise RuntimeError
        
        return member_type
