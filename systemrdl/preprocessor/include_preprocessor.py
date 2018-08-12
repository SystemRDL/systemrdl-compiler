import re
import os

from . import segment_map


def preprocess(env, path, search_paths=None):
    """
    Expand includes on the file provided
    
    search_paths contains a list of additional paths to use to find the file
    
    Returns: (text, SegmentMap)
    - text: Resulting preprocessed text
    - SegmentMap: Mapping object that provides back-references to original source
    """
    
    if search_paths is None:
        search_paths = []
    
    smap = segment_map.SegmentMap()
    text = flatten_includes(env, path, search_paths, smap)
    
    return(text, smap)


def flatten_includes(env, path, search_paths, smap, incl_parent=None, out_pos=0):
    
    with open(path, 'r') as f:
        input_text = f.read()
        
    inc_tokens = tokenize(env, input_text)
    
    str_parts = []
    
    src_pos = 0
    for start, end, inc_path_raw, inc_path_start, inc_path_end in inc_tokens:
        
        # Emit any text from before the include
        if start != src_pos:
            emit_text = input_text[src_pos:start]
            emit_text_len = len(emit_text)
            if incl_parent is None:
                map_seg = segment_map.UnalteredSegment(
                    out_pos, out_pos + emit_text_len - 1,
                    src_pos, src_pos + emit_text_len - 1,
                    path
                )
            else:
                map_seg = segment_map.IncludedSegment(
                    out_pos, out_pos + emit_text_len - 1,
                    src_pos, src_pos + emit_text_len - 1,
                    path, incl_parent
                )
                
            out_pos += emit_text_len
            src_pos += emit_text_len
            smap.segments.append(map_seg)
            str_parts.append(emit_text)
        
        inc_path = inc_path_raw
        
        # Resolve include path.
        if os.path.isabs(inc_path_raw):
            inc_path = inc_path_raw
        else:
            # Search include paths first.
            for search_path in search_paths:
                inc_path = os.path.join(search_path, inc_path_raw)
                if os.path.isfile(inc_path):
                    # found match!
                    break
            else:
                # Otherwise, assume it is relative to the current file
                inc_path = os.path.join(os.path.dirname(path), inc_path_raw)
        if not os.path.isfile(inc_path):
            env.msg.fatal(
                "Could not find '%s' in include search paths" % inc_path_raw
                # TODO: add context
            )
        
         # Check if path has already been referenced before
        incl_ref = incl_parent
        while incl_ref:
            if os.path.samefile(inc_path, incl_ref.path):
                env.msg.fatal(
                    "Include of '%s' results in a circular reference" % inc_path_raw
                    # TODO: add context
                )
            incl_ref = incl_ref.parent
        
        # Recurse into the include
        incl_ref = segment_map.IncludeRef(start, end, path, incl_parent)
        emit_text = flatten_includes(env, inc_path, search_paths, smap, incl_ref, out_pos)
        emit_text_len = len(emit_text)
        out_pos += emit_text_len
        src_pos = end + 1
        str_parts.append(emit_text)
    
    # Emit any remaining text
    if len(input_text) > src_pos:
        emit_text = input_text[src_pos:]
        emit_text_len = len(emit_text)
        if incl_parent is None:
            map_seg = segment_map.UnalteredSegment(
                out_pos, out_pos + emit_text_len - 1,
                src_pos, src_pos + emit_text_len - 1,
                path
            )
        else:
            map_seg = segment_map.IncludedSegment(
                out_pos, out_pos + emit_text_len - 1,
                src_pos, src_pos + emit_text_len - 1,
                path, incl_parent
            )
        
        out_pos += emit_text_len
        src_pos += emit_text_len
        smap.segments.append(map_seg)
        str_parts.append(emit_text)
    
    return "".join(str_parts)
        
            
def tokenize(env, text):
    """
    Scans through the text and finds all `include directives
    
    Returns a list of tuples that represent the include tokens:
        (start, end, inc_path, inc_path_start, inc_path_end)
    where:
        start: Start position of the entire include directive
        end: End position of the entire include directive
        inc_path: Raw text of include path
        inc_path_start: Start position of the include path
        inc_path_end: End position of the include path
    """
    
    inc_tokens = []
    
    # Pre-compile Regex that captures the include contents
    inc_regex = re.compile(r'`include\s+("([^\r\n]+)"|<([^\r\n]+)>)')
    
    # Iterate through include tokens, including other spans of text that
    # could result in a false-positive match (like a commented out `include)
    # Note: Only white space or a comment may appear on the same line as the
    # `include compiler directive.
    token_spec = [
        ('inc', r'^[ \t]*(`include)'),
        ('mlc', r'/\*.*?\*/'),
        ('slc', r'//[^\r\n]*?$'),
        ('str', r'"(?:\\"|\\\\|[^"\\])*"'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
    for mo in re.finditer(tok_regex, text, re.DOTALL+re.MULTILINE):
        if mo.lastgroup != "inc":
            continue
        
        # Found `include token. Now attempt to capture the path string
        m_inc = inc_regex.match(text, mo.start(2))
        if m_inc is None:
            env.msg.fatal(
                "Invalid usage of include directive"
                # TODO: add context
            )
            
        inc_path = m_inc.group(2) or m_inc.group(3)
        
        inc_token = (
            m_inc.start(0),
            m_inc.end(0)-1,
            inc_path,
            m_inc.start(1),
            m_inc.end(1)-1,
        )
        inc_tokens.append(inc_token)
    
    return inc_tokens
