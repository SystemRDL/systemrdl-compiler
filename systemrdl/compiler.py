from copy import deepcopy

from antlr4 import CommonTokenStream

from . import messages
from .parser.SystemRDLLexer import SystemRDLLexer
from .parser.SystemRDLParser import SystemRDLParser
from .core.ComponentVisitor import RootVisitor
from .core.properties import PropertyRuleBook, UserProperty
from .core.namespace import NamespaceRegistry
from .core.elaborate import ElabExpressionsListener, PrePlacementValidateListener, LateElabListener
from .core.elaborate import StructuralPlacementListener
from .core.validate import ValidateListener
from . import component as comp
from . import walker
from .node import RootNode
from .preprocessor import preprocessor

class RDLCompiler:
    
    def __init__(self, **kwargs):
        """
        RDLCompiler constructor.
        
        Parameters
        ----------
        message_printer: :class:`~systemrdl.messages.MessagePrinter`
            Override the default message printer
        warning_flags: int
            Flags to enable warnings. See :ref:`messages_warnings` for more details.
        """
        self.env = Environment(kwargs)
        
        # Check for stray kwargs
        if kwargs:
            raise TypeError("got an unexpected keyword argument '%s'" % list(kwargs.keys())[0])
        
        self.msg = self.env.msg
        self.namespace = NamespaceRegistry(self.env)
        self.visitor = RootVisitor(self)
        self.root = self.visitor.component
    
    def define_udp(self, name, valid_type, valid_components=None, default=None):
        """
        Pre-define a user-defined property.
        
        This is the equivalent to the following RDL:
        
        .. code-block:: none
            
            property <name> {
                type = <valid_type>;
                component = <valid_components>;
                default = <default>
            };
        
        Parameters
        ----------
        name: str
            Property name
        valid_components: list
            List of :class:`~systemrdl.component.Component` types the UDP can be bound to.
            If None, then UDP can be bound to all components.
        valid_type: type
            Assignment type that this UDP will enforce
        default:
            Default if a value is not specified when the UDP is bound to a component.
            Value must be compatible with ``valid_type``
            
        """
        if valid_components is None:
            valid_components = [
                comp.Field,
                comp.Reg,
                comp.Regfile,
                comp.Addrmap,
                comp.Mem,
                comp.Signal,
                #TODO constraint,
            ]
        
        if name in self.env.property_rules.rdl_properties:
            raise ValueError("name '%s' conflicts with existing built-in RDL property")
        
        udp = UserProperty(self.env, name, valid_components, [valid_type], default)
        
        self.env.property_rules.user_properties[udp.name] = udp
        
    
    def compile_file(self, path, incl_search_paths=None):
        """
        Parse & compile a single file and append it to RDLCompiler's root
        namespace.
        
        If any exceptions (:class:`~systemrdl.RDLCompileError` or other)
        occur during compilation, then the RDLCompiler object should be discarded.
        
        Parameters
        ----------
        path:str
            Path to an RDL source file
        
        incl_search_paths:list
            List of additional paths to search to resolve includes.
            If unset, defaults to an empty list.
            
            Relative include paths are resolved in the following order:
            
            1. Search each path specified in ``incl_search_paths``.
            2. Path relative to the source file performing the include.
            
        Raises
        ------
        :class:`~systemrdl.RDLCompileError`
            If any fatal compile error is encountered.
        """
        
        if incl_search_paths is None:
            incl_search_paths = []
        
        fpp = preprocessor.FilePreprocessor(self.env, path, incl_search_paths)
        preprocessed_text, seg_map = fpp.preprocess()
        input_stream = preprocessor.PreprocessedInputStream(preprocessed_text, seg_map)
        
        lexer = SystemRDLLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(messages.RDLAntlrErrorListener(self.msg))
        
        token_stream = CommonTokenStream(lexer)
        
        parser = SystemRDLParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(messages.RDLAntlrErrorListener(self.msg))
        
        # Run Antlr parser on input
        parsed_tree = parser.root()
        if self.msg.error_count:
            self.msg.fatal("Parse aborted due to previous errors")
        
        # Traverse parse tree with RootVisitor
        self.visitor.visit(parsed_tree)
        
        # Reset default property assignments from namespace.
        # They should not be shared between files since that would be confusing.
        self.namespace.default_property_ns_stack = [{}]
        
        if self.msg.error_count:
            self.msg.fatal("Compile aborted due to previous errors")
    
    def elaborate(self, top_def_name=None, inst_name=None, parameters=None):
        """
        Elaborates the design for the given top-level addrmap component.
        
        During elaboration, the following occurs:
        
        - An instance of the ``$root`` meta-component is created.
        - The addrmap component specified by ``top_def_name`` is instantiated as a
          child of ``$root``.
        - Expressions, parameters, and inferred address/field placements are elaborated.
        - Validation checks are performed.
        
        If a design contains multiple root-level addrmaps, ``elaborate()`` can be
        called multiple times in order to elaborate each individually.
        
        If any exceptions (:class:`~systemrdl.RDLCompileError` or other)
        occur during elaboration, then the RDLCompiler object should be discarded.
        
        Parameters
        ----------
        top_def_name: str
            Explicitly choose which addrmap  in the root namespace will be the
            top-level component.
            
            If unset, The last addrmap defined will be chosen.
            
        inst_name: str
            Overrides the top-component's instantiated name.
            By default, instantiated name is the same as ``top_def_name``
        
        parameters: TBD
            This feature is not implemented yet.
        
        Raises
        ------
        :class:`~systemrdl.RDLCompileError`
            If any fatal elaboration error is encountered
        
        Returns
        -------
        :class:`~systemrdl.node.RootNode`
            Elaborated root meta-component's Node object.
        """
        if parameters is None:
            parameters = {}
        
        # Get top-level component definition to elaborate
        if top_def_name is not None:
            # Lookup top_def_name
            if top_def_name not in self.root.comp_defs:
                self.msg.fatal("Elaboration target '%s' not found" % top_def_name)
            top_def = self.root.comp_defs[top_def_name]
            
            if not isinstance(top_def, comp.Addrmap):
                self.msg.fatal("Elaboration target '%s' is not an 'addrmap' component" % top_def_name)
        else:
            # Not specified. Find the last addrmap defined
            for comp_def in reversed(self.root.comp_defs.values()):
                if isinstance(comp_def, comp.Addrmap):
                    top_def = comp_def
                    top_def_name = comp_def.type_name
                    break
            else:
                self.msg.fatal("Could not find any 'addrmap' components to elaborate")
        
        # Create an instance of the root component
        root_inst = deepcopy(self.root)
        root_inst.is_instance = True
        root_inst.original_def = self.root
        root_inst.inst_name = "$root"
        
        # Create a top-level instance
        top_inst = deepcopy(top_def)
        top_inst.is_instance = True
        top_inst.original_def = top_def
        top_inst.addr_offset = 0
        if inst_name is not None:
            top_inst.inst_name = inst_name
        else:
            top_inst.inst_name = top_def_name
        
        # Override parameters as needed
        if len(parameters):
            # TODO: Add mechanism to set parameters of top-level component
            raise NotImplementedError
        
        # instantiate top_inst into the root component instance
        root_inst.children.append(top_inst)
        
        root_node = RootNode(root_inst, self.env, None)
        
        # Resolve all expressions
        walker.RDLWalker(skip_not_present=False).walk(
            root_node,
            ElabExpressionsListener(self.msg)
        )
        
        # Resolve address and field placement
        walker.RDLWalker(skip_not_present=False).walk(
            root_node,
            PrePlacementValidateListener(self.msg),
            StructuralPlacementListener(self.msg),
            LateElabListener(self.msg)
        )
        
        # Validate design
        # Only need to validate nodes that are present
        walker.RDLWalker(skip_not_present=True).walk(root_node, ValidateListener(self.env))
        
        if self.msg.error_count:
            self.msg.fatal("Elaborate aborted due to previous errors")
        
        return root_node


class Environment:
    """
    Container object for misc resources that are preserved outside the lifetime
    of source compilation
    """
    def __init__(self, args_dict):
        
        # Collect args
        message_printer = args_dict.pop('message_printer', messages.MessagePrinter())
        warning_flags = args_dict.pop('warning_flags', 0)
        
        # Warnings
        self.warn_missing_reset = bool(warning_flags & messages.W_MISSING_RESET)
        self.warn_implicit_field_pos = bool(warning_flags & messages.W_IMPLICIT_FIELD_POS)
        self.warn_implicit_addr = bool(warning_flags & messages.W_IMPLICIT_ADDR)
        
        self.msg = messages.MessageHandler(message_printer)
        self.property_rules = PropertyRuleBook(self)
