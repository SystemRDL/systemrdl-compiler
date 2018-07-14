from copy import deepcopy
from collections import OrderedDict

class Component:
    """
    Base class for all component types
    
    .. inheritance-diagram:: systemrdl.component
        :top-classes: ~Component
    """
    
    def __init__(self):
        #------------------------------
        # Component definition
        #------------------------------
        #: Named definition identifier.
        #: If declaration was anonymous, inherits the first instance's name.
        #: The type name of parameterized components is normalized based on the
        #: instance's parameter values.
        self.type_name = None
        
        #: Child elements instantiated inside this component
        #: 
        #: Child components are sorted as follows:
        #: 
        #: - Signals first
        #: - All other components follow.
        #: - AddressableComponents are sorted by ascending base_addr
        #: - Fields are sorted by ascending low bit
        self.children = []
        
        # Parameters of this component definition.
        # These are listed in the order that they were defined
        self.parameters = []
        
        # Properties applied to this component
        self.properties = {}
        
        # SourceRef for the component definition
        self.def_src_ref = None
        
        #------------------------------
        # Component instantiation
        #------------------------------
        #: If instantiated, set to True
        self.is_instance = False
        
        #: Name of instantiated element
        self.inst_name = None
        
        #: Reference to original component definition this instance is derived from
        self.original_def = None
        
        #: If internal vs external. None if undefined (will inherit default)
        self.external = None
        
        # SourceRef for the component instantiation
        self.inst_src_ref = None
    
    def __deepcopy__(self, memo):
        """
        Deepcopy all members except for ones that should be copied by reference
        """
        copy_by_ref = ["original_def", "def_src_ref", "inst_src_ref"]
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k in copy_by_ref:
                setattr(result, k, v)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result
    
    def get_child_by_name(self, inst_name):
        for child in self.children:
            if child.inst_name == inst_name:
                return child
        return None

class AddressableComponent(Component):
    """
    Base class for all components that can have an address
    """
    
    def __init__(self):
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        #: Address offset from the parent component.
        #: If left as None, compiler will resolve with inferred value.
        self.addr_offset = None
        
        #: Address alignment if explicitly defined by user.
        self.addr_align = None
        
        #------------------------------
        # Array Properties
        #------------------------------
        #: If true, then array_dimensions and array_stride are valid.
        self.is_array = False
        
        #: List of sizes for each array dimension.
        #: Last item in list iterates the most frequently.
        self.array_dimensions = None
        
        #: Address offset between array elements.
        #: If left as None, compiler will resolve with inferred value.
        self.array_stride = None
        
class VectorComponent(Component):
    """
    Base class for all components that are vector-like
    """
    
    def __init__(self):
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        #: Width of vector in bits
        self.width = None
        
        #: bit positions of most and least significant bits
        self.msb = None
        self.lsb = None
        
        #: bit range
        self.high = None
        self.low = None

#===============================================================================
class Root(Component):
    """
    Meta-component used by compiler to represent the root scope
    """
    def __init__(self):
        super().__init__()
        # Component definitions in the global root scope
        self.comp_defs = OrderedDict()
    
class Signal(VectorComponent):
    pass
    
class Field(VectorComponent):
    pass

class Reg(AddressableComponent):
    def __init__(self):
        super().__init__()
        #------------------------------
        # Alias Register
        #------------------------------
        #: If true, then alias_primary_inst is valid
        self.is_alias = False
        
        #: Reference to primary register instance
        self.alias_primary_inst = None
    
class Regfile(AddressableComponent):
    pass
    
class Addrmap(AddressableComponent):
    pass
    
class Mem(AddressableComponent):
    pass
