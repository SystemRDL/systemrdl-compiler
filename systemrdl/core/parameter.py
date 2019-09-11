from .value_normalization import normalize

class Parameter:
    def __init__(self, param_type, name, default_expr=None):
        self.name = name
        self.param_type = param_type

        self.expr = default_expr

        # Stores the evaluated result of self.expr so that subsequent queries do
        # not need to repeatedly re-evaluate it
        self._value = None

    def get_value(self):
        """
        Evaluate self.expr to get the parameter's value
        """
        if (self._value is None) and (self.expr is not None):
            self._value = self.expr.get_value()

        return self._value


    def get_normalized_parameter(self):
        """
        Converts the parameter to the normalized type name segment as defined in
        SystemRDL 2.0 Section 5.1.1.4-c

        Returns the whole parameter string:
            <parameter name> + "_" + <normalized value>
        """
        return self.name + "_" + normalize(self.get_value())
