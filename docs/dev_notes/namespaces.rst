
Namespaces
==========

Namespaces are only relevant during compilation in order to keep track of all
declared objects available in the current scope.

There are three distinct namespaces:

Type Namespace
    * Component definitions
    * enum/struct types

Element Namespace
    * Component instances
    * Parameters

Property Namespace
    * Contains builtin and user-defined properties


Each has slightly different lookup rules:

Type
    * Resolved by searching local scope, and traversing up until a match is
      found.

Element
    * Resolve in local scope only.
    * Only exception is a 'signal' instance that effectively uses 'type'
      namespace search rules.

Property
    * Global namespace
    * User-defined properties can only be added in the root namespace.


Implementation
--------------

A single namespace registry class exists throughout compilation that manages
namespaces. This single instance is carried through the compiler everywhere.

As objects are defined/instantiated, they are registered with the namespace
using the following methods:

* .register_element(name, ref)
* .register_type(name, ref)
* .register_property(name, ref)

At any point, the compiler can query the namespace:

* .lookup_element(name)
* .lookup_type(name)
* .lookup_property(name)

The above return None if not found.

Changing scope when entering/exiting a component definition:

.enter_scope()
    pushes a blank scope onto the type-stack and element-stack

.exit_scope()
    pop and discard top of type-stack and element-stack

Hierarchical references are handled elsewhere. Component instances are
traversed manually.
