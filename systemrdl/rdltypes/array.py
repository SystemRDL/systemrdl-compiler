from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .typing import PreElabRDLType

class ArrayPlaceholder():
    """
    Placeholder class to describe array types

    Once elaborated, arrays are converted to Python lists
    In the meantime, this placeholder is used to communicate expected type
    information during compilation type checking
    """
    def __init__(self, element_type: 'PreElabRDLType'):
        self.element_type = element_type

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ArrayPlaceholder):
            return self.element_type == other.element_type
        else:
            return NotImplemented
