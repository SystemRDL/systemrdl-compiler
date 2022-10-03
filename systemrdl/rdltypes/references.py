from typing import Tuple, List, Optional, Type, TYPE_CHECKING

from ..node import Node, AddressableNode
from .. import component as comp

if TYPE_CHECKING:
    from ..source_ref import SourceRefBase
    from ..compiler import RDLEnvironment


RefElement = Tuple[str, List[int], Optional['SourceRefBase']]

class ComponentRef:
    """
    Container for hierarchical component instance references.
    This is used internally to store information about the reference
    When a user requests the reference value, it is resolved into a Node object
    """

    def __init__(self, ref_root: 'comp.Component', ref_elements: List[RefElement]):
        # Handle to the component definition where ref_elements is relative to
        # This is the original_def, and NOT the actual instance
        self.ref_root = ref_root

        # List of hierarchical reference element tuples that make up the path
        # to the reference.
        # Path is relative to the instance of ref_root
        # Each tuple in the list represents a segment of the path:
        # [
        #   ( <ID string> , [ <Index int> , ... ], SourceRefBase ),
        # ]
        self.ref_elements = ref_elements

    def build_node_ref(self, assignee_node: Node, env: 'RDLEnvironment') -> Node:
        """
        Resolves the component reference into a Node object
        """
        current_node = assignee_node
        # Traverse up from assignee until ref_root is reached
        while True:
            if current_node is None:
                raise RuntimeError("Upwards traverse to ref_root failed")
            if current_node.inst.original_def is self.ref_root:
                break
            current_node = current_node.parent

        for inst_name, idx_list, name_src_ref in self.ref_elements:
            # find instance
            current_node = current_node.get_child_by_name(inst_name)


            # Check if indexes are valid
            if idx_list:
                # Reference contains one or more suffixes
                # Validation during compilation would have already enforced that
                # references are sane.
                # Safe to expect this to be an AddressableNode
                assert isinstance(current_node, AddressableNode)

                for i, idx in enumerate(idx_list):
                    if idx >= current_node.array_dimensions[i]:
                        env.msg.fatal(
                            "Array index out of range. Expected 0-%d, got %d."
                            % (current_node.array_dimensions[i]-1, idx),
                            name_src_ref
                        )

                # Assign indexes if appropriate
                if current_node.is_array:
                    current_node.current_idx = idx_list

        return current_node


class PropertyReference:
    """
    Base class for all property references used in RHS of an expression.

    The PropertyReference object represents the expression's reference target.
    Details of the reference can be determined using its ``node`` and ``name``
    variables.

    For example, the following property assignment:

    .. code-block:: systemrdl

        reg {
            ...
            fieldX->next = fieldY->intr;
        } my_reg;

    ... can be queried as follows:

    .. code-block:: python

        fieldX = my_reg.get_child_by_name("fieldX")
        fieldY = my_reg.get_child_by_name("fieldY")

        next_prop = fieldX.get_property('next')
        print(next_prop.node == fieldY) # prints: True
        print(next_prop.name) # prints: "intr"

    """
    allowed_inst_type = None # type: Type[comp.Component]

    def __init__(self, src_ref: 'SourceRefBase', env: 'RDLEnvironment', comp_ref: ComponentRef):
        self.env = env
        self.src_ref = src_ref
        self._comp_ref = comp_ref

        #: Node object that represents the component instance from which the
        #: property is being referenced.
        self.node = None # type: Node

    def __repr__(self) -> str:
        return "<%s %s->%s at 0x%x>" % (
            self.__class__.__qualname__,
            self.node.get_path(),
            self.name,
            id(self)
        )

    def __eq__(self, other: object) -> bool:
        """
        Property reference equality checks determine whether the other object
        represents the same reference (node represents the same position in the
        register model's hierarchy and the property referenced is the same)
        """
        if not isinstance(other, PropertyReference):
            return NotImplemented
        if self.name != other.name:
            return False
        return self.node.get_path() == other.node.get_path()

    @property
    def name(self) -> str:
        """
        Name of the property being referenced
        """
        return self.get_name()

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__.replace("PropRef_", "")

    def _resolve_node(self, assignee_node: Node) -> None:
        self.node = self._comp_ref.build_node_ref(assignee_node, self.env)

    def _validate(self) -> None:
        pass

    @property
    def width(self) -> Optional[int]:
        """
        Get the equivalent width of the property reference.

        Returns None if reference doesn't have a specifically defined width

        .. versionadded:: 1.21
        """
        raise NotImplementedError


class RefType:
    """
    This class it not a true RDL type, but rather an object that represents
    all possible RHS references that can be made. This represents all possible
    component references, as well as RHS property references.

    This is used primarily when pre-registering a UDP that has the generic
    'ref' datatype.

    .. versionadded:: 1.25
    """

    expanded = (
        comp.Field,
        comp.Signal,
        comp.Reg,
        comp.Regfile,
        comp.Addrmap,
        comp.Mem,
        PropertyReference,
        # TODO: eventually add constraint references
    )
