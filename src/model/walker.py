
from ..model import component as comp
from .node import Node

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
        for child in node.inst.typ.children:
            child_node = Node(node.compiler, child, node)
            self.walk(listener, child_node)
        self.do_exit(listener, node)
    
    def do_enter(self, listener:RDLListener, node):
        listener.enter_Component_before(node)
        
        if(type(node.inst.typ) == comp.Addrmap):
            listener.enter_Addrmap(node)
        elif(type(node.inst.typ) == comp.Regfile):
            listener.enter_Regfile(node)
        elif(type(node.inst.typ) == comp.Mem):
            listener.enter_Mem(node)
        elif(type(node.inst.typ) == comp.Reg):
            listener.enter_Reg(node)
        elif(type(node.inst.typ) == comp.Field):
            listener.enter_Field(node)
        elif(type(node.inst.typ) == comp.Signal):
            listener.enter_Signal(node)
        
        listener.enter_Component_after(node)
        
    def do_exit(self, listener:RDLListener, node):
        listener.exit_Component_before(node)
        
        if(type(node.inst.typ) == comp.Addrmap):
            listener.exit_Addrmap(node)
        elif(type(node.inst.typ) == comp.Regfile):
            listener.exit_Regfile(node)
        elif(type(node.inst.typ) == comp.Mem):
            listener.exit_Mem(node)
        elif(type(node.inst.typ) == comp.Reg):
            listener.exit_Reg(node)
        elif(type(node.inst.typ) == comp.Field):
            listener.exit_Field(node)
        elif(type(node.inst.typ) == comp.Signal):
            listener.exit_Signal(node)
        
        listener.exit_Component_after(node)
