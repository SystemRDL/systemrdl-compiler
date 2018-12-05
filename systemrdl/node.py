import re
import itertools

from . import component as comp
from . import rdltypes
from .core import rdlformatcode

class Node:
    """
    The Node object is a higher-level overlay that provides a more user-friendly
    interface to query the compiled RDL object model.
    
    .. inheritance-diagram:: systemrdl.node
        :top-classes: ~Node
    
    """
    
    def __init__(self, inst, env, parent):
        """
        Generic Node constructor.
        Do not call directly. Use factory() static method instead
        """
        self.env = env
        
        #: Reference to :class:`~systemrdl.component.Component` that instantiates this node
        self.inst = inst
        
        #: Reference to parent :class:`~Node`
        self.parent = parent
    
    def __repr__(self):
        return "<%s %s at 0x%x>" % (
            self.__class__.__qualname__,
            self.get_path(),
            id(self)
        )
    
    @staticmethod
    def _factory(inst, env, parent=None):
        if isinstance(inst, comp.Field):
            return FieldNode(inst, env, parent)
        elif isinstance(inst, comp.Reg):
            return RegNode(inst, env, parent)
        elif isinstance(inst, comp.Regfile):
            return RegfileNode(inst, env, parent)
        elif isinstance(inst, comp.Addrmap):
            return AddrmapNode(inst, env, parent)
        elif isinstance(inst, comp.Mem):
            return MemNode(inst, env, parent)
        elif isinstance(inst, comp.Signal):
            return SignalNode(inst, env, parent)
        else:
            raise RuntimeError
    
    
    @classmethod
    def add_derived_property(cls, getter_function, name=None):
        """
        Register a user-defined derived property
        
        Parameters
        ----------
        getter_function : function
            Function that fetches the result of the user-defined derived property
        name : str
            Derived property name
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
        :class:`~Node`
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
                    N = Node._factory(child_inst, self.env, self)
                    N.current_idx = idxs # pylint: disable=attribute-defined-outside-init
                    yield N
            else:
                yield Node._factory(child_inst, self.env, self)
    
    
    def descendants(self, unroll=False, skip_not_present=True, in_post_order=False):
        """
        Returns an iterator that provides nodes for all descendants of this
        component.
        
        Parameters
        ----------
        unroll : bool
            If True, any children that are arrays are unrolled.
        
        skip_not_present : bool
            If True, skips children whose 'ispresent' property is set to False
        
        in_post_order : bool
            If True, descendants are walked using post-order traversal
            (children first) rather than the default pre-order traversal
            (parents first).
        
        Yields
        ------
        :class:`~Node`
            All descendant nodes of this component
        """
        for child in self.children(unroll, skip_not_present):
            if in_post_order:
                yield from child.descendants(unroll, skip_not_present, in_post_order)
            
            yield child
            
            if not in_post_order:
                yield from child.descendants(unroll, skip_not_present, in_post_order)
    
    
    def signals(self, skip_not_present=True):
        """
        Returns an iterator that provides nodes for all immediate signals of
        this component.
        
        Parameters
        ----------
        skip_not_present : bool
            If True, skips children whose 'ispresent' property is set to False
        
        Yields
        ------
        :class:`~SignalNode`
            All signals in this component
        """
        for child in self.children(skip_not_present=skip_not_present):
            if isinstance(child, SignalNode):
                yield child
    
    
    def fields(self, skip_not_present=True):
        """
        Returns an iterator that provides nodes for all immediate fields of
        this component.
        
        Parameters
        ----------
        skip_not_present : bool
            If True, skips children whose 'ispresent' property is set to False
        
        Yields
        ------
        :class:`~FieldNode`
            All fields in this component
        """
        for child in self.children(skip_not_present=skip_not_present):
            if isinstance(child, FieldNode):
                yield child
    
    
    def registers(self, unroll=False, skip_not_present=True):
        """
        Returns an iterator that provides nodes for all immediate registers of
        this component.
        
        Parameters
        ----------
        unroll : bool
            If True, any children that are arrays are unrolled.
        
        skip_not_present : bool
            If True, skips children whose 'ispresent' property is set to False
        
        Yields
        ------
        :class:`~RegNode`
            All registers in this component
        """
        for child in self.children(unroll, skip_not_present):
            if isinstance(child, RegNode):
                yield child
    
    
    def get_child_by_name(self, inst_name):
        """
        Returns an immediate child :class:`~Node` whose instance name matches ``inst_name``
        
        Returns ``None`` if ``inst_name`` does not match
        
        Parameters
        ----------
        inst_name: str
            Name of immediate child to get
        
        Returns
        -------
        :class:`~Node` or None
            Child Node. None if not found.
        """
        child_inst = self.inst.get_child_by_name(inst_name)
        if child_inst is None:
            return None
        return Node._factory(child_inst, self.env, self)
    
    
    def find_by_path(self, path):
        """
        Finds the descendant node that is located at the relative path
        Returns ``None`` if not found
        Raises exception if path is malformed, or array index is out of range
        
        Parameters
        ----------
        path: str
            Path to target relative to current node
        
        Returns
        -------
        :class:`~Node` or None
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
    
    
    def get_property(self, prop_name, **kwargs):
        """
        Gets the SystemRDL component property
        
        If a property was not explicitly set in the RDL source, its default
        value is derived. In some cases, a default value is implied according to
        other property values.
        
        Properties values that are a reference to a component instance are
        converted to a :class:`~Node` overlay object.
        
        Parameters
        ----------
        prop_name: str
            SystemRDL property name
        default:
            Override built-in default value of property.
            If the property was not explicitly set, return this value rather than
            the property's intrinsic default value.
        
        Raises
        ------
        LookupError
            If prop_name is invalid
        """
        
        ovr_default = False
        default = None
        if 'default' in kwargs:
            ovr_default = True
            default = kwargs.pop('default')
        
        # Check for stray kwargs
        if kwargs:
            raise TypeError("got an unexpected keyword argument '%s'" % list(kwargs.keys())[0])
        
        # If its already in the component, then safe to bypass checks
        if prop_name in self.inst.properties:
            prop_value = self.inst.properties[prop_name]
            
            if isinstance(prop_value, rdltypes.ComponentRef):
                # If this is a hierarchical component reference, convert it to a Node reference
                prop_value = prop_value.build_node_ref(self, self.env)
            if isinstance(prop_value, rdltypes.PropertyReference):
                prop_value._resolve_node(self)
            
            return prop_value
        
        if ovr_default:
            # Default value is being overridden by user. Return their value
            return default
        
        # Otherwise, return its default value based on the property's rules
        rule = self.env.property_rules.lookup_property(prop_name)
        
        # Is it even a valid property or allowed for this component type?
        if rule is None:
            raise LookupError("Unknown property '%s'" % prop_name)
        if type(self.inst) not in rule.bindable_to:
            raise LookupError("Unknown property '%s'" % prop_name)
        
        # Return the default value as specified by the rulebook
        return rule.get_default(self)
    
    
    def list_properties(self, list_all=False):
        """
        Lists properties associated with this node.
        By default, only lists properties that were explicitly set. If ``list_all`` is
        set to ``True`` then lists all valid properties of this component type
        
        Parameters
        ----------
        list_all: bool
            If true, lists all valid properties of this component type.
        """
        
        if list_all:
            props = []
            for k,v in self.env.property_rules.rdl_properties.items():
                if type(self.inst) in v.bindable_to:
                    props.append(k)
            for k,v in self.env.property_rules.user_properties.items():
                if type(self.inst) in v.bindable_to:
                    props.append(k)
            return props
        else:
            return list(self.inst.properties.keys())
    
    
    def get_path_segment(self, array_suffix="[{index:d}]", empty_array_suffix="[]"):
        """
        Gets the hierarchical path segment for just this node.
        
        Parameters
        ----------
        array_suffix: str
            Override how array suffixes are represented when the index is known
        empty_array_suffix: str
            Override how array suffixes are represented when the index is not known
        """
        # pylint: disable=unused-argument
        return self.inst.inst_name
    
    
    def get_path(self, hier_separator=".", array_suffix="[{index:d}]", empty_array_suffix="[]"):
        """
        Generate an absolute path string to this node
        
        Parameters
        ----------
        hier_separator: str
            Override the hierarchy separator
        array_suffix: str
            Override how array suffixes are represented when the index is known
        empty_array_suffix: str
            Override how array suffixes are represented when the index is not known
        """
        if self.parent and not isinstance(self.parent, RootNode):
            return(
                self.parent.get_path(hier_separator, array_suffix, empty_array_suffix)
                + hier_separator
                + self.get_path_segment(array_suffix, empty_array_suffix)
            )
        else:
            return self.get_path_segment(array_suffix, empty_array_suffix)
    
    def get_html_desc(self):
        """
        Translates the node's 'desc' property into HTML.
        
        Any RDLFormatCode tags used in the description are converted to HTML.
        The text is also fed through a Markdown processor.
        
        The additional Markdown processing allows designers the choice to use a
        more modern lightweight markup language as an alternative to SystemRDL's
        "RDLFormatCode".
        
        Returns
        -------
        str or None
            HTML formatted string.
            If node does not have a description, returns ``None``
        
        """
        desc_str = self.get_property("desc")
        if desc_str is None:
            return None
        return rdlformatcode.rdlfc_to_html(desc_str, self)
    
    def __eq__(self, other):
        # Nodes are equal if they represent the same hierarchical position
        # in the register model
        return self.get_path() == other.get_path()
    
#===============================================================================
class AddressableNode(Node):
    """
    Base-class for any kind of node that can have an address
    """
    
    def __init__(self, inst, env, parent):
        super().__init__(inst, env, parent)
        
        #: List of current array indexes this node is referencing where the last
        #: item in this list iterates the most frequently
        #: 
        #: If None, then the current index is unknown
        self.current_idx = None
    
    
    def get_path_segment(self, array_suffix="[{index:d}]", empty_array_suffix="[]"):
        # Extends get_path_segment() in order to append any array suffixes
        path_segment = super().get_path_segment(array_suffix, empty_array_suffix)
        
        if self.inst.is_array:
            if self.current_idx is None:
                # Index is not known. append empty array suffixes
                return path_segment + empty_array_suffix * len(self.inst.array_dimensions)
            else:
                # Index list is known
                for idx in self.current_idx:
                    path_segment += array_suffix.format(index=idx)
                return path_segment
        else:
            return path_segment
    
    
    @property
    def address_offset(self):
        """
        Get the byte address offset of this node relative to its parent
        
        If this node is an array, it's index must be known
        
        Raises
        ------
        ValueError
            If this property is referenced on a node whose array index is not
            fully defined
        """
        if self.inst.is_array:
            if self.current_idx is None:
                raise ValueError("Index of array element must be known to derive address")
            
            # Calculate the "flattened" index of a general multidimensional array
            # For example, a component array declared as:
            #   foo[S0][S1][S2]
            # and referenced as:
            #   foo[I0][I1][I2]
            # Is flattened like this:
            #   idx = I0*S1*S2 + I1*S2 + I2
            idx = 0
            for i in range(len(self.current_idx)):
                sz = 1
                for j in range(i+1, len(self.inst.array_dimensions)):
                    sz *= self.inst.array_dimensions[j]
                idx += sz * self.current_idx[i]
            
            offset = self.inst.addr_offset + idx * self.inst.array_stride
                    
        else:
            offset = self.inst.addr_offset
        
        return offset
    
    
    @property
    def absolute_address(self):
        """
        Get the absolute byte address of this node.
        
        Indexes of all arrays in the node's lineage must be known
        
        Raises
        ------
        ValueError
            If this property is referenced on a node whose array lineage is not
            fully defined
        
        """
        if self.parent and not isinstance(self.parent, RootNode):
            return self.parent.absolute_address + self.address_offset
        else:
            return self.address_offset
    
    
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
            # Total size of arrays is technically supposed to be:
            #   self.inst.array_stride * (self.inst.n_elements-1) + self.size
            # However this opens up a whole slew of ugly corner cases that the
            # spec designers may not have anticipated.
            # Using a simplified calculation for now until someone actually cares
            return self.inst.array_stride * self.inst.n_elements

        else:
            return self.size
    
#===============================================================================
class VectorNode(Node):
    """
    Base-class for any kind of node that is vector-like.
    """

#===============================================================================
class RootNode(Node):
    @property
    def top(self):
        """
        Returns the top-level addrmap node
        """
        for child in self.children(skip_not_present=False):
            if not isinstance(child, AddrmapNode):
                continue
            return child
        raise RuntimeError
    
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
        True if combination of field access properties result in a field that
        should be interpreted as volatile.
        (Any hardware-writable field is inherently volatile)
        """
        
        hw = self.get_property('hw')
        return (
            (hw in (rdltypes.AccessType.rw, rdltypes.AccessType.rw1,
                    rdltypes.AccessType.w, rdltypes.AccessType.w1))
            or self.get_property('counter')
            or (self.get_property('next') is not None)
            or self.get_property('hwset')
            or self.get_property('hwclr')
        )
    
    @property
    def is_sw_writable(self):
        """
        Field is writable by software
        """
        sw = self.get_property('sw')
        
        return sw in (rdltypes.AccessType.rw, rdltypes.AccessType.rw1,
                        rdltypes.AccessType.w, rdltypes.AccessType.w1)
        
    @property
    def is_sw_readable(self):
        """
        Field is readable by software
        """
        sw = self.get_property('sw')
        
        return sw in (rdltypes.AccessType.rw, rdltypes.AccessType.rw1,
                        rdltypes.AccessType.r)
        
    @property
    def implements_storage(self):
        """
        True if combination of field access properties imply that the field
        implements a storage element.
        (Section 9.4.1, Table 12)
        """
        sw = self.get_property('sw')
        hw = self.get_property('hw')
        
        return (sw == rdltypes.AccessType.rw
            or sw == rdltypes.AccessType.rw1
            or ((sw == rdltypes.AccessType.r) and (hw == rdltypes.AccessType.rw))
            or ((sw == rdltypes.AccessType.w) and (hw == rdltypes.AccessType.rw))
            or ((sw == rdltypes.AccessType.w1) and (hw == rdltypes.AccessType.rw))
            or ((sw == rdltypes.AccessType.w) and (hw == rdltypes.AccessType.r))
            or ((sw == rdltypes.AccessType.w1) and (hw == rdltypes.AccessType.r))
        )

#===============================================================================
class RegNode(AddressableNode):
    
    @property
    def size(self):
        return self.get_property('regwidth') // 8
    
    @property
    def is_virtual(self):
        """
        True if this node represents a virtual register.
        (child of a mem component)
        """
        # since mem components can only contain reg instances, a reg can only be
        # virtual if its direct parent is of type mem
        return isinstance(self.parent, MemNode)
    
    @property
    def has_sw_writable(self):
        """
        Register contains one or more present fields writable by software
        """
        for field in self.fields():
            if field.is_sw_writable:
                return True
        return False
    
    @property
    def has_sw_readable(self):
        """
        Register contains one or more present fields readable by software
        """
        for field in self.fields():
            if field.is_sw_readable:
                return True
        return False

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
    last_child_node = Node._factory(node.inst.children[-1], node.env, node)
    return(
        last_child_node.inst.addr_offset
        + last_child_node.total_size
    )
