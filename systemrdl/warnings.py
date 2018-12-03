
#: Warn if a field that implements storage is missing it's reset value
MISSING_RESET = 1<<0

#: Warn if a field's bit offset is not explicitly specified
IMPLICIT_FIELD_POS = 1<<1

#: Warn if a component's address offset is not explicitly assigned
IMPLICIT_ADDR = 1<<2

#: Enable all warnings
ALL = MISSING_RESET | IMPLICIT_FIELD_POS | IMPLICIT_ADDR
