.. _api_importer:

Importer
========

The SystemRDL Importer class provides some base utilities for constructing your
own register model tree from an external source. For a more detailed walkthrough,
see the :ref:`example_json-importer` tutorial.

.. autoclass:: systemrdl.importer.RDLImporter
    :members: compiler, msg, default_src_ref

    .. automethod:: systemrdl.importer.RDLImporter.import_file
    .. automethod:: systemrdl.importer.RDLImporter.add_child
    .. automethod:: systemrdl.importer.RDLImporter.assign_property
    .. automethod:: systemrdl.importer.RDLImporter.register_root_component
    .. automethod:: systemrdl.importer.RDLImporter.lookup_root_component


Create Definitions
------------------
.. versionadded:: 1.16

Use these methods to create a named definition, and instantiate one or more times
using the methods described in the following section.

If ``type_name`` is not specified, then an anonymous definition is created and
can therefore only be instantiated once.

.. automethod:: systemrdl.importer.RDLImporter.create_field_definition
.. automethod:: systemrdl.importer.RDLImporter.create_reg_definition
.. automethod:: systemrdl.importer.RDLImporter.create_regfile_definition
.. automethod:: systemrdl.importer.RDLImporter.create_addrmap_definition
.. automethod:: systemrdl.importer.RDLImporter.create_mem_definition


Instantiate Definitions
-----------------------
.. versionadded:: 1.16

These methods take a component definition, and create an instance.

If given a named component definition, then an instantiated copy is returned.
If the given component definition is anonymous, then it is converted to an
instantiation in-place. Anonymous definitions can only be instantiated once.

To complete the instantiation, you must attach it to a valid parent component
using :meth:`~systemrdl.importer.RDLImporter.add_child()`.

.. automethod:: systemrdl.importer.RDLImporter.instantiate_field
.. automethod:: systemrdl.importer.RDLImporter.instantiate_reg
.. automethod:: systemrdl.importer.RDLImporter.instantiate_regfile
.. automethod:: systemrdl.importer.RDLImporter.instantiate_addrmap
.. automethod:: systemrdl.importer.RDLImporter.instantiate_mem
