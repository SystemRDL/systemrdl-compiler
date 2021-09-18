from typing import TYPE_CHECKING, Optional, Any, Dict
from copy import deepcopy

from .value_normalization import normalize

if TYPE_CHECKING:
    from .. import rdltypes
    from ..ast import ASTNode

class Parameter:
    def __init__(self, param_type: 'rdltypes.PreElabRDLType', name: str, default_expr: Optional['ASTNode']=None):
        self.name = name
        self.param_type = param_type

        self.expr = default_expr

        # Stores the evaluated result of self.expr so that subsequent queries do
        # not need to repeatedly re-evaluate it
        self._value = None # type: Any


    def __deepcopy__(self, memo: Dict[int, Any]) -> 'Parameter':
        """
        Never implicitly deepcopy a Parameter object. Parameters are pointed to
        by reference so that value overrides propagate through the expression
        tree correctly.
        """
        return self


    def _copy_for_inst(self, memo: Dict[int, Any]) -> 'Parameter':
        """
        Explicitly deepcopy this object. This is only used when instantiating
        the enclosing component
        """
        if id(self) in memo:
            return memo[id(self)]

        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


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
