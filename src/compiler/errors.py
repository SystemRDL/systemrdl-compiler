import sys
import antlr4
from antlr4.error.ErrorListener import *
from antlr4.Token import CommonToken
from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

import colorama
from colorama import Fore, Back, Style

#===============================================================================
# Antlr error listener
#===============================================================================
class RDLParserErrorListener(ErrorListener) :
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise RDLCompileError(
            msg,
            offendingSymbol
        )

#===============================================================================
class RDLErrorHandler:
    """
    Template class for any error handlers
    """
    def __init__(self):
        pass
    
    def handle_exception(self, e):
        """
        Implements error handling for any RDLException raised
        """
        raise NotImplementedError
        
    
class ConsoleErrorPrinter(RDLErrorHandler):
    def handle_exception(self, e):
        if(issubclass(type(e), RDLCompileError)):
            self.print_compile_error(e)
        else:
            print(e)
    
    def print_compile_error(self, e):
        ec = ErrorContext.from_antlr_obj(e.antlr_obj)
        ec.print_error(e.msg)
    

class ErrorContext:
    def __init__(self):
        self.filename = ""
        self.line = 0
        self.column = 0
        self.width = None
        self.line_text = None
    
    @classmethod
    def from_antlr_obj(cls, obj):
        if(type(obj) == CommonToken):
            return(cls.from_token(obj))
        elif(type(obj) == TerminalNodeImpl):
            return(cls.from_token(obj.symbol))
        elif(issubclass(type(obj), ParserRuleContext)):
            # TODO: Highlight entire context, not just the first token
            return(cls.from_token(obj.start))
        else:
            print(type(obj), issubclass(type(obj), ParserRuleContext))
        
    @classmethod
    def from_token(cls, token):
        ec = cls()
        ec.line = token.line
        ec.column = token.column
        inputStream = token.getInputStream()
        ec.filename = inputStream.fileName
        
        file_lines = inputStream.strdata.splitlines()
        file_lines.append("") # append an empty line just in case error is at EOF
        ec.line_text = file_lines[ec.line-1]
        ec.width = token.stop - token.start + 1
        return(ec)
        
    def print_error(self, msg):
        """
        GCC-style Error Printer
        """
        print(
            Fore.WHITE + Style.BRIGHT + "%s:%d:%d:" % (self.filename, self.line, self.column),
            Fore.RED + "error:",
            Style.RESET_ALL + msg,
            file=sys.stderr
        )
        
        if(self.width != 0):
            print(
                self.line_text[:self.column] 
                + Fore.RED + Style.BRIGHT + self.line_text[self.column:self.column+self.width] + Style.RESET_ALL 
                + self.line_text[self.column+self.width:],
                file=sys.stderr
            )
            
            print(
                " "*self.column 
                + Fore.RED + Style.BRIGHT + "^"*self.width + Style.RESET_ALL,
                file=sys.stderr
            )

#===============================================================================
# Exceptions
#===============================================================================
class RDLException(Exception):
    """
    Base class for all RDL user exceptions
    """
    pass

class RDLCompileError(RDLException):
    """
    Any exception that occurs during the compile process, where an appropriate
    Antlr object is available to provide source context
    The required Antlr object provided can be any of the following:
        Token, TerminalNode, ParserRuleContext
    """
    def __init__(self, msg, antlr_obj):
        super().__init__(msg)
        self.antlr_obj = antlr_obj
        self.msg = msg
    
class RDLNotSupportedYet(RDLCompileError):
    """
    Error thrown for any RDL features that I do not plan on supporting quite yet
    """
    pass