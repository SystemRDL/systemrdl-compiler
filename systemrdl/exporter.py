
from .compiler import RDLEnvironment

class RDLExporter:
    """
    Base class for exporters that generate outputs from the register model
    """
    def __init__(self, env:RDLEnvironment):
        self.env = env
        self.msg = env.msg
