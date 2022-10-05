from typing import Type, Union, Any, TYPE_CHECKING
import sys

if TYPE_CHECKING:
    from .builtin_enums import BuiltinEnum
    from .user_enum import UserEnum
    from .references import PropertyReference, RefType
    from .user_struct import UserStruct
    from .array import ArrayPlaceholder
    from ..node import Node
    from .. import component as comp

if sys.version_info >= (3,5,4):
    # RDL Types the user will encounter via the public API
    RDLValue = Union[
        int, bool, str, list,
        'BuiltinEnum', 'UserEnum', 'UserStruct', Type['UserEnum'],
        'Node', 'PropertyReference'
    ]
else:
    # Stub on 3.5.3 or older due to: https://github.com/python/typing/issues/266
    RDLValue = Any # type: ignore

# RDL Types used internally prior to elaboration
PreElabRDLValue = Union[
    int, bool, str,
    'BuiltinEnum', 'UserEnum', 'UserStruct',
    'PropertyReference', 'comp.Component', 'RefType'
]

if sys.version_info >= (3,5,4):
    PreElabRDLType = Union[Type[PreElabRDLValue], 'ArrayPlaceholder']
else:
    # Stub on 3.5.3 or older due to: https://github.com/python/typing/issues/266
    PreElabRDLType = Any # type: ignore
