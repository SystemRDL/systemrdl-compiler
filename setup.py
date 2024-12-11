import os
import platform
import setuptools
from glob import glob

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
            sources=glob("src/systemrdl/parser/ext/**/*.cpp", recursive=True),
            depends=glob("src/systemrdl/parser/ext/**/*.h", recursive=True),

            extra_compile_args=extra_compile_args.get(target, []),
            define_macros=[("Py_LIMITED_API", "0x03070000")],
            py_limited_api=True,
        )
        ext_modules = [parser_ext]
        options = {"bdist_wheel": {"py_limited_api": "cp37"}}
    else:
        ext_modules = []
        options = {}

    setuptools.setup(
        ext_modules=ext_modules,
        cmdclass={"build_ext": ve_build_ext},
        options=options,
    )


#===============================================================================
from setuptools.command.build_ext import build_ext

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

using_fallback = False
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
