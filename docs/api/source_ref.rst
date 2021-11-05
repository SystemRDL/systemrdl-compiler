.. _api_src_ref:

Source Reference
================

Every :ref:`api_component` in a SystemRDL register model is capable of providing
contextual information about where it originated:

* Component definition: :attr:`systemrdl.component.Component.def_src_ref`
* Component instantiation: :attr:`systemrdl.component.Component.inst_src_ref`

Similarly, information about where in the source a property assignment occurred
is available via: :attr:`systemrdl.component.Component.property_src_ref`

.. autoclass:: systemrdl.source_ref.SourceRefBase

.. autoclass:: systemrdl.source_ref.FileSourceRef
    :members: path

.. autoclass:: systemrdl.source_ref.DetailedFileSourceRef
    :members:
