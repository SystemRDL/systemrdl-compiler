
Messages
========

.. _messages_warnings:

Warnings
--------
The SystemRDL compiler provides several optional warnings. These lint-like
checks report constructs that are not inherently wrong, but may be considered
risky.

All warning messages are disabled by default.

Individual warning messages can be enabled by passing one or more of the
following flags into the ``warning_flags`` option of the
:class:`~systemrdl.RDLCompiler` constructor. Multiple flags can be combined
using bitwise OR (the ``|`` operator).

.. autodata:: systemrdl.warnings.ALL
    :annotation:

.. autodata:: systemrdl.warnings.MISSING_RESET
    :annotation:

.. autodata:: systemrdl.warnings.IMPLICIT_FIELD_POS
    :annotation:

.. autodata:: systemrdl.warnings.IMPLICIT_ADDR
    :annotation:

.. autodata:: systemrdl.warnings.STRIDE_NOT_POW2
    :annotation:

.. autodata:: systemrdl.warnings.STRICT_SELF_ALIGN
    :annotation:


Exceptions
----------
.. autoclass:: systemrdl.RDLCompileError
    :members:


Message Handling
----------------

.. warning::

    The ``MessagePrinter`` and ``MessageHandler`` classes will be deprecated in
    a future release. See the following page for details: https://github.com/SystemRDL/systemrdl-compiler/issues/168

.. autoclass:: systemrdl.messages.MessagePrinter
    :members:

.. autoclass:: systemrdl.messages.MessageHandler()
    :members:
