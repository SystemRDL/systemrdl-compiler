
#: Warn if a field that implements storage is missing it's reset value
MISSING_RESET = 1<<0

#: Warn if a field's bit offset is not explicitly specified
IMPLICIT_FIELD_POS = 1<<1

#: Warn if a component's address offset is not explicitly assigned
IMPLICIT_ADDR = 1<<2

#: Warn if an instance array's address stride is not a power of two
STRIDE_NOT_POW2 = 1<<3

#: Enforce that all addressable components are aligned based on their size.
#: Alignment is determined by the component's size rounded up to the next power
#: of two.
#: 
#: Strict self-alignment may be desireable since it can simplify address decode
#: logic for hierarchical designs.
#:
#: This rule is a superset of ``STRIDE_NOT_POW2``
STRICT_SELF_ALIGN = 1<<4

#-------------------------------------------------------------------------------
#: Enable all warnings
ALL = (
    MISSING_RESET 
    | IMPLICIT_FIELD_POS
    | IMPLICIT_ADDR
    | STRIDE_NOT_POW2
    | STRICT_SELF_ALIGN
)
