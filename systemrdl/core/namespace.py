from .. import component as comp

class NamespaceRegistry():
    
    def __init__(self, env):
        self.env = env
        self.msg = env.msg
        
        self.type_ns_stack = [{}]
        self.element_ns_stack = [{}]
        self.default_property_ns_stack = [{}]
    
    def register_type(self, name:str, ref, src_ref):
        if name in self.type_ns_stack[-1]:
            self.msg.fatal(
                "Multiple declarations of type '%s'" % name,
                src_ref
            )
        self.type_ns_stack[-1][name] = ref
        
    def register_element(self, name:str, ref, parent_comp_def, src_ref):
        if name in self.element_ns_stack[-1]:
            self.msg.fatal(
                "Multiple declarations of instance '%s'" % name,
                src_ref
            )
        self.element_ns_stack[-1][name] = (ref, parent_comp_def)
    
    def register_default_property(self, name:str, ref, src_ref, overwrite_ok=False):
        if not overwrite_ok:
            if name in self.default_property_ns_stack[-1]:
                self.msg.fatal(
                    "Default property '%s' was already assigned in this scope" % name,
                    src_ref
                )
        
        self.default_property_ns_stack[-1][name] = (src_ref, ref)
    
    def lookup_type(self, name:str):
        for scope in reversed(self.type_ns_stack):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_element(self, name:str):
        for idx, scope in enumerate(reversed(self.element_ns_stack)):
            if name in scope:
                el, parent_def = scope[name]
                if idx == 0:
                    # Return anything from local namespace
                    return (el, parent_def)
                elif isinstance(el, comp.Signal):
                    # Signals are allowed to be found in parent namespaces
                    return (el, parent_def)
                else:
                    return (None, None)
        return (None, None)
    
    def get_default_properties(self, comp_type):
        """
        Returns a flattened dictionary of all default property assignments
        visible in the current scope that apply to the current component type.
        """
        # Flatten out all the default assignments that apply to the current scope
        # This does not include any default assignments made within the current
        # scope, so exclude those.
        props = {}
        for scope in self.default_property_ns_stack[:-1]:
            props.update(scope)
            
        # filter out properties that are not relevant
        prop_names = list(props.keys())
        for prop_name in prop_names:
            rule = self.env.property_rules.lookup_property(prop_name)
            if rule is None:
                self.msg.fatal(
                    "Unrecognized property '%s'" % prop_name,
                    props[prop_name][0]
                )
            if comp_type not in rule.bindable_to:
                del props[prop_name]
            
        return props
    
    def enter_scope(self):
        self.type_ns_stack.append({})
        self.element_ns_stack.append({})
        self.default_property_ns_stack.append({})
        
    def exit_scope(self):
        self.type_ns_stack.pop()
        self.element_ns_stack.pop()
        self.default_property_ns_stack.pop()
