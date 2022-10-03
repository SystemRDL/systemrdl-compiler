from typing import TYPE_CHECKING, Any, Set, Type
import re

from . import component as comp

if TYPE_CHECKING:
    from .compiler import RDLEnvironment
    from .node import Node
    from .messages import MessageHandler

class UDPDefinition:
    """
    UDP definition descriptor class.
    """

    #: UDP definition name
    name = ""

    #: Set of :class:`~systemrdl.component.Component` types the UDP can be bound to.
    #: By default, the UDP can be bound to all components.
    valid_components = {
        comp.Field,
        comp.Reg,
        comp.Regfile,
        comp.Addrmap,
        comp.Mem,
        comp.Signal,
        # TODO: constraint,
    } # type: Set[Type[comp.Component]]

    #: Data type of the assignment value that this UDP will enforce.
    #: If this is a reference, either specify the specific component type class
    #: (eg. :class:`~systemrdl.component.Field`), or the generic representation
    #: of all references: :class:`~systemrdl.rdltypes.references.RefType`
    valid_type = None # type: Any

    #: Specifies the value assigned if a value is not specified when the UDP is bound to a component.
    #: Value must be compatible with ``valid_type``
    default_assignment = None # type: Any

    #: If set to True, enables a validation check that enforces that the
    #: assigned value of the property shall not have a value of 1 for any
    #: bit beyond the width of the field.
    #: This can only be used if ``valid_type`` is ``int``
    constr_componentwidth = False

    def __init__(self, env: 'RDLEnvironment') -> None:
        self.env = env

        # validate a few things
        if not re.fullmatch(r"[a-z_]\w*", self.name, re.IGNORECASE):
            raise ValueError("Invalid UDP name '%s'" % self.name)
        if not isinstance(self.valid_components, set):
            raise TypeError("UDP %s's 'valid_components' property shall be a set" % self.name)
        if self.valid_type is None:
            raise ValueError("UDP %s's 'valid_type' property was not defined" % self.name)
        if self.constr_componentwidth and self.valid_type != int:
            raise ValueError("'constr_componentwidth' can only be true if UDP is of integer type")

    @property
    def msg(self) -> 'MessageHandler':
        return self.env.msg

    def validate(self, node: 'Node', value: Any) -> None:
        """
        Optional user-defined validation function.

        This function is called after design elaboration on every assignment
        of the user defined property. This provides a mechanism to further
        validate the value assigend to your user-defined property.
        """

    def get_unassigned_default(self, node: 'Node') -> Any:
        """
        According to the SystemRDL spec, if a user-defined property is not explicitly
        assigned, then it does not get bound with any implied default value.

        For convenience to developers, this callback allows you to specify an implied
        default value if the UDP was never explicitly assigned.
        This only affects the behavior of Node.get_property() and does not
        affect the semantics of SystemRDL during compilaton.
        """

        # If a user-defined property is not explicitly assigned, then it
        # does not get bound with its default value
        return None
