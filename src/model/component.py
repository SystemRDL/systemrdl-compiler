#===============================================================================
# Instances
#===============================================================================

class Inst:
    def __init__(self, typ):
        
        # Component type definition that this instantiates
        self.typ = typ
        
        # If internal vs external. None if undefined (will inherit default)
        self.external = None
        
        # Instance name
        self.name = None
        
        # Reference to the parent component of this instance
        self.parent = None
        

class AddressableInst(Inst):
    """
    Instance wrapper for addressable components:
        reg, regfile, addrmap, mem
    """
    def __init__(self, typ):
        super().__init__(typ)
        
        # Relative address offset from the parent component
        self.addr_offset = None
        
        # Alignment
        self.addr_align = None
        
        #------------------------------
        # Array Properties
        #------------------------------
        # If true, then array_size and array_stride are valid
        self.is_array = False
        
        # List of sizes for each array dimension.
        # Last item in list iterates the most frequently
        self.array_size = None
        
        # Address offset between array elements
        self.array_stride = None


class VectorInst(Inst):
    """
    Instance wrapper for vector-like components:
        field, signal
    """
    def __init__(self, typ):
        super().__init__(typ)
        
        # Bit width and low-offset
        self.width = None
        self.offset = None
        self.msb = None
        self.lsb = None
        
        # Instance reset value (for Fields only)
        self.reset_value = None

#-------------------------------------------------------------------------------
class FieldInst(VectorInst):
    pass

class RegInst(AddressableInst):
    pass
    
class RegfileInst(AddressableInst):
    pass
    
class AddrmapInst(AddressableInst):
    pass
    
class SignalInst(VectorInst):
    pass
    
class MemInst(AddressableInst):
    pass
    

#===============================================================================
# Definitions
#===============================================================================
class ComponentDef:
    # field, reg, regfile, addrmap, signal, mem
    
    INST_TYPE = None
    
    def __init__(self):
        # Type name
        self.name = None
        
        # Instances of this component def
        self.instances = []
        
        # If the component got parameterized or modified, a copy of the def is
        # made.
        # This stores a link to the original def that the component was derived
        # If None, then this is the primary def
        self.derived_from_def = None
        
        # Child elements instantiated inside this component
        self.children = []
        
        # Parameters of this definition
        self.parameters = []
    
    def create_derived_def(self):
        """
        Returns a copy of the component definition so that a derivative variant
        can be created.
        This can be due to either non-default parameterization, or dynamic
        property assignment.
        """
        
        if(self.derived_from_def is not None):
            # Creating a derived def is only necessary when copying the primary
            # one. Doing yet another copy is unnecessary since it is already
            # unique.
            return(self)
        
        # TODO: Implement create_derived_def
        # Deepcopy self
        # - all properties, and their expressions
        # - all parameters
        # - all children
        
        # Link new copy to original
        # XXX.derived_from_def = self
        
        raise NotImplementedError
        # return(XXX)


#-------------------------------------------------------------------------------
class Root(ComponentDef):
    def __init__(self):
        super().__init__()
        # Component definitions in the global root scope
        self.comp_defs = {}
    
class Field(ComponentDef):
    INST_TYPE = FieldInst

class Reg(ComponentDef):
    INST_TYPE = RegInst
    
class Regfile(ComponentDef):
    INST_TYPE = RegfileInst
    
class Addrmap(ComponentDef):
    INST_TYPE = AddrmapInst
    
class Signal(ComponentDef):
    INST_TYPE = SignalInst
    
class Mem(ComponentDef):
    INST_TYPE = MemInst

