import unittest
import os
import logging
import re

from antlr4 import InputStream
from systemrdl import RDLCompiler
from systemrdl.parser import sa_systemrdl
from systemrdl.core.ExprVisitor import ExprVisitor
from systemrdl.messages import MessagePrinter, RDLCompileError, RdlSaErrorListener
#===============================================================================
# If test requests to NOT use C++ extension, force pure-python implementation
if 'SYSTEMRDL_DISABLE_ACCELERATOR' in os.environ:
    sa_systemrdl.USE_CPP_IMPLEMENTATION = False

#===============================================================================
class TestPrinter(MessagePrinter):
    def emit_message(self, lines):
        text = "\n".join(lines)
        logging.info(text)


#===============================================================================
class RDLSourceTestCase(unittest.TestCase):
    """
    Base class for SystemRDL unittest TestCase
    Implements mechanisms and tests common to interpreting an RDL testcase file
    """
    def setUp(self):
        self.compiler_warning_flags = 0
        self.compiler_error_flags = 0

    def compile(self, files, top_name=None, inst_name=None, parameters=None, incl_search_paths=None, defines=None):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        rdlc = RDLCompiler(
            message_printer=TestPrinter(),
            warning_flags=self.compiler_warning_flags,
            error_flags=self.compiler_error_flags
        )
        for file in files:
            rdlc.compile_file(os.path.join(this_dir, file), incl_search_paths, defines)
        return rdlc.elaborate(top_name, inst_name, parameters)


    def eval_RDL_expr(self, expr_text):
        input_stream = InputStream(expr_text)

        rdlc = RDLCompiler(message_printer=TestPrinter())

        tree = sa_systemrdl.parse(
            input_stream,
            "eval_expr_root",
            RdlSaErrorListener(rdlc.msg)
        )

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
