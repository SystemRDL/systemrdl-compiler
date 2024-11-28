# Contributing to the SystemRDL Compiler
We love your input! We want to make contributing to this project as easy and
transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer


## Open an issue using the [Issue Tracker](https://github.com/SystemRDL/systemrdl-compiler/issues)
Talking to us is the easiest way to contribute! Report a bug or feature request by
[opening a new issue](https://github.com/SystemRDL/systemrdl-compiler/issues).

Issue submission expectations:
* Please keep each issue submission limited to one topic. This helps us stay organized.
* Before opening an issue, check if one already exists for your topic. It may have already been discussed.
* If submitting a bug, provide enough details so we can reproduce it on our end. (version number, example SystemRDL, etc...)
* If submitting a feature request, please make sure ...
    * ... it does not violate the semantics of the SystemRDL standard.
      Submissions that would change the interpretation of the SystemRDL language
      and are not faithful to the [Accellera SystemRDL specification](http://accellera.org/downloads/standards/systemrdl) will be rejected.
      Additional notes on the spec's interpretation can be found in [our unofficial errata page](https://systemrdl-compiler.readthedocs.io/en/latest/dev_notes/rdl_spec_errata.html).
    * ... it does not break API compatibility. The SystemRDL compiler is a core
      component of many tools across numerous organizations. Any changes to the
      API need to be done with very careful consideration.
* Please be patient! This project is run by volunteers that are passionate about
  improving the state of register automation. Much of the work is done in their free time.


## Contribute code using a pull request
Pull requests are the best way to propose changes to the codebase. We actively
welcome your pull requests. To maximize the chance of your pull request getting accepted,
please review the expectations below.

Pull request expectations:
* Before starting a pull request, please consider discussing the change with us
  first by **opening an issue ticket**. Unfortunately many of the PRs that get rejected
  are because they implement changes that do not align with the  mission of this
  compiler project.
* PRs shall only contain only one feature/bug/concept change. **Bulk PRs that change numerous unrelated things will be rejected**.
* Use meaningful commit messages, squash commits as appropriate.

How to submit a PR:
1. Fork the repo and create your feature/bugfix branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Submit the pull request!

## Run the tests
Run: test/run.sh

If you see an error like:
```
fatal error: Python.h: No such file or directory
```
then install the header files and static libraries for python dev as instructed
at https://stackoverflow.com/questions/21530577

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions are understood to be
under the same [MIT License](http://choosealicense.com/licenses/mit/) that
covers this project. Feel free to contact the maintainers if that's a concern.
