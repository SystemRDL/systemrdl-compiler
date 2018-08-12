import colorama

class SegmentMap:
    
    def __init__(self):
        self.segments = []


class Segment:
    def __init__(self, start, end, src_start, src_end, src):
        
        # start/end offset of resulting text
        self.start = start
        self.end = end
        
        # start/end offset of original text
        # Offsets are relative to src
        self.src_start = src_start
        self.src_end = src_end
        
        # where the original text came from
        # If str, then this is a file path
        # otherwise this is another SegmentMap
        self.src = src

class UnalteredSegment(Segment):
    """
    Segment of unaltered text
    """
    
class MacroSegment(Segment):
    """
    Segment of text that was the result of a macro transformation
    """
    
class IncludedSegment(UnalteredSegment):
    """
    Segment of text that was included from another file
    """
    def __init__(self, start, end, src_start, src_end, src, parent):
        super().__init__(start, end, src_start, src_end, src)
        
        # IncludeRef object that describes from where this segment was included
        self.parent = parent

class IncludeRef:
    def __init__(self, start, end, path, parent=None):
        # Location of the `include statement
        self.start = start
        self.end = end
        self.path = path
        
        # Reference to parent IncludeRef if nested include
        self.parent = parent

def print_segment_debug(text, smap):
    colors = (
        colorama.Back.RED,
        colorama.Back.GREEN,
        colorama.Back.YELLOW,
        colorama.Back.BLUE,
        colorama.Back.MAGENTA,
        colorama.Back.CYAN,
        colorama.Back.WHITE,
    )
    
    color_idx = 0
    out_str_parts = []
    for seg in smap.segments:
        out_str_parts.append(colors[color_idx] + text[seg.start:seg.end+1])
        color_idx = (color_idx+1) % len(colors)
    out_str_parts.append(colorama.Back.RESET)
    
    print("".join(out_str_parts))
    