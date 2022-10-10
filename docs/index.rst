

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

Install from `PyPi`_ using pip

.. code-block:: bash

   python3 -m pip install systemrdl-compiler

.. _PyPi: https://pypi.org/project/systemrdl-compiler

Embedded Perl Preprocessor
^^^^^^^^^^^^^^^^^^^^^^^^^^
If source files contain embedded Perl preprocessor tags, an installation of
Perl that is visible through the ``PATH`` environment variable is required.

Windows users will have to `download and install Perl separately. <https://www.perl.org/get.html>`_

Links
-----

- `Source repository <https://github.com/SystemRDL/systemrdl-compiler>`_
- `Release Notes <https://github.com/SystemRDL/systemrdl-compiler/releases>`_
- `Issue tracker <https://github.com/SystemRDL/systemrdl-compiler/issues>`_
- `PyPi <https://pypi.org/project/systemrdl-compiler>`_
- `SystemRDL Specification <http://accellera.org/downloads/standards/systemrdl>`_



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

.. toctree::
   :hidden:
   :caption: Examples

   examples/print_hierarchy
   examples/json_exporter
   examples/json_importer

.. toctree::
   :hidden:
   :caption: API Reference

   api/compiler
   api/udp
   api/node
   api/walker
   api/component
   api/types
   api/messages
   api/source_ref
   api/importer

.. toctree::
   :hidden:
   :caption: Developer Notes

   dev_notes/rdl_spec_errata
   dev_notes/logbook

.. toctree::
   :hidden:
   :caption: Other

   property_reference
   known_issues
   genindex
