
from typing import Any, Optional, TYPE_CHECKING

from .builtin_enums import BuiltinEnum, AccessType, OnReadType, OnWriteType
from .builtin_enums import AddressingType, PrecedenceType, InterruptType

from .user_enum import UserEnumMemberContainer, UserEnum, is_user_enum

from .user_struct import UserStruct, is_user_struct

from .array import ArrayPlaceholder

from .references import ComponentRef, PropertyReference

if TYPE_CHECKING:
    from .typing import PreElabRDLType

#-------------------------------------------------------------------------------
def get_rdltype(value: Any) -> 'PreElabRDLType':
    """
    Given a value, return the type identifier object used within the RDL compiler
    If not a supported type, return None
    """

    if isinstance(value, (int, bool, str)):
        # Pass canonical types as-is
        return type(value)
    elif is_user_enum(type(value)):
        return type(value)
    elif is_user_struct(type(value)):
        return type(value)
    elif isinstance(value, BuiltinEnum):
        return type(value)
    elif isinstance(value, list):
        # Create ArrayPlaceholder representation
        # Determine element type and make sure it is uniform
        array_el_type = None # type: Optional[PreElabRDLType]
        for el in value:
            el_type = get_rdltype(el)
            if el_type is None:
                return None

            if (array_el_type is not None) and (el_type != array_el_type):
                return None
            array_el_type = el_type
        return ArrayPlaceholder(array_el_type)
    else:
        return None


class NoValue:
    """
    Non-value token used for UDPs that were bound to a component, but not
    actually assigned a value.
    (15.2.1-c)
    """
