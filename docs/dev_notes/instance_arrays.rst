
Arrays of Instances
===================

Implementation
--------------

Arrays of instances are implemented by pushing array details onto the component
class being instantiated.
This is most efficient since the size of the array has no impact on model
footprint.

Component classes have two members to describe this:

* .array_dimensions
* .array_stride

.array_dimensions is a list of integers for every dimension of the array

The instantiation::

    my_reg my_inst[32][8]

is encoded as::

    .array_dimensions = [32,8]

If the component is not instantiated as an array, it uses the same class,
array_dimensions is set to None.


No support for heterogeneous arrays
-----------------------------------

RDL spec allows parameters to be overridden via a dynamic property assignment.
One feature described is the ability to modify a subset of an array of
instances via dynamic assignment. This would result in an array of instances
that no longer share the same properties.

For now, I see no convincing reason to support dynamic property modifications
to sub-ranges of an instance array.
Dynamic assignments will only be supported when modifying the entire instance
array, and without using an array subscript (even if the subscript is a range
that represents the entire array)

For example:

.. code:: systemrdl

    my_reg my_inst[16];

    // Modifying all instances in the array is supported
    my_inst->property = 1234;

    // Modifying a subset is not supported
    my_inst[2]->property = 1234;
    my_inst[1:4]->property = 1234;
    my_inst[0:15]->property = 1234;

Not only would this add a bunch of complexities to encoding this construct in a
register model, but it also would make downstream outputs a nightmare.
Having a heterogeneous array of something would require all kinds of nonsense
tricks to be done in model outputs (C headers, Verilog RTL).

A heterogeneous array would also end up being pretty conceptually confusing
to the end-user. It would be fundamentally better for the designer to simply
break something up into separate sets of instances that have different
behaviors.
