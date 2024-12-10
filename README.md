[![Documentation Status](https://readthedocs.org/projects/systemrdl-compiler/badge/?version=latest)](http://systemrdl-compiler.readthedocs.io)
[![build](https://github.com/SystemRDL/systemrdl-compiler/workflows/build/badge.svg)](https://github.com/SystemRDL/systemrdl-compiler/actions?query=workflow%3Abuild+branch%3Amain)
[![Coverage Status](https://coveralls.io/repos/github/SystemRDL/systemrdl-compiler/badge.svg?branch=main)](https://coveralls.io/github/SystemRDL/systemrdl-compiler?branch=main)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/systemrdl-compiler.svg)](https://pypi.org/project/systemrdl-compiler)

# SystemRDL Compiler

The `systemrdl-compiler` project implements a generic compiler front-end for
Accellera's [SystemRDL 2.0](http://accellera.org/downloads/standards/systemrdl)
register description language. The goal of this project is to provide a free and
open compiler that lowers the barrier to entry to using an industry standard
register description language.

By providing an elaborated register model that is easy to traverse and query,
it should be far easier to write custom register space view generators.

![overview](https://raw.githubusercontent.com/SystemRDL/systemrdl-compiler/main/docs/img/overview.svg?sanitize=true)

## Documentation
See the [SystemRDL Compiler Documentation](http://systemrdl-compiler.readthedocs.io) for more details

## Related Projects

If you are looking for a complete SystemRDL command line tool, see the [PeakRDL project](https://peakrdl.readthedocs.io).

## License

The SystemRDL Compiler is published and distributed under the [MIT License](LICENSE).
