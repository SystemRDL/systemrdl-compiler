from copy import deepcopy
from collections import OrderedDict
from typing import TYPE_CHECKING, Union, Type, Optional, Any, Dict, Tuple, List

from .. import component as comp
from .. import rdltypes
from .helpers import truncate_int

if TYPE_CHECKING:
    from ..compiler import RDLEnvironment
    from .parameter import Parameter
    from ..source_ref import SourceRefBase

OSourceRef = Optional['SourceRefBase']

class Expr:
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef):
        self.env = env
        self.msg = env.msg

        # Source Ref to use for error context
        self.src_ref = src_ref

    def __deepcopy__(self, memo: Dict[int, Any]) -> 'Expr':
        """
        Deepcopy all members except for ones that should be copied by reference
        """
        copy_by_ref = ["env", "msg"]
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k in copy_by_ref:
                setattr(result, k, v)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def predict_type(self) -> rdltypes.PreElabRDLType:
        """
        Returns the expected type of the result of the expression
        This function shall call any child expression's predict_type()
        even if the child type is not relevant to the resulting type.
        Raises exception if input types are not compatible.
        """
        raise NotImplementedError

    def get_min_eval_width(self) -> int:
        """
        Returns the expressions resulting integer width based on the
        self-determined expression bit-width rules
        (SystemVerilog LRM: IEEE Std 1800-2012, Table 11-21)
        """
        raise RuntimeError

    def get_value(self, eval_width: Optional[int]=None) -> Any:
        """
        Compute the value of the result of the expression

        Since predict_type() was already called, safe to assume that types are
        compatible.

        The eval_width parameter controls the integer width resolution context
        - If eval_width is irrelevant:
            For example, comparison operator, integer literal, non-integer expression)
            OK to ignore eval_width.
            Otherwise...
        - If eval_width is None:
            This expression node is the start of a new self-determined context.
            Query the relevant operands to determine the context's eval_width
        - If eval_width is set to a value:
            Parent expression is propagating the eval_width
        """
        raise NotImplementedError

#-------------------------------------------------------------------------------
# Literals

class BoolLiteral(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, val: bool):
        super().__init__(env, src_ref)
        self.val = val

    def predict_type(self) -> Type[bool]:
        return bool

    def get_min_eval_width(self) -> int:
        return 1

    def get_value(self, eval_width: Optional[int]=None) -> bool:
        return self.val


class IntLiteral(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, val: int, width: int=64):
        super().__init__(env, src_ref)
        self.val = val
        self.width = width

    def predict_type(self) -> Type[int]:
        return int

    def get_min_eval_width(self) -> int:
        return self.width

    def get_value(self, eval_width: Optional[int]=None) -> int:
        return self.val


class BuiltinEnumLiteral(Expr):
    """
    Expr wrapper for builtin RDL enumeration types:
    AccessType, OnReadType, OnWriteType, AddressingType, PrecedenceType
    """
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, val: rdltypes.BuiltinEnum):
        super().__init__(env, src_ref)
        self.val = val

    def predict_type(self) -> Type[rdltypes.BuiltinEnum]:
        return type(self.val)

    def get_value(self, eval_width: Optional[int]=None) -> rdltypes.BuiltinEnum:
        return self.val


class EnumLiteral(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, val: rdltypes.UserEnum):
        super().__init__(env, src_ref)
        self.val = val

    def predict_type(self) -> Type[rdltypes.UserEnum]:
        return type(self.val)

    def get_min_eval_width(self) -> int:
        return 64

    def get_value(self, eval_width: Optional[int]=None) -> rdltypes.UserEnum:
        return self.val


class StructLiteral(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, struct_type: Type[rdltypes.UserStruct], values: Dict[str, Tuple[Expr, OSourceRef]]):
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


class StringLiteral(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, val: str):
        super().__init__(env, src_ref)
        self.val = val

    def predict_type(self) -> Type[str]:
        return str

    def get_value(self, eval_width: Optional[int]=None) -> str:
        return self.val


class ArrayLiteral(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, elements: List[Expr]):
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


class ExternalLiteral(Expr):
    """
    Expr wrapper for literal value that was not compiled from a source file.
    The value provided is not an expression, but the actual value.
    """
    def __init__(self, env: 'RDLEnvironment', value: rdltypes.RDLValue):
        super().__init__(env, None)
        self.value = value

    def predict_type(self) -> rdltypes.PreElabRDLType:
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

    def get_value(self, eval_width: Optional[int]=None) -> rdltypes.RDLValue:
        return self.value

#-------------------------------------------------------------------------------
# Sequence Operators

class Concatenate(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, elements: List[Expr]):
        super().__init__(env, src_ref)
        self.elements = elements
        self.type = None # type: Union[Type[int], Type[str]]

    def predict_type(self):
        # type: () -> Union[Type[int], Type[str]]

        # Get type of first element
        element_iter = iter(self.elements)
        element_type = next(element_iter).predict_type()

        # All remaining elements shall match
        for element in element_iter:
            if element_type != element.predict_type():
                self.msg.fatal(
                    "Elements of a concatenation shall be the same type",
                    self.src_ref
                )
        if is_castable(element_type, int):
            self.type = int
        elif is_castable(element_type, str):
            self.type = str
        else:
            self.msg.fatal(
                "Concatenation operator can only be used for integral or string types",
                self.src_ref
            )
        return self.type

    def get_min_eval_width(self) -> int:
        if self.type == int:
            width = 0
            for element in self.elements:
                width = width + element.get_min_eval_width()

            return width
        else:
            raise RuntimeError

    def get_value(self, eval_width: Optional[int]=None) -> Union[int, str]:
        if self.type == int:
            int_result = 0
            for element in self.elements:
                width = element.get_min_eval_width()
                int_result <<= width
                int_result |= int(element.get_value())
            return int_result

        elif self.type == str:
            str_result = ""
            for element in self.elements:
                str_result += element.get_value()
            return str_result

        else:
            raise RuntimeError


class Replicate(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, reps: Expr, concat: Expr):
        super().__init__(env, src_ref)
        self.reps = reps
        self.concat = concat
        self.type = None # type: Union[Type[int], Type[str]]
        self.reps_value = None # type: int

    def predict_type(self):
        # type: () -> Union[Type[int], Type[str]]

        if not is_castable(self.reps.predict_type(), int):
            self.msg.fatal(
                "Replication count operand of replication expression is not a compatible numeric type",
                self.reps.src_ref
            )

        element_type = self.concat.predict_type()

        if is_castable(element_type, int):
            self.type = int
            return int
        elif is_castable(element_type, str):
            self.type = str
            return str
        else:
            # All replications contain a nested concatenation
            # Type check for invalid type is already handled there
            raise RuntimeError

    def get_min_eval_width(self) -> int:
        # Evaluate number of repetitions
        if self.reps_value is None:
            self.reps_value = self.reps.get_value()

        if self.type == int:
            # Get width of single contents
            width = self.concat.get_min_eval_width()
            width *= self.reps_value
            return width
        else:
            raise RuntimeError

    def get_value(self, eval_width: Optional[int]=None) -> Union[int, str]:
        # Evaluate number of repetitions
        if self.reps_value is None:
            self.reps_value = self.reps.get_value()

        if self.type == int:
            width = self.concat.get_min_eval_width()
            val = int(self.concat.get_value())

            int_result = 0
            for _ in range(self.reps_value):
                int_result <<= width
                int_result |= val

            return int_result

        elif self.type == str:
            str_result = self.concat.get_value()
            str_result *= self.reps_value
            return str_result

        else:
            raise RuntimeError

#-------------------------------------------------------------------------------
# Integer binary operators:
#   +  -  *  /  %  &  |  ^  ^~  ~^
# Normal expression context rules
class _BinaryIntExpr(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, l: Expr, r: Expr):
        super().__init__(env, src_ref)
        self.l = l
        self.r = r

    def predict_type(self) -> Type[int]:
        l_type = self.l.predict_type()
        r_type = self.r.predict_type()
        if not is_castable(l_type, int):
            self.msg.fatal(
                "Left operand of expression is not a compatible numeric type",
                self.src_ref
            )
        if not is_castable(r_type, int):
            self.msg.fatal(
                "Right operand of expression is not a compatible numeric type",
                self.src_ref
            )
        return int

    def get_min_eval_width(self) -> int:
        return(max(
            self.l.get_min_eval_width(),
            self.r.get_min_eval_width()
        ))

class Add(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l + r, eval_width)

class Sub(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l - r, eval_width)

class Mult(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l * r, eval_width)

class Div(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))

        if r == 0:
            self.msg.fatal(
                "Division by zero",
                self.src_ref
            )
        return truncate_int(l // r, eval_width)

class Mod(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))

        if r == 0:
            self.msg.fatal(
                "Modulo by zero",
                self.src_ref
            )
        return truncate_int(l % r, eval_width)

class BitwiseAnd(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l & r, eval_width)

class BitwiseOr(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l | r, eval_width)

class BitwiseXor(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l ^ r, eval_width)

class BitwiseXnor(_BinaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l ^~ r, eval_width)

#-------------------------------------------------------------------------------
# Integer unary operators:
#   +  -  ~
# Normal expression context rules
class _UnaryIntExpr(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, n: Expr):
        super().__init__(env, src_ref)
        self.n = n

    def predict_type(self) -> Type[int]:
        op_type = self.n.predict_type()
        if not is_castable(op_type, int):
            self.msg.fatal(
                "Operand of expression is not a compatible numeric type",
                self.src_ref
            )
        return int

    def get_min_eval_width(self) -> int:
        return self.n.get_min_eval_width()

class UnaryPlus(_UnaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        return truncate_int(n, eval_width)

class UnaryMinus(_UnaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        return truncate_int(-n, eval_width)

class BitwiseInvert(_UnaryIntExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        return truncate_int(~n, eval_width)

#-------------------------------------------------------------------------------
# Relational operators:
#   == != < > <= >=
# Result is always 1 bit bool
# Creates a new evaluation context
# Child operands are evaluated in the same width context, sized to the max
# of either op.
class _RelationalExpr(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, l: Expr, r: Expr):
        super().__init__(env, src_ref)
        self.l = l
        self.r = r
        self.is_numeric = None # type: bool

    def predict_type(self) -> Type[bool]:
        l_type = self.l.predict_type()
        r_type = self.r.predict_type()

        # Type of L and R operands shall be compatible
        if is_castable(l_type, int) and is_castable(r_type, int):
            self.is_numeric = True
        elif l_type == r_type:
            # Same types. Inherently compatible
            self.is_numeric = False
        else:
            # Incompatible
            self.msg.fatal(
                "Left and right operands of expression are not compatible types",
                self.src_ref
            )
        return bool

    def get_min_eval_width(self) -> int:
        return 1

    def get_ops(self) -> Tuple[Any, Any]:

        if self.is_numeric:
            # New width context. Determine eval_width here
            eval_width = max(
                self.l.get_min_eval_width(),
                self.r.get_min_eval_width()
            )

            l = int(self.l.get_value(eval_width))
            r = int(self.r.get_value(eval_width))
        elif not self.is_numeric:
            l = self.l.get_value()
            r = self.r.get_value()
        else:
            raise RuntimeError

        return l, r

class _NumericRelationalExpr(_RelationalExpr):

    def predict_type(self) -> Type[bool]:
        l_type = self.l.predict_type()
        r_type = self.r.predict_type()

        # Type of L and R operands shall be integral types
        self.is_numeric = True
        if not is_castable(l_type, int):
            self.msg.fatal(
                "Left operand of expression is not a compatible numeric type",
                self.src_ref
            )
        if not is_castable(r_type, int):
            self.msg.fatal(
                "Right operand of expression is not a compatible numeric type",
                self.src_ref
            )
        return bool



class Eq(_RelationalExpr):
    def get_value(self, eval_width: Optional[int]=None) -> bool:
        l, r = self.get_ops()
        return l == r

class Neq(_RelationalExpr):
    def get_value(self, eval_width: Optional[int]=None) -> bool:
        l, r = self.get_ops()
        return l != r

class Lt(_NumericRelationalExpr):
    def get_value(self, eval_width: Optional[int]=None) -> bool:
        l, r = self.get_ops()
        return l < r

class Gt(_NumericRelationalExpr):
    def get_value(self, eval_width: Optional[int]=None) -> bool:
        l, r = self.get_ops()
        return l > r

class Leq(_NumericRelationalExpr):
    def get_value(self, eval_width: Optional[int]=None) -> bool:
        l, r = self.get_ops()
        return l <= r

class Geq(_NumericRelationalExpr):
    def get_value(self, eval_width: Optional[int]=None) -> bool:
        l, r = self.get_ops()
        return l >= r

#-------------------------------------------------------------------------------
# Reduction operators:
#   &  ~&  |  ~|  ^  ^~  !
# Result is always 1 bit int
# Creates a new evaluation context
class _ReductionExpr(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, n: Expr):
        super().__init__(env, src_ref)
        self.n = n

    def predict_type(self) -> Type[int]:
        op_type = self.n.predict_type()
        if not is_castable(op_type, int):
            self.msg.fatal(
                "Operand of expression is not a compatible numeric type",
                self.src_ref
            )
        return int

    def get_min_eval_width(self) -> int:
        return 1

class AndReduce(_ReductionExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        eval_width = self.n.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        n = truncate_int(~n, eval_width)
        return int(n == 0)

class NandReduce(_ReductionExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        eval_width = self.n.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        n = truncate_int(~n, eval_width)
        return int(n != 0)

class OrReduce(_ReductionExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        n = int(self.n.get_value())
        return int(n != 0)

class NorReduce(_ReductionExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        n = int(self.n.get_value())
        return int(n == 0)

class XorReduce(_ReductionExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        n = int(self.n.get_value())
        v = 0
        while n:
            if n & 1:
                v ^= 1
            n >>= 1
        return v

class XnorReduce(_ReductionExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        n = int(self.n.get_value())
        v = 1
        while n:
            if n & 1:
                v ^= 1
            n >>= 1
        return v

class BoolNot(_ReductionExpr):
    def predict_type(self) -> Type[bool]:
        super().predict_type()
        return bool

    def get_value(self, eval_width: Optional[int]=None) -> bool:
        n = int(self.n.get_value())
        return not n

#-------------------------------------------------------------------------------
# Logical boolean operators:
#   && ||
# Both operands are self-determined
class _BoolExpr(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, l: Expr, r: Expr):
        super().__init__(env, src_ref)
        self.l = l
        self.r = r

    def predict_type(self) -> Type[bool]:
        l_type = self.l.predict_type()
        r_type = self.r.predict_type()
        if not is_castable(l_type, bool):
            self.msg.fatal(
                "Left operand of expression is not a compatible boolean type",
                self.src_ref
            )
        if not is_castable(r_type, bool):
            self.msg.fatal(
                "Right operand of expression is not a compatible boolean type",
                self.src_ref
            )
        return bool

    def get_min_eval_width(self) -> int:
        return 1

class BoolAnd(_BoolExpr):
    def get_value(self, eval_width: Optional[int]=None) -> bool:
        l = bool(self.l.get_value())
        r = bool(self.r.get_value())
        return l and r

class BoolOr(_BoolExpr):
    def get_value(self, eval_width: Optional[int]=None) -> bool:
        l = bool(self.l.get_value())
        r = bool(self.r.get_value())
        return l or r

#-------------------------------------------------------------------------------
# Exponent & shift operators:
#   **  <<  >>
# Righthand operand is self-determined
class _ExpShiftExpr(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, l: Expr, r: Expr):
        super().__init__(env, src_ref)
        self.l = l
        self.r = r

    def predict_type(self) -> Type[int]:
        l_type = self.l.predict_type()
        r_type = self.r.predict_type()
        if not is_castable(l_type, int):
            self.msg.fatal(
                "Left operand of expression is not a compatible numeric type",
                self.src_ref
            )
        if not is_castable(r_type, int):
            self.msg.fatal(
                "Right operand of expression is not a compatible numeric type",
                self.src_ref
            )
        return int

    def get_min_eval_width(self) -> int:
        # Righthand op has no influence in evaluation context
        return self.l.get_min_eval_width()

class Exponent(_ExpShiftExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.l.get_min_eval_width()
        # Right operand is self-determined
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value())
        return truncate_int(int(l ** r), eval_width)

class LShift(_ExpShiftExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.l.get_min_eval_width()
        # Right operand is self-determined
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value())
        return truncate_int(l << r, eval_width)

class RShift(_ExpShiftExpr):
    def get_value(self, eval_width: Optional[int]=None) -> int:
        if eval_width is None:
            eval_width = self.l.get_min_eval_width()
        # Right operand is self-determined
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value())
        return truncate_int(l >> r, eval_width)

#-------------------------------------------------------------------------------
# Ternary conditional operator
#   i ? j : k
# Truth expression is self-determined and does not contribute to context

class TernaryExpr(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, i: Expr, j: Expr, k: Expr):
        super().__init__(env, src_ref)
        self.i = i
        self.j = j
        self.k = k
        self.is_numeric = None # type: bool

    def predict_type(self) -> rdltypes.PreElabRDLType:
        t_i = self.i.predict_type()
        if not is_castable(t_i, bool):
            self.msg.fatal(
                "Conditional operand of expression is not a compatible boolean type",
                self.src_ref
            )

        # Type of j and k shall be compatible
        t_j = self.j.predict_type()
        t_k = self.k.predict_type()

        typ = None # type: Any
        if is_castable(t_j, int) and is_castable(t_k, int):
            self.is_numeric = True
            typ = int
        elif t_j == t_k:
            # Same types. Inherently compatible
            self.is_numeric = False
            typ = t_j
        else:
            # Incompatible
            self.msg.fatal(
                "True/False results of ternary conditional are not compatible types",
                self.src_ref
            )
        return typ

    def get_min_eval_width(self) -> int:
        # Truth operand has no influence in evaluation context
        return(max(
            self.j.get_min_eval_width(),
            self.k.get_min_eval_width()
        ))

    def get_value(self, eval_width: Optional[int]=None) -> Any:
        # i is self-determined
        i = bool(self.i.get_value())

        if self.is_numeric:
            if eval_width is None:
                eval_width = max(
                    self.j.get_min_eval_width(),
                    self.k.get_min_eval_width()
                )
            j = self.j.get_value(eval_width)
            k = self.k.get_value(eval_width)
        elif not self.is_numeric:
            j = self.j.get_value()
            k = self.k.get_value()
        else:
            raise RuntimeError

        if i:
            return j
        else:
            return k

#-------------------------------------------------------------------------------
# Width cast operator
# the cast type informs the parser what width to cast to
# The cast width determines the result's width
# Also influences the min eval width of the value expression
class WidthCast(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, v: Expr, w_expr: Optional[Expr]=None, w_int: int=64):
        super().__init__(env, src_ref)

        if w_expr is not None:
            self.v = v
            self.w_expr = w_expr
            self.cast_width = None
        else:
            self.v = v
            self.w_expr = None
            self.cast_width = w_int

    def predict_type(self) -> Type[int]:
        if self.cast_width is None:
            if not is_castable(self.w_expr.predict_type(), int):
                self.msg.fatal(
                    "Width operand of cast expression is not a compatible numeric type",
                    self.w_expr.src_ref
                )
        if not is_castable(self.v.predict_type(), int):
            self.msg.fatal(
                "Value operand of cast expression cannot be cast to an integer",
                self.v.src_ref
            )

        return int

    def get_min_eval_width(self) -> int:
        if self.cast_width is None:
            self.cast_width = int(self.w_expr.get_value())
        return self.cast_width


    def get_value(self, eval_width: Optional[int]=None) -> int:
        # Truncate to cast width instead of eval width
        if self.cast_width is None:
            self.cast_width = int(self.w_expr.get_value())
        if self.cast_width == 0:
            self.msg.fatal(
                "Cannot cast to width of zero",
                self.src_ref
            )

        eval_width = max(self.cast_width, self.v.get_min_eval_width())
        n = int(self.v.get_value(eval_width))

        return truncate_int(n, self.cast_width)

#-------------------------------------------------------------------------------
# Boolean cast operator

class BoolCast(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, n: Expr):
        super().__init__(env, src_ref)
        self.n = n

    def predict_type(self) -> Type[bool]:
        if not is_castable(self.n.predict_type(), bool):
            self.msg.fatal(
                "Value operand of cast expression cannot be cast to a boolean",
                self.src_ref
            )
        return bool

    def get_min_eval_width(self) -> int:
        return 1

    def get_value(self, eval_width: Optional[int]=None) -> bool:
        n = int(self.n.get_value())
        return n != 0

#-------------------------------------------------------------------------------
# References

class ParameterRef(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, param: 'Parameter'):
        super().__init__(env, src_ref)
        self.param = param

    def predict_type(self) -> rdltypes.PreElabRDLType:
        return self.param.param_type

    def get_min_eval_width(self) -> int:
        if self.param.expr is None:
            self.msg.fatal(
                "Value for parameter '%s' was never assigned" % self.param.name,
                self.src_ref
            )
        return self.param.expr.get_min_eval_width()

    def get_value(self, eval_width: Optional[int]=None) -> Any:
        if self.param.expr is None:
            self.msg.fatal(
                "Value for parameter '%s' was never assigned" % self.param.name,
                self.src_ref
            )
        return self.param.expr.get_value(eval_width)


class ArrayIndex(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, array: Expr, index: Expr):
        super().__init__(env, src_ref)
        self.array = array
        self.index = index

    def predict_type(self) -> rdltypes.PreElabRDLType:
        if not is_castable(self.index.predict_type(), int):
            self.msg.fatal(
                "Array index is not a compatible numeric type",
                self.index.src_ref
            )

        array_type = self.array.predict_type()
        if not isinstance(array_type, rdltypes.ArrayPlaceholder):
            self.msg.fatal(
                "Cannot index non-array type",
                self.array.src_ref
            )
        assert isinstance(array_type, rdltypes.ArrayPlaceholder)

        return array_type.element_type

    def get_min_eval_width(self) -> int:
        # TODO: Need to actually reach in and get eval width of array element
        return 64

    def get_value(self, eval_width: Optional[int]=None) -> Any:
        index = self.index.get_value()
        array = self.array.get_value()
        if index >= len(array):
            self.msg.fatal(
                "Array index '%d' is out of range" % index,
                self.src_ref
            )
        return array[index]


class MemberRef(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, struct: Expr, member_name: str):
        super().__init__(env, src_ref)
        self.struct = struct
        self.member_name = member_name

    def predict_type(self): # type: ignore
        struct_type = self.struct.predict_type()

        if not rdltypes.is_user_struct(struct_type):
            self.msg.fatal(
                "Cannot reference member of non-struct type",
                self.struct.src_ref
            )

        if self.member_name not in struct_type._members:
            self.msg.fatal(
                "'%s' is not a valid member of struct type '%s'"
                % (self.member_name, struct_type.__name__),
                self.src_ref
            )

        return struct_type._members[self.member_name]

    def get_min_eval_width(self) -> int:
        # TODO: Need to actually reach in and get eval width of struct member
        return 64

    def get_value(self, eval_width: Optional[int]=None) -> Any:
        struct = self.struct.get_value()
        return struct._values[self.member_name]


RefElementsType = List[
    Tuple[str, List[Expr], OSourceRef]
]
class InstRef(Expr):
    def __init__(self, env: 'RDLEnvironment', ref_root: comp.Component, ref_elements: RefElementsType):
        super().__init__(env, None) # single src_ref doesn't make sense for InstRef

        # Handle to the component definition where ref_elements is relative to
        # This is the original_def, and NOT the actual instance
        # When deepcopying, this is copied by reference in order to preserve
        # the original def object
        self.ref_root = ref_root

        # List of hierarchical reference element tuples that make up the path
        # to the reference.
        # Path is relative to ref_inst
        # Each tuple in the list represents a segment of the path:
        # [
        #   ( str , [ <Index Expr> , ... ] , SourceRefBase),
        #   ( str , [ <Index Expr> , ... ] , SourceRefBase)
        # ]
        self.ref_elements = ref_elements

    def __deepcopy__(self, memo: Dict[int, Any]) -> 'InstRef':
        """
        Copy any Source Ref by ref within the ref_elements list when deepcopying
        """
        copy_by_ref = ["env", "msg", "ref_root"]
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k in copy_by_ref:
                setattr(result, k, v)
            elif k == "ref_elements":
                # Manually deepcopy the ref_elements list
                new_ref_elements = []
                for src_name, src_array_suffixes, src_src_ref in v:
                    new_array_suffixes = deepcopy(src_array_suffixes, memo)
                    new_ref_elements.append((src_name, new_array_suffixes, src_src_ref))
                setattr(result, k, new_ref_elements)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def predict_type(self) -> Type[comp.Component]:
        """
        Traverse the ref_elements path and determine the component type being
        referenced.
        Also do some checks on the array indexes
        """
        current_comp = self.ref_root
        for name, array_suffixes, name_src_ref in self.ref_elements:

            # find instance
            current_comp = current_comp.get_child_by_name(name)
            if current_comp is None:
                # Not found!
                self.msg.fatal(
                    "Could not resolve hierarchical reference to '%s'" % name,
                    name_src_ref
                )

            # Do type-check in array suffixes
            for array_suffix in array_suffixes:
                array_suffix.predict_type()

            # Check array suffixes
            if (isinstance(current_comp, comp.AddressableComponent)) and current_comp.is_array:
                assert isinstance(current_comp.array_dimensions, list)
                # is an array
                if len(array_suffixes) != len(current_comp.array_dimensions):
                    self.msg.fatal(
                        "Incompatible number of index dimensions after '%s'. Expected %d, found %d."
                        % (name, len(current_comp.array_dimensions), len(array_suffixes)),
                        name_src_ref
                    )
            elif array_suffixes:
                # Has array suffixes. Check if compatible with referenced component
                self.msg.fatal(
                    "Unable to index non-array component '%s'" % name,
                    name_src_ref
                )

        return type(current_comp)

    def get_value(self, eval_width: Optional[int]=None) -> rdltypes.ComponentRef:
        """
        Build a resolved ComponentRef container that describes the relative path
        """

        resolved_ref_elements = []

        for name, array_suffixes, name_src_ref in self.ref_elements:
            idx_list = [suffix.get_value() for suffix in array_suffixes]
            resolved_ref_elements.append((name, idx_list, name_src_ref))

        # Create container
        cref = rdltypes.ComponentRef(self.ref_root, resolved_ref_elements)

        return cref


class PropRef(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, inst_ref: Expr, prop_ref_type: Type[rdltypes.PropertyReference]):
        super().__init__(env, src_ref)
        # InstRef to the component whose property is being referenced
        self.inst_ref = inst_ref

        # PropertyReference class
        self.prop_ref_type = prop_ref_type

    def predict_type(self) -> Type[rdltypes.PropertyReference]:
        """
        Predict the type of the inst_ref, and make sure the property being
        referenced is allowed
        """
        inst_type = self.inst_ref.predict_type()

        if self.prop_ref_type.allowed_inst_type != inst_type:
            self.msg.fatal(
                "'%s' is not a valid property of instance" % self.prop_ref_type.get_name(),
                self.src_ref
            )

        return self.prop_ref_type

    def get_value(self, eval_width: Optional[int]=None) -> rdltypes.PropertyReference:
        cref = self.inst_ref.get_value()
        return self.prop_ref_type(self.src_ref, self.env, cref)

#-------------------------------------------------------------------------------
# Assignment cast
# This is a wrapper expression that normalizes the expression result
# to the expected data type
# This wrapper forces the operand to be evaluated in a self-determined context
# The cast type has no effect on expression evaluation
# During post-compile:
#   Checks that the expression result is of a compatible type
#
# When getting value:
#   Ensures that the expression result gets converted to the resulting type
class AssignmentCast(Expr):
    def __init__(self, env: 'RDLEnvironment', src_ref: OSourceRef, v: Expr, dest_type: rdltypes.PreElabRDLType):
        super().__init__(env, src_ref)

        self.v = v
        self.dest_type = dest_type

    def predict_type(self) -> rdltypes.PreElabRDLType:
        op_type = self.v.predict_type()

        if not is_castable(op_type, self.dest_type):
            self.msg.fatal(
                "Result of expression is not compatible with the expected type",
                self.src_ref
            )

        return self.dest_type

    def get_min_eval_width(self) -> int:
        return self.v.get_min_eval_width()

    def get_value(self, eval_width: Optional[int]=None) -> Any:
        v = self.v.get_value()

        if self.dest_type == bool:
            return bool(v)
        elif self.dest_type == int:
            return int(v)
        else:
            return v


#===============================================================================

def is_castable(src: Any, dst: Any) -> bool:
    """
    Check if src type can be cast to dst type
    """
    if ((src in [int, bool]) or rdltypes.is_user_enum(src)) and (dst in [int, bool]):
        # Pure numeric or enum can be cast to a numeric
        return True
    elif (src == rdltypes.ArrayPlaceholder) and (dst == rdltypes.ArrayPlaceholder):
        # Check that array element types also match
        if src.element_type is None:
            # indeterminate array type. Is castable
            return True
        elif src.element_type == dst.element_type:
            return True
        else:
            return False
    elif rdltypes.is_user_struct(dst):
        # Structs can be assigned their derived counterparts - aka their subclasses
        return issubclass(src, dst)
    elif dst == rdltypes.PropertyReference:
        return issubclass(src, rdltypes.PropertyReference)
    elif src == dst:
        return True
    else:
        return False
