
Hierarchical References
=======================

Encoding references to components is an interesting problem since they need to
work properly in all sorts of assignment scenarios.

**Assignment scenarios (LHS)**

* Direct (local) property assignment:
    ``property = RHS;``
* Dynamic (hierarchical) property assignment:
    ``hier.path.to->property = RHS;``
* Default property assignment:
    ``default property = RHS;``

**Reference types (RHS)**

Local instance ref
    Reference a component instance that is instantiated locally, in the
    current scope.

Hierarchical instance ref
    Reference an instance using one or more dot operators, though instance
    children

Parent scope signal ref
    Signals from an enclosing parent lexical scope are available to be
    referenced


Implementation
--------------

Compile Phase
^^^^^^^^^^^^^

Whenever a component is instantiated, the instance is registered into the
element namespace. Along with the instance handle, a handle to the parent
definition (non-instance) component is stored. This becomes useful later.

When building an expression tree, and an instance reference is encountered,
it is encoded as an expressions.InstRef object.

This object contains the following:

* Handle to a component def object to use as a path startpoint (ref_root)
  This is the parent definition that was stored in the element namespace
  earlier.
* List of hierarchical path segments (ref_elements)
  Each segment consists of an identifier token, and a list of array
  suffix ASTNode

As usual, after an expression tree is built, predict_type() is called.
For InstRef expression nodes, the following is performed:

* Predict types of each index expression and check if it is numeric.
* Starting at ref_root, traverse each path segment to determine if the
  referenced instance exists.
* Once the target is reached, return its component type.

Elaborate Phase
^^^^^^^^^^^^^^^

During elaboration, property values are resolved.
When InstRef.get_value() is called, a very similar looking object,
rdl_types.ComponentRef() is created.

In this object:

* ref_root remains the same
* ref_elements is resolved so that identifiers are now strings, and array
  indexes are evaluated into normal integers.

ComponentRef is still not in a very useful form, but it contains the
information required to re-construct the reference.

During validation, when property values are checked, any resulting out-of-range
array indexes are checked and caught.


During User Traversal
^^^^^^^^^^^^^^^^^^^^^

Transformation of the reference is deferred all the way to the end when
the property is fetched by the user through the Node interface via
Node.get_property().

Rather than returning the ComponentRef object, the get_property function
reconstructs the reference using a Node overlay lineage, and grafts it onto
the current traversal tree.

Providing a Node overlay object is way more useful to the user since it is
consistent with other traversal methods, and also provides an unambiguous
reference to the target component.

The contents of ComponentRef are used as follows:

* Given a startpoint node (where the property assignment was applied),
  traverse up through Node.parent until a node is reached that was derived
  from the component def described by ComponentRef.ref_root
* Once the reference node is found, use ComponentRef.ref_elements to traverse
  back down to the appropriate child Nodes until the target is reached.

The resulting Node object is returned to the user.
