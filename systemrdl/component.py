import operator
import functools
from copy import deepcopy
from collections import OrderedDict

class Component:
    """
    Base class for all component types

    .. inheritance-diagram:: systemrdl.component
        :top-classes: ~Component
    """

    def __init__(self):
        #------------------------------
        # Component definition
        #------------------------------

        #: Reference to parent :class:`~systemrdl.component.Component`
        #: definition that lexically encloses this component type definition.
        #:
        #: May remain ``None`` if scope is not known or not applicable.
        #:
        #: .. note::
        #:      This represents the parent *lexical* scope! This does *not*
        #:      refer to the hierarchical parent of this component.
        self.parent_scope = None

        # Name of this component's declaration scope
        # This field is only valid in non-instantiated components (referenced
        # via an instance's original_def)
        # If declaration was anonymous, inherits the first instance's name,
        # otherwise it contains the original type name.
        self._scope_name = None

        #: Named definition identifier.
        #: If declaration was anonymous, instantiation type names inherit
        #: the first instance's name.
        #: The type name of parameterized components is normalized based on the
        #: instance's parameter values.
        #:
        #: If this is a non-instantiated component (referenced via an
        #: instance's original_def), then it will contain either the original
        #: type name, or None if the declaration was anonymous.
        #:
        #: Importers may leave this as ``None`` if an appropriate type name
        #: cannot be imported.
        self.type_name = None

        #: List of :class:`~systemrdl.component.Component` instances that are
        #: direct descendants of this component.
        #:
        #: Child components are sorted as follows:
        #:
        #: - Signals first
        #: - All other components follow.
        #: - AddressableComponents are sorted by ascending base_addr
        #: - Fields are sorted by ascending low bit
        self.children = []

        # Parameters of this component definition.
        # These are listed in the order that they were defined
        self.parameters = []

        # Properties applied to this component
        self.properties = {}

        # SourceRef for the component definition
        self.def_src_ref = None

        #------------------------------
        # Component instantiation
        #------------------------------
        #: If instantiated, set to True
        self.is_instance = False

        #: Name of instantiated element
        self.inst_name = None

        #: Reference to original :class:`~systemrdl.component.Component`
        #: definition this instance is derived from.
        #:
        #: Importers may leave this as ``None`` if appropriate.
        self.original_def = None

        #: True if instance type is external. False if internal.
        self.external = None

        # SourceRef for the component instantiation.
        self.inst_src_ref = None

        #------------------------------
        # List of property names that were assigned via a dynamic property
        # assignment.
        self._dyn_assigned_props = []

        # List of child instances that were assigned "through" this component,
        # from outside this component's scope.
        self._dyn_assigned_children = []

    def __deepcopy__(self, memo):
        """
        Deepcopy all members except for ones that should be copied by reference
        """
        copy_by_ref = ["original_def", "def_src_ref", "inst_src_ref", "parent_scope"]
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k in copy_by_ref:
                setattr(result, k, v)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def __repr__(self):
        if self.is_instance:
            name_str = "%s (%s)" % (self.inst_name, self.type_name)
        else:
            name_str = self.type_name

        return "<%s %s at 0x%x>" % (
            self.__class__.__qualname__,
            name_str,
            id(self)
        )


    def get_child_by_name(self, inst_name):
        for child in self.children:
            if child.inst_name == inst_name:
                return child
        return None


    def get_scope_path(self, scope_separator="::"):
        """
        Generate a string that represents this component's declaration namespace
        scope.

        Parameters
        ----------
        scope_separator: str
            Override the separator between namespace scopes
        """
        if self.parent_scope is None:
            # Importer likely never set the scope
            return ""
        elif isinstance(self.parent_scope, Root):
            # Declaration was in root scope
            return ""
        else:
            # Get parent definition's scope path
            parent_path = self.parent_scope.get_scope_path(scope_separator)

            # Extend it with its scope name
            if parent_path:
                return(
                    parent_path
                    + scope_separator
                    + self.parent_scope._scope_name
                )
            else:
                return self.parent_scope._scope_name


class AddressableComponent(Component):
    """
    Base class for all components that can have an address
    """

    def __init__(self):
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        #: Address offset from the parent component.
        #: If left as None, compiler will resolve with inferred value.
        self.addr_offset = None

        #: Address alignment if explicitly assigned by user.
        self.addr_align = None

        #------------------------------
        # Array Properties
        #------------------------------
        #: If true, then ``array_dimensions`` and ``array_stride`` are valid.
        self.is_array = False

        #: List of sizes for each array dimension.
        #: Last item in the list iterates the most frequently.
        self.array_dimensions = None

        #: Address offset between array elements.
        #: If left as None, compiler will resolve with inferred value.
        self.array_stride = None


    @property
    def n_elements(self):
        """
        Total number of array elements.
        If array is multidimensional, array is flattened.
        Returns 1 if not an array.
        """
        if self.is_array:
            return functools.reduce(operator.mul, self.array_dimensions)
        else:
            return 1

class VectorComponent(Component):
    """
    Base class for all components that are vector-like
    """

    def __init__(self):
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        #: Width of vector in bits
        self.width = None

        #: Bit position of most significant bit
        self.msb = None
        #: Bit position of least significant bit
        self.lsb = None

        #: High index of bit range
        self.high = None
        #: Low index of bit range
        self.low = None

#===============================================================================
class Root(Component):
    """
    Meta-component used by compiler to represent the root scope
    """
    def __init__(self):
        super().__init__()
        #: List of :class:`~systemrdl.component.Component` definitions in the
        #: global root scope.
        self.comp_defs = OrderedDict()

class Signal(VectorComponent):
    pass

class Field(VectorComponent):
    pass

class Reg(AddressableComponent):
    def __init__(self):
        super().__init__()

        #: If true, fields are to be arranged in msb0 order
        #:
        #: .. versionadded:: 1.7
        self.is_msb0_order = False
        #------------------------------
        # Alias Register
        #------------------------------
        #: If true, then ``alias_primary_inst`` is valid
        self.is_alias = False

        #: Reference to primary register :class:`~systemrdl.component.Component`
        #: instance
        self.alias_primary_inst = None

class Regfile(AddressableComponent):
    pass

class Addrmap(AddressableComponent):
    pass

class Mem(AddressableComponent):
    pass
