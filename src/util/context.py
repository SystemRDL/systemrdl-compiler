
class RDLContext:
    def __init__(self, inst, parent=None):
        self.inst = inst
        self.comp = inst.typ
        self.parent = parent
    
    def get_address(self):
        """
        Calculate the absolute address of this node
        """
        # TODO
        raise NotImplementedError
    
    def get_path(self, hier_separator=".", array_suffix="[{index:d}]"):
        """
        Generate an absolute path string to this node
        """
        # TODO
        raise NotImplementedError