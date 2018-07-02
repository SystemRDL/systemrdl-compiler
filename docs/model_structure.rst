
Register Model Structure
========================

Component Tree
--------------
After compilation, the resulting register model is modeled as an object tree.

Consider the following snippet of SystemRDL:

.. code-block:: none

    reg my_reg_t {
        field {} f1;
        field {} f2;
    };
    
    addrmap top {
        my_reg_t A;
        my_reg_t B[4];
    };

Once compiled, the resulting component tree is as follows:

.. image:: img/component-tree.svg
   :align: center

The resulting tree has the following characteristics:

- Each component instance is represented by a :class:`~systemrdl.component.Component` object.
- Any instances within a component are referenced as children of the component.
- All instances and their descendants are unique objects.
- Instances of a named definition (for example, ``my_reg_t``) including their descendants are unique, but
  refer back to copy of the original defined component.
- Arrays of instances are encoded as a single object and storing the array's dimensions.

Node Overlay
------------

The "Node" overlay is an additional data structure that is used to make model traversal
unambiguous. 

Each :class:`~systemrdl.node.Node` object provides the following:

- Reference to its corresponding :class:`~systemrdl.component.Component` instance.
- Reference to its immediate parent
- The current array index of an instance.
- Helper functions that simplify querying and traversing the register model.

Most of the your interaction with the register model should be through
:class:`~systemrdl.node.Node` objects.

When the you traverse the register model, :class:`~systemrdl.node.Node` objects are
dynamically created in order to provide unambiguous context as to which instance is being represented.

Consider the following lineage of instances from the previous example ``top -> A -> f1``.
Note that register "A" is declared as an array of 4 instances.

.. image:: img/node-overlay.svg
   :align: center

Since the overlay provides references back up to each node's parent as well as an array index,
the unambiguous lineage can be known. (purple ``f1`` node vs orange ``f1`` node)
