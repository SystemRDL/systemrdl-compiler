
Properties
==========

The Property Rulebook
---------------------

SystemRDL defines a vast assortment of properties that can be specified for
each component definition. Each property has its own set of semantics, and
quirks. The PropertyRuleBook class provides an interface to query each
property's rule class. It also maintains a list of user-defined property rules.

Each property rule is encoded as a Python class with various static variables
and classmethods

Each rule class has the following static variables set:

* Property name
* List of component types it can be applied to
* List of types that are allowed to be assigned to it
* Whether it can be dynamically assigned
* List of mutually exclusive other properties
* Unambiguous default value, if any

Rule classes also have the following classmethods:

assign_value(cls, comp_def, value)
    Used by the compiler for either static or dynamic prop assignments
    After the value's type has been validated to be appropriate, and mutex
    rules checked, apply it to the component def.
    Base class will simply toss it in the property dictionary.
    Some properties extend this if they have additional side-effects
    that impact other properties

get_default(cls, node)
    Used when the user queries a property, and it was not explicitly set.
    Default values are not always directly known. Sometimes they
    depend on one or more other properties.
    The base class will simply return the static variable's value
    but for more complex ones, this method will derive it from the
    context class


Property Parsing
----------------

For local property assignments, the parse visitor will blindly collect all
properties into a dict, where the key is the property name.
If any assignment already exists in the dict, throws an error immediately.

At the end of the component body, flip through each local property assignment
and:

* Check for mutex collisions
* Coerce assignments to appropriate type (predict expr type, assignment cast,
  etc...)


Misc
----

In grammar, property names include existing keywords, and other non-keyword ID

LHS assignments can be:

* numeric
* reference to a signal instance
* reference to a "virtual signal" property
* Reference to any other component types? I don't think so?

RHS references can be:

* only a "virtual signal" property of a field or reg

    * These are shown in the spec in Annex G, marked under the "Ref target"
      column.
    * It looks like RHS reference to copy a component property's value is NOT a
      thing. In fact, it hardly has anything to do with the property that bears
      its name. Instead, it looks like its reference implies a "virtual signal"
      that has its own dynamic behavior based on the component's state.

Misc rules
^^^^^^^^^^
* Each property has an expected type

    * Some can accept more than one type (numeric OR signal ref)

* Some properties are mutually exclusive

    * Each mutex set is listed in Annex G

* Not all are allowed to be dynamically assigned

Default properties
^^^^^^^^^^^^^^^^^^

User-set defaults are propagated according to namespace scope, not by
structural parent->child inheritance
Defaults may need to be propagated at parse time instead
Spec basically implies another "default property" namespace
