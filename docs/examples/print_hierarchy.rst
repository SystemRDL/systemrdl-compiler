.. _example_print-hierarchy:

Print Compiled Hierarchy
========================

This example walks through a simple program that:

* Compiles one or more RDL files provided from the command line
* Elaborates the design register model
* Uses the walker/listener traversal method to print a hierarchical text
  representation of the register model

The full example code can be found in the ``systemrdl-compiler`` repository at:
``examples/print_hierarchy.py``



Walkthrough
-----------

First, a few classes are imported, and a list of requested input files
collected from the command line arguments.

.. literalinclude:: ../../examples/print_hierarchy.py
    :lines: 27-33
    :dedent: 4

Next, an instance of the compiler object is created. This represents a single
compilation scope.

.. literalinclude:: ../../examples/print_hierarchy.py
    :lines: 35-36
    :dedent: 4

All the input files are compiled into the root scope, and then elaborated.
Since no top-level component name was specified in the ``elaborate`` call, the
last ``addrmap`` component definition is automatically chosen.

If the RDL file contains any syntax or semantic errors, the compile and
elaborate steps will raise an :class:`~systemrdl.RDLCompileError` exception. It
is recommended to wrap this in a try/except block.

.. literalinclude:: ../../examples/print_hierarchy.py
    :lines: 38-47
    :dedent: 4

For this example, we want to print out some information about the register
model. This listener class defines callbacks that will output an indented tree
view of the register model. For ``field`` components, some additional
information is printed about the bit range, and software access policy.

.. literalinclude:: ../../examples/print_hierarchy.py
    :lines: 3-24

Finally, the walker is created, and is used to traverse the elaborated register
model. At each node, the listener callbacks are executed.

.. literalinclude:: ../../examples/print_hierarchy.py
    :lines: 49-52
    :dedent: 4



Output
------

Below is the example's output if it is run with the SPI controller RDL file:

.. literalinclude:: print_hierarchy_spi.stdout
    :language: none
    :prepend: $ cd examples/
              $ print_hierarchy.py atxmega_spi.rdl
