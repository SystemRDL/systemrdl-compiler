import sys
import os
import platform
import fnmatch
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

# Replace relative image path with github-hosted one
long_description = long_description.replace(
    "docs/img/overview.svg",
    "https://raw.githubusercontent.com/SystemRDL/systemrdl-compiler/main/docs/img/overview.svg?sanitize=true"
)

with open(os.path.join("systemrdl", "__about__.py"), encoding='utf-8') as f:
    v_dict = {}
    exec(f.read(), v_dict)
    rdl_version = v_dict['__version__']

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
            include_dirs=["systemrdl/parser/ext/antlr4-cpp-runtime"],

            # Rather than listing each C++ file (Antlr has a lot!), discover them automatically
            sources=get_files("systemrdl/parser/ext", "*.cpp"),
            depends=get_files("systemrdl/parser/ext", "*.h"),

            extra_compile_args=extra_compile_args.get(target, [])
        )
        ext_modules = [parser_ext]
    else:
        ext_modules = []

    setuptools.setup(
        name="systemrdl-compiler",
        version=rdl_version,
        author="Alex Mykyta",
        author_email="amykyta3@github.com",
        description="Parse and elaborate front-end for SystemRDL 2.0",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/SystemRDL/systemrdl-compiler",
        packages=setuptools.find_packages(exclude=["test"]),
        include_package_data=True,
        ext_modules=ext_modules,
        cmdclass={"build_ext": ve_build_ext},
        python_requires='>=3.5.2',
        install_requires=[
            "antlr4-python3-runtime >= 4.11, < 4.12",
            "colorama",
            "markdown",
        ],
        classifiers=(
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3 :: Only",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
            "Topic :: Software Development :: Compilers",
            "Topic :: Software Development :: Code Generators",
        ),
        project_urls={
            "Documentation": "http://systemrdl-compiler.readthedocs.io",
            "Source": "https://github.com/SystemRDL/systemrdl-compiler",
            "Tracker": "https://github.com/SystemRDL/systemrdl-compiler/issues",
        },
    )


#===============================================================================
from setuptools.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

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
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError):
            raise BuildFailed()
        except ValueError:
            # this can happen on Windows 64 bit, see Python issue 7511
            if "'path'" in str(sys.exc_info()[1]):  # works with Python 2 and 3
                raise BuildFailed()
            raise


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
