import re
import itertools
import operator
import functools

from . import component as comp
from . import rdltypes

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
    def _factory(inst, compiler, parent=None):
        if isinstance(inst, comp.Field):
            return FieldNode(inst, compiler, parent)
        elif isinstance(inst, comp.Reg):
            return RegNode(inst, compiler, parent)
        elif isinstance(inst, comp.Regfile):
            return RegfileNode(inst, compiler, parent)
        elif isinstance(inst, comp.Addrmap):
            return AddrmapNode(inst, compiler, parent)
        elif isinstance(inst, comp.Mem):
            return MemNode(inst, compiler, parent)
        elif isinstance(inst, comp.Signal):
            return SignalNode(inst, compiler, parent)
        else:
            raise RuntimeError
    
    
    @classmethod
    def add_meta_property(cls, getter_function, name=None):
        """
        Register a user-defined meta-property
        
        Parameters
        ----------
        getter_function : function
            Function that fetches the result of the user-defined meta-property
        name : str
            Meta-property name
            If unassigned, will default to the function's name
        """
        
        if name is None:
            name = getter_function.__name__
        mp = property(fget=getter_function)
        setattr(cls, name, mp)
    
    
    def children(self, unroll=False, skip_not_present=True):
        """
        Returns an iterator that provides nodes for all immediate children of
        this component.
        
        Parameters
        ----------
        unroll : bool
            If True, any children that are arrays are unrolled.
        
        skip_not_present : bool
            If True, skips children whose 'ispresent' property is set to False
        
        Yields
        ------
        :class:`~systemrdl.node.Node`
            All immediate children
        """
        for child_inst in self.inst.children:
            if skip_not_present:
                # Check if property ispresent == False
                if not child_inst.properties.get('ispresent', True):
                    # ispresent was explicitly set to False. Skip it
                    continue
                
            if unroll and isinstance(child_inst, comp.AddressableComponent) and child_inst.is_array:
                # Unroll the array
                range_list = [range(n) for n in child_inst.array_dimensions]
                for idxs in itertools.product(*range_list):
                    N = Node._factory(child_inst, self.compiler, self)
                    N.current_idx = idxs # pylint: disable=attribute-defined-outside-init
                    yield N
            else:
                yield Node._factory(child_inst, self.compiler, self)
    
    
    def get_child_by_name(self, inst_name):
        """
        Returns an immediate child Node whose instance name matches *inst_name*
        Returns None if not inst_name does not match
        
        Parameters
        ----------
        inst_name: str
            Name of immediate child to get
        
        Returns
        -------
        :class:`~systemrdl.node.Node` or None
            Child Node. None if not found.
        """
        child_inst = self.inst.get_child_by_name(inst_name)
        if child_inst is None:
            return None
        return Node._factory(child_inst, self.compiler, self)
    
    
    def find_by_path(self, path):
        """
        Finds the descendant node that is located at the relative path
        Returns None if not found
        Raises exception if path is malformed, or array index is out of range
        
        Parameters
        ----------
        path: str
            Path to target relative to current node
        
        Returns
        -------
        :class:`~systemrdl.node.Node` or None
            Descendant Node. None if not found.
        
        Raises
        ------
        ValueError
            If path syntax is invalid
        IndexError
            If an array index in the path is invalid
        """
        pathparts = path.split('.')
        current_node = self
        for pathpart in pathparts:
            m = re.fullmatch(r'^(\w+)((?:\[(?:\d+|0[xX][\da-fA-F]+)\])*)$', pathpart)
            if not m:
                raise ValueError("Invalid path")
            inst_name, array_suffix = m.group(1,2)
            idx_list = [ int(s,0) for s in re.findall(r'\[(\d+|0[xX][\da-fA-F]+)\]', array_suffix) ]
            
            current_node = current_node.get_child_by_name(inst_name)
            if current_node is None:
                return None
            
            if len(idx_list):
                if (isinstance(current_node, AddressableNode)) and current_node.inst.is_array:
                    # is an array
                    if len(idx_list) != len(current_node.inst.array_dimensions):
                        raise IndexError("Wrong number of array dimensions")
                    
                    current_node.current_idx = [] # pylint: disable=attribute-defined-outside-init
                    for i in range(len(idx_list)):
                        if idx_list[i] >= current_node.inst.array_dimensions[i]:
                            raise IndexError("Array index out of range")
                        current_node.current_idx.append(idx_list[i])
                else:
                    raise IndexError("Index attempted on non-array component")
            
        return current_node
    
    
    def get_property(self, prop_name):
        # If its already in the component, then safe to bypass checks
        if prop_name in self.inst.properties:
            prop_value = self.inst.properties[prop_name]
            
            # If this is a hierarchical component reference, convert it to a Node reference
            if isinstance(prop_value, rdltypes.ComponentRef):
                prop_value = prop_value.build_node_ref(self)
            
            return prop_value
        
        rule = self.compiler.property_rules.lookup_property(prop_name)
        
        # Is it even a valid property or allowed for this component type?
        if rule is None:
            raise LookupError("Unknown property '%s'" % prop_name)
        if type(self.inst) not in rule.bindable_to:
            raise LookupError("Unknown property '%s'" % prop_name)
        
        # Return the default value as specified by the rulebook
        return rule.get_default(self)
        
    
    def get_path(self, hier_separator=".", array_suffix="[{index:d}]", empty_array_suffix="[]"):
        """
        Generate an absolute path string to this node
        """
        if self.parent:
            return(
                self.parent.get_path(hier_separator, array_suffix, empty_array_suffix)
                + hier_separator
                + self.inst.inst_name
            )
        else:
            return self.inst.inst_name

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
        
        if self.inst.is_array:
            if self.current_idx is None:
                # Index is not known. append empty array suffixes
                return path + empty_array_suffix * len(self.inst.array_dimensions)
            else:
                # Index list is known
                for idx in self.current_idx:
                    path += array_suffix.format(index=idx)
                return path
        else:
            return path
    
    
    @property
    def absolute_address(self):
        """
        Calculate the absolute byte address of this node
        """
        # TODO: Implement absolute_address getter
        raise NotImplementedError
    
    
    @property
    def size(self):
        """
        Determine the size (in bytes) of this node.
        If an array, returns the size of a single element
        """
        # must be overridden
        raise NotImplementedError
    
    
    @property
    def total_size(self):
        """
        Determine the size (in bytes) of this node.
        If an array, returns size of the entire array
        """
        if self.inst.is_array:
            num_elements = functools.reduce(operator.mul, self.inst.array_dimensions)
            return self.inst.array_stride * (num_elements-1) + self.size
        else:
            return self.size
    
#===============================================================================
class VectorNode(Node):
    """
    Base-class for any kind of node that is vector-like
    (signal, field)
    """

#===============================================================================
class SignalNode(VectorNode):
    pass

#===============================================================================
class FieldNode(VectorNode):
    
    @property
    def is_virtual(self):
        """
        Determines if this node represents a virtual field (child of a virtual register)
        """
        return self.parent.is_virtual
    
    @property
    def is_volatile(self):
        """
        Returns True if combination of field access properties result in a field
        that should be interpreted as volatile.
        (Any hardware-writable field is inherently volatile)
        """
        # TODO: Implement is_volatile getter
        raise NotImplementedError
    
    @property
    def is_sw_writable(self):
        """
        Field is writable by software
        """
        # TODO: Implement is_sw_writable getter
        raise NotImplementedError
        
    @property
    def is_sw_readable(self):
        """
        Field is readable by software
        """
        # TODO: Implement is_sw_readable getter
        raise NotImplementedError
        
    @property
    def implements_storage(self):
        """
        Returns True if combination of field access properties imply that the
        field implements a storage element.
        (Section 9.4.1, Table 12)
        """
        # TODO: Implement implements_storage getter
        raise NotImplementedError
    
#===============================================================================
class RegNode(AddressableNode):
    
    @property
    def size(self):
        return self.get_property('regwidth') // 8
    
    @property
    def is_virtual(self):
        """
        Determines if this node represents a virtual register (child of a mem component)
        """
        # since mem components can only contain reg instances, a reg can only be
        # virtual if its direct parent is of type mem
        return isinstance(self.parent, MemNode)

#===============================================================================
class RegfileNode(AddressableNode):
    
    @property
    def size(self):
        return get_group_node_size(self)
        
#===============================================================================
class AddrmapNode(AddressableNode):
    
    @property
    def size(self):
        return get_group_node_size(self)

#===============================================================================
class MemNode(AddressableNode):
    
    @property
    def size(self):
        entry_size = self.get_property('memwidth') // 8
        num_entries = self.get_property('mementries')
        return entry_size * num_entries

#===============================================================================
def get_group_node_size(node):
    """
    Shared getter for AddrmapNode and RegfileNode's "size" property
    """
    # After structural placement, children are sorted
    if((len(node.inst.children) == 0)
        or (not isinstance(node.inst.children[-1], comp.AddressableComponent))
    ):
        # No addressable child exists.
        return 0
    
    # Current node's size is based on last child
    last_child_node = Node._factory(node.inst.children[-1], node.compiler, node)
    return(
        last_child_node.inst.addr_offset
        + last_child_node.total_size
    )
