
import inspect
from antlr4 import *

from ..parser.SystemRDLParser import SystemRDLParser

from .ComponentVisitor import ComponentVisitor

class RootVisitor(ComponentVisitor):
    comp_type = None
    
    def __init__(self):
        super().__init__()
    
    def visitRoot(self, ctx:SystemRDLParser.RootContext):
        
        self.visitChildren(ctx)
        
        return(self.component)