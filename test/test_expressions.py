#!/usr/bin/env python3
import unittest

import sys
import os
this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))


from antlr4 import InputStream, CommonTokenStream
from systemrdl.parser.SystemRDLLexer import SystemRDLLexer
from systemrdl.parser.SystemRDLParser import SystemRDLParser
from systemrdl.core.ExprVisitor import ExprVisitor
from systemrdl.core.properties import PropertyRuleBook
from systemrdl.core.namespace import NamespaceRegistry

#===============================================================================
def eval_RDL_expr(expr_text):
    input_stream = InputStream(expr_text)
    lexer = SystemRDLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SystemRDLParser(token_stream)
    tree = parser.expr()
    
    ns = NamespaceRegistry()
    pr = PropertyRuleBook()
    
    visitor = ExprVisitor(ns, pr, None)
    result = visitor.visit(tree)
    
    pred_type = result.predict_type()
    result.resolve_expr_width()
    return(pred_type, result.get_value())

#===============================================================================
class TestNumericExpressions(unittest.TestCase):
    
    def test_width_propagation(self):
        self.assertEqual((int, 0x00FF), eval_RDL_expr("8'h00 - 1'h1"))
        self.assertEqual((int, 0x00FF), eval_RDL_expr("8'h00 - 1'h1"))
        self.assertEqual((int, 0x0000), eval_RDL_expr("(8'h00 - 1'h1) + 16'h1"))
        self.assertEqual((int, 0x0100), eval_RDL_expr("(8'hFF) + 16'h1"))
        self.assertEqual((int, 0xFFFF), eval_RDL_expr("(8'h00 - 1'h1) + 16'h0"))
        self.assertEqual((int, 0x0000), eval_RDL_expr("((8'h00 - 1'h1) - 8'hFF)"))
        self.assertEqual((int, 0xFF00), eval_RDL_expr("((8'h00- 1'h1) - 8'hFF) + 16'h0"))
        self.assertEqual((int, 0xFFFF), eval_RDL_expr("(~(~(8'h00 - 1'h1))) + 16'h0"))
        self.assertEqual((int, 0xFFFF), eval_RDL_expr("(~(8'h00)) + 16'h0"))
        self.assertEqual((int, 0xFF00), eval_RDL_expr("(~(8'hFF)) + 16'h0"))
        self.assertEqual((int, 0x0100), eval_RDL_expr("((8'hFF + 8'h1)) + 16'h0"))
        self.assertEqual((int, 0x0000), eval_RDL_expr("8'hFF + 8'h1"))
        self.assertEqual((int, 0x0100), eval_RDL_expr("8'hFF + 16'h1"))
        self.assertEqual((int, 0x00FF), eval_RDL_expr("8'hFF + 16'h0"))
        self.assertEqual((int, 0x0100), eval_RDL_expr("((8'hFF + 8'h1) + 8'h0) + 16'h0"))
        self.assertEqual((int, 0x0000), eval_RDL_expr("((8'hFF + 8'h1) + 8'h0) + 8'h0"))
        self.assertEqual((int, 0x0000), eval_RDL_expr("(8'hFF + 8'h1) + 8'h0"))
        self.assertEqual((int, 0x0000), eval_RDL_expr("((8'hFF + 8'h1)) + ((8'hFF + 8'h1))"))
        self.assertEqual((int, 0x0200), eval_RDL_expr("((8'hFF + 8'h1)) + ((8'hFF + 8'h1) + 16'b0)"))
        self.assertEqual((int, 0x0000), eval_RDL_expr("1'b1 << 3"))
        self.assertEqual((int, 0x0008), eval_RDL_expr("(1'b1 << 3) + 8'b0"))
        self.assertEqual((int, 0x0000), eval_RDL_expr("(|(~(4'hF))) + 8'b0"))
        self.assertEqual((int, 0x00FF), eval_RDL_expr("(~(&(4'b1))) + 8'b0"))
    
    def test_width_cast(self):
        self.assertEqual((int, 0x0100), eval_RDL_expr("(16)'(8'hFF + 8'h1) + 8'h0)"))
        self.assertEqual((int, 0x000F), eval_RDL_expr("(4)'(8'hFF)"))
    
    def test_boolean_expr(self):
        self.assertEqual((bool, False), eval_RDL_expr("16 == 3"))
        
#===============================================================================
if __name__ == '__main__':
    unittest.main()