import enum

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
