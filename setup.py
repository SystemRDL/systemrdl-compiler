import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Replace relative image path with github-hosted one
long_description = long_description.replace(
    "docs/img/overview.svg",
    "https://raw.githubusercontent.com/SystemRDL/systemrdl-compiler/master/docs/img/overview.svg?sanitize=true"
)

with open(os.path.join("systemrdl", "__about__.py")) as f:
    v_dict = {}
    exec(f.read(), v_dict)
    rdl_version = v_dict['__version__']

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
    install_requires=[
        "antlr4-python3-runtime",
        "colorama",
    ],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
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
