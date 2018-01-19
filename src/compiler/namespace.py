from ..model import component as comp

class NamespaceRegistry():
    
    def __init__(self):
        self.type_ns_stack = [{}]
        self.element_ns_stack = [{}]
        self.property_ns = {}
    
    def register_type(self, name:str, ref):
        if(name in self.type_ns_stack[-1]):
            raise ValueError("Multiple declarations of type '%s'" % name)
        self.type_ns_stack[-1][name] = ref
        
    def register_element(self, name:str, ref):
        if(name in self.element_ns_stack[-1]):
            raise ValueError("Multiple declarations of instance '%s'" % name)
        self.element_ns_stack[-1][name] = ref
    
    def register_property(self, name:str, ref):
        if(name in self.property_ns):
            raise ValueError
        self.property_ns[name] = ref
        
    def lookup_type(self, name:str):
        for scope in reversed(self.type_ns_stack):
            if(name in scope):
                return(scope[name])
        else:
            return(None)
    
    def lookup_element(self, name:str):
        for idx, scope in enumerate(reversed(self.element_ns_stack)):
            if(name in scope):
                el = scope[name]
                if(idx == 0):
                    # Return anything from local namespace
                    return(el)
                elif((type(el) == comp.VectorInst) and (type(el.typ) == comp.Signal)):
                    # Signals are allowed to be found in parent namespaces
                    return(el)
                else:
                    return(None)
        else:
            return(None)
    
    def lookup_property(self, name:str):
        if(name in self.property_ns):
            return(self.property_ns[name])
        else:
            return(None)
    
    def enter_scope(self):
        self.type_ns_stack.append({})
        self.element_ns_stack.append({})
        
    def exit_scope(self):
        self.type_ns_stack.pop()
        self.element_ns_stack.pop()