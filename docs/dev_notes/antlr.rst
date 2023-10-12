
Antlr
=====

This is only required by the developer to re-generate the lexer/parser
based on a grammar file.

From: https://github.com/antlr/antlr4/blob/master/doc/getting-started.md

Download antlr4::

    cd /usr/local/lib
    sudo curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar


Antlr API reference: http://www.antlr.org/api/Java/index.html


Upgrading the Antlr version
---------------------------

* Download latest jar file (See above)
* Install latest python packages::

    python3 -m pip install -U antlr4-python3-runtime speedy-antlr-tool mypy

* Download C++ runtime source distribution from https://www.antlr.org/download.html

    * Extract zip
    * Update: ``<zip file>/runtime/src`` to ``systemrdl/parser/ext/antlr4-cpp-runtime``

* Update ``systemrdl/parser/generate_parser.sh`` to point to the latest antlr jar
* Run ``systemrdl/parser/generate_parser.sh``
* Increment systemrdl minor version
* Update antlr runtime version pins in ``setup.py``
* Run unit tests
* Publish release!
