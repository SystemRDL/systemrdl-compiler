
Antlr
=====

This is only required by the developer to re-generate the lexer/parser
based on a grammar file.

From: https://github.com/antlr/antlr4/blob/master/doc/getting-started.md

Download antlr4::

    cd /usr/local/lib
    curl -O http://www.antlr.org/download/antlr-4.7.2-complete.jar

Add some convenience aliases to ``.bash_aliases``::

    export CLASSPATH=".:/usr/local/lib/antlr-4.7.2-complete.jar:$CLASSPATH"
    alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.7.2-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
    alias grun='java org.antlr.v4.gui.TestRig'

Extra alias used in py3antlr4book examples::

    alias antlr4py3='antlr4 -Dlanguage=Python3'

Antlr API reference: http://www.antlr.org/api/Java/index.html
