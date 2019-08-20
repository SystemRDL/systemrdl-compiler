
Compilation
===========

Phases of compilation
---------------------

1. Preprocessing
^^^^^^^^^^^^^^^^

Verilog & Perl preprocessing.

2. Lex & Parse
^^^^^^^^^^^^^^

* Handled by Antlr
* Creates a parse tree

3. Compile
^^^^^^^^^^

* Walk the parsed tree and construct our Python class objects
* As types/parameters/etc are defined, a namespace stack is maintained
* Identifiers are always resolved immediately

    * If an id token is not within any available namespace, then throw an
      error immediately

* Instance tree is created
* All expressions are left unresolved

    * Class representation of the expression is kept so that any parameters
      in it can be fully resolved later.

* Dynamic property assignments replace property expressions as they are
  seen.

4. Elaborate
^^^^^^^^^^^^

In the following order:

1. User specifies a single top-level component from root

    * Specifies any parameters where applicable

2. All expressions are resolved to their resulting values

    * Parameters
    * Properties
    * Instance addressing expressions
    * Instance array sizes

3. Resolve item addresses

4. Component type names are uniquified according to RDL rules in section
   5.1.1.4


5. Validate
^^^^^^^^^^^

Perform structural validation checks



Component Model Structure
-------------------------

Everything encapsulated into a single class type per component:

* Members assigned during definition:

    * type_name
    * children
    * parameters
    * properties

* Members assigned during instantiation:

    * is_instance = True
    * external
    * inst_name
    * original_def

* Type-specific instance members:

    * addressable component stuff
    * or a vector instance



Instantiations
^^^^^^^^^^^^^^

When a named definition is instantiated, the original definition object is
deepcopied to become the instance.
The instance-specific members are filled in, including ``original_def`` which
holds a reference back to the original.
``original_def`` is always excluded from any deepcopy operations

Instances of anonymous definitions probably do not need to be deepcopied
since they are guaranteed to be unique

Parameters
^^^^^^^^^^

Parameter expressions are directly overridden during instantiation
No other special action needs to be taken
A Post-elaborate step will adjust the type_name appropriately as per
the spec's uniquification rules.


Signal References
^^^^^^^^^^^^^^^^^

Signals are described in the RDL spec as "non-structural"
This, as well as their usage seems to imply that their hierarchical
instantiation is not really relevant. Still, since they get instantiated,
signals become part of the hierarchy.


Dynamic property assignments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Replacing the expression on assignment is OK
Extra consideration needs to be made if the assignment is a component reference
since the target reference may be outside of the original component's scope
(UpRef).


User traversal
^^^^^^^^^^^^^^
Use a Node overlay in order to provide consistent array unrolling lineage
This is also a good way to divide model storage from model
manipulation/interpretation. Derived properties go here.
