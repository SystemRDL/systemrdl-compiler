
class Node:
    """
    The Node object is a higher-level overlay that provides a more user-friendly
    interface to query the compiled RDL object model.
    """
    def __init__(self, compiler, inst, parent=None):
        self.compiler = compiler
        self.inst = inst
        self.comp = inst.typ
        self.parent = parent
    
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
    
# TODO: Create nodes for all the different component types