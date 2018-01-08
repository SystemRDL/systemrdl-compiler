#!/usr/bin/env python3

import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))

from antlr4 import *


from src.parser.SystemRDLLexer import SystemRDLLexer
from src.parser.SystemRDLParser import SystemRDLParser
from src.compiler.ExprVisitor import ExprVisitor


def eval_RDL_expr(expr_text):
    input_stream = InputStream(expr_text)
    lexer = SystemRDLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SystemRDLParser(token_stream)
    tree = parser.expr()

    visitor = ExprVisitor()
    result = visitor.visit(tree)
    
    pred_type = result.predict_type()
    result.resolve_expr_width()
    return(pred_type, result.get_value())
    


assert((int, 0x00FF) == eval_RDL_expr("8'h00 - 1'h1"))
assert((int, 0x00FF) == eval_RDL_expr("8'h00 - 1'h1"))
assert((int, 0x0000) == eval_RDL_expr("(8'h00 - 1'h1) + 16'h1"))
assert((int, 0x0100) == eval_RDL_expr("(8'hFF) + 16'h1"))
assert((int, 0xFFFF) == eval_RDL_expr("(8'h00 - 1'h1) + 16'h0"))
assert((int, 0x0000) == eval_RDL_expr("((8'h00 - 1'h1) - 8'hFF)"))
assert((int, 0xFF00) == eval_RDL_expr("((8'h00- 1'h1) - 8'hFF) + 16'h0"))
assert((int, 0xFFFF) == eval_RDL_expr("(~(~(8'h00 - 1'h1))) + 16'h0"))
assert((int, 0xFFFF) == eval_RDL_expr("(~(8'h00)) + 16'h0"))
assert((int, 0xFF00) == eval_RDL_expr("(~(8'hFF)) + 16'h0"))
assert((int, 0x0100) == eval_RDL_expr("((8'hFF + 8'h1)) + 16'h0"))
assert((int, 0x0000) == eval_RDL_expr("8'hFF + 8'h1"))
assert((int, 0x0100) == eval_RDL_expr("8'hFF + 16'h1"))
assert((int, 0x00FF) == eval_RDL_expr("8'hFF + 16'h0"))
assert((int, 0x0100) == eval_RDL_expr("((8'hFF + 8'h1) + 8'h0) + 16'h0"))
assert((int, 0x0000) == eval_RDL_expr("((8'hFF + 8'h1) + 8'h0) + 8'h0"))
assert((int, 0x0000) == eval_RDL_expr("(8'hFF + 8'h1) + 8'h0"))
assert((int, 0x0000) == eval_RDL_expr("1'b1 << 3"))
assert((int, 0x0008) == eval_RDL_expr("(1'b1 << 3) + 8'b0"))
assert((int, 0x0000) == eval_RDL_expr("(|(~(4'hF))) + 8'b0"))
assert((int, 0x0000) == eval_RDL_expr("((8'hFF + 8'h1)) + ((8'hFF + 8'h1))"))
assert((int, 0x0200) == eval_RDL_expr("((8'hFF + 8'h1)) + ((8'hFF + 8'h1) + 16'b0)"))
assert((int, 0x00FF) == eval_RDL_expr("(~(&(4'b1))) + 8'b0"))
assert((int, 0x0100) == eval_RDL_expr("(16)'(8'hFF + 8'h1) + 8'h0)"))
assert((int, 0x000F) == eval_RDL_expr("(4)'(8'hFF)"))
assert((bool, False) == eval_RDL_expr("16 == 3"))
