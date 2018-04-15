import enum
from .node import AddressableNode

class AutoEnum(enum.Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

#===============================================================================
class AccessType(AutoEnum):
    na  = ()
    rw  = ()
    wr  = ()
    r   = ()
    w   = ()
    rw1 = ()
    w1  = ()

class OnReadType(AutoEnum):
    rclr    = ()
    rset    = ()
    ruser   = ()

class OnWriteType(AutoEnum):
    woset   = ()
    woclr   = ()
    wot     = ()
    wzs     = ()
    wzc     = ()
    wzt     = ()
    wclr    = ()
    wset    = ()
    wuser   = ()

class AddressingType(AutoEnum):
    compact     = ()
    regalign    = ()
    fullalign   = ()

class PrecedenceType(AutoEnum):
    hw  = ()
    sw  = ()

class InterruptType(AutoEnum):
    level  = ()
    posedge  = ()
    negedge  = ()
    bothedge  = ()

#===============================================================================
class UserEnum(enum.Enum):
    """
    All user-defined enumerations are based on this class
    UserEnum types can be identified using: issubclass(my_enum, UserEnum)
    """

class UserStruct():
    """
    TODO Implementation TBD,
    but whatever it is, shall be identifiable using issubclass()
    """

#===============================================================================
class ComponentRef:
    """
    Container for hierarchical component instance references.
    This is used internally to store information about the reference
    When a user requests the reference value, it is resolved into a Node object
    """
    
    def __init__(self, uplevels_to_ref, ref_elements):
        # Number of Node parents to traverse up from the assignee to reach the
        # root of the relative path specified by ref_elements
        self.uplevels_to_ref = uplevels_to_ref
        
        # List of hierarchical reference element tuples that make up the path
        # to the reference.
        # Each tuple in the list represents a segment of the path:
        # [
        #   ( <ID string> , [ <Index int> , ... ] ),
        #   ( <ID string> , None )
        # ]
        self.ref_elements = ref_elements
    
    def build_node_ref(self, assignee_node):
        current_node = assignee_node
        
        # Traverse up from assignee as needed
        for _ in range(self.uplevels_to_ref):
            if(current_node.parent is None):
                raise RuntimeError("Upref attempted past last parent")
            current_node = current_node.parent
        
        for inst_name, idx_list in self.ref_elements:
            # find instance
            current_node = current_node.get_child_by_name(inst_name)
            if(current_node is None):
                raise RuntimeError
            
            # Assign indexes if appropriate
            if((issubclass(type(current_node), AddressableNode)) and current_node.inst.is_array):
                current_node.current_idx = idx_list
            
        return(current_node)
        