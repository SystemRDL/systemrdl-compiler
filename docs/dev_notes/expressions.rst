
Expressions
===========

Evaluation Phases
-----------------

Parse phase
^^^^^^^^^^^

* Using Antlr visitor, construct tree of ASTNode classes that represent the
  computation.
* Literals:

    * Any non-aggregate literals are converted directly to their resulting
      types.

        * integer, string, boolean, enum, RDL literals

    * Others result in expression-like placeholders.

        * struct, array
        * These get resolved in the elaboration phase with everything else

* References:

    * All references are looked up in the current namespace
    * Throw error if the result cannot be found
    * Parameter

        * Represented by an "unresolved parameter" class
        * Placeholder until Elaboration phase, where either a default value is
          used, or instantiation's.

    * Instance ref
    * Ref to property value

        * Not clear from spec, but grammar seems to allow it

No semantic/type checking is done. Only checking that is done is that any
references actually refer to something that is in the current namespace.

Visitor returns the resulting ASTNode class as the result.


Parse-exit phase
^^^^^^^^^^^^^^^^

* After an expression tree is constructed, the top-level visitor will return
  the top-level ASTNode object
* Whatever is using this ASTNode (an RDL property assignment) should check that
  the resulting type is compatible with the assignment (or whether it can be
  cast)
* Wrap the top-level ASTNode in the desired AssignmentCast expr operation

    * This is different from a regular cast. All it does is:

        * Implement type casting compatibility checks.
        * Enforces the expression to evaluate in a self determined context.
        * get_value truncates towards the target type as appropriate.

* Run ".predict_type()"

    * This is a function of ASTNode that recurses down and validates that all
      types are compatible.

    * If any errors exist, an error is thrown.

At this point, it should be proof that the expression is allowed to be
evaluated.


Elaboration phase
^^^^^^^^^^^^^^^^^

At this point, a top-level component would have been chosen by the user
and any top-level parameters would have been specified.

Iterate over all expression assignments in the design, and resolve their value
by running ".get_value()". If any parameter remains undefined, throw an error.


Width propagation rules
-----------------------

Expression evaluation follows the same bit-width evaluation rules as
SystemVerilog does in a self-determined context.

The SV spec is slightly vague, but the general process is as follows:

For every expression "region":

* propagate expected bit width bottom-->up based on SV expression rules
* Use resulting top-level bit-width for all expressions within "region"

    * includes up-sizing literals if needed
    * Also upsizes results of a different "region" if needed.

* Propagate calculation using fixed-width 2's complement

A "region" is the set of operations where resulting bit-width is ambiguous:

* Ambiguous:

    * operand of a unary reduction operator
    * operands of a binary logical operator

* Unambiguous:

    * Contents of a cast's value (top's width inherits max(cast, expr) width)


Implementation
^^^^^^^^^^^^^^

Construct ASTNode class tree as usual

Each ASTNode has:

ASTNode.get_min_eval_width()
    * literals return their declared size
    * unary reductions return 1
    * size casts return the fixed size
    * everything else returns the bit width based on children
      according to SV rules
    * non-integral expressions raise a RuntimeError.
      It is up to the caller to know the type of the expression result
      and only call this if width resolution is needed

ASTNode.get_value(eval_width=None)
    * Recursively calls all operands and computes expression's result
    * If eval_width is unset:

        * Parent expression has dictated that this is a self-determined
          context.
        * Query relevant operands to determine the context's evaluation width.

    * If eval_width is irrelevant (ex. comparison operator)

        * ignore the eval_width parameter if it was passed in.
        * don't bother resolving anything. Nothing to do here.

    * Get operand values

        * If eval_width context propagates down to an operand, pass width
          down when calling op.get_value()
        * If an operand is self-determined, call op.get_value() without the
          width.

    * Resolve expression
    * Truncate result down based on the current eval_width
