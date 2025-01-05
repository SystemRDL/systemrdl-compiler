import operator
import functools
from copy import deepcopy
from collections import OrderedDict
from typing import Optional, List, Dict, TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from typing import TypeVar
    from .core.parameter import Parameter
    from .source_ref import SourceRefBase
    from .ast import ASTNode

    ComponentClass = TypeVar('ComponentClass', bound='Component')

class Component:
    """
    Base class for all component types

    .. inheritance-diagram:: systemrdl.component
        :top-classes: ~Component
    """

    def __init__(self) -> None:
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
        self.parent_scope: Optional[Component] = None

        # Name of this component's declaration scope
        # This field is only valid in non-instantiated components (referenced
        # via an instance's original_def, or a component's parent_scope)
        # If declaration was anonymous, inherits the first instance's name,
        # otherwise it contains the original type name.
        self._scope_name: Optional[str] = None

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
        self.type_name: Optional[str] = None

        #: List of :class:`~systemrdl.component.Component` instances that are
        #: direct descendants of this component.
        #:
        #: Child components are sorted as follows:
        #:
        #: - Signals first
        #: - All other components follow.
        #: - AddressableComponents are sorted by ascending base_addr
        #: - Fields are sorted by ascending low bit
        self.children: List[Component] = []

        # Parameters of this component definition.
        # These are listed in the order that they were defined
        self.parameters: List[Parameter] = []

        # Properties applied to this component
        self.properties: Dict[str, Any] = {}

        #: :ref:`api_src_ref` for each explicit property assignment (if available)
        self.property_src_ref: Dict[str, SourceRefBase] = {}

        #: :ref:`api_src_ref` for the component definition
        self.def_src_ref: Optional[SourceRefBase] = None

        #------------------------------
        # Component instantiation
        #------------------------------
        #: If instantiated, set to True
        self.is_instance: bool = False

        #: Name of instantiated element
        self.inst_name: Optional[str] = None

        #: Reference to original :class:`~systemrdl.component.Component`
        #: definition this instance is derived from.
        #:
        #: Importers may leave this as ``None`` if appropriate.
        self.original_def: Optional[Component] = None

        #: True if instance type is external. False if internal.
        self.external: Optional[bool] = None

        #: :ref:`api_src_ref` for the component instantiation.
        self.inst_src_ref: Optional[SourceRefBase] = None

        #------------------------------
        # List of property names that were assigned via a dynamic property
        # assignment.
        self._dyn_assigned_props: List[str] = []

        # List of child instances that were assigned "through" this component,
        # from outside this component's scope.
        self._dyn_assigned_children: List[str] = []


    def _copy_for_inst(self: 'ComponentClass', memo: Dict[int, Any]) -> 'ComponentClass':
        """
        Make a copy of the component tree in order to instantiate it.

        This is subtly different from a normal deepcopy since it ensures that
        references within the component tree are deepcopied, while references
        to external parameters are copied by reference.
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        # First, explicitly copy all parameter objects
        result.parameters = [param._copy_for_inst(memo) for param in self.parameters]

        # Ensure child components get copied first
        result.children = [child._copy_for_inst(memo) for child in self.children]

        # Finally, continue deepcopying everything else
        copy_by_ref = {"original_def", "parent_scope", "comp_defs"}
        skip = {"parameters", "children"}
        for k, v in self.__dict__.items():
            if k in skip:
                continue
            if k in copy_by_ref:
                setattr(result, k, v)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def __deepcopy__(self: 'ComponentClass', memo: Dict[int, Any]) -> 'ComponentClass':
        return self._copy_for_inst(memo)

    def __repr__(self) -> str:
        if self.is_instance:
            name_str = f"{self.inst_name} ({self.type_name})"
        else:
            name_str = str(self.type_name)

        return f"<{self.__class__.__qualname__} {name_str} at {id(self):#x}>"


    def get_child_by_name(self, inst_name: str) -> Optional['Component']:
        for child in self.children:
            if child.inst_name == inst_name:
                return child
        return None


    def get_scope_path(self, scope_separator: str="::") -> Optional[str]:
        """
        Generate a string that represents this component's declaration namespace
        scope.

        Returns ``None`` if scope is not known or not applicable.

        For example, the following SystemRDL snippet:

        .. code-block:: systemrdl

            reg my_reg_t {
                field {} x;
            };

            addrmap top {
                my_reg_t foo;
                reg my_other_reg_t {
                    field {} y;
                } bar;
                reg {
                    field {} z;
                } baz, xyz;
            };

        ... results in:

        * Field ``x`` of hierarchical path ``top.foo.x`` was declared in the
          lexical scope ``my_reg_t``
        * Field ``y`` of hierarchical path ``top.bar.y`` was declared in the
          lexical scope ``top::my_other_reg_t``
        * Both fields ``z`` of hierarchical paths ``top.baz.z`` and ``top.xyz.z``
          were declared in the same lexical scope ``top::baz``
        * Register ``foo`` was declared in the root scope which is represented
          by an empty string.

        Parameters
        ----------
        scope_separator: str
            Override the separator between namespace scopes
        """
        if self.parent_scope is None:
            # Importer likely never set the scope
            return None
        elif isinstance(self.parent_scope, Root):
            # Declaration was in root scope
            return ""
        else:
            # Get parent definition's scope path
            parent_path = self.parent_scope.get_scope_path(scope_separator)

            # Extend it with its scope name
            if parent_path:
                # If parent scope exists, then its scope name is also guaranteed to
                # exist
                assert self.parent_scope._scope_name is not None

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
    original_def: Optional['AddressableComponent']

    def __init__(self) -> None:
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        #: Address offset from the parent component.
        #: If left as None, compiler will resolve with inferred value during
        #: elaboration
        self.addr_offset: Optional[int] = None

        #: Address alignment if explicitly assigned by user.
        self.addr_align: Optional[int] = None

        #------------------------------
        # Array Properties
        #------------------------------
        #: If true, then ``array_dimensions`` and ``array_stride`` are valid.
        self.is_array: bool = False

        #: List of sizes for each array dimension.
        #: Last item in the list iterates the most frequently.
        self.array_dimensions: Optional[List[int]] = None

        #: Address offset between array elements.
        #: If left as None, compiler will resolve with inferred value.
        self.array_stride: Optional[int] = None


    @property
    def n_elements(self) -> int:
        """
        Total number of array elements.
        If array is multidimensional, array is flattened.
        Returns 1 if not an array.
        """
        if self.array_dimensions:
            return functools.reduce(operator.mul, self.array_dimensions)
        else:
            return 1

class AddressableComponent_PreExprElab(AddressableComponent):
    """
    Alternately typed representation for type hinting prior to expression
    elaboration
    """
    addr_offset: Optional[Union[int, 'ASTNode']] # type: ignore
    addr_align: Optional[Union[int, 'ASTNode']] # type: ignore
    array_stride: Optional[Union[int, 'ASTNode']] # type: ignore


class VectorComponent(Component):
    """
    Base class for all components that are vector-like
    """
    original_def: Optional['VectorComponent']

    def __init__(self) -> None:
        super().__init__()
        #------------------------------
        # Component instantiation
        #------------------------------
        # Note: All of these are guaranteed to be resolved after elaboration to
        # not be None. For this reason, type-hints are specified to represent the
        # post-elaboration user-facing state.

        #: Width of vector in bits
        self.width: int = None # type: ignore

        #: Bit position of most significant bit
        self.msb: int = None # type: ignore
        #: Bit position of least significant bit
        self.lsb: int = None # type: ignore

        #: High index of bit range
        self.high: int = None # type: ignore
        #: Low index of bit range
        self.low: int = None # type: ignore


class VectorComponent_PreExprElab(VectorComponent):
    """
    Alternately typed representation for type hinting prior to expression
    elaboration
    """
    width: Optional[Union[int, 'ASTNode']] # type: ignore
    msb: Optional[Union[int, 'ASTNode']] # type: ignore
    lsb: Optional[Union[int, 'ASTNode']] # type: ignore

#===============================================================================
class Root(Component):
    """
    Meta-component used by compiler to represent the root scope
    """
    def __init__(self) -> None:
        super().__init__()
        #: Dictionary of :class:`~systemrdl.component.Component` definitions in
        #: the global root scope.
        self.comp_defs: Dict[str, Component] = OrderedDict()

class Signal(VectorComponent):
    original_def: Optional['Signal']

class Signal_PreStructuralElab(Signal):
    """
    Alternately typed representation for type hinting prior to structural placement
    elaboration
    """
    width: Optional[int] # type: ignore
    msb: Optional[int] # type: ignore
    lsb: Optional[int] # type: ignore
    high: Optional[int] # type: ignore
    low: Optional[int] # type: ignore

class Field(VectorComponent):
    original_def: Optional['Field']

class Field_PreStructuralElab(Field):
    """
    Alternately typed representation for type hinting prior to structural placement
    elaboration
    """
    width: Optional[int] # type: ignore
    msb: Optional[int] # type: ignore
    lsb: Optional[int] # type: ignore
    high: Optional[int] # type: ignore
    low: Optional[int] # type: ignore

class Reg(AddressableComponent):
    original_def: Optional['Reg']

    def __init__(self) -> None:
        super().__init__()

        #: If true, fields are to be arranged in msb0 order
        #:
        #: .. versionadded:: 1.7
        self.is_msb0_order: bool = False

        # List of register inst names that are aliases of this primary
        # Due to limitations in RDL grammar, these can only be siblings in the hierarchy
        # so names are unambiguous
        self._alias_names: List[str] = []

        #------------------------------
        # Alias Register
        #------------------------------
        #: If true, then ``alias_primary_inst`` is valid
        self.is_alias: bool = False

        #: Reference to primary register :class:`~systemrdl.component.Component`
        #: instance
        self.alias_primary_inst: Optional[Reg] = None

class Regfile(AddressableComponent):
    original_def: Optional['Regfile']

class Addrmap(AddressableComponent):
    original_def: Optional['Addrmap']

class Mem(AddressableComponent):
    original_def: Optional['Mem']
