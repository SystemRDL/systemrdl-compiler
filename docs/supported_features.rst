
Supported RDL Features
======================

.. role:: red
.. role:: yellow
.. role:: green

.. raw:: html

    <style>
        .red {color:#c00;} 
        .yellow {color:#c60;} 
        .green {color:#0c0;}
      
        /* override table width restrictions */
        @media screen and (min-width: 767px) {
            .wy-table-responsive table td {
                white-space: normal;
            }
            .wy-table-responsive {
                overflow: visible;
            }
        }
    </style>


Below is a rough enumeration of SystemRDL 2.0 features, and their current state
of support by the compiler.

The *priority* column denotes how high the item is on my to-do list:

- 5: Highest priority. I don't consider the tool usable until this is done
- 3-4: Definitely plan on implementing
- 1-2: Would be nice.



.. list-table:: 
    :header-rows: 1
    :widths: 25 10 10 55
    
    *   - Feature
        - Supported
        - Priority
        - Description


    *   - Signal component
        - :green:`Yes`
        - 
        - 

    *   - Field component
        - :green:`Yes`
        - 
        - 

    *   - Reg component
        - :green:`Yes`
        - 
        - 

    *   - Addrmap component
        - :green:`Yes`
        - 
        - 

    *   - Regmap component
        - :green:`Yes`
        - 
        - 

    *   - Mem component
        - :green:`Yes`
        - 
        - 

    *   - constraint block
        - :red:`No`
        - 3
        - 

    *   - user-defined properties
        - :red:`No`
        - 5
        - 

    *   - Parameterized components
        - :green:`Yes`
        - 
        - 

    *   - Property assignment
        - :green:`Yes`
        - 
        - 

    *   - Default property assignment
        - :yellow:`Partial`
        - 5
        - Assigning a hierarchical instance reference to a default property is not supported yet

    *   - Dynamic property assignment
        - :green:`Yes`
        - 
        - 

    *   - interrupt property modifier
        - :red:`No`
        - 5
        - 

    *   - Property references
        - :red:`No`
        - 4
        - References to a component's signal-like property (Table G1: Ref target)

    *   - ispresent property
        - :green:`Yes`
        - 
        - Iterators skip non-present components by default

    *   - Hierarchical instance references
        - :green:`Yes`
        - 
        - 

    *   - Addressing modes
        - :green:`Yes`
        - 
        - compact, regalign, fullalign

    *   - Address allocation operators
        - :green:`Yes`
        - 
        - @, +=, and %= operators

    *   - Inferred field placement
        - :green:`Yes`
        - 
        - lsb0 and msb0 modes. Explicit and implied

    *   - alias instances
        - :green:`Yes`
        - 
        - 

    *   - internal/external instances
        - :green:`Yes`
        - 
        - 

    *   - array datatype
        - :red:`No`
        - 5
        - 

    *   - enum datatype
        - :red:`No`
        - 5
        - 

    *   - struct datatype
        - :red:`No`
        - 4
        - 

    *   - Numeric datatypes
        - :green:`Yes`
        - 
        - 

    *   - string datatype
        - :green:`Yes`
        - 
        - 

    *   - boolean datatype
        - :green:`Yes`
        - 
        - 

    *   - Arithmetic operators
        - :green:`Yes`
        - 
        - 

    *   - Binary operators
        - :green:`Yes`
        - 
        - 

    *   - Reduction operators
        - :green:`Yes`
        - 
        - 

    *   - Shift operators
        - :green:`Yes`
        - 
        - 

    *   - Static casting
        - :green:`Yes`
        - 
        - 

    *   - Relational operators
        - :yellow:`Partial`
        - 5
        - Only support numeric comparisons

    *   - Concatenate operator
        - :red:`No`
        - 5
        - 

    *   - Replication operator
        - :red:`No`
        - 5
        - 

    *   - Semantic checking
        - :red:`No`
        - 5
        - 

    *   - Perl preprocessing
        - :red:`No`
        - 2
        - 

    *   - Verilog-style preprocessing
        - :red:`No`
        - 2
        - 

    *   - RDLFormatCode String post-processing
        - :red:`No`
        - 3
        - 
