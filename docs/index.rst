

SystemRDL Compiler
==================

The ``systemrdl-compiler`` module implements a generic compiler front-end for
Accellera's `SystemRDL 2.0`_ register description language. The goal of this
project is to provide a free and open compiler that lowers the barrier to entry
to using an industry standard register description language.

By providing an elaborated register model that is easy to traverse and query,
it should be far easier to write custom register space view generators.

.. image:: img/overview.svg
   :align: center

.. _SystemRDL 2.0: http://accellera.org/downloads/standards/systemrdl

Installing
----------

Install using pip

.. code-block:: bash
   
   pip3 install systemrdl-compiler


.. toctree::
   :hidden:
   :caption: Introduction
   
   self
   
.. toctree::
   :hidden:
   :caption: Getting Started
   
   model_structure
   model_traversal
   properties
   examples
   
.. toctree::
   :hidden:
   :caption: Class Reference
   
   api/compiler
   api/node
   api/walker
   api/component
   api/types
   api/messages

.. toctree::
   :hidden:
   :caption: Other
   
   known_issues
   genindex
