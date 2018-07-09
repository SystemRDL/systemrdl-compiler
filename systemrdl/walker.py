
from .node import AddressableNode, VectorNode, FieldNode, RegNode, RegfileNode
from .node import AddrmapNode, MemNode, SignalNode
from .node import RootNode

#===============================================================================
class RDLListener:
    """
    Base class for user-defined RDL traversal listeners
    """
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
    Each node is visited exactly once.
    
    Each node is visited as follows:
    
    1. Run :func:`~RDLListener.enter_Component` callback
    2. Run :func:`~RDLListener.enter_AddressableComponent` or :func:`~RDLListener.enter_VectorComponent` callback
    3. Run type-specific ``enter_*()`` callback, such as :func:`~RDLListener.enter_Reg`
    4. Traverse any children
    5. Run type-specific ``exit_*()`` callback, such as :func:`~RDLListener.exit_Reg`
    6. Run :func:`~RDLListener.exit_AddressableComponent` or :func:`~RDLListener.exit_VectorComponent` callback
    7. Run :func:`~RDLListener.exit_Component` callback
    
    """
    def __init__(self, unroll=False, skip_not_present=True):
        """
        Parameters
        ----------
        unroll : bool
            If True, any nodes that are arrays are unrolled.
            When the walker arrives at an array node, it will be visited multiple
            times according to the array dimensions.
            
        skip_not_present : bool
            If True, walker skips nodes whose 'ispresent' property is set
            to False
        """
        self.unroll = unroll
        self.skip_not_present = skip_not_present
        
        
    def walk(self, node, *listeners:RDLListener):
        """
        Initiates the walker to traverse the current ``node`` and its children.
        Calls the corresponding callback for each of the ``listeners`` provided in
        the order that they are listed.
        
        Parameters
        ----------
        node : :class:`~systemrdl.node.Node`
            Node to start traversing.
            Listener traversal includes this node.
            
        listeners : list
            List of :class:`~RDLListener` that are invoked during
            node traversal.
            Listener callbacks are executed in the same order as provided by this
            parameter.
        """
        
        
        for listener in listeners:
            self.do_enter(node, listener)
        for child in node.children(unroll=self.unroll, skip_not_present=self.skip_not_present):
            self.walk(child, *listeners)
        for listener in listeners:
            self.do_exit(node, listener)
    
    
    def do_enter(self, node, listener:RDLListener):
        
        # Skip RootNode since it isn't really a component
        if not isinstance(node, RootNode):
            listener.enter_Component(node)
        
        if isinstance(node, AddressableNode):
            listener.enter_AddressableComponent(node)
        elif isinstance(node, VectorNode):
            listener.enter_VectorComponent(node)
        
        if isinstance(node, FieldNode):
            listener.enter_Field(node)
        elif isinstance(node, RegNode):
            listener.enter_Reg(node)
        elif isinstance(node, RegfileNode):
            listener.enter_Regfile(node)
        elif isinstance(node, AddrmapNode):
            listener.enter_Addrmap(node)
        elif isinstance(node, MemNode):
            listener.enter_Mem(node)
        elif isinstance(node, SignalNode):
            listener.enter_Signal(node)
    
    
    def do_exit(self, node, listener:RDLListener):
        if isinstance(node, FieldNode):
            listener.exit_Field(node)
        elif isinstance(node, RegNode):
            listener.exit_Reg(node)
        elif isinstance(node, RegfileNode):
            listener.exit_Regfile(node)
        elif isinstance(node, AddrmapNode):
            listener.exit_Addrmap(node)
        elif isinstance(node, MemNode):
            listener.exit_Mem(node)
        elif isinstance(node, SignalNode):
            listener.exit_Signal(node)
        
        if isinstance(node, AddressableNode):
            listener.exit_AddressableComponent(node)
        elif isinstance(node, VectorNode):
            listener.exit_VectorComponent(node)
        
        # Skip RootNode since it isn't really a component
        if not isinstance(node, RootNode):
            listener.exit_Component(node)
