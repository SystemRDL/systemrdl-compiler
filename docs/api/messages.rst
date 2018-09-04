
Messages
========

.. _messages_warnings:

Warnings
--------
The SystemRDL compiler provides several optional warnings. These diagnostic
messages report constructs that are not inherently erroneous, but may be considered
risky. All warning messages are disabled by default.

Individual warning messages can be enabled by passing one or more of the following flags into the ``warning_flags`` option of the :class:`~systemrdl.RDLCompiler` constructor. Multiple flags can be combined using bitwise OR (the ``|`` operator).

.. autodata:: systemrdl.messages.W_ALL
    :annotation:

.. autodata:: systemrdl.messages.W_MISSING_RESET
    :annotation:

.. autodata:: systemrdl.messages.W_IMPLICIT_FIELD_POS
    :annotation:

.. autodata:: systemrdl.messages.W_IMPLICIT_ADDR
    :annotation:


Exceptions
----------
.. autoclass:: systemrdl.RDLCompileError
    :members:


Message Handling
----------------
.. autoclass:: systemrdl.messages.MessagePrinter
    :members:

.. autoclass:: systemrdl.messages.SourceRef
    :members:
