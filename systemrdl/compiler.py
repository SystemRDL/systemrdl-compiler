from copy import deepcopy

from antlr4 import FileStream, CommonTokenStream

from . import messages
from .parser.SystemRDLLexer import SystemRDLLexer
from .parser.SystemRDLParser import SystemRDLParser
from .core.ComponentVisitor import RootVisitor
from .core.properties import PropertyRuleBook
from .core.namespace import NamespaceRegistry
from .core.elaborate import ElabExpressionsListener, PrePlacementValidateListener, LateElabListener
from .core.elaborate import StructuralPlacementListener
from .core.validate import ValidateListener
from . import component as comp
from . import walker
from .node import RootNode

class RDLCompiler:
    
    def __init__(self, message_printer=None):
        """
        RDLCompiler constructor.
        
        Parameters
        ----------
        message_printer: :class:`~systemrdl.messages.MessagePrinter`
            Override the default message printer
        """
        self.env = Environment()
        
        # Set up message handling
        if message_printer is None:
            message_printer = messages.MessagePrinter()
        self.msg = messages.MessageHandler(message_printer)
        
        self.env.msg = self.msg
        
        self.namespace = NamespaceRegistry(self.env)
        self.property_rules = PropertyRuleBook(self.env)
        self.env.property_rules = self.property_rules
        
        self.visitor = RootVisitor(self)
        self.root = self.visitor.component
    
    
    def compile_file(self, path):
        """
        Parse & compile a single file and append it to RDLCompiler's root
        namespace.
        
        If any exceptions (:class:`~systemrdl.messages.RDLCompileError` or other)
        occur during compilation, then the RDLCompiler object should be discarded.
        
        Parameters
        ----------
        path:str
            Path to an RDL source file
        
        Raises
        ------
        :class:`~systemrdl.messages.RDLCompileError`
            If any fatal compile error is encountered.
        """
        
        input_stream = FileStream(path)
        
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
        
        If any exceptions (:class:`~systemrdl.messages.RDLCompileError` or other)
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
        :class:`~systemrdl.messages.RDLCompileError`
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
    def __init__(self):
        self.msg = None
        self.property_rules = None
