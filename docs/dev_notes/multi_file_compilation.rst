.. _multifile_compilation:

Multi-file Compilation
======================

The ability to split a SystemRDL register model into several RDL files seems
like an inherently useful way to manage a design that spans multiple
components.

Unfortunately, the SystemRDL 2.0 spec provides no insight on how "compilation
units" are handled. Below are the assumptions I made to guide the
implementation of this compiler.


Each file is its own compilation unit
-------------------------------------

* The contents of files included using one or more `include` directives become
  part of the compilation unit of the file within which they are included.
* Declarations must be completed within the boundaries of a compilation unit.
  If there is a declaration that is incomplete at the end of a compilation
  unit, it shall be a compile error.
* Any Verilog-style preprocessor macros defined within a file are discarded at
  the end of the compilation unit.

**Rationale**

Isolating each file provided to the compiler to a design unit reduces
confusing scenarios where things like preprocessor macros 'leak' unexpectedly
between files.



Namespaces are global across compilation units
----------------------------------------------
The root scope of the official SystemRDL namespaces are shared across files.

Specifically the three namespaces described in the SystemRDL 2.0 spec:

* **Type namespace**

  Component definitions, enum types, and struct types

* **Element namespace**

  In the $root scope, this is limited to signal instances.
* **Property namespace**

  User-defined properties declared in the root scope

**Rationale**

If supporting multiple file compile, then sharing these namespaces is
essential.



Default property assignments are limited to the compilation unit
----------------------------------------------------------------
Any default property assignments made in the root scope are limited to the
current compilation unit. Default property assignments are discarded from the
root scope at the end of each compilation unit.

**Rationale**

Allowing default property assignments to carry over between files/compilation
units would be incredibly confusing.
A default property assignment in a prior design unit's root scope would
inevitably influence all subsequent files, causing all kinds of unintended
consequences.
