import unittest
from inspect import stack, getmodule
from typing import Callable, Tuple


def describe(description: str, *test_config) -> None:
    """
    Constructs a ... containing zero or more test cases.

    :param description:
    :param test_config:
    """
    class_name = description.title().replace(" ", "")

    test_class = type(class_name, (unittest.TestCase,),
                      {test_name: test_function for test_name, test_function in test_config})

    module = getmodule(stack()[1][0])
    module.__dict__[class_name] = test_class


def it(description: str, test_def: Callable) -> Tuple[str, Callable]:
    """
    Constructs a test case consisting of a description and an assertion line.

    :param description: intended for documentation of this test case; the description is also transformed into the
    test method name
    :param test_def: assertion line passed to describe() block for
    :return: a tuple composed of the test method name and the assertion line; this is only intended to be
    used by describe()
    """
    return f"test_{description.replace(' ', '_')}", test_def


def expect(actual_value):
    def _get_actual_value():
        return actual_value() if hasattr(actual_value, '__call__') else actual_value

    class Asserter(unittest.TestCase):

        def to_be(self, expected_value) -> Callable:
            def run_test(_):
                self.assertEqual(expected_value, _get_actual_value())

            return run_test

        def to_not_be(self, expected_value) -> Callable:
            def run_test(_):
                self.assertNotEqual(expected_value, _get_actual_value())

            return run_test

        def to_be_of_type(self, expected_type) -> Callable:
            def run_test(_):
                self.assertIsInstance(_get_actual_value(), expected_type)

            return run_test

        def to_equal_list(self, expected_list) -> Callable:
            def run_test(_):
                self.assertListEqual(expected_list, _get_actual_value())

            return run_test

        def to_contain(self, expected_element) -> Callable:
            def run_test(_):
                self.assertTrue(expected_element in _get_actual_value())

            return run_test

        def to_contain_all(self, expected_elements) -> Callable:
            def run_test(_):
                is_contained = True
                for element in expected_elements:
                    if element not in _get_actual_value():
                        is_contained = False
                        break
                self.assertTrue(is_contained)
            return run_test

        def to_be_true(self) -> Callable:
            def run_test(_):
                self.assertTrue(_get_actual_value())

            return run_test

        def to_be_false(self) -> Callable:
            def run_test(_):
                self.assertFalse(_get_actual_value())

            return run_test

        def to_be_none(self) -> Callable:
            def run_test(_):
                self.assertIsNone(_get_actual_value())

            return run_test

        def to_not_be_none(self) -> Callable:
            def run_test(_):
                self.assertIsNotNone(_get_actual_value())

            return run_test

        def to_be_a_list(self) -> Callable:
            return self.to_be_of_type(list)

        def to_be_a_dict(self) -> Callable:
            return self.to_be_of_type(dict)

        def to_be_a_set(self) -> Callable:
            return self.to_be_of_type(set)

        def to_be_of_length(self, expected_length: int) -> Callable:
            def run_test(_):
                self.assertEqual(expected_length, len(_get_actual_value()))

            return run_test

    return Asserter()
