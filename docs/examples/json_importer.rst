.. _example_json-importer:

Importing from JSON
===================

In this example, we will use the same schema defined in the
:ref:`previous example <example_json-exporter>` to build an importer that
re-constructs a register model from a JSON file.

We will use Python's built-in `JSON library <https://docs.python.org/3/library/json.html>`_
to read the input file, as well as the :class:`~systemrdl.importer.RDLImporter`
helper class to help construct RDL components.

The full example code can be found in the ``systemrdl-compiler`` repository at:
``examples/import_json.py``


Walkthrough
-----------

Start by creating a JSON importer class extended from :class:`~systemrdl.importer.RDLImporter`.

.. literalinclude:: ../../examples/import_json.py
    :lines: 5, 8-9

Just like the :ref:`JSON exporter example <example_json-exporter>`, we will
define a function that converts each component type.
This time, Python's JSON library will read the input and present each component
as a dictionary of keys:value pairs that represents its description.

Per-component conversion functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When developing your importer, it is important to always validate inputs, and
create human-friendly error messages or warnings whenever appropriate.
Prior to decoding any component, we start by checking the validity of the JSON
``dict`` object. Starting with the function to decode fields:

.. literalinclude:: ../../examples/import_json.py
    :lines: 33-44

Next, we use some methods provided by the :class:`~systemrdl.importer.RDLImporter`
to:

* Create an anonymous definition of a field component
* Assign some properties
* Instantiate it

Note that the field instance is not fully instantiated yet. It still needs to be
attached to a parent component. This will be done later outside of this function.

.. literalinclude:: ../../examples/import_json.py
    :lines: 46-65

Next is the function that constructs the enclosing register component. The reg
component is constructed in nearly the same way as before, except that here
we iterate over all the child fields and attach them to the parent reg definition.

.. literalinclude:: ../../examples/import_json.py
    :lines: 68-99
    :emphasize-lines: 13,22-24

Decoding a regfile is nearly the same. Here, children can be multiple different
types, so we call the appropriate decode function based on the 'type' key:

.. literalinclude:: ../../examples/import_json.py
    :lines: 102-130
    :emphasize-lines: 11-16,22

The addrmap decode function is nearly identical, however we need the
option to produce a named definition instead of an anonymous component
instantiation. This is because we want to be able to register the top-level
addrmap in the root type namespace. The type namespace can only contain
component definitions, not instances.

.. literalinclude:: ../../examples/import_json.py
    :lines: 133-179
    :emphasize-lines: 1,10-13,37-39


Loading JSON and decoding
^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have our decoding utility functions completed, we are ready to
implement the importer's :meth:`~systemrdl.importer.RDLImporter.import_file()`
entry function.

First, call the superclass. This ensures that per-component error message context
works properly later.

.. literalinclude:: ../../examples/import_json.py
    :lines: 11-12

Next, load the JSON file. For this importer, we'll be assuming that the top-level
component is always an addrmap. Any time an assumption about the input is made,
you should validate it to ensure it is true:

.. literalinclude:: ../../examples/import_json.py
    :lines: 14-23

Finally, call our decode function and register the resulting top-level component
definition with the root namespace:

.. literalinclude:: ../../examples/import_json.py
    :lines: 25-30



Using our new importer
----------------------

Importing data into the SystemRDL compiler is similar to compiling a file
normally. You can even intermingle compiling RDL files with importing custom
formats.

* Create a :class:`~systemrdl.RDLCompiler` instance
* Bind any custom importers
* Compile RDL inputs and/or import custom file formats
* Run elaboration

Here we detect the file type based on its extension:

.. literalinclude:: ../../examples/import_json.py
    :lines: 191-213
    :emphasize-lines: 3,14
    :dedent: 4



Equivalence check
-----------------

Let's see if our importer is working properly.
We can use the model printing listener from :ref:`the first example <example_print-hierarchy>`
to dump the register model:

.. literalinclude:: ../../examples/import_json.py
    :lines: 216-219
    :dedent: 4


Running the example code on ``tiny.rdl`` and its JSON counterpart we exported
in the previous example, ``tiny.json``, we should see identical output:

.. code-block:: text

    $ ./import_json.py tiny.json
    tiny
            r1
                    [7:0] f1 sw=rw
                    [15:8] f2 sw=r
    $ ./import_json.py tiny.rdl
    tiny
            r1
                    [7:0] f1 sw=rw
                    [15:8] f2 sw=r
