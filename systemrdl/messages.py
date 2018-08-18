
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
    
    def warning(self, text, src_ref=None):
        self.printer.print_message("warning", text, src_ref)
        self.warning_count += 1
    
    def error(self, text, src_ref=None):
        self.printer.print_message("error", text, src_ref)
        self.error_count += 1
    
    def fatal(self, text, src_ref=None):
        self.printer.print_message("error", text, src_ref)
        raise RDLCompileError(text)
        
#===============================================================================
class SourceRef:
    """
    Reference to a segment of compiled source.
    
    This is used to provide useful context when reporting error messages.
    """
    def __init__(self, filename, start, end):
        
        #: Source filename
        self.filename = filename
        
        #: Character position of start of selection
        self.start = start
        
        #: Character position of end of selection
        self.end = end
        
        #: Line number of start of selection
        self.start_line = None
        
        #: Column of first character in selection
        self.start_col = None
        
        #: Line number of end of selection
        self.end_line = None
        
        #: Column of last character in selection
        self.end_col = None
        
        self.start_line_text = None
    
    def derive_coordinates(self):
        # TODO: For now, assumes selection is contained within a single file
        line_start = 0
        lineno = 1
        
        with open(self.filename) as fp:
            
            while True:
                line_text = fp.readline()
                if line_text == "":
                    break
                
                if (self.start_line is None) and (self.start <= fp.tell()):
                    self.start_line = lineno
                    self.start_col = self.start - line_start
                    self.start_line_text = line_text.rstrip("\n")
                
                if (self.end_line is None) and (self.end <= fp.tell()):
                    self.end_line = lineno
                    self.end_col = self.end - line_start
                    break
                
                lineno += 1
                line_start = fp.tell()
        
        
    
    @classmethod
    def from_antlr(cls, antlr_ref):
        
        # Normalize
        if isinstance(antlr_ref, CommonToken):
            token = antlr_ref
            end_token = None
        elif isinstance(antlr_ref, TerminalNodeImpl):
            token = antlr_ref.symbol
            end_token = None
        elif isinstance(antlr_ref, ParserRuleContext):
            # antlr_ref is an entire context (token range)
            token = antlr_ref.start
            end_token = antlr_ref.stop
        else:
            print(antlr_ref)
            raise NotImplementedError
        
        # Get filename
        inputStream = token.getInputStream()
        if isinstance(inputStream, FileStream):
            filename = inputStream.fileName
        else:
            filename = None
            
        # Extract selection coordinates
        start = token.start
        if end_token is None:
            end = token.stop
        else:
            end = end_token.stop
        
        # Create object
        src_ref = cls(filename, start, end)
        return src_ref

#===============================================================================
class MessagePrinter:
    """
    Printer class that handles formatting and emitting compiler messages
    
    This class can be extended in order to provide custom compiler message
    formatting or logging
    """
    
    def print_message(self, severity, text, src_ref):
        lines = self.format_message(severity, text, src_ref)
        self.emit_message(lines)
        
    def format_message(self, severity, text, src_ref):
        """
        Formats the message prior to emitting it.
        
        Parameters
        ----------
        severity: str
            Message severity. "error" or "warning"
        text: str
            Body of message
        src_ref: :class:`SourceRef`
            Antlr message src_ref wrapper
        
        Returns
        -------
        list
            List of strings for each line of the message
        """
        lines = []
        
        if severity == "error":
            color = Fore.RED
        else:
            color = Fore.YELLOW
            
        if src_ref is None:
            lines.append(
                color + Style.BRIGHT + severity + ": " + Style.RESET_ALL + text
            )
        else:
            src_ref.derive_coordinates()
            
            lines.append(
                Fore.WHITE + Style.BRIGHT
                + "%s:%d:%d: " % (src_ref.filename, src_ref.start_line, src_ref.start_col)
                + color + severity + ": "
                + Style.RESET_ALL
                + text
            )
            
            # If src_ref highlights anything interesting, print it
            if src_ref.start_line != src_ref.end_line:
                # multi-line reference
                # Select remainder of the line
                width = len(src_ref.start_line_text) - src_ref.start_col
                
                lines.append(
                    src_ref.start_line_text[:src_ref.start_col] 
                    + Fore.RED + Style.BRIGHT
                    + src_ref.start_line_text[src_ref.start_col:]
                    + Style.RESET_ALL 
                )
                
                lines.append(
                    " "*src_ref.start_col 
                    + Fore.RED + Style.BRIGHT
                    + "^"*width
                    + Style.RESET_ALL
                )
                
            elif src_ref.start_col != src_ref.end_col:
                # Single line, Nonzero width
                width = src_ref.end_col - src_ref.start_col + 1
                
                lines.append(
                    src_ref.start_line_text[:src_ref.start_col] 
                    + Fore.RED + Style.BRIGHT
                    + src_ref.start_line_text[src_ref.start_col : src_ref.end_col+1]
                    + Style.RESET_ALL 
                    + src_ref.start_line_text[src_ref.end_col+1:]
                )
                
                lines.append(
                    " "*src_ref.start_col 
                    + Fore.RED + Style.BRIGHT
                    + "^"*width
                    + Style.RESET_ALL
                )
            
        return lines
        
        
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
            SourceRef.from_antlr(offendingSymbol)
        )
