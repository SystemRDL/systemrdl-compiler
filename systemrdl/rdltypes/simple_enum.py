# This was copied from Python's standard library implementation for 'enum',
# then severely stripped down.
#
# Python's Enum implementation allows users to reference enum members by name
# directly using the getattr dot operator (enum_type.member).
# This ends up imposing a lot of restrictions on what names enum members can
# have since they cannot collide with internal members that define the unerlying
# Enum implementation.
#
# For the purposes of the SystemRDL compiler, user-defined enums need to be able
# to accept ANY type/member naming scheme.
# To accomplish this, this stripped down version of Python's Enum removes the
# ability to access members using the getattr dot operator, and therefore also
# removes the member naming limitations.
#
# Since this is only intended to be used for RDL UserEnum, the following
# capabilities were also removed:
# - Remove support for extended subclassing, mixins, etc. (Simplifies
#   implementation signifcantly)
# - Cant get member via value from callable (simplifies object creation)
# - Simplified Enum funtional API to only support defining new enum via a
#   mapping.

import sys
from collections import OrderedDict

# pylint: disable=no-member,unused-argument,function-redefined,no-value-for-parameter

def _make_class_unpicklable(cls):
    """
    Make the given class un-picklable.
    """
    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)
    cls.__reduce_ex__ = _break_on_call_reduce
    cls.__module__ = '<unknown>'


class _EnumDict(dict):
    def __init__(self):
        super().__init__()
        self.enum_members = {}


# Dummy value for SimpleEnum as SimpleEnumMeta explicitly checks for it, but of course
# until SimpleEnumMeta finishes running the first time the SimpleEnum class doesn't exist.
# This is also why there are checks in SimpleEnumMeta like `if SimpleEnum is not None`
SimpleEnum = None

class SimpleEnumMeta(type):
    """
    Metaclass for SimpleEnum
    """
    @classmethod
    def __prepare__(cls, class_name, bases, **kwds):
        # create the namespace dict
        enum_dict = _EnumDict()
        return enum_dict

    def __new__(cls, class_name, bases, classdict, **kwds):
        # retrieve enum members
        enum_members = classdict.enum_members

        enum_class = super().__new__(cls, class_name, bases, classdict, **kwds)
        enum_class._member_map_ = OrderedDict()      # name->value map

        for member_name, args in enum_members.items():
            enum_member = object.__new__(enum_class)
            enum_member._name_ = member_name
            enum_member.__objclass__ = enum_class
            enum_member.__init__(*args)
            enum_class._member_map_[member_name] = enum_member

        return enum_class

    def __bool__(cls):
        # classes/types should always be True.
        return True

    def __call__(cls, class_name, members):
        # DEPRECATED
        return cls.create(
            class_name,
            members
        )

    def __contains__(cls, obj):
        if not isinstance(obj, SimpleEnum):
            raise TypeError(
                "unsupported operand type(s) for 'in': '%s' and '%s'"
                % (
                    type(obj).__qualname__, cls.__class__.__qualname__
                )
            )
        return isinstance(obj, cls) and obj._name_ in cls._member_map_

    def __getitem__(cls, name):
        return cls._member_map_[name]

    def __iter__(cls):
        return (member for member in cls._member_map_.values())

    def __len__(cls):
        return len(cls._member_map_)

    @property
    def __members__(cls):
        """
        Returns a mapping of member name->value.
        """
        return cls._member_map_

    def __repr__(cls):
        return "<SimpleEnum %r>" % cls.__name__

    def __reversed__(cls):
        """
        Returns members in reverse definition order.
        """
        return (member for member in reversed(cls._member_map_.values()))

    def create(cls, class_name, members):
        """
        Convenience method to create a new SimpleEnum class.

        `members` can be:

        * A mapping of member name -> value pairs.
        """
        metacls = cls.__class__
        bases = (cls, )
        classdict = metacls.__prepare__(class_name, bases)

        # Stash members into classdict
        classdict.enum_members = members

        enum_class = metacls.__new__(metacls, class_name, bases, classdict)

        # TODO: replace the frame hack if a blessed way to know the calling
        # module is ever developed
        try:
            module = sys._getframe(2).f_globals['__name__']
        except (AttributeError, ValueError, KeyError):
            pass
        if module is None:
            _make_class_unpicklable(enum_class)
        else:
            enum_class.__module__ = module

        return enum_class


class SimpleEnum(metaclass=SimpleEnumMeta):
    def __repr__(self):
        return "<%s.%s: %r>" % (
            self.__class__.__name__, self._name_, self._value_
        )

    def __str__(self):
        return "%s.%s" % (
            self.__class__.__name__, self._name_
        )

    @property
    def name(self):
        return self._name_

    @property
    def value(self):
        return self._value_
