import re
import subprocess
import json
import shutil

from . import segment_map

def preprocess(env, input_text, parent_smap):
    """
    Run perl preprocessor on the text provided
    
    Returns: (text, SegmentMap)
    - text: Resulting preprocessed text
    - SegmentMap: Mapping object that provides back-references to original source
    """
    
    segments = parse_segments(env, input_text)
    
    if (len(segments) == 1) and isinstance(segments[0], PPPUnalteredSegment):
        # The only segment collected was a bypass.
        # No need to continue perl preprocessor
        output_text = input_text
        
        # Create a pass-through segment map
        smap = segment_map.SegmentMap()
        smap.segments.append(
            segment_map.UnalteredSegment(
                segments[0].start, segments[0].end,
                segments[0].start, segments[0].end, parent_smap
            )
        )
    else:
        # Execute remainder of perl preprocessor
        emit_list = run_miniscript(env, input_text, segments)
        output_text, smap = generate_output(parent_smap, input_text, segments, emit_list)
    
    return (output_text, smap)

#-------------------------------------------------------------------------------
# Preprocessor Internals
#-------------------------------------------------------------------------------
class PPPSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def get_text(self, input_text):
        return input_text[self.start:self.end+1]

class PPPUnalteredSegment(PPPSegment):
    pass

class PPPPerlSegment(PPPSegment):
    def get_text(self, input_text):
        return input_text[self.start+2:self.end-1]

class PPPMacroSegment(PPPSegment):
    def get_text(self, input_text):
        return input_text[self.start+3:self.end-1]


def parse_segments(env, text):
    """
    Parse input text and create a list of PPPSegments
    """
    # TODO: Rewrite this to use comment-aware tokenization
    
    segments = []
    pos = 0;
    
    while True:
        # Seek to start brace
        i = text.find('<%', pos)
        
        if i==-1:
            # Reached EOF
            if pos != len(text):
                pp_seg = PPPUnalteredSegment(pos, len(text)-1)
                segments.append(pp_seg)
            break
        
        if i != pos:
            pp_seg = PPPUnalteredSegment(pos, i-1)
            segments.append(pp_seg)
        
        pos = i
        
        # seek to end brace
        i = text.find('%>', pos+2)
        
        if i==-1:
            # Unmatched tag
            env.msg.fatal(
                "Unmatched Perl preprocessor tag"
                # TODO: add context
            )
        
        if text[pos+2] == '=':
            pp_seg = PPPMacroSegment(pos, i+1)
            segments.append(pp_seg)
        else:
            pp_seg = PPPPerlSegment(pos, i+1)
            segments.append(pp_seg)
        
        pos = i+2
    
    return segments


def run_miniscript(env, input_text, segments):
    """
    Generates and runs a perl miniscript that derives the text that will be
    emitted from the preprocessor
    
    returns the resulting emit list
    """
    
    # Check if perl is installed
    if shutil.which("perl") is None:
        env.msg.fatal(
            "Input contains Perl preprocessor tags, but an installation of Perl could not be found"
        )
    
    # Generate minimal perl script that captures activities described in the source file
    lines = []
    for i,pp_seg in enumerate(segments):
        if isinstance(pp_seg, PPPUnalteredSegment):
            # Text outside preprocessor tags that should remain unaltered
            # Insert command to emit reference to this text segment
            lines.append("rdlppp_utils::emit_ref(%d);" % i)
            
        elif isinstance(pp_seg, PPPPerlSegment):
            # Perl code snippet. Insert directly
            lines.append(pp_seg.get_text(input_text))
            
        elif isinstance(pp_seg, PPPMacroSegment):
            # Preprocessor macro print tag
            # Insert command to store resulting text
            var = pp_seg.get_text(input_text)
            
            # Check for any illegal characters
            if re.match(r'[\s;]', var):
                env.msg.fatal(
                    "Invalid text found in Perl macro expansion"
                    # TODO: Add context
                )
                raise RuntimeError("Invalid text in var emit thing")
            
            lines.append("rdlppp_utils::emit_text(%d, %s);" % (i, var))
    miniscript = '\n'.join(lines)
    
    # Run miniscript
    result = subprocess.run(
        ["perl","ppp_runner.pl"],
        input=miniscript.encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=5
    )
    if result.returncode:
        env.msg.fatal(
            "Encountered errors while executing embedded Perl preprocessor commands:\n"
            + result.stderr.decode("utf-8")
            # TODO: Add context
        )
        raise RuntimeError(result.stderr.decode("utf-8"))
    
    # miniscript returns the emit list in JSON format. Convert it
    emit_list = json.loads(result.stdout, encoding="utf-8")
    
    return emit_list


def generate_output(parent_smap, input_text, segments, emit_list):
    str_parts = []
    smap = segment_map.SegmentMap()
    
    offset = 0
    
    for entry in emit_list:
        if entry['type'] == "ref":
            pp_seg = segments[entry['ref']]
            emit_text = pp_seg.get_text(input_text)
            
            map_seg = segment_map.UnalteredSegment(
                offset, offset + len(emit_text) - 1,
                pp_seg.start, pp_seg.end, parent_smap
            )
            offset += len(emit_text)
            smap.segments.append(map_seg)
            str_parts.append(emit_text)
        
        elif entry['type'] == "text":
            pp_seg = segments[entry['ref']]
            emit_text = entry['text']
            
            map_seg = segment_map.MacroSegment(
                offset, offset + len(emit_text) - 1,
                pp_seg.start, pp_seg.end, parent_smap
            )
            offset += len(emit_text)
            smap.segments.append(map_seg)
            str_parts.append(emit_text)
    
    return ("".join(str_parts), smap)
