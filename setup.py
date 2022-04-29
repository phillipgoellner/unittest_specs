from setuptools import setup

import unittest_specs

setup(
    name="unittest-specs",
    version=unittest_specs.__version__,
    description="A simple wrapper around the unittest package with different styles for specs",
    url="https://github.com/phillipgoellner/unittest-specs",
    author=unittest_specs.__author__,
    license="GPL-3.0 License",
    packages=["unittest_specs"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
