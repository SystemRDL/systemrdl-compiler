
import sys

from antlr4.error.ErrorListener import ErrorListener
from antlr4.Token import CommonToken
from antlr4 import ParserRuleContext, FileStream
from antlr4.tree.Tree import TerminalNodeImpl
from colorama import Fore, Style

#===============================================================================
class RDLCompileError(Exception):
    """
    Base class for all SystemRDL compiler exceptions
    """
    
#===============================================================================
class MessageHandler:
    def __init__(self, printer):
        self.printer = printer
        self.warning_count = 0
        self.error_count = 0
    
    def warning(self, text, context=None):
        if(context is not None):
            context = MessageContext(context)
        
        self.printer.print_message("warning", text, context)
        self.warning_count += 1
    
    def error(self, text, context=None):
        if(context is not None):
            context = MessageContext(context)
        
        self.printer.print_message("error", text, context)
        self.error_count += 1
    
    def fatal(self, text, context=None):
        if(context is not None):
            context = MessageContext(context)
        
        self.printer.print_message("error", text, context)
        raise RDLCompileError(text)
        
#===============================================================================
class MessageContext:
    """
    Wrapper class for the various types of Antlr objects that can provide message
    context.
    """
    
    def __init__(self, antlr_obj):
        self.filename = ""
        self.line = 0
        self.column = 0
        self.width = None
        self.line_text = None
        
        if(type(antlr_obj) == CommonToken):
            self.init_from_single_token(antlr_obj)
        elif(type(antlr_obj) == TerminalNodeImpl):
            self.init_from_single_token(antlr_obj.symbol)
        elif(issubclass(type(antlr_obj), ParserRuleContext)):
            # antlr_obj is an entire context (multiple tokens)
            self.init_from_token_range(antlr_obj.start, antlr_obj.stop)
        else:
            print(antlr_obj)
            raise NotImplementedError
        
    def init_from_single_token(self, token):
        self.line = token.line
        self.column = token.column
        inputStream = token.getInputStream()
        if(type(inputStream) == FileStream):
            self.filename = inputStream.fileName
        
        file_lines = inputStream.strdata.splitlines()
        file_lines.append("") # append an empty line just in case error is at EOF
        self.line_text = file_lines[self.line-1]
        self.width = token.stop - token.start + 1
    
    def init_from_token_range(self, start_token, end_token):
        self.line = start_token.line
        self.column = start_token.column
        inputStream = start_token.getInputStream()
        if(type(inputStream) == FileStream):
            self.filename = inputStream.fileName
        
        file_lines = inputStream.strdata.splitlines()
        file_lines.append("") # append an empty line just in case error is at EOF
        self.line_text = file_lines[self.line-1]
        
        # Select entire token range
        if(self.line == end_token.line):
            # range is within the same line
            self.width = end_token.stop - start_token.start + 1
        else:
            # Range spans multiple lines. Only select the first line
            self.width = len(self.line_text) - start_token.column
            
        

#===============================================================================
class MessagePrinter:
    
    def print_message(self, severity, text, context):
        lines = self.format_message(severity, text, context)
        self.emit_message(lines)
        
    def format_message(self, severity, text, context):
        """
        Formats the message prior to emitting it.
        
        Parameters
        ----------
        severity: str
            Message severity. "error" or "warning"
        text: str
            Body of message
        context: :class:`MessageContext`
            Antlr message context wrapper
        
        Returns
        -------
        list
            List of strings for each line of the message
        """
        lines = []
        
        if(severity == "error"):
            color = Fore.RED
        else:
            color = Fore.YELLOW
            
        if(context is None):
            lines.append(
                color + Style.BRIGHT + severity + ": " + Style.RESET_ALL + text
            )
        else:
            lines.append(
                Fore.WHITE + Style.BRIGHT + "%s:%d:%d: " % (context.filename, context.line, context.column)
                + color + severity + ": " + Style.RESET_ALL + text
            )
            
            # If context highlights anything interesting, print it
            if(context.width != 0):
                lines.append(
                    context.line_text[:context.column] 
                    + Fore.RED + Style.BRIGHT + context.line_text[context.column:context.column+context.width] + Style.RESET_ALL 
                    + context.line_text[context.column+context.width:]
                )
                
                lines.append(
                    " "*context.column 
                    + Fore.RED + Style.BRIGHT + "^"*context.width + Style.RESET_ALL
                )
            
        return(lines)
        
        
    def emit_message(self, lines):
        """
        Emit message.
        Default printer emits messages to stderr
        
        Parameters
        ----------
        lines: list
            List of strings containing each line of the message
        """
        
        for line in lines:
            print(line, file=sys.stderr)

#===============================================================================
# Antlr error listener
#===============================================================================
class RDLAntlrErrorListener(ErrorListener) :
    
    def __init__(self, msg_handler):
        self.msg = msg_handler
        
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.msg.error(
            msg,
            offendingSymbol
        )
