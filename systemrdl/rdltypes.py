import enum
import inspect
from .node import AddressableNode

class AutoEnum(enum.Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

#===============================================================================
class AccessType(AutoEnum):
    #: Not Accessible
    na  = ()
    
    #: Readable and writable
    rw  = ()
    
    #: Read-only
    r   = ()
    
    #: Write-only
    w   = ()
    
    #: Readable and writable. After a reset occurs, can only be written once.
    rw1 = ()
    
    #: Write-only. After a reset occurs, can only be written once.
    w1  = ()

class OnReadType(AutoEnum):
    #: Cleared on read
    rclr    = ()
    
    #: Set on read
    rset    = ()
    
    #: User-defined read side-effect
    ruser   = ()

class OnWriteType(AutoEnum):
    #: Bitwise write one to set
    woset   = ()
    
    #: Bitwise write one to clear
    woclr   = ()
    
    #: Bitwise write one to toggle
    wot     = ()
    
    #: Bitwise write zero to set
    wzs     = ()
    
    #: Bitwise write zero to clear
    wzc     = ()
    
    #: Bitwise write zero to toggle
    wzt     = ()
    
    #: All bits are cleared on write
    wclr    = ()
    
    #: All bits are set on write
    wset    = ()
    
    #: Write modification is user-defined
    wuser   = ()

class AddressingType(AutoEnum):
    #: Components are packed tightly together
    compact     = ()
    
    #: Components are packed so each component’s start address is a multiple of its size
    regalign    = ()
    
    #: Same as regalign, except arrays are aligned to their entire size
    fullalign   = ()

class PrecedenceType(AutoEnum):
    #: Hardware writes take precedence over software
    hw  = ()
    
    #: Software writes take precedence over hardware
    sw  = ()

class InterruptType(AutoEnum):
    """
    A field's interrupt type is set when using an RDL interrupt property modifier:
    
    .. code-block:: none
        
        field f {
            negedge intr;
        };
    
    The modifier is stored in the internal "intr type" property. (note the intentional space in the name)
    
    It can be fetched the same way as other properties:
    
    .. code-block:: python
    
        intr_type = my_field_node.get_property("intr type")
    
    """
    #: Interrupt when asserted and maintained
    level  = ()
    
    #: Interrupt on low-to-high transition
    posedge  = ()
    
    #: Interrupt on high-to-low transition
    negedge  = ()
    
    #: Interrupt on any transition
    bothedge  = ()

#===============================================================================
class UserEnum(enum.Enum):
    """
    All user-defined enumerations are based on this class.
    
    UserEnum types can be identified using: :meth:`is_user_enum`
    """
    def __init__(self, value, rdl_name, rdl_desc):
        self._value_ = value
        self._rdl_name_ = rdl_name
        self._rdl_desc_ = rdl_desc
    
    @property
    def rdl_desc(self):
        """
        Enum entry's ``desc`` property
        """
        return self._rdl_desc_
    
    @property
    def rdl_name(self):
        """
        Enum entry's ``name`` property
        """
        return self._rdl_name_
    
    def __int__(self):
        return self.value
    
    def __bool__(self):
        return bool(self.value)
        
    def __deepcopy__(self, memo):
        # Do not deepcopy enumerations
        return self


def is_user_enum(t):
    """
    Test if type ``t`` is a :class:`~UserEnum`
    
    .. note:: Returns false if ``t`` is referencing a UserEnum value member
    """
    return inspect.isclass(t) and (issubclass(t, UserEnum))

#===============================================================================
class UserStruct():
    """
    All user-defined structs are based on this class.
    
    UserStruct types can be identified using: :meth:`is_user_struct`
    
    .. note:: Not implemented yet.
    """
    # TODO: Implement structs
    
def is_user_struct(t):
    """
    Test if type ``t`` is a :class:`~UserStruct`
    """
    return inspect.isclass(t) and (issubclass(t, UserStruct))

#===============================================================================
class ComponentRef:
    """
    Container for hierarchical component instance references.
    This is used internally to store information about the reference
    When a user requests the reference value, it is resolved into a Node object
    """
    
    def __init__(self, ref_root, ref_elements):
        # Handle to the component definition where ref_elements is relative to
        # This is the original_def, and NOT the actual instance
        self.ref_root = ref_root
        
        # List of hierarchical reference element tuples that make up the path
        # to the reference.
        # Path is relative to the instance of ref_root
        # Each tuple in the list represents a segment of the path:
        # [
        #   ( <ID string> , [ <Index int> , ... ] ),
        #   ( <ID string> , None )
        # ]
        self.ref_elements = ref_elements
    
    def build_node_ref(self, assignee_node, compiler):
        current_node = assignee_node
        
        # Traverse up from assignee until ref_root is reached
        while True:
            if current_node is None:
                raise RuntimeError("Upwards traverse to ref_root failed")
            if current_node.inst.original_def is self.ref_root:
                break
            current_node = current_node.parent
        
        for inst_name, idx_list in self.ref_elements:
            # find instance
            current_node = current_node.get_child_by_name(inst_name)
            if current_node is None:
                raise RuntimeError
            
            # Check if indexes are valid
            for i in range(len(idx_list)):
                if idx_list[i] >= current_node.inst.array_dimensions[i]:
                    compiler.msg.fatal(
                        "Array index out of range. Expected 0-%d, got %d."
                        % (current_node.inst.array_dimensions[i]-1, idx_list[i]),
                        None # TODO: Provide context here
                    )
            
            # Assign indexes if appropriate
            if (isinstance(current_node, AddressableNode)) and current_node.inst.is_array:
                current_node.current_idx = idx_list
            
        return current_node
        
#===============================================================================

class ArrayPlaceholder():
    """
    Placeholder class to describe array types
    
    Once elaborated, arrays are converted to Python lists
    In the meantime, this placeholder is used to communicate expected type 
    information during compilation type checking
    """
    def __init__(self, element_type):
        self.element_type = element_type
    
    def __eq__(self, other):
        if isinstance(other, ArrayPlaceholder):
            return self.element_type == other.element_type
        else:
            return False
