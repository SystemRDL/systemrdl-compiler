import sys
import os
import platform
import fnmatch
import setuptools

target = platform.system().lower()
PLATFORMS = {'windows', 'linux', 'darwin', 'cygwin'}
for known in PLATFORMS:
    if target.startswith(known):
        target = known

def run_setup(with_binary):
    if with_binary:
        extra_compile_args = {
            'windows': ['/DANTLR4CPP_STATIC', '/Zc:__cplusplus', '/std:c++17'],
            'linux': ['-std=c++17'],
            'darwin': ['-std=c++17'],
            'cygwin': ['-std=c++17'],
        }

        # Define an Extension object that describes the Antlr accelerator
        parser_ext = setuptools.Extension(
            name='systemrdl.parser.sa_systemrdl_cpp_parser',

            # Add the Antlr runtime source directory to the include search path
            include_dirs=["src/systemrdl/parser/ext/antlr4-cpp-runtime"],

            # Rather than listing each C++ file (Antlr has a lot!), discover them automatically
            sources=get_files("src/systemrdl/parser/ext", "*.cpp"),
            depends=get_files("src/systemrdl/parser/ext", "*.h"),

            extra_compile_args=extra_compile_args.get(target, [])
        )
        ext_modules = [parser_ext]
    else:
        ext_modules = []

    setuptools.setup(
        ext_modules=ext_modules,
        cmdclass={"build_ext": ve_build_ext},
    )


#===============================================================================
from setuptools.command.build_ext import build_ext

def get_files(path, pattern):
    """
    Recursive file search that is compatible with python3.4 and older
    """
    matches = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


class BuildFailed(Exception):
    pass


class ve_build_ext(build_ext):
    """
    This class extends setuptools to fail with a common BuildFailed exception
    if a build fails
    """

    def run(self):
        try:
            build_ext.run(self)
        except Exception:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except Exception:
            raise BuildFailed()


# Detect if an alternate interpreter is being used
is_jython = "java" in sys.platform
is_pypy = hasattr(sys, "pypy_version_info")

# Antlr accelerator is no longer supported on older Python versions
is_old_python = sys.version_info[0:2] <= (3, 5)

# Force using fallback python parser under some conditions
using_fallback = is_jython or is_pypy or is_old_python

if not using_fallback:
    try:
        run_setup(with_binary=True)
    except BuildFailed:
        if 'SYSTEMRDL_REQUIRE_BINARY_BUILD' in os.environ:
            # Force failure if binary build is required
            raise
        else:
            using_fallback = True

if using_fallback:
    run_setup(with_binary=False)
