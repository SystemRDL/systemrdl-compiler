
Known Issues & Limitations
==========================

This page lists anything from the SystemRDL 2.0 spec that the
``systemrdl-compiler`` does not support yet.



Constraints
-----------

SystemRDL ``constraint`` blocks are not implemented yet.



Limited support for heterogeneous arrays
----------------------------------------

RDL spec allows parameters to be overridden via a dynamic property assignment.
One feature described is the ability to modify a subset of an array of
instances via a dynamic property assignment. This would result in an array of
instances that no longer share the same properties.

Indexed dynamic property assignments are supported **only** for the ``reset``
property. This allows per-element reset values without changing the structural
layout of the array (for example, ``my_inst[2].field->reset = 8'hFF``).

All other properties, array sub-ranges, and references that index more than
one array in the same path remain unsupported.

For example:

.. code-block:: systemrdl

    my_reg my_inst[16];

    // Modifying all instances in the array is supported
    my_inst->some_property = 1234;

    // Modifying a single element's reset is supported
    my_inst[2].field->reset = 8'hFF;

    // Everything else is not supported
    my_inst[2]->some_property = 1234;
    my_inst[1:4]->some_property = 1234;
    my_inst[0:15]->some_property = 1234;



Property assignments using references shall be constant
-------------------------------------------------------

Use of property or component references are only supported if the resulting
assignment value can be determined during RDL elaboration-time.

Supported:
    .. code-block:: systemrdl

            some_property = PARAMETER ? my_reg.my_field : my_reg.my_field->some_property;

Not supported:
    .. code-block:: systemrdl

            some_property = my_signal ? my_field : my_field->some_property;
