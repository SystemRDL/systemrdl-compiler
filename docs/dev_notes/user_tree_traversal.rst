
The 'Node' User-interface
=========================

When traversing the tree, the user will interact with the object model solely
through the simplified interface provided by the Node object.

Even though the Component class reference tree is an accurate representation
of the compiled SystemRDL, it is cumbersome to use since all references are
in the top-down direction (parent --> child). This makes upward traversal
impossible for certain queries (absolute address, full path, etc)::

                        /---> comp_X
                        |
    top_comp --> comp_A[*] --> comp_B --> comp_C

The Node is an overlay class that is bound to each instance as the design
is traversed hierarchically. Lineage of the node overlay is maintained in the
bottom-up direction which completes bi-directional linking.
The node overlay also provides current array index information so that
references to specific instances are unambiguous::

                        /---> comp_X
                        |
    top_comp --> comp_A[*] --> comp_B --> comp_C
        |           |             |          |
    top_node <-- node_A[3] <-- node_B <-- node_C
                        ^
                        \---- node_X


Direct RDL property access
--------------------------

Use the following method to lookup the value::

    result = node.get_property('my_prop')

``get_property`` is implemented roughly as follows:

- Is it in the component's property dictionary?

    - if so, return the value

- Otherwise, Is it even a valid property of this component type?
- Return the default value as specified by the rulebook
- If the rulebook contains <TBD> as the default, then
  a more dynamic resolution needs to be made
