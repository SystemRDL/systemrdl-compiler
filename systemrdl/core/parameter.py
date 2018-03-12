
class Parameter:
    def __init__(self, param_type, name, default_expr=None):
        self.name = name
        self.param_type = param_type
        
        self.expr = default_expr
        