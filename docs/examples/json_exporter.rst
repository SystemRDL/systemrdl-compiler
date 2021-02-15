Building a JSON exporter
========================

This example walks through how to export a compiled SystemRDL register model into
a simple JSON data object.

The full example code can be found in the ``systemrdl-compiler`` repository at:
``examples/json_exporter.py``




Defining a schema
-----------------

Before we start, we need to define a schema for our custom JSON output. Since
there isn't really a "standard" JSON schema available, we'll make up our own
simple one. For the sake of this example, it will be very limited:

* Each SystemRDL component type will be represented as its own JSON object.
* The type of the object is represented by a "type" string.
* ``addrmap`` and ``regfile`` components will be treated interchangably.
* Arrays will not be supported.
* Only the field's "reset" and "sw" properties are encoded. All other properties will be ignored.

Each object's key/value mappings will be as follows:

field
    .. code-block:: text

        type: "field",
        inst_name: <string>,
        lsb: <integer>,
        msb: <integer>,
        reset: <integer>
        sw_access: <string>

reg
    .. code-block:: text

        type: "reg",
        inst_name: <string>,
        addr_offset: <integer>,
        children: <array of field objects>

addrmap or regfile
    .. code-block:: text

        type: "addrmap" or "regfile",
        inst_name: <string>,
        addr_offset: <integer>,
        children: <array of any object>



A note on register model traversal
----------------------------------

In the previous example, we used the :class:`~systemrdl.RDLWalker` & :class:`~systemrdl.RDLListener`.
This let us automatically traverse the design, and trigger callbacks. This is an
easy way to traverse the design, but only in situations where keeping track of
the register model's herarchical context is not needed.

For a JSON exporter we want to convert each node in the hierarchy and keep
track of parent/child relationships. Doing so with the walker/visitor method
would be cumbersome, so instead we will explicitly visit child nodes using the
:meth:`Node.children() <systemrdl.node.Node.children>` method.



Walkthrough
-----------

Python has an excellent `JSON serializer in its standard library <https://docs.python.org/3/library/json.html>`_.
This means that all we need to do is distill the information from the register
model into primitive datatypes that convert well to JSON (python dictionaries & lists).



Per-component conversion functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each component type will have a function that converts the corresponding
:class:`~systemrdl.node.Node` object into a Python dictionary.

The function to convert a :class:`~systemrdl.node.FieldNode` is pretty straightforward:

.. literalinclude:: ../../examples/export_json.py
    :lines: 12-20


Next, we write the function to convert a :class:`~systemrdl.node.RegNode`. Remember
how the schema we defined doesn't support arrays? This is a good time to check
if the register instance is an array, and throw an error. We will use the
compiler's message handler to emit a message to the user, as well as a reference
to the offending location in the RDL source file:

.. literalinclude:: ../../examples/export_json.py
    :lines: 23-30

After validating the register is not an array, we can continue and distill the
:class:`~systemrdl.node.RegNode` into a Python dictionary. Note how this calls
the :meth:`~systemrdl.node.Node.fields()` method to fetch all fields of this
register.

.. literalinclude:: ../../examples/export_json.py
    :lines: 32-44

Next, we create a common function to convert both :class:`~systemrdl.node.AddrmapNode`
and :class:`~systemrdl.node.RegfileNode` objects.

* Since this function is reused for both node types, use ``isinstance`` to make
  sure the ``type`` attribute is set correctly.
* In SystemRDL, ``addrmap`` components can contain additional ``addrmap``/``regfile``
  children, or ``reg`` components. When iterating over :meth:`~systemrdl.node.Node.children()`,
  use ``isinstance`` again to call the appropriate conversion function.

.. literalinclude:: ../../examples/export_json.py
    :lines: 47-74



Dumping JSON
^^^^^^^^^^^^

Finally, we need a top-level function that starts the conversion process at the top-level,
and then serializes the resulting tree of Python dictionaries/lists into proper JSON.

.. literalinclude:: ../../examples/export_json.py
    :lines: 77-83



Bringing it all together
^^^^^^^^^^^^^^^^^^^^^^^^

Now thast we have all our utility functions defined, we can put it all together.

First, compile and elaborate input files provided from the command line, as was
done in the previous example:

.. literalinclude:: ../../examples/export_json.py
    :lines: 88-95

Finally, call the top-level conversion function which writes out the JSON file:

.. literalinclude:: ../../examples/export_json.py
    :lines: 97



Output
------

Given the input file ``tiny.rdl``:

.. literalinclude:: ../../examples/tiny.rdl
    :language: systemrdl

converting to JSON produces the following:

.. literalinclude:: ../../examples/tiny.json
