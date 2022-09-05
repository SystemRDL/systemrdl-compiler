from typing import TYPE_CHECKING, Optional, Any

from .ast_node import ASTNode

from .cast import is_castable

if TYPE_CHECKING:
    from ..compiler import RDLEnvironment
    from ..source_ref import SourceRefBase
    from rdltypes.typing import PreElabRDLType

    OptionalSourceRef = Optional[SourceRefBase]

# conditional operator
#   i ? j : k
# Truth expression is self-determined and does not contribute to context

class Conditional(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', i: ASTNode, j: ASTNode, k: ASTNode):
        super().__init__(env, src_ref)
        self.i = i
        self.j = j
        self.k = k
        self.is_numeric = None # type: bool

    def predict_type(self) -> 'PreElabRDLType':
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
