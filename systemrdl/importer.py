
from .compiler import RDLCompiler
from .component import Component

class RDLImporter:
    """
    Base class for external parsers to import data into the register model
    """
    def __init__(self, compiler:RDLCompiler):
        self.compiler = compiler
        self.msg = compiler.env.msg

    def import_file(self, path:str):
        raise NotImplementedError

    def register_root_component(self, definition:Component):

        if definition.type_name is None:
            raise ValueError("Component must have a type_name")

        if definition.is_instance:
            raise ValueError("Component cannot be instantiated")

        self.compiler.namespace.register_type(
            definition.type_name,
            definition,
            definition.def_src_ref
        )

    def lookup_root_component(self, type_name:str):
        t = self.compiler.namespace.lookup_type(type_name)

        if not isinstance(Component):
            t = None

        return t
