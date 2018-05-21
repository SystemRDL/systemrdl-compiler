from ..parser.SystemRDLParser import SystemRDLParser

from .BaseVisitor import BaseVisitor
from .ExprVisitor import ExprVisitor

class UDPVisitor(BaseVisitor):
    def __init__(self, compiler):
        super().__init__(compiler)
    
    def visitUdp_def(self, ctx:SystemRDLParser.Udp_defContext):
        # TODO: Implement UDP
        raise NotImplementedError
    
    def visitUdp_attr(self, ctx:SystemRDLParser.Udp_attrContext):
        raise NotImplementedError

    def visitUdp_type(self, ctx:SystemRDLParser.Udp_typeContext):
        raise NotImplementedError

    def visitUdp_data_type(self, ctx:SystemRDLParser.Udp_data_typeContext):
        raise NotImplementedError

    def visitUdp_usage(self, ctx:SystemRDLParser.Udp_usageContext):
        raise NotImplementedError

    def visitUdp_comp_types(self, ctx:SystemRDLParser.Udp_comp_typesContext):
        raise NotImplementedError

    def visitUdp_comp_type(self, ctx:SystemRDLParser.Udp_comp_typeContext):
        raise NotImplementedError

    def visitUdp_default(self, ctx:SystemRDLParser.Udp_defaultContext):
        raise NotImplementedError

    def visitUdp_constraint(self, ctx:SystemRDLParser.Udp_constraintContext):
        raise NotImplementedError