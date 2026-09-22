
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


Limited support for heterogeneous arrays
----------------------------------------

RDL spec allows parameters to be overridden via a dynamic property assignment.
One feature described is the ability to modify a subset of an array of
instances via dynamic assignment. This would result in an array of instances
that no longer share the same properties.

The compiler provides **limited** support for this via indexed dynamic
property assignments, restricted to the ``reset`` property only. This allows
per-element reset values (for example, ``my_inst[2].field->reset = 8'hFF``)
without altering the structural layout of the array.

All other properties, array sub-ranges (``my_inst[1:4]``), and indexed
assignments targeting more than one array in the same reference path are not
supported.

For example:

.. code:: systemrdl

    my_reg my_inst[16];

    // Modifying all instances in the array is supported
    my_inst->property = 1234;

    // Modifying a single element's reset is supported
    my_inst[2].field->reset = 8'hFF;

    // Everything else is not supported
    my_inst[2]->property = 1234;
    my_inst[1:4]->property = 1234;
    my_inst[0:15]->property = 1234;
    my_inst[0].other_array[1].field->reset = 8'hFF;

When an indexed dynamic property assignment targets one array element, the
compiler stores a per-element override in ``AddressableComponent.array_element_overrides``.
Elements without an entry continue to share the array's component tree.
Override instances retain the parent array's ``array_dimensions`` and
``array_stride`` so that addressing and unrolling behave consistently.
