
Types
=====

Once compiled, SystemRDL types are mapped to Python types as follows:

.. list-table::
    :header-rows: 1

    *   - SystemRDL Type
        - Python Type

    *   - ``longint unsigned``
        - ``int``

    *   - ``bit``
        - ``int``

    *   - ``boolean``
        - ``bool``

    *   - ``string``
        - ``str``

    *   - ``accesstype``
        - :class:`~systemrdl.rdltypes.builtin_enums.AccessType`

    *   - ``onreadtype``
        - :class:`~systemrdl.rdltypes.builtin_enums.OnReadType`

    *   - ``onwritetype``
        - :class:`~systemrdl.rdltypes.builtin_enums.OnWriteType`

    *   - ``addressingtype``
        - :class:`~systemrdl.rdltypes.builtin_enums.AddressingType`

    *   - ``precedencetype``
        - :class:`~systemrdl.rdltypes.builtin_enums.PrecedenceType`

    *   - ``intr`` property modifier
        - :class:`~systemrdl.rdltypes.builtin_enums.InterruptType`

    *   - User-defined ``enum``
        - :class:`~systemrdl.rdltypes.user_enum.UserEnum`

    *   - User-defined ``struct``
        - :class:`~systemrdl.rdltypes.user_struct.UserStruct`

    *   - arrays
        - ``list``

    *   - Component ``ref``
        - :class:`~systemrdl.node.Node` if queried using :meth:`Node.get_property() <systemrdl.node.Node.get_property>`

    *   - RHS property reference
        - :class:`~systemrdl.rdltypes.references.PropertyReference`

--------------------------------------------------------------------------------

Built-in Enumeration Types
--------------------------

.. autoclass:: systemrdl.rdltypes.builtin_enums.AccessType
    :members:

.. autoclass:: systemrdl.rdltypes.builtin_enums.OnReadType
    :members:

.. autoclass:: systemrdl.rdltypes.builtin_enums.OnWriteType
    :members:

.. autoclass:: systemrdl.rdltypes.builtin_enums.AddressingType
    :members:

.. autoclass:: systemrdl.rdltypes.builtin_enums.PrecedenceType
    :members:

.. autoclass:: systemrdl.rdltypes.builtin_enums.InterruptType
    :members:

--------------------------------------------------------------------------------

Enumerations
------------
.. autoclass:: systemrdl.rdltypes.user_enum.UserEnum
    :members:

.. autofunction:: systemrdl.rdltypes.user_enum.is_user_enum

--------------------------------------------------------------------------------

Structures
----------
.. autoclass:: systemrdl.rdltypes.user_struct.UserStruct
    :members:

.. autofunction:: systemrdl.rdltypes.user_struct.is_user_struct

--------------------------------------------------------------------------------

Property Reference
------------------
.. autoclass:: systemrdl.rdltypes.references.PropertyReference
    :members:
