from . import component as comp
import itertools

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
        self.parent = parent
    
    
    @staticmethod
    def factory(inst, compiler, parent=None):
        if(type(inst) == comp.Field):
            return(FieldNode(inst, compiler, parent))
        elif(type(inst) == comp.Reg):
            return(RegNode(inst, compiler, parent))
        elif(type(inst) == comp.Regfile):
            return(RegfileNode(inst, compiler, parent))
        elif(type(inst) == comp.Addrmap):
            return(AddrmapNode(inst, compiler, parent))
        elif(type(inst) == comp.Mem):
            return(MemNode(inst, compiler, parent))
        elif(type(inst) == comp.Signal):
            return(SignalNode(inst, compiler, parent))
    
    
    def children(self, unroll=False):
        for child_inst in self.inst.children:
            if(unroll and issubclass(type(child_inst), comp.AddressableComponent) and child_inst.is_array):
                # Unroll the array
                range_list = [range(n) for n in child_inst.array_dimensions]
                for idxs in itertools.product(*range_list):
                    N = Node.factory(child_inst, self.compiler, self)
                    N.current_idx = idxs
                    yield N
            else:
                yield Node.factory(child_inst, self.compiler, self)
    
    
    def get_property(self, prop_name):
        # If its already in the component, then safe to bypass checks
        if(prop_name in self.inst.properties):
            return(self.inst.properties[prop_name])
        
        rule = self.compiler.property_rules.lookup_property(prop_name)
        
        # Is it even a valid property or allowed for this component type?
        if(rule is None):
            raise LookupError("Unknown property '%s'" % prop_name)
        if(type(self.inst) not in rule.bindable_to):
            raise LookupError("Unknown property '%s'" % prop_name)
        
        # Return the default value as specified by the rulebook
        return(rule.get_default(self))
        
    
    def get_path(self, hier_separator=".", array_suffix="[{index:d}]", empty_array_suffix="[]"):
        """
        Generate an absolute path string to this node
        """
        if(self.parent):
            return(
                self.parent.get_path(hier_separator, array_suffix, empty_array_suffix)
                + hier_separator
                + self.inst.inst_name
            )
        else:
            return(self.inst.inst_name)

#===============================================================================
class AddressableNode(Node):
    """
    Base-class for any kind of node that can have an address
    (addrmap, regfile, reg, mem)
    """
    
    def __init__(self, inst, compiler, parent):
        super().__init__(inst, compiler, parent)
        
        # Keeps track of the current array indices this node is referencing
        # The last item in this list iterates the most frequently
        # If None, then the current index is unknown
        self.current_idx = None
    
    
    def get_path(self, hier_separator=".", array_suffix="[{index:d}]", empty_array_suffix="[]"):
        """
        Extends get_path() in order to append any array suffixes
        """
        path = super().get_path(hier_separator, array_suffix, empty_array_suffix)
        
        if(self.inst.is_array):
            if(self.current_idx is None):
                # Index is not known. append empty array suffixes
                return(path + empty_array_suffix * len(self.inst.array_dimensions))
            else:
                # Index list is known
                for idx in self.current_idx:
                    path += array_suffix.format(index=idx)
                return(path)
        else:
            return(path)
    
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
