
.. _SystemRDL 2.0: http://accellera.org/downloads/standards/systemrdl

SystemRDL Spec Errata
=====================

This document keeps track of all ambiguities, contradictions, and typos found
in Accelera's `SystemRDL 2.0`_
language specification.

For each issue, I include the resolved interpretation that is used in this
project.

--------------------------------------------------------------------------------

Inconsistencies & Contradictions
--------------------------------

Semantic rule 10.6.1.c is violated in 5.1.2.2.2-Example 2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Rule 10.6.1.c states that ``accesswidth`` cannot be greater than ``regwidth``.

However, in the example:

* reg 'a' has an implied regwidth of 32
* reg 'a' gets assigned an accesswidth of 64 via default.
  Results in accesswidth > regwidth!

**Resolution:**

None. Example is invalid and violates rule 10.6.1.c.



Grammar does not allow empty array literals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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



Invalid SystemRDL 2.0 in Table E1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In Annex E, Table E1, many of the cells in the "SystemRDL 2.0" column show
what appears to be incorrect usage of the ``onread`` and ``onwrite`` side-effect
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



Constraint example uses struct datatype in an undocumented way
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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



RDLFormatCode paragraph tag listed as a single tag?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In annex F.2, the ``[p]`` paragraph tag is listed as a "single-tag" construct.
Since all the other tags seem to closely mirror HTML tags, this seems
out-of-place. The description from the phpBB site makes more sense since it
shows the paragraph tag as a pair: ``[p] paragraph text [/p]``.

Also, the example in F.4 shows the paragraph tag used as expected - as a pair.

**Resolution:**

Implement paragraph tag as an open/close pair.



.. _dev_notes-errata-rdlfc_desc:

Existence of the RDLFormatCode ``[desc]`` tag is inappropriate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
I fail to understand why the ``[desc]`` tag exists and how it could possibly be
useful.

If the ``[desc]`` tag is used within the ``desc`` property, then a recursive
self-reference is created.

If the ``[desc]`` tag is used in the ``name`` property, then it would
technically work, but then the designer is horrifically abusing the semantics
of the ``name`` property by polluting it with a long-form description.

**Resolution:**

Not implementing the ``[desc]`` tag.



Use of RDLFormatCode tags in ``name`` property is inappropriate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use of block formatting tags in a component's ``name`` property
seems out of scope from what the property's intent is.

**Resolution:**

Only implementing tags that control inline text style. Not implementing
structural formatting tags such as ``[p]`` and ``[list]``.



Definition of the ``hdl_path_slice`` property is shortsighted
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
14.1.2 Example 2 shows how multiple entries in an hdl_path_slice would be used:

* A field ``f2`` is declared with bit-range [5:3]
* The field's ``hdl_path_slice`` is assigned the following strings: ``'{"rtl_f2_5_4", "rtl_f2_3"}``

Given the naming convention used in the string, this implies that the
backdoor paths for these slices are to be mapped asymmetrically to logical bits
as follows:

* "rtl_f2_5_4" --> bit slice [5:4]
* "rtl_f2_3" --> bit slice [3:3]

However these are merely strings, and the end user could name them something
entirely different. It is impossible to infer the intent of the user! The
mapping could have just as easily been:

* "foo" --> bit slice [5:5]
* "bar" --> bit slice [4:3]

To illustrate this issue, `UVM requires that the explicit bit positions of each
slice be provided when defining them in the model. <https://verificationacademy.com/verification-methodology-reference/uvm/docs_1.2/html/files/reg/uvm_reg-svh.html#uvm_reg.add_hdl_path>`_
One cannot simply provide a list of slice strings to the UVM register model.

**Resolution:**

Recommended interpretation is to only honor the ``hdl_path_slice`` property
in situations where its value is completely unambiguous.

* If a field is given a single slice, it is assumed it represents the hdl path
  to *all bits* in the field.
* If a field is given multiple slices, it is assumed each slice represents
  *exactly 1 bit* of the field. The slice order is assumed to be from msb down
  to lsb.
* If multiple slices are given, and the length of the string array does not
  match the field's bit-width, then this represents an ambiguous slice definition.
  Tools should ignore this property and emit a warning.



Verilog does not have an ```if`` preprocessor directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In 16.2.1 - Table 32, the SystemRDL spec references an ```if`` preprocessor
directive. Nowhere in SystemVerilog IEEE Std 1800-2012 is this defined, nor
does the RDL spec offer an explanation for its semantics.

**Resolution:**

Do not implement an ```if`` preprocessor directive.



Inconsistent definition of the ``ref`` type keyword
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In section 6.1, Table 7's denotes that the ``ref`` keyword is allowed to be used in
both "parameter or struct member type names". This is in direct conflict with
what the formal grammar in Annex B defines:

.. code-block:: text
    :emphasize-lines: 1,2

    struct_type ::= data_type | component_type
    param_def_elem ::= data_type id [ array_type ] [ = constant_expression ]
    component_type ::= component_primary_type | signal
    component_primary_type ::= addrmap | regfile | reg | field | mem

According to the grammar, parameters are not allowed to use component references.
This is further corroborated in clause 5.1.1.2-e that explicitly forbids it.
Similarly, the grammar definition forbids structs from using the ``ref`` keyword
but allows specific component type keywords to be used instead.

The only place where the ``ref`` keyword is allowed to be used is in a User
Defined Property (UDP) definition.

**Resolution:**

Ignore the implication in Table 7 that the ``ref`` keyword can be used in parameters
or structs. Other areas in the specification forbid it more directly.


--------------------------------------------------------------------------------

Compilation issues in examples
------------------------------
Some very minor typos found while attempting to compile several code snippet examples.
These issues do not have any significant effect on the interpretation of the
language.



5.1.2.5, Examples 1,2, and 3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All three examples fail to create an instance of ``regfile example`` inside
the ``top`` addrmap component. This results in an empty component definition
which violates the rule described in 13.3-b.



6.3.2.4, Examples 1 and 2
^^^^^^^^^^^^^^^^^^^^^^^^^
Numerous uses of "bool". Keyword should be "boolean" as required by the grammar.



9.8.1, Example 1
^^^^^^^^^^^^^^^^
Illegal integer literal ``4'3``.



14.2.3
^^^^^^
Field ``f2`` uses enumeration literals that are missing their ``color::`` prefix.



15.2.2, Example 1
^^^^^^^^^^^^^^^^^
Missing semicolon in ``some_num_p`` after ``regfile``.



15.2.2, Example 2
^^^^^^^^^^^^^^^^^
Enumeration literals are missing their ``myEncoding::`` prefix.



--------------------------------------------------------------------------------

Typos in the spec
-----------------

Typo in semantic rule 11.2-f
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Virtual registers, **register files**, and fields shall have the same
    software access (sw property value) as the parent memory.

Mentions "register files", even though they are not allowed in "mem" components
as per 11.1-b-1-ii.



Typo in type name generation BNF snippet 5.1.1.4-c
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BNF-style description implies parentheses are part of the generated type name
but the text in the same section only mentions underscore delimiters.
Assuming the red parentheses are to be ignored.


--------------------------------------------------------------------------------

Open Questions
--------------
Topics where the SystemRDL spec leaves too much ambiguity and further
clarification would have been beneficial.


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

Interaction between ``include`` directives and Perl-style preprocessor variable
scope needs clarification. Using a strict interpretation of the spec would result in
surprising behavior that does not seem desireable.

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



Precedence of ``hwclr`` and ``hwset`` at runtime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The ``hwclr`` and ``hwset`` properties provide a mechanism to clear or set a
field at runtime using a user signal. Nothing prevents the user from enabling
both of these control signals, however their runtime precedence is ambiguous.

Consider the following:

.. code-block:: systemrdl

    signal {} set_me;
    signal {} clear_me;

    field {
        hwset = set_me;
        hwclr = clear_me;
    } my_field;

If at runtime, a design simultaneously asserts the ``set_me`` and ``clear_me``
signals, is the next value of ``my_field`` 1 or 0? Table 17 does not specify the
assignment priority.

**Resolution:**
It is out of scope for the compiler to suggest either has preference. Instead,
any RTL generators should clearly state the precedence used.

--------------------------------------------------------------------------------

Clarifications
--------------
Areas of the specification that are not ambiguous, but could have been more
explicitly described to the reader. Often requires *very* careful interpretation
across separate chapters to come to an accurate understanding of the author's intent.


Interpretation of ``swwe`` and ``swwel`` properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The spec is vague in describing the logic these properties infer. The ``swwe``
and ``swwel`` properties are used to infer logic that overrides a field's
ability to be written at runtime.

If either property is set to a field or signal component reference, then the state
of that signal/field determines whether the current field is writable by software.

If either property is set to a boolean ``true``, then an input signal is inferred,
which controls software's ability to write the field.



Property "Ref Targets"
^^^^^^^^^^^^^^^^^^^^^^

In Annex G, the specification vaguely suggests that some properties can be
referenced in the right-hand side of assignment expressions. Only through
detailed reading of examples and some property semantics is it possible to infer
how these work.

Let's take the ``anded`` property as an example. If assigned ``true`` using a
normal property assignment, a hardware output signal will be generated. This
signal will be assigned the AND-reduction of that field's value.

.. code-block:: systemrdl

    field {
        anded = true;
    } my_field[7:0];

A Verilog code generator may output something similar to this:

.. code-block:: verilog

    output wire my_field__anded;

    logic [7:0] my_field;
    // (field logic not shown)
    assign my_field__anded = &(my_field);


If the ``anded`` property is referenced in the right-hand side of an assignment
expression (aka a "ref target"), then the assigned property receives the
AND-reduction of the field's value at *runtime*.

.. code-block:: systemrdl

    field {
        sw=rw; hw=r;
    } my_field[7:0];

    field {
        sw=rw; hw=r;
    } my_anded_field[8:8];
    my_anded_field->next = my_field->anded;

A Verilog code generator may output something similar to this:

.. code-block:: verilog

    logic [7:0] my_field;
    // (field logic not shown)

    logic my_anded_field;
    always_ff @(posedge clk) begin
        if(my_anded_field_swwe) begin
            my_anded_field <= cpuif_bus[8];
        end else begin
            my_anded_field <= &(my_field);
        end
    end

The spec really ought to have a brief section explaining this in more explicit
detail.


Determining counter direction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Section 9.8.1 describes that it is possible to create three types of counters:

    A SystemRDL compiler shall imply the nature of a counter as a up counter,
    a down counter, or an up/down counter by the properties specified for
    that counter field.

Unfortunately none of the semantics in section 9.8 explicitly describe *how* one
determines the type of counter. Only after examining the examples in detail is
it possible to infer how a counter's directionality is determined.

Up-counter properties:
    * incrvalue
    * incrwidth
    * incr
    * incrsaturate/saturate
    * incrthreshold/threshold
    * overflow

Down-counter properties:
    * decrvalue
    * decrwidth
    * decr
    * decrsaturate
    * decrthreshold
    * underflow

* If a counter field specifies at least one of the **Up-counter properties**
  properties, it is implied to be an up-counter
* If a counter field specifies at least one of the **Down-counter properties**
  properties, it is implied to be a down-counter
* If a counter field specifies at least one property of both groups, it is
  implied to be an up/down counter.
* If a counter field does not assign any additional counter properties, it is
  implied to be an up-counter.

To assist users in this interpretation, the following helper properties have been added:

* :data:`FieldNode.is_up_counter <systemrdl.node.FieldNode.is_up_counter>`
* :data:`FieldNode.is_down_counter <systemrdl.node.FieldNode.is_down_counter>`


Field's 'next' Property
^^^^^^^^^^^^^^^^^^^^^^^

Section 9.5 describes a field's ``next`` property as a mechanism to access the
D-input of the field's flip-flop. If taken too literally, it is easy to
misinterpret this as a *direct* connection to the FF's D-pin that unconditionally
overrides the field's next value. After careful reading of several examples in
other sections (9.9 - Interrupt Properties), it becomes clear that the ``next``
property should really be interpreted as a general hardware input signal to the
field's logic. Assignment of this property effectively replaces the inferred
input signal to the field.

Some examples:
    ``hw=rw; we;``
        * Implies a hardware input signal for the field's next value as well as a write-enable.
        * The field's next value is only sampled if the write-enable is asserted.

    ``hw=rw; we; next = some_reference;``
        * Same as the previous case, but the next value input signal is no longer inferred.
        * Instead, the field's next value is from the reference provided.
        * As before, the next value is only loaded if the associated write-enable signal
          is asserted.

    ``hw=rw; level intr; stickybit;``
        * Implies a hardware input signal that controls assertion of the interrupt field bits.
        * A '1' in any bit position of the value input sets the corresponding bit in the
          field's storage element.

    ``hw=rw; level intr; stickybit; next = some_reference;``
        * Same as the previous example, except the inferred hardware input signal is
          replaced by an explicit reference.
        * Field's behavior is still the same. The referenced value controls setting
          of sticky bits in the field.


In addition to the above, a passing comment in the example in 17.2.8 appears to imply that
use of the ``next`` property requires the field to be writable by hardware:

.. code-block:: systemrdl

    default hw = w; // w needed since dyn assign below implies interconnect to hw
                    // global_int.global_int->next = master_int->intr;

Unfortunately the text does not provide this detail in any of the semantics.
Fortunately it is still consistent with the interpretation clarified here.
