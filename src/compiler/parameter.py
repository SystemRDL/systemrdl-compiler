from . import expressions

class Parameter:
    def __init__(self, param_type, name, default_expr=None):
        self.name = name
        self.param_type = param_type
        
        # wrap expression in assignment cast
        default_expr = expressions.AssignmentCast(default_expr, param_type)
        
        self.expr = default_expr
        
    def set_inst_value(self, expr):
        """
        During an instantiation, set the override for the parameter
        """
        # wrap expression in assignment cast
        expr = expressions.AssignmentCast(expr, param_type)
        
        self.expr = expr
        
    def get_value(self):
        raise NotImplementedError
        return(None)
        