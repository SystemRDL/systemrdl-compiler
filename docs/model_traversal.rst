
Traversing the Register Model
=============================

Using the Walker/Listener
-------------------------

The easiest way to traverse a compiled register model is using a register-tree
listener interface, triggered by a :class:`~systemrdl.walker.RDLWalker`.

The listener interface is a collection of callback methods contained in a class
extended from :class:`~systemrdl.walker.RDLListener`. As the walker visits each
node, the type-specific callback method is triggered.

The built-in :class:`~systemrdl.walker.RDLWalker` performs a depth-first walk
through the register model as shown in the diagram below:

.. image:: img/walker-listener.svg
   :align: center


To create a listener, extend :class:`~systemrdl.walker.RDLListener` and implement
your custom callback methods. In the example below, ``MyListener`` prints a message
each time the walker enters and exits type-specific nodes:

.. code-block:: python
    
    from systemrdl import RDLListener, RDLWalker
    
    class MyListener(RDLListener):
        def enter_Addrmap(self, node):
            print("Entering addrmap", node.get_path())
        
        def exit_Addrmap(self, node):
            print("Exiting addrmap", node.get_path())
        
        def enter_Reg(self, node):
            print("Entering register", node.get_path())
            
        def exit_Reg(self, node):
            print("Exiting register", node.get_path())
        
        def enter_Field(self, node):
            print("Entering field", node.get_path())
        
        def exit_Field(self, node):
            print("Exiting field", node.get_path())


Next, the walker can be started using an instance of :class:`~systemrdl.walker.RDLWalker`. In this
example, the input ``root_node`` is assumed to represent the top-level addrmap
component called "top".

.. code-block:: python

    RDLWalker().walk(root_node, MyListener())


Results in the following output:

.. code-block:: none

    Entering addrmap top
    Entering register top.A[]
    Entering field top.A[].f1
    Exiting field top.A[].f1
    Entering field top.A[].f2
    Exiting field top.A[].f2
    Exiting register top.A[]
    Exiting addrmap top


To unroll all arrays during traversal, create a walker with loop unrolling enabled:

.. code-block:: python

    RDLWalker(unroll=True).walk(root_node, MyListener())

.. code-block:: none

    Entering addrmap top
    Entering register top.A[0]
    Entering field top.A[0].f1
    Exiting field top.A[0].f1
    Entering field top.A[0].f2
    Exiting field top.A[0].f2
    Exiting register top.A[0]
    Entering register top.A[1]
    Entering field top.A[1].f1
    Exiting field top.A[1].f1
    Entering field top.A[1].f2
    Exiting field top.A[1].f2
    Exiting register top.A[1]
    
    ... etc ...
    
    Exiting register top.A[3]
    Exiting addrmap top

Using Iterators
---------------

Sometimes it is necessary to have more fine-grain control of how the register model
is explored. The :meth:`Node.children() <systemrdl.node.Node.children>` method
provides an iterator that can be used to manually traverse the tree.

.. code-block:: python

    for child in root_node.children(unroll=True):
        print(child.get_path())

The above outputs the following:

.. code-block:: none

    top.A[0]
    top.A[1]
    top.A[2]
    top.A[3]


Other Methods
-------------

Node objects provide several other mechanisms to traverse the register model,
such as  :meth:`Node.get_child_by_name() <systemrdl.node.Node.get_child_by_name>`
or :meth:`Node.find_by_path() <systemrdl.node.Node.find_by_path>`.
See the class reference for more details.
