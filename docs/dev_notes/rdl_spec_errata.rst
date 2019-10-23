
.. _SystemRDL 2.0: http://accellera.org/downloads/standards/systemrdl

SystemRDL Spec Errata
=====================

This document keeps track of all ambiguities, contradictions, and typos found
in Accelera's `SystemRDL 2.0`_
language specification.

For each issue, I include the resolved interpretation that is used in this
project.


Semantic rule 10.6.1.c is violated in 5.1.2.2.2-Example 2
---------------------------------------------------------
Rule 10.6.1.c states that ``accesswidth`` cannot be greater than ``regwidth``.

However, in the example:

* reg 'a' has an implied regwidth of 32
* reg 'a' gets assigned an accesswidth of 64 via default.
  Results in accesswidth > regwidth!

**Resolution:**

The use-case shown in the example seems reasonable.
Rule 10.6.1.c seems unnecessary. Waiving checks for it.



Example in 6.2.6 uses an invalid hierarchical reference
-------------------------------------------------------
In section 6.2.6, an example shows a child component definition incorrectly
inheriting a parameter from its parent lexical scope:


.. code-block:: systemrdl

    regfile some_regfile #( my_struct arg ) {
        reg {
            desc = arg.inner.foo; // <-- Illegal out-of-scope reference to 'arg'
            field {} a;
        } regA;
    };

This is inconsistent with the namespace rules described in 5.1.4.
Also, 5.1.1.2-d explicitly says that nested component definitions do not inherit
parents' parameters.

**Resolution:**

Invalid example appears to be an accidental oversight.
Implementation will enforce semantics described in 5.1.1.2-d.



Grammar does not allow empty array literals
-------------------------------------------
The grammar in appendix B.10 shows that an array literal's
``array_literal_body`` requires at one or more instances of a
``constant_expression``

Section 6.3.1-d states that empty array literals are allowed to be declared
using the following:

.. code-block:: systemrdl

    left_hand_side = '{}


However based on appendix B.10, this is grammatically incorrect.

**Resolution:**

Arrays of zero-size seem like a reasonable concept, especially since 6.3.1-d
explicitly makes note of them.

Grammar is implemented to allow this.



Automatic address allocation rules have many ambiguities
--------------------------------------------------------
TODO: fill in details

**Resolution:**

TODO: fill in details




Invalid SystemRDL 2.0 in Table E1
---------------------------------
In Annex E, Table E1, many of the cells in the "SystemRDL 2.0" column show
what appears to be incorrect usage of the "onread" and "onwrite" side-effect
properties.

The table shows assignments of invalid rhs keywords such as:

* ``onread = r``
* ``onwrite = w``

... where ``r`` and ``w`` do not seem to be allowed in this context.

Section 9.6 shows that these properties only accept the ``onreadtype`` and
``onwritetype`` enumeration values.
These enumerations are defined in Table 15 and 16, as well as the grammar:

::

    onreadtype ::= rclr | rset | ruser
    onwritetype ::= woset | woclr | wot | wzs | wzc | wzt | wclr | wset | wuser


**Resolution:**

Ignore illegal assignments in Table E1.
This looks like a mistake by the author.
Invalid entries appear to be redundant anyways.



Constraint example uses struct datatype in an illegal way
---------------------------------------------------------
In 14.2.3, the example declares a struct data type called "RGB".
Immediately after, the struct is apparently "instantiated" as if it is a
component.

.. code-block:: systemrdl

    struct RGB {
        longint unsigned red1;
        longint unsigned green1;
        longint unsigned blue1;
    };

    reg regfoo {
        RGB pixelvalue;
    };

Nowhere in the SystemRDL spec does it describe the ability to do this. The
author seems to imply that the struct members are akin to register fields.
Furthermore, 6.3.2.1.2-a pretty clearly describes the use-cases for structs.

**Resolution:**

Based on the usage in the rest of the constraints example, it seems like
the author intended to imply that a register "regfoo" was declared to
contain three fields: red1, green1, blue1.
It will be assumed that the example does NOT include a struct declaration for
"RGB", but instead the following declaration for "regfoo":

.. code-block:: systemrdl

    reg regfoo {
        field {} red1[8];
        field {} green1[8];
        field {} blue1[8];
    };



Likely typo in semantic rule 11.2-f
-----------------------------------

    Virtual registers, **register files**, and fields shall have the same
    software access (sw property value) as the parent memory.

Mentions "register files", even though they are not allowed in "mem" components
as per 11.1-b-1-ii.


Likely typo in type name generation BNF snippet 5.1.1.4-c
---------------------------------------------------------

BNF-style description implies parentheses are part of the generated type name
but the text in the same section only mentions underscore delimiters.
Assuming the red parentheses are to be ignored.


Misc compilation issues in examples
-----------------------------------
Some very minor typos found while compiling several code snippet examples.
These issues do not have any significant effect on the interpretation of the
language.

5.1.2.5, Examples 1,2, and 3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All three examples fail to create an instance of `regfile example` inside
the `top` addrmap component. This results in an empty component definition
which violates the rule described in 13.3-b.

6.3.2.4, Examples 1 and 2
^^^^^^^^^^^^^^^^^^^^^^^^^
Numerous uses of "bool" instead of "boolean" keyword as described by grammar.

9.8.1, Example 1
^^^^^^^^^^^^^^^^
Illegal integer literal "4'3"

15.2.2, Example 1
^^^^^^^^^^^^^^^^^
Missing semicolon in some_num_p after "regfile"

15.2.2, Example 2
^^^^^^^^^^^^^^^^^
Enumeration literals are missing their "myEncoding::" prefix



RDLFormatCode paragraph tag listed as a single tag?
---------------------------------------------------
In annex F.2, the ``[p]`` paragraph tag is listed as a "single-tag" construct.
Since all the other tags seem to closely mirror HTML tags, this seems
out-of-place. The description from the phpBB site makes more sense since it
shows the paragraph tag as a pair: ``[p] paragraph text [/p]``.

Also, the example in F.4 shows the paragraph tag used as expected - as a pair.

**Resolution:**

Implement paragraph tag as an open/close pair.


.. _dev_notes-errata-rdlfc_desc:

Existence of the RDLFormatCode ``[desc]`` tag seems misguided
-------------------------------------------------------------
I fail to understand why the ``[desc]`` tag exists and how it could possibly be
useful.

If the ``[desc]`` tag is used within the ``desc`` property, then a recursive
self-reference is created.

If the ``[desc]`` tag is used in the ``name`` property, then it would
technically work, but then the designer is horrifically abusing the semantics
of the ``name`` property by polluting it with a long-form description.

**Resolution:**

Not implementing the ``[desc]`` tag.


Use of RDLFormatCode tags in ``name`` property seems inappropriate
------------------------------------------------------------------
Use of block formatting tags in a component's ``name`` property
seems out of scope from what the property's intent is.

**Resolution:**

Only implementing tags that control inline text style. Not implementing
structural formatting tags such as ``[p]`` and ``[list]``.



Open Questions
--------------


User-defined property's "type" attribute can not be "signal"?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Grammar seems to describe that a property's type attribute does not allow
"signal" types.
Furthermore, text in 15.1, Table 31 implies that the "ref" type generalization
also does not include "signal".

The spec is pretty clear about this, and it appears to be intentional.
I'm just a little surprised since it seems like an odd exclusion to make.
UDPs are basically user-extensions that can be used to describe things
outside of the RDL spec.
Why restrict a user's ability to use these?
Plus, there are several built-in properties that expect signal reference
types, so the precedent is simply not there... (resetsignal, some counter
properties)

**Resolution:**
None for now.
Implemented according to spec until I hear otherwise.



Compilation units and their scope not described in SystemRDL spec
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The SystemRDL 2.0 spec does not address the concept of "compilation units"
and how multiple RDL files share namespaces.

If multiple RDL files are compiled together, how are their namespaces shared?

**Resolution:**
I have provided my own interpretation of how compilation units in
SystemRDL should work.
Some concepts are borrowed from SystemVerilog, but are simplified significantly
in order to have the least "surprising" effects.

See :ref:`multifile_compilation` notes for more details.



Interaction of Verilog-style ``include`` with Perl tags needs clarification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Interaction between ``include`` directives and Perl-style preprocessor context
needs clarification. Using a strict interpretation of the spec would result in
surprising behavior that does not seem intentional.

See :ref:`dev_notes-include_preprocessor` implementation notes for more
details.



Generated type names should also account for dynamic property assignments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The SystemRDL 2.0 spec goes at great lengths to describe how component type
names are uniquified when parameters get overridden (5.1.1.4). Unfortunately
the spec falls short when it comes to accounting for dynamic property
assignments.

**Resolution:**

Since the semantics for this are not included in the SystemRDL 2.0 spec, I have
provided my own extended interpretation of how dynamic property assignments
should affect a component's generated type name.

See :ref:`dpa_type_generation` notes for more details.
