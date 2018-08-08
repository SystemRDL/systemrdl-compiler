
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
    
class IncludedSegment(Segment):
    """
    Segment of text that was included from another file
    """
    def __init__(self, start, end, src_start, src_end, src, incl_start, incl_end, incl_src):
        super().__init__(start, end, src_start, src_end, src)
        
        # Location of the include pragma itself
        self.incl_start = incl_start
        self.incl_end = incl_end
        self.incl_src = incl_src