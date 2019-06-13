
SystemRDL Property Reference
============================

This page summarizes all of the properties described in the SystemRDL spec.
This is only intended for quick reference. For more details on usage and
semantics, refer to the full `SystemRDL 2.0 specification <http://accellera.org/downloads/standards/systemrdl>`_.

Global Properties
-----------------

.. csv-filter:: Global Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: 'ALL'}
   :included_cols: 0, 2, 4
   :widths: auto


Field Properties
----------------

.. csv-filter:: Software Access Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bfield\\b', 3: 'sw access'}
   :included_cols: 0, 2, 4
   :widths: auto

.. csv-filter:: Hardware Access Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bfield\\b', 3: 'hw access'}
   :included_cols: 0, 2, 4
   :widths: auto

.. csv-filter:: Counter Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bfield\\b', 3: 'counter'}
   :included_cols: 0, 2, 4
   :widths: auto

.. csv-filter:: Interrupt Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bfield\\b', 3: 'interrupt'}
   :included_cols: 0, 2, 4
   :widths: auto

.. csv-filter:: Verification Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bfield\\b', 3: 'verif'}
   :included_cols: 0, 2, 4
   :widths: auto

.. csv-filter:: Misc Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bfield\\b', 3: 'misc'}
   :included_cols: 0, 2, 4
   :widths: auto

Register Properties
-------------------

.. csv-filter:: Register Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\breg\\b'}
   :included_cols: 0, 2, 4
   :widths: auto

Address Map Properties
----------------------

.. csv-filter:: Address Map Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\baddrmap\\b'}
   :included_cols: 0, 2, 4
   :widths: auto

Register File Properties
------------------------

.. csv-filter:: Register File Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bregfile\\b'}
   :included_cols: 0, 2, 4
   :widths: auto

Memory Properties
-----------------
.. csv-filter:: Memory Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bmem\\b'}
   :included_cols: 0, 2, 4
   :widths: auto

Signal Properties
-----------------

.. csv-filter:: Signal Properties
   :header-rows: 1
   :file: properties.csv
   :include: {1: '.*\\bsignal\\b'}
   :included_cols: 0, 2, 4
   :widths: auto
