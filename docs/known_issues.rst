
Known Issues & Limitations
==========================

This page lists anything from the SystemRDL 2.0 spec that the
``systemrdl-compiler`` does not support yet.

Limitations are listed roughly in order of priority, where the first items are
likely to be fixed the soonest.


Semantic Checking is Incomplete
-------------------------------

The SystemRDL spec implies hundreds of rules & semantics that need to be
enforced. Many of them are implicitly enforced by the language's syntax.
However, most others require additional post-compile checking in order to
validate.

Adding these semantic checks is an ongoing effort. I am keeping track of which
checks are implemented here:
:download:`semantic_checks.ods<implementation_notes/semantic_checks.ods>`



Constraints
-----------

SystemRDL ``constraint`` blocks are not implemented yet.




Partial implementation of Verilog Preprocessor
----------------------------------------------

The Verilog-style preprocessor currently only implements ```include`` directive
expansion.
Conditional and macro directives are not implemented yet. (```ifdef``,
```else``, ```define``, etc.)

As a workaround, equivalent preprocessing can be accomplished using the
embedded Perl preprocessor.



No support for non-homogeneous arrays
-------------------------------------

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

.. code-block:: none

    my_reg my_inst[16];

    // Modifying all instances in the array is supported
    my_inst -> some_property = 1234;

    // Modifying a subset is not supported
    my_inst[2] -> some_property = 1234;
    my_inst[1:4] -> some_property = 1234;
    my_inst[0:15] -> some_property = 1234;
