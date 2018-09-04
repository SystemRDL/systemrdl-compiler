import colorama

class SegmentMap:
    
    def __init__(self):
        self.segments = []
    
    def derive_source_offset(self, offset, is_end=False):
        """
        Given a post-preprocessed coordinate, derives the corresponding coordinate
        in the original source file.
        
        Returns result in the following tuple:
            (src_offset, src_path, include_ref)
        where:
            - src_offset is the translated coordinate
                If the input offset lands on a macro expansion, then src_offset
                returns the start or end coordinate according to is_end
            - src_path points to the original source file
            - include_ref describes any `include lineage using a IncludeRef object
                Is none if file was not referenced via include
        """
        for segment in self.segments:
            if offset <= segment.end:
                if isinstance(segment, MacroSegment):
                    if is_end:
                        return (
                            segment.src_end,
                            segment.src,
                            segment.incl_ref
                        )
                    else:
                        return (
                            segment.src_start,
                            segment.src,
                            segment.incl_ref
                        )
                else:
                    return (
                        segment.src_start + (offset - segment.start),
                        segment.src,
                        segment.incl_ref
                    )
        
        # Reached end. Assume end of last segment
        return (
            self.segments[-1].src_end,
            self.segments[-1].src,
            self.segments[-1].incl_ref
        )


class Segment:
    """
    Base class for various segment map segments.
    Not to be used directly
    """
    def __init__(self, start, end, src_start, src_end, src, incl_ref = None):
        
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
        
        # IncludeRef object that describes from where this segment was included
        self.incl_ref = incl_ref

class UnalteredSegment(Segment):
    """
    Segment of unaltered text
    """
    
class MacroSegment(Segment):
    """
    Segment of text that was the result of a macro transformation
    """

class IncludeRef:
    def __init__(self, start, end, path, parent=None):
        # Location of the `include statement
        self.start = start
        self.end = end
        self.path = path
        
        # Reference to parent IncludeRef if nested include
        self.parent = parent


def print_segment_debug(text, smap): # pragma: no cover
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
    