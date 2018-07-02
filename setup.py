import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="systemrdl-compiler",
    version="0.1",
    author="Alex Mykyta",
    author_email="amykyta3@github.com",
    description="Parse and elaborate front-end for SystemRDL 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SystemRDL/systemrdl-compiler",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
