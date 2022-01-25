
Known Issues & Limitations
==========================

This page lists anything from the SystemRDL 2.0 spec that the
``systemrdl-compiler`` does not support yet.



Constraints
-----------

SystemRDL ``constraint`` blocks are not implemented yet.



No support for heterogeneous arrays
-----------------------------------

RDL spec allows parameters to be overridden via a dynamic property assignment.
One feature described is the ability to modify a subset of an array of
instances via dynamic assignment. This would result in an array of instances
that no longer share the same properties.

Currently, I don't see a convincing reason to support dynamic property
modifications to sub-ranges of an instance array.
Dynamic assignments are only supported when modifying the entire instance
array, and without using an array subscript (even if the subscript is a range
that represents the entire array).

For example:

.. code-block:: systemrdl

    my_reg my_inst[16];

    // Modifying all instances in the array is supported
    my_inst -> some_property = 1234;

    // Modifying a subset is not supported
    my_inst[2] -> some_property = 1234;
    my_inst[1:4] -> some_property = 1234;
    my_inst[0:15] -> some_property = 1234;



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
