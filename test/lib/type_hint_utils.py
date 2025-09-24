import typing
import inspect

def hint_is_a_generic(hint) -> bool:
    """
    Typing generics have an __origin__ attribute
    """
    if "__origin__" in dir(hint):
        return True
    return False

def hint_is(hint, generic_origin) -> bool:
    """
    Compare whether the hint matches a generic origin
    """
    if not hint_is_a_generic(hint):
        return False
    return hint.__origin__ == generic_origin


def value_is_compatible(value, hint) -> bool:
    """
    Given any value, check whether it is compatible with a type hint annotation
    """
    if hint_is_a_generic(hint):
        # Unpack the generic
        if hint_is(hint, typing.Union):
            # Check if value matches any of the types in the Union
            for arg_hint in hint.__args__:
                if value_is_compatible(value, arg_hint):
                    return True
            return False
        elif hint_is(hint, type):
            if not inspect.isclass(value):
                return False
            expected_type = hint.__args__[0]
            return issubclass(value, expected_type)
        elif hint_is(hint, list):
            # Check if value is a list
            if inspect.isclass(value):
                return False
            if not isinstance(value, list):
                return False
            # Check that all members of the list match the expected list type
            expected_hint = hint.__args__[0]
            for element in value:
                if not value_is_compatible(element, expected_hint):
                    return False
            return True
        elif hint_is(hint, dict):
            # Check if value is a dict
            if inspect.isclass(value):
                return False
            if not isinstance(value, dict):
                return False
            expected_key_hint, expected_value_hint = hint.__args__
            # Check that all keys match the expected type
            for key in value.keys():
                if not value_is_compatible(key, expected_key_hint):
                    return False
            # Check that all values match the expected type
            for element in value.values():
                if not value_is_compatible(element, expected_value_hint):
                    return False
            return True
        else:
            raise RuntimeError(f"Unhandled generic {hint}: {hint.__origin__}")

    if hint is typing.Any:
        return True

    # hint is an actual class
    return isinstance(value, hint)
