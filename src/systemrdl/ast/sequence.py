from typing import TYPE_CHECKING, Optional, Type, List, Union

from .ast_node import ASTNode
from .conditional import is_castable

if TYPE_CHECKING:
    from ..compiler import RDLEnvironment
    from ..source_ref import SourceRefBase

    OptionalSourceRef = Optional[SourceRefBase]

class Concatenate(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', elements: List[ASTNode]):
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


class Replicate(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', reps: ASTNode, concat: ASTNode):
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
