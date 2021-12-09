.. _dpa_type_generation:

Extended Type Name Generation
=============================

The SystemRDL 2.0 spec goes at great lengths to describe how component type
names are uniquified when parameters get overridden (5.1.1.4). Unfortunately
the spec falls short when it comes to accounting for dynamic property
assignments.

Dynamic property assignments (DPAs) have the capacity to override a component
instance's internal definition, and therefore break the ability for a user to
distinguish type equivalence based on the type name alone.

Consider the following example:

.. code:: systemrdl

    field my_field {
        sw = rw;
        hw = rw;
        we;
    };

    my_field A;
    my_field B;

    B->rclr = true;

Fields ``A`` and ``B`` are no longer equivalent types, yet they still have the
same type name!

Proposal is to extend the semantics described in 5.1.1.4 to also include
situations where a DPA changes a type's definition.

In the above example, the DPA would alter the type name
of field ``B`` from ``my_field`` to ``my_field_rclr_t``.

Proposal
--------

The semantics described in 5.1.1.4 for parameter overrides remain as-is,
however additional text to the type name may be appended to account for any
dynamic property assignments.

*   If the instance was not augmented by any dynamic property assignments, then
    no additional changes are made to the generated type name. Specifically:

    *   The instance's property values were all assigned using local property
        assignments. (no DPAs)
    *   No descendant instances were augmented by a dynamic property assignment
        originating from outside the current instance's definition.

Otherwise, the generated type name shall be extended as follows::

    <type_name>{_<param_name>_<normalized_value>}*{_<child_inst_name>_<normalized_child_type_name>}*{_<prop_name>_<normalized_value>}*

... where ``<type_name>``, ``<param_name>``, and ``<normalized_value>`` are
part of the original semantics from 5.1.1.4.


DPAs "through" the instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^
If a dynamic property assignment "reached through" the current instance and
overrode a descendant's property, append::

    _<child_inst_name>_<normalized_child_type_name>

... where:

*   ``<child_inst_name>`` represents the instance name of the immediate child
    of the current instance that was augmented by the DPA.
*   ``<normalized_child_type_name>`` is rendered by using the fully-resolved
    generated type name of the child instance, and hashing the same way string
    types are normalized in 5.1.1.4-c.3.
*   If multiple child instances were affected, append the above sequence in
    alphabetical order.

DPAs to the instance's properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If an instance's property value was overridden by a dynamic property
assignment, append::

    _<prop name>_<normalized_value>

*   Derive the normalized value the same rules as defined in 5.1.1.4-c, as well
    as the extended rules in the following section.
*   If multiple properties were assigned, append the above sequence in
    alphabetical order.

Additional type normalization semantics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The types encountered in in dynamic property assignments go beyond what is
described in 5.1.1.4-c. This section defines additional normalization rules for
these types.

Instance reference
    An instance reference is normalized by deriving the relative hierarchical
    path from the current instance to the referenced instance. The normalized
    value is the first eight characters of the md5 of the path.

    Hierarchy separators shall use ``.``, and parent references use ``^``.

    For example, the hierarchical path from component ``foo.bar.baz`` to
    ``foo.abc.def`` is represented by the string ``^.^.abc.def``

    The resulting 8-characters of md5 are: b0698608

Property reference
    Property references (ref targets) are normalized the same as instance
    references, except the property reference is included in the path prior
    to the md5 operation. There shall be no spaces between the property
    reference operator.

    For example, a property reference from component ``foo.bar.baz`` to
    the property ``foo.abc.def->anded`` is represented by the string
    ``^.^.abc.def->anded``.

    The resulting 8-characters of md5 are: 429a9577

Enum type references
    Enum type references shall be rendered using their enumeration type name.


Example
-------

.. code:: systemrdl

    reg my_reg {
        field my_field {
            sw = rw;
            hw = rw;
            we;
        };

        my_field f1;
        my_field f2;
        f2->rclr;
    };

    my_reg r0;

    my_reg r1;
    r1.f1->rclr;

    my_reg r2;
    r2.f1->next = r0.f1;

The type names for each instance in this example are generated as follows:

* ``r0.f1`` = "my_field"
* ``r0.f2`` = "my_field_rclr_t"
* ``r0`` = "my_reg"
* ``r1.f1`` = "my_field_rclr_t"
* ``r1.f2`` = "my_field_rclr_t"
* ``r1`` = "my_reg_f1_4e12afb6"
* ``r2.f1`` = "my_field_next_c9e1f96f"
* ``r2.f2`` = "my_field_rclr_t"
* ``r2`` = "my_reg_f1_e0f883f9"
