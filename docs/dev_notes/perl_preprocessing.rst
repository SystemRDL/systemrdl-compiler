
.. _dev_notes-perl:

Perl Preprocessing
==================

Perl preprocessing is implemented in the following four steps:

* Tokenize
* Generate Preprocessor Text Segment List
* Generate and run a Perl "miniscript"
* Generate flattened output text

Consider the following simple example text:

.. code-block:: systemrdl

    reg myReg {
        <%for( $i = 0; $i < 4; $i += 1 ) {%>
        myField data<%=$i%> [1];
        <% } %>
    };


Tokenize
--------

The source file text is scanned using a simple regex-based tokenizer.
The tokenizer identifies the character positions of of all Perl preprocessor
tags, while still being aware of line and block comments.
Perl tags inside comments are ignored since comment-capturing regexes match
first.

The example RDL results in three Perl tags being found.


Generate Preprocessor Text Segment List
---------------------------------------

Using the list of Perl tag coordinates, a list of "preprocessor segments" is
generated. Each segment represents a selection of the input text.

A segment can be one of the following:

* Perl Command Segment

    * Encloses Perl statements to be run by a Perl interpreter
    * ``<% perl statements %>``

* Perl Emit Segment

    * Encloses a Perl expression that will be "printed" to the preprocessed
      output.
    * ``<%=perl_expression%>``

* Unaltered Text Segment

    * All other text that is outside of Perl tags

The example RDL results in the following segments to be generated:

* [0] Unaltered Text: ``reg myReg {``
* [1] Perl Command: ``for( $i = 0; $i < 4; $i += 1 ) {``
* [2] Unaltered Text: ``myField data``
* [3] Perl Emit: ``$i``
* [4] Unaltered Text: ``[1];``
* [5] Perl Command: ``}``
* [6] Unaltered Text: ``};``


Generate and run a Perl "miniscript"
------------------------------------

In order to interpret embedded Perl statements, and their effect on text
output, a reference-based Perl "miniscript" is generated based on the segment
list. This miniscript is run in a restricted Perl context and generates a list
of text emit directions.

The restricted Perl context uses Perl's `Safe <https://perldoc.perl.org/Safe.html>`_
package to prevent the user from performing various IO operations, and other
potentially malicious things.

Example RDL results in the following Perl miniscript:

.. code-block:: perl

    rdlppp_utils::emit_ref(0);
    for( $i = 0; $i < 4; $i += 1 ) {
        rdlppp_utils::emit_ref(2);
        rdlppp_utils::emit_text(3, $i);
        rdlppp_utils::emit_ref(4);
    }
    rdlppp_utils::emit_ref(5);

... which generates the following emit directions that are returned to the
python environment:

* emit segment [0]
* emit segment [2]
* emit text "0"
* emit segment [4]
* emit segment [2]
* emit text "1"
* emit segment [4]
* emit segment [2]
* emit text "2"
* emit segment [4]
* emit segment [2]
* emit text "3"
* emit segment [4]
* emit segment [5]


Generate flattened output text
------------------------------

Emit directions are used to concatenate unaltered text segments and Perl output
text strings to form the preprocessed output.
