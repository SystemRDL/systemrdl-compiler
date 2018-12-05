
import sys
import enum

from antlr4.error.ErrorListener import ErrorListener
from antlr4.Token import CommonToken
from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

import colorama
from colorama import Fore, Style

# Colorama needs to be initialized to properly work in Windows
# This is a no-op in other OSes
colorama.init()

#===============================================================================
class RDLCompileError(Exception):
    """
    Base class for all SystemRDL compiler exceptions
    """
    
#===============================================================================
class Severity(enum.IntEnum):
    NONE = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3

#===============================================================================
class MessageHandler:
    def __init__(self, printer):
        self.printer = printer
        self.warning_count = 0
        self.error_count = 0
    
    def message(self, severity, text, src_ref=None):
        if severity == Severity.WARNING:
            self.warning(text, src_ref)
        if severity == Severity.ERROR:
            self.error(text, src_ref)
        if severity == Severity.FATAL:
            self.fatal(text, src_ref)

    def warning(self, text, src_ref=None):
        self.printer.print_message(Severity.WARNING, text, src_ref)
        self.warning_count += 1
    
    def error(self, text, src_ref=None):
        self.printer.print_message(Severity.ERROR, text, src_ref)
        self.error_count += 1
    
    def fatal(self, text, src_ref=None):
        self.printer.print_message(Severity.FATAL, text, src_ref)
        raise RDLCompileError(text)
        
#===============================================================================
class SourceRef:
    """
    Reference to a segment of source.
    
    This is used to provide useful context to the original RDL source when
    reporting compiler messages.
    """
    def __init__(self, start, end, filename=None, seg_map=None):
        
        #: SegmentMap object that provides character coordinate mapping table
        self.seg_map = seg_map
        
        #: Character position of start of selection
        self.start = start
        
        #: Character position of end of selection
        self.end = end
        
        #: Path to file from start of selection
        self.filename = filename
        
        #: Line number of start of selection
        self.start_line = None
        
        #: Column of first character in selection
        self.start_col = None
        
        #: Line number of end of selection
        self.end_line = None
        
        #: Column of last character in selection
        self.end_col = None
        
        #: Raw line of text that corresponds to start_line
        self.start_line_text = None
    
    def derive_coordinates(self):
        """
        Depending on the compilation source, some members of the SourceRef
        object may be incomplete.
        Calling this function performs the necessary derivations to complete the
        object.
        """
        if self.seg_map is not None:
            # Translate coordinates
            self.start, self.filename, include_ref = self.seg_map.derive_source_offset(self.start)
            self.end, end_filename, _ = self.seg_map.derive_source_offset(self.end, is_end=True)
        else:
            end_filename = self.filename
        
        line_start = 0
        lineno = 1
        file_pos = 0
        
        # Skip deriving end coordinate if selection spans multiple files
        if self.filename != end_filename:
            get_end = False
        else:
            get_end = True
        
        
        with open(self.filename, 'r', newline='', encoding='utf_8') as fp:
            
            while True:
                line_text = fp.readline()
                
                file_pos += len(line_text)
                
                if line_text == "":
                    break
                
                if (self.start_line is None) and (self.start < file_pos):
                    self.start_line = lineno
                    self.start_col = self.start - line_start
                    self.start_line_text = line_text.rstrip("\n").rstrip("\r")
                    if not get_end:
                        break
                
                if get_end and (self.end_line is None) and (self.end < file_pos):
                    self.end_line = lineno
                    self.end_col = self.end - line_start
                    break
                
                lineno += 1
                line_start = file_pos
        
        # If no end coordinate was derived, just do a single char selection
        if not get_end:
            self.end_line = self.start_line
            self.end_col = self.start_col
            self.end = self.start
        
    
    @classmethod
    def from_antlr(cls, antlr_ref):
        from .preprocessor.preprocessor import PreprocessedInputStream
        
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
        
        # Get source segment map
        inputStream = token.getInputStream()
        if isinstance(inputStream, PreprocessedInputStream):
            seg_map = inputStream.seg_map
        else:
            seg_map = None
        
        # Extract selection coordinates
        start = token.start
        if end_token is None:
            end = token.stop
        else:
            end = end_token.stop
        
        # Create object
        src_ref = cls(start, end, seg_map=seg_map)
        return src_ref
    
    @classmethod
    def from_antlr_recognizer(cls, recognizer):
        from .preprocessor.preprocessor import PreprocessedInputStream
        
        inputStream = recognizer.inputStream
        if isinstance(inputStream, PreprocessedInputStream):
            seg_map = inputStream.seg_map
        else:
            seg_map = None
        
        idx = recognizer.getCharIndex()
        
        # Create object
        src_ref = cls(idx, idx, seg_map=seg_map)
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
        severity: :class:`Severity`
            Message severity.
        text: str
            Body of message
        src_ref: :class:`SourceRef`
            Reference to source context object
        
        Returns
        -------
        list
            List of strings for each line of the message
        """
        lines = []
        
        if severity >= Severity.ERROR:
            color = Fore.RED
        else:
            color = Fore.YELLOW
            
        if src_ref is None:
            lines.append(
                color + Style.BRIGHT + severity.name().lower() + ": " + Style.RESET_ALL + text
            )
        else:
            src_ref.derive_coordinates()
            
            lines.append(
                Fore.WHITE + Style.BRIGHT
                + "%s:%d:%d: " % (src_ref.filename, src_ref.start_line, src_ref.start_col)
                + color + severity.name().lower() + ": "
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
                    + color + Style.BRIGHT
                    + src_ref.start_line_text[src_ref.start_col:]
                    + Style.RESET_ALL 
                )
                
                lines.append(
                    " "*src_ref.start_col 
                    + color + Style.BRIGHT
                    + "^"*width
                    + Style.RESET_ALL
                )
                
            else:
                # Single line
                width = src_ref.end_col - src_ref.start_col + 1
                
                lines.append(
                    src_ref.start_line_text[:src_ref.start_col] 
                    + color + Style.BRIGHT
                    + src_ref.start_line_text[src_ref.start_col : src_ref.end_col+1]
                    + Style.RESET_ALL 
                    + src_ref.start_line_text[src_ref.end_col+1:]
                )
                
                lines.append(
                    " "*src_ref.start_col 
                    + color + Style.BRIGHT
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
        if offendingSymbol is not None:
            src_ref = SourceRef.from_antlr(offendingSymbol)
        elif recognizer is not None:
            # If a offendingSymbol is not provided, then the next-best option is
            # to use the current recognizer's state
            src_ref = SourceRef.from_antlr_recognizer(recognizer)
        else:
            # Out of options to provide context
            src_ref = None
        
        self.msg.error(
            msg,
            src_ref
        )
