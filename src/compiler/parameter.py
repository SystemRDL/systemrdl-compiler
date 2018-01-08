
class Parameter:
    def __init__(self, param_type, name, default_expr=None):
        self.name = name
        self.param_type = param_type
        
        self.check_compatible(default_expr)
        self.expr = default_expr
        
    def check_compatible(self, expr):
        print("TODO: Check that expr is compatible with param_type")
        
    def set_inst_value(self, expr):
        """
        During an instantiation, set the override for the parameter
        """
        self.check_compatible(expr)
        
        self.expr = expr
        
    def get_value(self):
        raise NotImplementedError
        return(None)
        