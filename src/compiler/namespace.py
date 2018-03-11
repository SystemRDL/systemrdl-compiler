from .errors import RDLCompileError, RDLNotSupportedYet
from ..model import component as comp
from . import expressions

class NamespaceRegistry():
    
    def __init__(self):
        self.type_ns_stack = [{}]
        self.element_ns_stack = [{}]
        self.default_property_ns_stack = [{}]
    
    def register_type(self, name:str, ref, err_token):
        if(name in self.type_ns_stack[-1]):
            raise ValueError("Multiple declarations of type '%s'" % name)
        self.type_ns_stack[-1][name] = ref
        
    def register_element(self, name:str, ref, err_token):
        if(name in self.element_ns_stack[-1]):
            raise ValueError("Multiple declarations of instance '%s'" % name)
        self.element_ns_stack[-1][name] = ref
    
    def register_default_property(self, name:str, ref, err_token):
        if(name in self.default_property_ns_stack[-1]):
            raise RDLCompileError(
                "Default property '%s' was already assigned in this scope" % name,
                err_token
            )
        
        # TODO: default properties that resolve to an instance reference
        # won't work properly yet.
        prop_token, rhs = ref
        if(issubclass(type(rhs), expressions.Expr)):
            result_type = rhs.predict_type()
            if(issubclass(result_type, comp.Component)):
                raise RDLNotSupportedYet(
                    "Assigning a reference to a component instance in a property default is not supported yet",
                    prop_token
                )
        
        self.default_property_ns_stack[-1][name] = ref
    
    def lookup_type(self, name:str):
        for scope in reversed(self.type_ns_stack):
            if(name in scope):
                return(scope[name])
        return(None)
    
    def lookup_element(self, name:str):
        for idx, scope in enumerate(reversed(self.element_ns_stack)):
            if(name in scope):
                el = scope[name]
                if(idx == 0):
                    # Return anything from local namespace
                    return(el)
                elif(type(el) == comp.Signal):
                    # Signals are allowed to be found in parent namespaces
                    return(el)
                else:
                    return(None)
        return(None)
    
    def get_default_properties(self, comp_type, PR):
        """
        Returns a flattened dictionary of all default property assignments
        visible in the current scope that apply to the current component type.
        Requires access to the current property rulebook (PR)
        """
        # Flatten current scope's assignments
        props = {}
        for scope in self.default_property_ns_stack:
            props.update(scope)
            
        # filter out properties that are not relevant
        prop_names = list(props.keys())
        for prop_name in prop_names:
            rule = PR.lookup_property(prop_name)
            if(rule is None):
                raise RDLCompileError(
                    "Unrecognized property '%s'" % prop_name,
                    props[prop_name][0]
                )
            if(comp_type not in rule.bindable_to):
                del props[prop_name]
            
        return(props)
    
    def enter_scope(self):
        self.type_ns_stack.append({})
        self.element_ns_stack.append({})
        self.default_property_ns_stack.append({})
        
    def exit_scope(self):
        self.type_ns_stack.pop()
        self.element_ns_stack.pop()
        self.default_property_ns_stack.pop()