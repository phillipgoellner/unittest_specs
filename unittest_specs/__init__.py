"""
unittest-specs

A simple wrapper around the unittest package with different styles for specs
"""

__version__ = "1.2.0"
__author__ = "Phillip Goellner"


from unittest_specs.simple_test_spec import SimpleFlatSpec
from unittest_specs.fun_test_spec import describe, it, expect
from unittest_specs.with_test_spec import scenario, setup, run, assertion, teardown
