#!/usr/bin/env python3

import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from antlr4 import *

from src.parser.SystemRDLLexer import SystemRDLLexer
from src.parser.SystemRDLParser import SystemRDLParser
from src.compiler.ComponentVisitor import RootVisitor
from src.compiler.errors import *

input_stream = FileStream("test.rdl")
lexer = SystemRDLLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = SystemRDLParser(token_stream)

parser.removeErrorListeners()
err_listener = ContextErrorListener()
parser.addErrorListener(err_listener)

tree = parser.root()

visitor = RootVisitor()
try:
    result = visitor.visit(tree)
    print(result.comp_defs)
except RDLCompileError as e:
    e.print()

