import unittest
from inspect import stack, getmodule
from typing import Callable, Tuple, Type, Any


def describe(description: str, *test_config) -> None:
    """
    Constructs a test suite containing zero or more test cases.

    :param description: intended for documentation of this describe() block; this description is transformed into
    the type name of the generated unittest.TestCase subclass
    :param test_config: zero or more test case defined by it() blocks
    """
    class_name = description.title().replace(" ", "")

    test_class = type(class_name, (unittest.TestCase,),
                      {test_name: test_function for test_name, test_function in test_config})

    module = getmodule(stack()[1][0])
    module.__dict__[class_name] = test_class


def it(description: str, test_def: Callable, intercept: Type[Exception] = None) -> Tuple[str, Callable]:
    """
    Constructs a test case consisting of a description and an assertion line.

    :param description: intended for documentation of this test case; the description is also transformed into the
    test method name
    :param test_def: assertion line passed to describe() block for
    :param intercept: Intercepts an expected Exception object occurring in this it() declaration. If no Exception
    of the specified type is raised, the test fails.
    :return: a tuple composed of the test method name and the assertion line; this is only intended to be
    used by describe()
    """

    if intercept and issubclass(intercept, Exception):
        def intercept_block(_):
            with unittest.TestCase().assertRaises(expected_exception=intercept):
                test_def()

        return f"test_{description.replace(' ', '_')}", intercept_block

    return f"test_{description.replace(' ', '_')}", test_def


def expect(actual_value: Any):
    """
    Sets up an actual value to be compared against an expectation

    :param actual_value: the value computed by the function(ality) to be tested
    :return: an Asserter object providing different ways to define the expected result
    """
    class Asserter(unittest.TestCase):
        def to_be(self, expected_value) -> Callable:
            def run_test(_=None):
                self.assertEqual(actual_value, expected_value)

            return run_test

        def to_not_be(self, expected_value) -> Callable:
            def run_test(_=None):
                self.assertNotEqual(actual_value, expected_value)

            return run_test

        def to_be_of_type(self, expected_type) -> Callable:
            def run_test(_=None):
                self.assertIsInstance(actual_value, expected_type)

            return run_test

        def to_equal_list(self, expected_list) -> Callable:
            def run_test(_=None):
                self.assertListEqual(actual_value, expected_list)

            return run_test

        def to_contain(self, expected_element) -> Callable:
            def run_test(_=None):
                self.assertTrue(expected_element in actual_value)

            return run_test

        def to_contain_all(self, expected_elements) -> Callable:
            def run_test(_=None):
                is_contained = True
                for element in expected_elements:
                    if element not in actual_value:
                        is_contained = False
                        break
                self.assertTrue(is_contained)

            return run_test

        def to_be_true(self) -> Callable:
            def run_test(_=None):
                self.assertTrue(actual_value)

            return run_test

        def to_be_false(self) -> Callable:
            def run_test(_=None):
                self.assertFalse(actual_value)

            return run_test

        def to_be_none(self) -> Callable:
            def run_test(_=None):
                self.assertIsNone(actual_value)

            return run_test

        def to_not_be_none(self) -> Callable:
            def run_test(_=None):
                self.assertIsNotNone(actual_value)

            return run_test

        def to_be_a_list(self) -> Callable:
            return self.to_be_of_type(list)

        def to_be_a_dict(self) -> Callable:
            return self.to_be_of_type(dict)

        def to_be_a_set(self) -> Callable:
            return self.to_be_of_type(set)

        def to_be_of_length(self, expected_length: int) -> Callable:
            def run_test(_=None):
                self.assertEqual(len(actual_value), expected_length)

            return run_test

    return Asserter()
