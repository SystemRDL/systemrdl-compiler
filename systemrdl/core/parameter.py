from typing import TYPE_CHECKING, Optional, Any
from .value_normalization import normalize

if TYPE_CHECKING:
    from .. import rdltypes
    from .expressions import Expr

class Parameter:
    def __init__(self, param_type: 'rdltypes.PreElabRDLType', name: str, default_expr: Optional['Expr']=None):
        self.name = name
        self.param_type = param_type

        self.expr = default_expr

        # Stores the evaluated result of self.expr so that subsequent queries do
        # not need to repeatedly re-evaluate it
        self._value = None # type: Any

    def get_value(self) -> Any:
        """
        Evaluate self.expr to get the parameter's value
        """
        if (self._value is None) and (self.expr is not None):
            self._value = self.expr.get_value()

        return self._value


    def get_normalized_parameter(self) -> str:
        """
        Converts the parameter to the normalized type name segment as defined in
        SystemRDL 2.0 Section 5.1.1.4-c

        Returns the whole parameter string:
            <parameter name> + "_" + <normalized value>
        """
        return self.name + "_" + normalize(self.get_value())
