#!/usr/bin/env python3

import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from antlr4 import *

from src.parser.SystemRDLLexer import SystemRDLLexer
from src.parser.SystemRDLParser import SystemRDLParser
from src.compiler.RootVisitor import RootVisitor


input_stream = FileStream("test.rdl")
lexer = SystemRDLLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = SystemRDLParser(token_stream)
tree = parser.root()

visitor = RootVisitor()
result = visitor.visit(tree)