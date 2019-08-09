Inferred Placement
==================

If unspecified, the elaboration phase needs to assign offets for fields and
addressable components.


Field placement
---------------

Width
^^^^^
* array suffix dictates the field width

    * If fieldwidth property is specified, then it must agree with the array
      suffix (9.7)

* If there is no array suffix

    * inherit width from fieldwidth property. If not set, default to 1-bit
      (9.2.h)

Placement
^^^^^^^^^

addrmap defines properties lsb0/msb0

If in lsb0 mode (default):
    Pack against previous field starting from bit 0

If in msb0 mode:
    Pack against previous field starting from regwidth-1 (9.2 c,d,e)

Who defines regwidth?
    Default is 32



Address Placement
-----------------

Properties
^^^^^^^^^^

'alignment'
    * Component's address is a multiple of alignment
    * Must be ^2
    * Spec says: "if unspecified, alignment is based on register's width."
    * However, this is not consistent with 'compact' addressing rules.
      (ex. if accesswidth < regwidth). Instead, it looks like it is safe to
      assume that if the 'alignment' property is left undefined, then it
      essentially does not contribute to the resulting alignment.
    * Set in: addrmap, regfile

'addressing'
    * Sets addressing modes:

      compact
        * tightly packed. Reg is aligned to 'accesswidth'
        * Spec does not say what the alignment is for other components

            * For now, assuming naive compact packing.
            * Rule checkers will detect if child regs are not aligned to
              'accesswidth'

      regalign
        * component's start address is a multiple of its size
        * Spec implies that it may also be rounded up to next ^2
          (see section 13.4.1-e)

      fullalign
        * Same as regalign except for arrays
        * start address alignment is size of entire array, rounded up to
          next ^2

    * Set in: addrmap

'accesswidth'
    Set in: reg



Calculating base address
^^^^^^^^^^^^^^^^^^^^^^^^

* A = Get alignment based on 'alignment' property, if any
* B = Calculate alignment based on current addressing mode
* C = Get alignment specified by '%=' allocator, if any

resolved_alignment = max(A,B,C)

base address is next address that satisfies resolved_alignment


Calculating stride
^^^^^^^^^^^^^^^^^^

By default, stride is assumed to be the size of the element.

Is it rounded to any alignment?
"Array elements are aligned according to the individual element’s size"
I'm interpreting that as no. just to the size of the contents
Again, rule-checks will catch situations where a register's accesswidth
gets violated.
