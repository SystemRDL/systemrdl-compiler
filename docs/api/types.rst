
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
          after design elaboration.

          Prior to design elaboration, when pre-registring UDPs, component references
          are specified by their specific :class:`~systemrdl.component.Component` class, or
          the generic :class:`~systemrdl.rdltypes.references.RefType` object.

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

    .. automethod:: define_new

    .. automethod:: get_parent_scope

    .. automethod:: get_scope_path

    .. py:property:: type_name
        :type: str

        The type name of the struct as declared in RDL.

        .. versionadded:: 1.25

    .. py:property:: members
        :type: Dict[str, UserEnum]

        Returns a mapping of member name->value.

        .. versionadded:: 1.25


.. autofunction:: systemrdl.rdltypes.user_enum.is_user_enum

--------------------------------------------------------------------------------

Structures
----------
.. autoclass:: systemrdl.rdltypes.user_struct.UserStruct
    :members:

    .. automethod:: define_new

    .. py:property:: type_name
        :type: str

        The type name of the struct as declared in RDL.

        .. versionadded:: 1.24

.. autofunction:: systemrdl.rdltypes.user_struct.is_user_struct

--------------------------------------------------------------------------------

References
----------
.. autoclass:: systemrdl.rdltypes.references.PropertyReference
    :members:

.. autoclass:: systemrdl.rdltypes.references.RefType
