from typing import Optional, Any, TYPE_CHECKING

from .compiler import RDLCompiler
from .component import Component

if TYPE_CHECKING:
    from .source_ref import SourceRefBase

class RDLImporter:
    """
    Base class for external parsers to import data into the register model
    """
    def __init__(self, compiler: RDLCompiler):
        self.compiler = compiler
        self.msg = compiler.env.msg

    def import_file(self, path: str) -> None:
        raise NotImplementedError

    def register_root_component(self, definition: Component) -> None:

        if definition.type_name is None:
            raise ValueError("Component must have a type_name")

        if definition.is_instance:
            raise ValueError("Component cannot already be instantiated")

        if len(self.compiler.namespace.type_ns_stack) != 1:
            raise RuntimeError("Namespace was not properly reset to root scope")

        # Register with namespace
        self.compiler.namespace.register_type(
            definition.type_name,
            definition,
            definition.def_src_ref
        )

        # Add to root component definition list
        self.compiler.root.comp_defs[definition.type_name] = definition

    def lookup_root_component(self, type_name: str) -> Optional[Component]:
        return self.compiler.root.comp_defs.get(type_name, None)

    def assign_property(self, component: Component, prop_name: str, value: Any, src_ref: 'SourceRefBase') -> None:
        rule = self.compiler.env.property_rules.lookup_property(prop_name)
        if rule is None:
            self.msg.fatal(
                "Unrecognized property '%s'" % prop_name,
                src_ref
            )
        rule.assign_value(component, value, src_ref)
