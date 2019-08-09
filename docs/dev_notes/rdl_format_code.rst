
Implementation of RDLFormatCode
===============================

A simple RDLFormatCode processing function is accessible via the Node API that
handles conversion of a raw ``desc`` property into HTML. Mapping from RDLFC to
HTML is actually pretty trivial, but here are some additional considerations.

Array index tags
----------------

In order to support dynamic page generation, the ``[index]`` and
``[index_parent]`` tags are outputted as ``<span>`` tags. These tags are
annotated with ``class='rdlfc-index'`` and ``class='rdlfc-index_parent'``
respectively. The tag's text contains the indexes as described by the spec.
Annotating the tags with a class allows dynamic HTML pages to
search-and-replace the contents of these tags with updated values
as-appropriate.

The ``[desc]`` tag
------------------

Intentionally not implemented.

See :ref:`SystemRDL Spec Errata <dev_notes-errata-rdlfc_desc>` for more
details.


Markdown Extension
------------------

After RDLFormatCode processing, the resulting text is passed through a Markdown
formatter. This gives the user the option to use a more modern lightweight
markup language as an alternative to RDLFormatCode.
