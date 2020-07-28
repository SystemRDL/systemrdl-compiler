.. _dev_notes-include_preprocessor:

Preprocessor Includes
=====================

The SystemRDL spec says that Perl preprocessor is executed first, followed by
the Verilog-style preprocessor.

How are Verilog ```include`` directives handled alongside Perl? There are
generally three different interpretations I can think of.

Consider the following input files:

.. code-block:: systemrdl
    :caption: x.rdl

    <% $foo = 1; %>
    `include "y.rdl"
    something = <%=$foo%>;


.. code-block:: systemrdl
    :caption: y.rdl

    something_else = <%=$foo%>;
    <% $foo = 2; %>


Interpretation 1
----------------

A super-strict interpretation could imply that ``y.rdl`` never gets processed
by the Perl preprocessor since the ```include`` in ``x.rdl`` only gets expanded
in the final verilog-style preprocess phase, after Perl preprocessing has
completed.

This is pretty unreasonable since Perl tags would only be able to be used at
the top-level file.


Interpretation 2
----------------

Another interpretation is that the Perl preprocessor is run in an isolated
context for each file read. This would also apply to includes.

This would result in Perl scope between files not being shared.

Result of the above example:

* something == 1
* something_else == undefined since ``$foo`` was never set in ``y.rdl``


Interpretation 3
----------------

Perl variables are allowed to be shared across files.

Result of the above example:

* something == 2 (because ``$foo`` was overridden during the include of
  ``y.rdl``)
* something_else == 1 (because the original value of ``$foo`` from ``x.rdl``)


Resolution: Interpretation 3
----------------------------

Based on conversations with a SystemRDL committee member, the preferred
interpretation is to allow Perl scope to be shared across files. Reasoning is
that users can set Perl configuration variables in an include file, which are
later used to augment a design. The "sata_ahci" example from SystemRDL 1.0
suggests this as well. They also mentioned that other existing tools adopt a
similar behavior, providing historical precedent for this interpretation.


Implementation
--------------

A unified Perl scope is implemented by promoting Verilog include directives to
be expanded *before* Perl preprocessing. This is technically not how the RDL
spec describes it, but doing so would allow Perl scope to be shared as intended
by the SystemRDL committee.

The implementation performs include expansion during the tokenization/segment
generation steps described in :ref:`dev_notes-perl`
