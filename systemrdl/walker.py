
from .node import AddressableNode, VectorNode, FieldNode, RegNode, RegfileNode
from .node import AddrmapNode, MemNode, SignalNode

#===============================================================================
class RDLListener:
    
    def enter_Component(self, node):
        pass
    
    def exit_Component(self, node):
        pass
    
    def enter_AddressableComponent(self, node):
        pass
    
    def exit_AddressableComponent(self, node):
        pass
    
    def enter_VectorComponent(self, node):
        pass
    
    def exit_VectorComponent(self, node):
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
    """
    Implements a walker instance that traverses the elaborated RDL instance tree
    Each node is visited exactly once
    """
    
    def walk(self, node, *listeners:RDLListener):
        """
        Initiates the walker to traverse the current *node* and its children.
        Calls the corresponding callback for each of the *listeners* provided in
        the order that they are listed.
        """
        for listener in listeners:
            self.do_enter(node, listener)
        for child in node.children():
            self.walk(child, *listeners)
        for listener in listeners:
            self.do_exit(node, listener)
    
    
    def do_enter(self, node, listener:RDLListener):
        listener.enter_Component(node)
        
        if(issubclass(type(node), AddressableNode)):
            listener.enter_AddressableComponent(node)
        elif(issubclass(type(node), VectorNode)):
            listener.enter_VectorComponent(node)
        
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
    
    
    def do_exit(self, node, listener:RDLListener):
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
        
        if(issubclass(type(node), AddressableNode)):
            listener.exit_AddressableComponent(node)
        elif(issubclass(type(node), VectorNode)):
            listener.exit_VectorComponent(node)
        
        listener.exit_Component(node)
        
#-------------------------------------------------------------------------------
class RDLUnrollWalker(RDLWalker):
    """
    Implements an RDL instance walker that unrolls any arrays of instances.
    If the walker arrives at an array node, then it will be visited multiple
    times according to the array dimensions
    """
    def walk(self, node, *listeners:RDLListener):
        for listener in listeners:
            self.do_enter(node, listener)
        for child in node.children(unroll=True):
            self.walk(child, *listeners)        
        for listener in listeners:
            self.do_exit(node, listener)