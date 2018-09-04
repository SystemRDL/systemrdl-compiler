
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
        - :class:`~systemrdl.rdltypes.AccessType`
    
    *   - ``onreadtype``
        - :class:`~systemrdl.rdltypes.OnReadType`
    
    *   - ``onwritetype``
        - :class:`~systemrdl.rdltypes.OnWriteType`
    
    *   - ``addressingtype``
        - :class:`~systemrdl.rdltypes.AddressingType`
    
    *   - ``precedencetype``
        - :class:`~systemrdl.rdltypes.PrecedenceType`
    
    *   - ``intr`` property modifier
        - :class:`~systemrdl.rdltypes.InterruptType`
    
    *   - User-defined ``enum``
        - :class:`~systemrdl.rdltypes.UserEnum`
    
    *   - User-defined ``struct``
        - :class:`~systemrdl.rdltypes.UserStruct`
    
    *   - arrays
        - ``list``
    
    *   - Component ``ref``
        - :class:`~systemrdl.node.Node` if queried using :meth:`Node.get_property() <systemrdl.node.Node.get_property>`
    
    *   - RHS property reference
        - :class:`~systemrdl.rdltypes.PropertyReference`

Reserved Enumeration Types
--------------------------

.. autoclass:: systemrdl.rdltypes.AccessType
    :members:

.. autoclass:: systemrdl.rdltypes.OnReadType
    :members:

.. autoclass:: systemrdl.rdltypes.OnWriteType
    :members:

.. autoclass:: systemrdl.rdltypes.AddressingType
    :members:

.. autoclass:: systemrdl.rdltypes.PrecedenceType
    :members:

.. autoclass:: systemrdl.rdltypes.InterruptType
    :members:

Enumerations
------------
.. autoclass:: systemrdl.rdltypes.UserEnum
    :members:
    
    .. autoattribute:: rdl_desc
    .. autoattribute:: rdl_name

.. autofunction:: systemrdl.rdltypes.is_user_enum

Structures
----------
.. autoclass:: systemrdl.rdltypes.UserStruct
    :members:

.. autofunction:: systemrdl.rdltypes.is_user_struct

Property Reference
------------------
.. autoclass:: systemrdl.rdltypes.PropertyReference
    :members:
