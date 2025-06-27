from typing import TYPE_CHECKING, Optional, Any

from .value_normalization import normalize

if TYPE_CHECKING:
    from .. import rdltypes
    from ..ast import ASTNode
    from ..node import Node

class Parameter:
    def __init__(self, param_type: 'rdltypes.PreElabRDLType', name: str, default_expr: Optional['ASTNode']=None):
        self.name = name
        self.param_type = param_type

        self.expr = default_expr


    def get_value(self, assignee_node: 'Node') -> Any:
        """
        Evaluate self.expr to get the parameter's value
        """
        if self.expr is None:
            # No expression was assigned
            return None

        return self.expr.get_value(assignee_node=assignee_node)


    def get_normalized_parameter(self, assignee_node: 'Node') -> str:
        """
        Converts the parameter to the normalized type name segment as defined in
        SystemRDL 2.0 Section 5.1.1.4-c

        Returns the whole parameter string:
            <parameter name> + "_" + <normalized value>
        """
        return self.name + "_" + normalize(self.get_value(assignee_node))
