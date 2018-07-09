#!/usr/bin/env python3

import unittest
import sys
import os
import logging
import re

from antlr4 import InputStream, CommonTokenStream
from systemrdl import RDLCompiler
from systemrdl.parser.SystemRDLLexer import SystemRDLLexer
from systemrdl.parser.SystemRDLParser import SystemRDLParser
from systemrdl.core.ExprVisitor import ExprVisitor
from systemrdl.messages import MessagePrinter, RDLCompileError
#===============================================================================
class TestPrinter(MessagePrinter):
    def print_message(self, severity, text, context):
        logging.error(text)


#===============================================================================
class RDLSourceTestCase(unittest.TestCase):
    """
    Base class for SystemRDL unittest TestCase
    Implements mechanisms and tests common to interpreting an RDL testcase file
    """
    def compile(self, files, top_name):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        rdlc = RDLCompiler(message_printer=TestPrinter())
        for file in files:
            rdlc.compile_file(os.path.join(this_dir, file))
        return rdlc.elaborate(top_name)
    
    
    def eval_RDL_expr(self, expr_text):
        input_stream = InputStream(expr_text)
        lexer = SystemRDLLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = SystemRDLParser(token_stream)
        tree = parser.expr()
        
        rdlc = RDLCompiler(message_printer=TestPrinter())
        
        visitor = ExprVisitor(rdlc)
        result = visitor.visit(tree)
        
        pred_type = result.predict_type()
        return pred_type, result.get_value()
    
    
    def assertRDLExprError(self, expr_text, msg_regex):
        with self.assertLogs() as cm:
            with self.assertRaises(RDLCompileError):
                self.eval_RDL_expr(expr_text)
        
        for record in cm.records:
            if re.search(msg_regex, record.getMessage()):
                break
        else:
            msg = []
            msg.append("Error test FAILED")
            msg.append("")
            msg.append("No RDL error message found that matched regex: '%s'" % msg_regex)
            msg.append("")
            msg.append("Got the following messages:")
            for record in cm.records:
                msg.append("\t%s" % record.getMessage())
            
            self.fail("\n".join(msg))
    
    
    def assertRDLCompileError(self, files, top_name, msg_regex):
        with self.assertLogs() as cm:
            with self.assertRaises(RDLCompileError):
                self.compile(files, top_name)
        
        for record in cm.records:
            if re.search(msg_regex, record.getMessage()):
                break
        else:
            msg = []
            msg.append("Error test FAILED")
            msg.append("")
            msg.append("No RDL error message found that matched regex: '%s'" % msg_regex)
            msg.append("")
            msg.append("Got the following messages:")
            for record in cm.records:
                msg.append("\t%s" % record.getMessage())
            
            self.fail("\n".join(msg))
