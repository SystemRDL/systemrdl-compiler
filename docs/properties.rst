
Properties
==========

SystemRDL Properties
--------------------

All built-in and user-defined SystemRDL component properties can be accessed
using the :meth:`Node.get_property() <systemrdl.node.Node.get_property>` interface.

If a property was not explicitly set in the RDL source, its default or implied
value will be returned. When using the ``get_property()`` interface, any
instance references are converted to their
representative :class:`~systemrdl.node.Node` objects.

Derived Properties
------------------

The ``systemrdl-compiler`` provides additional derived properties that intend to
simplify interpretation of the compiled register model. These derived properties
may query multiple characteristics to determine their value.

Some examples:

* :data:`AddressableNode.absolute_address <systemrdl.node.AddressableNode.absolute_address>`
* :data:`FieldNode.implements_storage <systemrdl.node.FieldNode.implements_storage>`
* :data:`RegNode.is_virtual <systemrdl.node.RegNode.is_virtual>`

See the :ref:`api_node` class reference for more details.

Custom Derived Properties
-------------------------

If the built-in derived properties are insufficient, you can register your own
custom derived property so you can avoid repeating yourself.

.. code-block:: python
    
    from systemrdl import AddressableNode
    
    # Define a "getter" function
    def test_if_4k_aligned(node):
        if node.absolute_address % 0x1000 == 0:
            return True
        else:
            return False
    
    # Register it with the appropriate Node class
    AddressableNode.add_derived_property(test_if_4k_aligned, "is_4k_aligned")

Now, the derived property is available to be queried:

.. code-block:: python
    
    aligned = my_node.is_4k_aligned

.. note:: If you wrote your own derived property and think it should be added,
    let me know!