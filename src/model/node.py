from . import component as comp

class Node:
    """
    The Node object is a higher-level overlay that provides a more user-friendly
    interface to query the compiled RDL object model.
    """
    
    def __init__(self, inst, compiler, parent):
        """
        Generic Node constructor.
        Do not call directly. Use factory() static method instead
        """
        self.compiler = compiler
        self.inst = inst
        self.comp = inst.typ
        self.parent = parent
    
    
    @staticmethod
    def factory(inst, compiler, parent=None):
        if(type(inst) == comp.FieldInst):
            return(FieldNode(inst, compiler, parent))
        elif(type(inst) == comp.RegInst):
            return(RegNode(inst, compiler, parent))
        elif(type(inst) == comp.RegfileInst):
            return(RegfileNode(inst, compiler, parent))
        elif(type(inst) == comp.AddrmapInst):
            return(AddrmapNode(inst, compiler, parent))
        elif(type(inst) == comp.MemInst):
            return(MemNode(inst, compiler, parent))
        elif(type(inst) == comp.SignalInst):
            return(SignalNode(inst, compiler, parent))
    
    
    def children(self, unroll=False):
        for child_inst in self.comp.children:
            yield Node.factory(child_inst, self.compiler, self)
    
    
    def get_property(self, prop_name):
        # If its already in the component, then safe to bypass checks
        if(prop_name in self.comp.properties):
            return(self.comp.properties[prop_name])
        
        rule = self.compiler.property_rules.lookup_property(prop_name)
        
        # Is it even a valid property or allowed for this component type?
        if(rule is None):
            raise LookupError("Unknown property '%s'" % prop_name)
        if(type(self.comp) not in rule.bindable_to):
            raise LookupError("Unknown property '%s'" % prop_name)
        
        # Return the default value as specified by the rulebook
        return(rule.get_default(self))
        
    
    def get_path(self, hier_separator=".", array_suffix="[{index:d}]"):
        """
        Generate an absolute path string to this node
        """
        # TODO
        raise NotImplementedError

#===============================================================================
class AddressableNode(Node):
    """
    Base-class for any kind of node that can have an address
    (addrmap, regfile, reg, mem)
    """
    @property
    def absolute_address(self):
        """
        Calculate the absolute address of this node
        """
        # TODO
        raise NotImplementedError
    
#===============================================================================
class SignalNode(Node):
    pass

#===============================================================================
class FieldNode(Node):
    pass
    
#===============================================================================
class RegNode(AddressableNode):
    pass

#===============================================================================
class RegfileNode(AddressableNode):
    pass

#===============================================================================
class AddrmapNode(AddressableNode):
    pass

#===============================================================================
class MemNode(AddressableNode):
    pass
