from typing import TYPE_CHECKING, Optional, Any, List, Tuple, Dict, Type
from copy import deepcopy

from .. import rdltypes
from .. import component as comp

from .ast_node import ASTNode
from .conditional import is_castable

if TYPE_CHECKING:
    from ..compiler import RDLEnvironment
    from ..core.parameter import Parameter
    from ..source_ref import SourceRefBase
    from rdltypes.typing import PreElabRDLType, RDLValue

    OptionalSourceRef = Optional[SourceRefBase]

class ParameterRef(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', param: 'Parameter'):
        super().__init__(env, src_ref)
        self.param = param

    def predict_type(self) -> 'PreElabRDLType':
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


class ArrayIndex(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', array: ASTNode, index: ASTNode):
        super().__init__(env, src_ref)
        self.array = array
        self.index = index

    def predict_type(self) -> 'PreElabRDLType':
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


class MemberRef(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', struct: ASTNode, member_name: str):
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
    Tuple[str, List[ASTNode], 'OptionalSourceRef']
]
class InstRef(ASTNode):
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
        #   ( str , [ <Index ASTNode> , ... ] , SourceRefBase),
        #   ( str , [ <Index ASTNode> , ... ] , SourceRefBase)
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


class PropRef(ASTNode):
    def __init__(self, env: 'RDLEnvironment', src_ref: 'OptionalSourceRef', inst_ref: ASTNode, prop_ref_type: Type[rdltypes.PropertyReference]):
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
