from copy import deepcopy

class Component:
    """
    Base class for all component types:
        field, reg, regfile, addrmap, signal, mem
    """
    
    def __init__(self):
        #------------------------------
        # Component definition
        #------------------------------
        # Named definition identifier. Remains None if declaration was anonymous
        self.type_name = None
        
        # Child elements instantiated inside this component
        self.children = []
        
        # Parameters of this component definition
        self.parameters = []
        
        # Properties applied to this component
        self.properties = {}
        
        #------------------------------
        # Component instantiation
        #------------------------------
        # If instantiated, set to True
        self.is_instance = False
        
        # Name of instantiated element
        self.inst_name = None
        
        # Reference to original component definition this instance is derived from
        self.original_def = None
        
        # If internal vs external. None if undefined (will inherit default)
        self.external = None
    
    def __deepcopy__(self, memo):
        """
        Deepcopy all members except for ones that should be copied by reference
        """
        copy_by_ref = ["original_def"]
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if(k in copy_by_ref):
                setattr(result, k, v)
            else:
                setattr(result, k, deepcopy(v, memo))
        return(result)

class AddressableComponent(Component):
    """
    Base class for all components that can have an address:
        reg, regfile, addrmap, mem
    """
    
    def __init__(self):
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        # Address offset from the parent component
        # If left as None, compiler will resolve with inferred value
        self.addr_offset = None
        
        # Address alignment if explicitly defined by user
        self.addr_align = None
        
        #------------------------------
        # Array Properties
        #------------------------------
        # If true, then array_dimensions and array_stride are valid
        self.is_array = False
        
        # List of sizes for each array dimension.
        # Last item in list iterates the most frequently
        self.array_dimensions = None
        
        # Address offset between array elements
        # If left as None, compiler will resolve with inferred value
        self.array_stride = None
        
class VectorComponent(Component):
    """
    Base class for all components that are vector-like:
        field, signal
    """
    
    def __init__(self):
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        # Bit width and low-offset
        self.width = None
        self.offset = None
        self.msb = None
        self.lsb = None

#===============================================================================
class Root(Component):
    """
    Meta-component used by compiler to represent the root scope
    """
    def __init__(self):
        super().__init__()
        # Component definitions in the global root scope
        self.comp_defs = {}
    
class Signal(VectorComponent):
    pass
    
class Field(VectorComponent):
    def __init__(self):
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        self.reset_value = None

class Reg(AddressableComponent):
    pass
    
class Regfile(AddressableComponent):
    pass
    
class Addrmap(AddressableComponent):
    pass
    
class Mem(AddressableComponent):
    pass
