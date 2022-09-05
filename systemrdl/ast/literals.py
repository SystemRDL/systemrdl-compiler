from collections import OrderedDict
from typing import TYPE_CHECKING, Optional, Type, Dict, Tuple, List, Any

from .ast_node import ASTNode
from .conditional import is_castable

from .. import rdltypes

if TYPE_CHECKING:
    from ..compiler import RDLEnvironment
    from ..source_ref import SourceRefBase
    from rdltypes.typing import PreElabRDLType, RDLValue

    OptionalSourceRef = Optional[SourceRefBase]

class BoolLiteral(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', val: bool):
        super().__init__(env, src_ref)
        self.val = val

    def predict_type(self) -> Type[bool]:
        return bool

    def get_min_eval_width(self) -> int:
        return 1

    def get_value(self, eval_width: Optional[int]=None) -> bool:
        return self.val


class IntLiteral(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', val: int, width: int=64):
        super().__init__(env, src_ref)
        self.val = val
        self.width = width

    def predict_type(self) -> Type[int]:
        return int

    def get_min_eval_width(self) -> int:
        return self.width

    def get_value(self, eval_width: Optional[int]=None) -> int:
        return self.val


class BuiltinEnumLiteral(ASTNode):
    """
    ASTNode wrapper for builtin RDL enumeration types:
    AccessType, OnReadType, OnWriteType, AddressingType, PrecedenceType
    """
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', val: rdltypes.BuiltinEnum):
        super().__init__(env, src_ref)
        self.val = val

    def predict_type(self) -> Type[rdltypes.BuiltinEnum]:
        return type(self.val)

    def get_value(self, eval_width: Optional[int]=None) -> rdltypes.BuiltinEnum:
        return self.val


class EnumLiteral(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', val: rdltypes.UserEnum):
        super().__init__(env, src_ref)
        self.val = val

    def predict_type(self) -> Type[rdltypes.UserEnum]:
        return type(self.val)

    def get_min_eval_width(self) -> int:
        return 64

    def get_value(self, eval_width: Optional[int]=None) -> rdltypes.UserEnum:
        return self.val


class StructLiteral(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', struct_type: Type[rdltypes.UserStruct], values: Dict[str, Tuple[ASTNode, 'OptionalSourceRef']]):
        super().__init__(env, src_ref)
        self.struct_type = struct_type
        # values is a dict of member_name : (member_expr, member_name_src_ref)
        self.values = values

    def predict_type(self) -> Type[rdltypes.UserStruct]:
        for member_name, (member_expr, member_name_src_ref) in self.values.items():
            member_type = member_expr.predict_type()
            if not is_castable(member_type, self.struct_type._members[member_name]):
                self.msg.fatal(
                    "Expression for member '%s' is not compatible with the expected type"
                    % member_name,
                    member_expr.src_ref
                )

        return self.struct_type

    def get_value(self, eval_width: Optional[int]=None) -> rdltypes.UserStruct:
        resolved_values = OrderedDict()
        for member_name, (member_expr, member_name_src_ref) in self.values.items():
            resolved_values[member_name] = member_expr.get_value()

        return self.struct_type(resolved_values)


class StringLiteral(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', val: str):
        super().__init__(env, src_ref)
        self.val = val

    def predict_type(self) -> Type[str]:
        return str

    def get_value(self, eval_width: Optional[int]=None) -> str:
        return self.val


class ArrayLiteral(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', elements: List[ASTNode]):
        super().__init__(env, src_ref)
        self.elements = elements

    def predict_type(self) -> rdltypes.ArrayPlaceholder:

        if not self.elements:
            # Empty array. Element type is indeterminate
            return rdltypes.ArrayPlaceholder(None)

        # Get type of first element
        element_iter = iter(self.elements)
        element_type = next(element_iter).predict_type()

        # All remaining elements shall match
        for element in element_iter:
            if element_type != element.predict_type():
                self.msg.fatal(
                    "Elements of an array shall be the same type",
                    self.src_ref
                )

        return rdltypes.ArrayPlaceholder(element_type)

    def get_value(self, eval_width: Optional[int]=None) -> List[Any]:
        result = []
        for element in self.elements:
            result.append(element.get_value())
        return result


class ExternalLiteral(ASTNode):
    """
    ASTNode wrapper for literal value that was not compiled from a source file.
    The value provided is not an expression, but the actual value.
    """
    def __init__(self, env: 'RDLEnvironment', value: 'RDLValue'):
        super().__init__(env, None)
        self.value = value

    def predict_type(self) -> 'PreElabRDLType':
        return rdltypes.get_rdltype(self.value)

    def get_min_eval_width(self) -> int:
        if isinstance(self.value, bool):
            return 1
        elif isinstance(self.value, int):
            return 64
        elif rdltypes.is_user_enum(self.value):
            return 64
        else:
            raise RuntimeError

    def get_value(self, eval_width: Optional[int]=None) -> 'RDLValue':
        return self.value
