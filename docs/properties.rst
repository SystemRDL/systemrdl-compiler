
Properties
==========

SystemRDL Properties
--------------------

All built-in and user-defined SystemRDL component properties can be accessed
using the :meth:`Node.get_property() <systemrdl.node.Node.get_property>`
interface.

If a property was not explicitly set in the RDL source, its default or implied
value will be returned. When using the ``get_property()`` interface, any
instance references are converted to their
representative :class:`~systemrdl.node.Node` objects.


Implied Property Values
-----------------------
The SystemRDL language describes numerous properties. Many of them are very
closely interrelated. Even if not explicitly assigned, some of these may inherit
an implied value based on other properties. In order to simplify the designer's
job of interpreting user input, the SystemRDL compiler's :meth:`Node.get_property() <systemrdl.node.Node.get_property>`
method will automatically return these implied default values.

For example:

.. code-block:: systemrdl

    field my_field {
        sw=rw;
        rclr;
    };

The above example describes a field that is cleared when software reads it.
Although not explicitly set, if you were to do the following query:
``my_field.get_property('onread')``, it would return the value
:attr:`OnReadType.rclr <systemrdl.rdltypes.builtin_enums.OnReadType.rclr>`, as if the user assigned it as follows:

.. code-block:: systemrdl

    field my_field {
        sw=rw;
        onread = rclr;
    };


Other properties that may infer a value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(This is not an exhaustive list!)

* If not explicitly set, ``resetsignal`` may return a signal marked with
  ``field_reset`` in the enclosing hierarchy.
* ``rclr`` and ``rset`` can be implied from ``onread`` and vice-versa.
* ``woclr`` and ``woset`` can be implied from ``onwrite`` and vice-versa.
* ``incrvalue`` and ``decrvalue`` may infer a value of 1 for counters that do
  not specify otherwise.
* ``stickybit`` is true for interrupt fields unless specified otherwise.
* ``accesswidth`` defaults to the width of the register.
* ``fieldwidth`` and ``signalwidth`` will inherit from their field/signal
  instance widths respectively.
* Boolean property pairs that imply the opposites of each-other:

    * ``sync`` and ``async``
    * ``bigendian`` and ``littleendian``
    * ``msb0`` and ``lsb0``



Derived Properties
------------------

The ``systemrdl-compiler`` provides additional derived properties that intend
to further simplify interpretation of the compiled register model. These derived
properties may query multiple characteristics to determine their value.

Some examples:

* :data:`AddressableNode.absolute_address <systemrdl.node.AddressableNode.absolute_address>`
* :data:`FieldNode.implements_storage <systemrdl.node.FieldNode.implements_storage>`
* :data:`RegNode.is_virtual <systemrdl.node.RegNode.is_virtual>`

See the :ref:`api_node` class reference for more details.
