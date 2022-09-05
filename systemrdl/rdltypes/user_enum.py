from typing import Optional, List, Type, Dict, Any, TYPE_CHECKING
from collections import OrderedDict
import inspect

from .simple_enum import SimpleEnum
from .. import component as comp
from ..core import rdlformatcode

if TYPE_CHECKING:
    from markdown import Markdown

class UserEnumMemberContainer:
    """
    Container class used only when defining a new UserEnum.
    This shall only be used by importers.


    .. versionadded:: 1.24
    """
    def __init__(self, name: str, value: int, rdl_name: Optional[str] = None, rdl_desc: Optional[str] = None) -> None:
        self.name = name
        self.value = value
        self.rdl_name = rdl_name
        self.rdl_desc = rdl_desc


class UserEnum(SimpleEnum): # type: ignore
    """
    All user-defined enumerations are based on this class.

    UserEnum types can be identified using: :meth:`is_user_enum`


    .. versionchanged:: 1.24
        UserEnum is no longer extended from Python's standard library ``Enum``.
        Instead, an internal enum implementation is used.
    """

    @staticmethod
    def define_new(name: str, members: List[UserEnumMemberContainer]) -> Type['UserEnum']:
        """
        Define a new UserEnum class

        Parameters
        ----------
        name: str
            Name of the enum type
        members: UserEnumMemberContainer
            List of enum members


        .. versionadded:: 1.24
        """

        # Validate all member names and values are unique
        names = [m.name for m in members]
        values = [m.value for m in members]
        if len(names) != len(set(names)):
            raise ValueError("All members of an enum shall have unique names")
        if len(values) != len(set(values)):
            raise ValueError("All members of an enum shall have unique values")

        # Re-pack into dict as required by the enum functional API
        members_dict = OrderedDict()
        for m in members:
            members_dict[m.name] = (m.value, m.rdl_name, m.rdl_desc)

        return UserEnum.create(name, members_dict)


    @classmethod
    def _set_parent_scope(cls, scope: comp.Component) -> None:
        cls._parent_scope = scope

    @classmethod
    def get_parent_scope(cls) -> Optional[comp.Component]:
        """
        Returns reference to parent component that contains this type definition.
        """
        return getattr(cls, "_parent_scope", None)

    @classmethod
    def get_scope_path(cls, scope_separator: str="::") -> str:
        """
        Generate a string that represents this enum's declaration namespace
        scope.

        Parameters
        ----------
        scope_separator: str
            Override the separator between namespace scopes
        """
        parent_scope = cls.get_parent_scope()
        if parent_scope is None:
            # Importer likely never set the scope
            return ""
        elif isinstance(parent_scope, comp.Root):
            # Declaration was in root scope
            return ""
        else:
            # Get parent definition's scope path
            parent_path = parent_scope.get_scope_path(scope_separator)

            # Extend it with its scope name
            if parent_path:
                return(
                    parent_path
                    + scope_separator
                    + parent_scope._scope_name
                )
            else:
                return parent_scope._scope_name


    def __init__(self, value: int, rdl_name: Optional[str], rdl_desc: Optional[str]):
        self._value_ = value
        self._rdl_name_ = rdl_name
        self._rdl_desc_ = rdl_desc

    @property
    def rdl_desc(self) -> Optional[str]:
        """
        Enum entry's ``desc`` property
        """
        return self._rdl_desc_

    @property
    def rdl_name(self) -> Optional[str]:
        """
        Enum entry's ``name`` property
        """
        return self._rdl_name_

    def get_html_desc(self, markdown_inst: Optional['Markdown']=None) -> Optional[str]:
        """
        Translates the enum's 'desc' property into HTML.

        Any RDLFormatCode tags used are converted to HTML.
        The text is also fed through a Markdown processor.

        The additional Markdown processing allows designers the choice to use a
        more modern lightweight markup language as an alternative to SystemRDL's
        "RDLFormatCode".

        Parameters
        ----------
        markdown_inst: ``markdown.Markdown``
            Override the class instance of the Markdown processor.
            See the `Markdown module <https://python-markdown.github.io/reference/#Markdown>`_
            for more details.

        Returns
        -------
        str or None
            HTML formatted string.
            If enum entry does not have a description, returns ``None``


        .. versionchanged:: 1.6
            Added ``markdown_inst`` option.
        """
        desc_str = self._rdl_desc_
        if desc_str is None:
            return None
        return rdlformatcode.rdlfc_to_html(desc_str, md=markdown_inst)

    def get_html_name(self) -> Optional[str]:
        """
        Translates the enum's 'name' property into HTML.

        Any RDLFormatCode tags used are converted to HTML.

        Returns
        -------
        str or None
            HTML formatted string.
            If enum entry does not have an explicitly set name, returns ``None``


        .. versionadded:: 1.8
        """
        name_str = self._rdl_name_
        if name_str is None:
            return None
        return rdlformatcode.rdlfc_to_html(name_str, is_desc=False)


    def __int__(self) -> int:
        return self.value

    def __bool__(self) -> bool:
        return bool(self.value)

    def __deepcopy__(self, memo: Dict[int, Any]) -> 'UserEnum':
        # Do not deepcopy enumerations
        return self


def is_user_enum(t: Any) -> bool:
    """
    Test if type ``t`` is a :class:`~UserEnum`

    .. note:: Returns false if ``t`` is referencing a UserEnum value member
    """
    return inspect.isclass(t) and issubclass(t, UserEnum)
