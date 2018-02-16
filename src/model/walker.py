
from .node import Node, SignalNode, FieldNode, RegNode, RegfileNode, AddrmapNode, MemNode

#===============================================================================
class RDLListener:
    
    def enter_Component_before(self, node):
        pass
    
    def enter_Component_after(self, node):
        pass
        
    def exit_Component_before(self, node):
        pass
        
    def exit_Component_after(self, node):
        pass
    
    def enter_Addrmap(self, node):
        pass
    
    def exit_Addrmap(self, node):
        pass
    
    def enter_Regfile(self, node):
        pass
    
    def exit_Regfile(self, node):
        pass
    
    def enter_Mem(self, node):
        pass
    
    def exit_Mem(self, node):
        pass
    
    def enter_Reg(self, node):
        pass
    
    def exit_Reg(self, node):
        pass
    
    def enter_Field(self, node):
        pass
    
    def exit_Field(self, node):
        pass
    
    def enter_Signal(self, node):
        pass
    
    def exit_Signal(self, node):
        pass

#===============================================================================
class RDLWalker:
    
    def walk(self, listener:RDLListener, node):
        self.do_enter(listener, node)
        for child in node.children():
            self.walk(listener, child)
        self.do_exit(listener, node)
    
    
    def do_enter(self, listener:RDLListener, node):
        listener.enter_Component_before(node)
        
        if(type(node) == FieldNode):
            listener.enter_Field(node)
        elif(type(node) == RegNode):
            listener.enter_Reg(node)
        elif(type(node) == RegfileNode):
            listener.enter_Regfile(node)
        elif(type(node) == AddrmapNode):
            listener.enter_Addrmap(node)
        elif(type(node) == MemNode):
            listener.enter_Mem(node)
        elif(type(node) == SignalNode):
            listener.enter_Signal(node)
        
        listener.enter_Component_after(node)
    
    
    def do_exit(self, listener:RDLListener, node):
        listener.exit_Component_before(node)
        
        if(type(node) == FieldNode):
            listener.exit_Field(node)
        elif(type(node) == RegNode):
            listener.exit_Reg(node)
        elif(type(node) == RegfileNode):
            listener.exit_Regfile(node)
        elif(type(node) == AddrmapNode):
            listener.exit_Addrmap(node)
        elif(type(node) == MemNode):
            listener.exit_Mem(node)
        elif(type(node) == SignalNode):
            listener.exit_Signal(node)
        
        listener.exit_Component_after(node)
