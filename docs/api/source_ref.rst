.. _api_src_ref:

Source Reference
================

Source references are objects that capture contextual information about where in
the original source code an RDL concept originated. This is useful for providing
additional information for error messages and other back-annotation to source files.

Every :ref:`api_node` in a SystemRDL register model is capable of providing
contextual information about where it originated:

* Component definition: :attr:`systemrdl.node.Node.def_src_ref`
* Component instantiation: :attr:`systemrdl.node.Node.inst_src_ref`

Similarly, information about where in the source a property assignment occurred
is available via: :attr:`systemrdl.node.Node.property_src_ref`

.. autoclass:: systemrdl.source_ref.SourceRefBase

.. autoclass:: systemrdl.source_ref.FileSourceRef
    :members: path

.. autoclass:: systemrdl.source_ref.DetailedFileSourceRef
    :members:
