from copy import deepcopy
from collections import OrderedDict

from .. import component as comp
from .. import rdltypes
from .helpers import truncate_int

class Expr:
    def __init__(self, env, src_ref):
        self.env = env
        self.msg = env.msg
        
        # SourceRef to use for error context
        self.src_ref = src_ref
    
    def __deepcopy__(self, memo):
        """
        Deepcopy all members except for ones that should be copied by reference
        """
        copy_by_ref = ["src_ref", "env", "msg"]
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k in copy_by_ref:
                setattr(result, k, v)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result
        
    def predict_type(self):
        """
        Returns the expected type of the result of the expression
        This function shall call any child expression's predict_type()
        even if the child type is not relevant to the resulting type.
        Raises exception if input types are not compatible.
        """
        raise NotImplementedError
        
    def get_min_eval_width(self):
        """
        Returns the expressions resulting integer width based on the
        self-determined expression bit-width rules
        (SystemVerilog LRM: IEEE Std 1800-2012, Table 11-21)
        """
        raise RuntimeError
        
    def get_value(self, eval_width=None):
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
class IntLiteral(Expr):
    def __init__(self, env, src_ref, val, width=64):
        super().__init__(env, src_ref)
        self.val = val
        self.width = width
    
    def predict_type(self):
        return int
        
    def get_min_eval_width(self):
        return self.width
    
    def get_value(self, eval_width=None):
        return self.val

#-------------------------------------------------------------------------------
class BuiltinEnumLiteral(Expr):
    """
    Expr wrapper for builtin RDL enumeration types:
    AccessType, OnReadType, OnWriteType, AddressingType, PrecedenceType
    """
    def __init__(self, env, src_ref, val):
        super().__init__(env, src_ref)
        self.val = val
    
    def predict_type(self):
        return type(self.val)
    
    def get_value(self, eval_width=None):
        return self.val

#-------------------------------------------------------------------------------
class EnumLiteral(Expr):
    def __init__(self, env, src_ref, val):
        super().__init__(env, src_ref)
        self.val = val
    
    def predict_type(self):
        return type(self.val)
        
    def get_min_eval_width(self):
        return 64
    
    def get_value(self, eval_width=None):
        return self.val

#-------------------------------------------------------------------------------
class StructLiteral(Expr):
    def __init__(self, env, src_ref, struct_type, values):
        super().__init__(env, src_ref)
        self.struct_type = struct_type
        # values is a dict of member_name : (member_expr, member_name_src_ref)
        self.values = values
    
    def predict_type(self):
        for member_name, (member_expr, member_name_src_ref) in self.values.items():
            member_type = member_expr.predict_type()
            if not is_castable(member_type, self.struct_type._members[member_name]):
                self.msg.fatal(
                    "Expression for member '%s' is not compatible with the expected type"
                    % member_name,
                    member_expr.src_ref
                )
            
        return self.struct_type
    
    def get_value(self, eval_width=None):
        resolved_values = OrderedDict()
        for member_name, (member_expr, member_name_src_ref) in self.values.items():
            resolved_values[member_name] = member_expr.get_value()
        
        return self.struct_type(resolved_values)

#-------------------------------------------------------------------------------
class StringLiteral(Expr):
    def __init__(self, env, src_ref, val):
        super().__init__(env, src_ref)
        self.val = val
    
    def predict_type(self):
        return str
    
    def get_value(self, eval_width=None):
        return self.val

#-------------------------------------------------------------------------------
class ArrayLiteral(Expr):
    def __init__(self, env, src_ref, elements):
        super().__init__(env, src_ref)
        self.elements = elements
    
    def predict_type(self):
        
        if len(self.elements) == 0:
            # Empty array. Element type is indeterminate
            return rdltypes.ArrayPlaceholder(None)
        
        # Get type of first element
        element_iter = iter( self.elements)
        element_type = next(element_iter).predict_type()
        
        # All remaining elements shall match
        for element in element_iter:
            if element_type != element.predict_type():
                self.msg.fatal(
                    "Elements of an array shall be the same type",
                    self.src_ref
                )
        
        return rdltypes.ArrayPlaceholder(element_type)
    
    def get_value(self, eval_width=None):
        result = []
        for element in self.elements:
            result.append(element.get_value())
        return result
    
#-------------------------------------------------------------------------------
class Concatenate(Expr):
    def __init__(self, env, src_ref, elements):
        super().__init__(env, src_ref)
        self.elements = elements
        self.type = None
    
    def predict_type(self):
        
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
            return int
        elif is_castable(element_type, str):
            self.type = str
            return str
        else:
            self.msg.fatal(
                "Concatenation operator can only be used for integral or string types",
                self.src_ref
            )
            
    def get_min_eval_width(self):
        if self.type == int:
            width = 0
            for element in self.elements:
                width = width + element.get_min_eval_width()
            
            return width
        else:
            raise RuntimeError
    
    def get_value(self, eval_width=None):
        if self.type == int:
            result = 0
            for element in self.elements:
                width = element.get_min_eval_width()
                result <<= width
                result |= int(element.get_value())
            return result
        
        elif self.type == str:
            result = ""
            for element in self.elements:
                result += element.get_value()
            return result
        
        else:
            raise RuntimeError

#-------------------------------------------------------------------------------
class Replicate(Expr):
    def __init__(self, env, src_ref, reps, concat):
        super().__init__(env, src_ref)
        self.reps = reps
        self.concat = concat
        self.type = None
        self.reps_value = None
    
    def predict_type(self):
        
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
            # Type check for invalid type is already halded there
            raise RuntimeError
    
    def get_min_eval_width(self):
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
    
    def get_value(self, eval_width=None):
        # Evaluate number of repetitions
        if self.reps_value is None:
            self.reps_value = self.reps.get_value()
        
        if self.type == int:
            width = self.concat.get_min_eval_width()
            val = int(self.concat.get_value())
            
            result = 0
            for i in range(self.reps_value):
                result <<= width
                result |= val
            
            return result
        
        elif self.type == str:
            result = self.concat.get_value()
            result *= self.reps_value
            return result
        
        else:
            raise RuntimeError
    
#-------------------------------------------------------------------------------
# Integer binary operators:
#   +  -  *  /  %  &  |  ^  ^~  ~^
# Normal expression context rules
class _BinaryIntExpr(Expr):
    def __init__(self, env, src_ref, l, r):
        super().__init__(env, src_ref)
        self.l = l
        self.r = r
        
    def predict_type(self):
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
    
    def get_min_eval_width(self):
        return(max(
            self.l.get_min_eval_width(),
            self.r.get_min_eval_width()
        ))
        
class Add(_BinaryIntExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l + r, eval_width)

class Sub(_BinaryIntExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l - r, eval_width)

class Mult(_BinaryIntExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l * r, eval_width)

class Div(_BinaryIntExpr):
    def get_value(self, eval_width=None):
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
    def get_value(self, eval_width=None):
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
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l & r, eval_width)
        
class BitwiseOr(_BinaryIntExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l | r, eval_width)
        
class BitwiseXor(_BinaryIntExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value(eval_width))
        return truncate_int(l ^ r, eval_width)

class BitwiseXnor(_BinaryIntExpr):
    def get_value(self, eval_width=None):
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
    def __init__(self, env, src_ref, n):
        super().__init__(env, src_ref)
        self.n = n
        
    def predict_type(self):
        op_type = self.n.predict_type()
        if not is_castable(op_type, int):
            self.msg.fatal(
                "Operand of expression is not a compatible numeric type",
                self.src_ref
            )
        return int
    
    def get_min_eval_width(self):
        return self.n.get_min_eval_width()
        
class UnaryPlus(_UnaryIntExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        return truncate_int(n, eval_width)

class UnaryMinus(_UnaryIntExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        return truncate_int(-n, eval_width)

class BitwiseInvert(_UnaryIntExpr):
    def get_value(self, eval_width=None):
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
    def __init__(self, env, src_ref, l, r):
        super().__init__(env, src_ref)
        self.l = l
        self.r = r
        self.is_numeric = None
        
    def predict_type(self):
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
    
    def get_min_eval_width(self):
        return 1
        
    def get_ops(self):
        
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
        
        return l,r

class _NumericRelationalExpr(_RelationalExpr):
    
    def predict_type(self):
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
    def get_value(self, eval_width=None):
        l,r = self.get_ops()
        return l == r

class Neq(_RelationalExpr):
    def get_value(self, eval_width=None):
        l,r = self.get_ops()
        return l != r

class Lt(_NumericRelationalExpr):
    def get_value(self, eval_width=None):
        l,r = self.get_ops()
        return l < r
        
class Gt(_NumericRelationalExpr):
    def get_value(self, eval_width=None):
        l,r = self.get_ops()
        return l > r

class Leq(_NumericRelationalExpr):
    def get_value(self, eval_width=None):
        l,r = self.get_ops()
        return l <= r

class Geq(_NumericRelationalExpr):
    def get_value(self, eval_width=None):
        l,r = self.get_ops()
        return l >= r

#-------------------------------------------------------------------------------
# Reduction operators:
#   &  ~&  |  ~|  ^  ^~  !
# Result is always 1 bit bool
# Creates a new evaluation context
class _ReductionExpr(Expr):
    def __init__(self, env, src_ref, n):
        super().__init__(env, src_ref)
        self.n = n
    
    def predict_type(self):
        op_type = self.n.predict_type()
        if not is_castable(op_type, int):
            self.msg.fatal(
                "Operand of expression is not a compatible numeric type",
                self.src_ref
            )
        return int
    
    def get_min_eval_width(self):
        return 1
    
class AndReduce(_ReductionExpr):
    def get_value(self, eval_width=None):
        eval_width = self.n.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        n = truncate_int(~n, eval_width)
        return int(n == 0)
        
class NandReduce(_ReductionExpr):
    def get_value(self, eval_width=None):
        eval_width = self.n.get_min_eval_width()
        n = int(self.n.get_value(eval_width))
        n = truncate_int(~n, eval_width)
        return int(n != 0)
        
class OrReduce(_ReductionExpr):
    def get_value(self, eval_width=None):
        n = int(self.n.get_value())
        return int(n != 0)
        
class NorReduce(_ReductionExpr):
    def get_value(self, eval_width=None):
        n = int(self.n.get_value())
        return int(n == 0)

class XorReduce(_ReductionExpr):
    def get_value(self, eval_width=None):
        n = int(self.n.get_value())
        v = 0
        while n:
            if n & 1:
                v ^= 1
            n >>= 1
        return v

class XnorReduce(_ReductionExpr):
    def get_value(self, eval_width=None):
        n = int(self.n.get_value())
        v = 1
        while n:
            if n & 1:
                v ^= 1
            n >>= 1
        return v
        
class BoolNot(_ReductionExpr):
    def get_value(self, eval_width=None):
        n = int(self.n.get_value())
        return not n
    
    def predict_type(self):
        super().predict_type()
        return bool

#-------------------------------------------------------------------------------
# Logical boolean operators:
#   && ||
# Both operands are self-determined
class _BoolExpr(Expr):
    def __init__(self, env, src_ref, l, r):
        super().__init__(env, src_ref)
        self.l = l
        self.r = r
    
    def predict_type(self):
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
    
    def get_min_eval_width(self):
        return 1
    
class BoolAnd(_BoolExpr):
    def get_value(self, eval_width=None):
        l = bool(self.l.get_value())
        r = bool(self.r.get_value())
        return l and r
        
class BoolOr(_BoolExpr):
    def get_value(self, eval_width=None):
        l = bool(self.l.get_value())
        r = bool(self.r.get_value())
        return l or r
        
#-------------------------------------------------------------------------------
# Exponent & shift operators:
#   **  <<  >>
# Righthand operand is self-determined
class _ExpShiftExpr(Expr):
    def __init__(self, env, src_ref, l, r):
        super().__init__(env, src_ref)
        self.l = l
        self.r = r
    
    def predict_type(self):
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
    
    def get_min_eval_width(self):
        # Righthand op has no influence in evaluation context
        return self.l.get_min_eval_width()
    
class Exponent(_ExpShiftExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.l.get_min_eval_width()
        # Right operand is self-determined
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value())
        return truncate_int(int(l ** r), eval_width)

class LShift(_ExpShiftExpr):
    def get_value(self, eval_width=None):
        if eval_width is None:
            eval_width = self.l.get_min_eval_width()
        # Right operand is self-determined
        l = int(self.l.get_value(eval_width))
        r = int(self.r.get_value())
        return truncate_int(l << r, eval_width)

class RShift(_ExpShiftExpr):
    def get_value(self, eval_width=None):
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
    def __init__(self, env, src_ref, i, j, k):
        super().__init__(env, src_ref)
        self.i = i
        self.j = j
        self.k = k
        self.is_numeric = None
        
    def predict_type(self):
        t_i = self.i.predict_type()
        if not is_castable(t_i, bool):
            self.msg.fatal(
                "Conditional operand of expression is not a compatible boolean type",
                self.src_ref
            )
        
        # Type of j and k shall be compatible
        t_j = self.j.predict_type()
        t_k = self.k.predict_type()
        
        if is_castable(t_j, int) and is_castable(t_k, int):
            self.is_numeric = True
            return int
        elif t_j == t_k:
            # Same types. Inherently compatible
            self.is_numeric = False
            return t_j
        else:
            # Incompatible
            self.msg.fatal(
                "True/False results of ternary conditional are not compatible types",
                self.src_ref
            )
    
    def get_min_eval_width(self):
        # Truth operand has no influence in evaluation context
        return(max(
            self.j.get_min_eval_width(),
            self.k.get_min_eval_width()
        ))
    
    def get_value(self, eval_width=None):
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
    def __init__(self, env, src_ref, v, w_expr=None, w_int=64):
        super().__init__(env, src_ref)
        
        if w_expr is not None:
            self.v = v
            self.w_expr = w_expr
            self.cast_width = None
        else:
            self.v = v
            self.w_expr = None
            self.cast_width = w_int
        
    def predict_type(self):
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
    
    def get_min_eval_width(self):
        if self.cast_width is None:
            self.cast_width = int(self.w_expr.get_value())
        return self.cast_width
        
    
    def get_value(self, eval_width=None):
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
    def __init__(self, env, src_ref, n):
        super().__init__(env, src_ref)
        self.n = n
    
    def predict_type(self):
        if not is_castable(self.n.predict_type(), bool):
            self.msg.fatal(
                "Value operand of cast expression cannot be cast to a boolean",
                self.src_ref
            )
        return bool
    
    def get_min_eval_width(self):
        return 1
        
    def get_value(self, eval_width=None):
        n = int(self.n.get_value())
        return n != 0

#-------------------------------------------------------------------------------
# References

class ParameterRef(Expr):
    def __init__(self, env, src_ref, param):
        super().__init__(env, src_ref)
        self.param = param
    
    def predict_type(self):
        return self.param.param_type
    
    def get_min_eval_width(self):
        if self.param.expr is None:
            self.msg.fatal(
                "Value for parameter '%s' was never assigned" % self.param.name,
                self.src_ref
            )
        return self.param.expr.get_min_eval_width()
    
    def get_value(self, eval_width=None):
        if self.param.expr is None:
            self.msg.fatal(
                "Value for parameter '%s' was never assigned" % self.param.name,
                self.src_ref
            )
        return self.param.expr.get_value(eval_width)


class ArrayIndex(Expr):
    def __init__(self, env, src_ref, array, index):
        super().__init__(env, src_ref)
        self.array = array
        self.index = index
        
    def predict_type(self):
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
        
        return array_type.element_type
    
    def get_min_eval_width(self):
        # TODO: Need to actually reach in and get eval width of array element
        return 64
    
    def get_value(self, eval_width=None):
        index = self.index.get_value()
        array = self.array.get_value()
        if index >= len(array):
            self.msg.fatal(
                "Array index '%d' is out of range" % index,
                self.src_ref
            )
        return array[index]
    

class MemberRef(Expr):
    def __init__(self, env, src_ref, struct, member_name):
        super().__init__(env, src_ref)
        self.struct = struct
        self.member_name = member_name
        
    def predict_type(self):
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
    
    def get_min_eval_width(self):
        # TODO: Need to actually reach in and get eval width of struct member
        return 64
    
    def get_value(self, eval_width=None):
        struct = self.struct.get_value()
        return struct._values[self.member_name]


class InstRef(Expr):
    def __init__(self, env, ref_root, ref_elements):
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
        #   ( str , [ <Index Expr> , ... ] , SourceRef),
        #   ( str , [ <Index Expr> , ... ] , SourceRef)
        # ]
        self.ref_elements = ref_elements
    
    def __deepcopy__(self, memo):
        """
        Copy any SourceRef by ref within the ref_elements list when deepcopying
        """
        copy_by_ref = ["src_ref", "env", "msg", "ref_root"]
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
    
    def predict_type(self):
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
                # is an array
                if len(array_suffixes) != len(current_comp.array_dimensions):
                    self.msg.fatal(
                        "Incompatible number of index dimensions after '%s'. Expected %d, found %d."
                        % (name, len(current_comp.array_dimensions), len(array_suffixes)),
                        name_src_ref
                    )
            elif len(array_suffixes):
                # Has array suffixes. Check if compatible with referenced component
                self.msg.fatal(
                    "Unable to index non-array component '%s'" % name,
                    name_src_ref
                )
        
        return type(current_comp)
        
    def get_value(self, eval_width=None):
        """
        Build a resolved ComponentRef container that describes the relative path
        """
        
        resolved_ref_elements = []
        
        for name, array_suffixes, name_src_ref in self.ref_elements:
            idx_list = [ suffix.get_value() for suffix in array_suffixes ]
            resolved_ref_elements.append((name, idx_list, name_src_ref))
        
        # Create container
        cref = rdltypes.ComponentRef(self.ref_root, resolved_ref_elements)
        
        return cref
    
    
class PropRef(Expr):
    def __init__(self, env, src_ref, inst_ref, prop_ref_type):
        super().__init__(env, src_ref)
        # InstRef to the component whose property is being referenced
        self.inst_ref = inst_ref
        
        # PropertyReference class
        self.prop_ref_type = prop_ref_type
    
    def predict_type(self):
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
    
    def get_value(self, eval_width=None):
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
    def __init__(self, env, src_ref, v, dest_type):
        super().__init__(env, src_ref)
        
        self.v = v
        self.dest_type = dest_type
    
    def predict_type(self):
        op_type = self.v.predict_type()
        
        if not is_castable(op_type, self.dest_type):
            self.msg.fatal(
                "Result of expression is not compatible with the expected type",
                self.src_ref
            )
        
        return self.dest_type
    
    def get_min_eval_width(self):
        return self.v.get_min_eval_width()
    
    def get_value(self, eval_width=None):
        v = self.v.get_value()
        
        if self.dest_type == bool:
            return bool(v)
        elif self.dest_type == int:
            return int(v)
        else:
            return v


#===============================================================================

def is_castable(src, dst):
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
