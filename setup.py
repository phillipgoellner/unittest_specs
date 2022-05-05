from setuptools import setup

import unittest_specs

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="unittest-specs",
    version=unittest_specs.__version__,
    description="A simple wrapper around the unittest package with different styles for specs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phillipgoellner/unittest_specs",
    project_urls={
        "Source (GitHub)": "https://github.com/phillipgoellner/unittest_specs",
        "Source (GitLab)": "https://gitlab.com/goellnerphillip/unittest_specs"
    },
    author=unittest_specs.__author__,
    license="BSD Three-Clause License",
    packages=["unittest_specs"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
