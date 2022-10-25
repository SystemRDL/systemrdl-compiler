.. _api_udp:

User-Defined Properties
=======================

The SystemRDL standard allows users to extend components with custom properties.
These UDPs are declared within the user's SystemRDL source code prior to use.
Inevitably, these UDPs are processed by a downstream tool that has some
well-defined semantics for these language extensions.
This compiler provides an API that allows tool develoers to define additional
validation for these properties.


Pre-registering a UDP
---------------------
UDP semantics can be pre-loaded into the compiler namespace as a way to formalize
extensions to SystemRDL that your tool supports.

Registration of a UDP is done as follows:

.. code-block:: python

    from systemrdl.udp import UDPDefinition
    from systemrdl.components import Field, Signal

    # 1. Describe your UDP
    class MyUDPDefinition(UDPDefinition):
        name = "my_udp"
        valid_components = {Field, Signal}
        valid_type = int

        # Optional callback that validates values assigned to 'my_udp'
        def validate(self, node, value):
            if(value == 42):
                self.msg.error(
                    "The value assigned to 'my_udp' cannot be 42! That number is reserved.",
                    self.get_src_ref(node)
                )

    # 2. Register it with your RDLCompiler instance
    rdlc.register_udp(MyUDPDefinition)

The above definition is equivalent to the following SystemRDL:

.. code-block:: systemrdl

    property my_udp {
        type = longint unsigned;
        component = field | signal;
    };


Soft UDPs
---------
By default, :meth:`~systemrdl.RDLCompiler.register_udp()` registers
UDPs as "soft" definitions. Soft UDP definitions behave as follows:

* The UDP is not available to be used until it is explicitly defined in the
  SystemRDL source. If a user attempts to use a soft UDP prior to it being
  declared, the compiler will flag an error.
* Upon definition, the user's declaration shall be equivalent to the
  pre-registered definition. If the user's declaration does not match, the
  compiler will flag an error.
  This ensures that the user's declaration matches the expectations of your tool.
* If the user's RDL source never defines the UDP, querying it via
  ``node.get_property()`` will gracefully return its unassigned default (as
  defined by :meth:`~systemrdl.udp.UDPDefinition.get_unassigned_default()`)
  instead of a ``LookupError`` exception. This simplifies how tool developers
  interact with users' RDL code.
* Once defined by the user in RDL source, the UDP is no longer considered
  'soft', and can be assigned normally.


.. important::
    Although it may initially seem like more steps for the end-user, having them
    declare the UDP in the RDL source is preferred over pre-declaring "hard"
    UDPs within your tool.

    Silently declaring hard UDPs not recommended since it encourages users to write
    SystemRDL that uses UDP extensions that are not formally declared in the
    RDL source. This bends the rules of the SystemRDL specification and hurts
    the cross-vendor compatibility of your users' SystemRDL source code.

    Using soft UDPs has the benefit of enforcing that the user
    defines and uses UDPs correctly whilst not violating the official
    SystemRDL language specification.


The UDPDefinition descriptor
----------------------------

The full details of the ``UDPDefinition`` class is as follows:

Class variables and methods that you can define
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: systemrdl.udp.UDPDefinition
    :members: name, valid_components, valid_type, default_assignment, constr_componentwidth, validate, get_unassigned_default
    :member-order: bysource

Utilities
^^^^^^^^^

.. autoclass:: systemrdl.udp.UDPDefinition
    :noindex:
    :members: msg, get_src_ref
