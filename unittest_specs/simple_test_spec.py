import unittest
from typing import Any


class SimpleFlatSpec(unittest.TestCase):
    @staticmethod
    def expect(actual_value: Any):
        """
        Set up an 'actual' value to be compared against an expectation/assertion.

        :param actual_value: the value computed by the SUT to be compared against an expectation
        :return: an Asserter to perform an assertion on
        """
        return Asserter(actual_value)

    @staticmethod
    def parameterize(params):
        """
        Injects provided test data sets into the decorated function with every data set being provided as a set of
        parameters. For each set, a separate sub-test is performed using unittest's subTest.

        :param params: a list of tuples containing the test data
        """

        def decorator_function(function):
            def parameter_handler(self):
                for param in params:
                    if isinstance(param, tuple):
                        test_params = [_p for _p in param]
                    else:
                        test_params = [param]

                    with self.subTest(i=test_params[0]):
                        function(self, *test_params)

            return parameter_handler

        return decorator_function

    @staticmethod
    def intercept(expected_exception):
        """
        Intercepts an expected Exception object occurring the decorated test function. If no Exception
        of the specified type is raised, the test fails.

        :param expected_exception: the Exception type that is expected to occur
        """

        def decorator_function(function):
            def nested_execution_handler(self, *args, **kwargs):
                interceptor = unittest.TestCase()

                with interceptor.assertRaises(expected_exception=expected_exception):
                    function(self, *args, **kwargs)

            return nested_execution_handler

        return decorator_function


class Asserter(unittest.TestCase):
    def __init__(self, actual_value: Any):
        super().__init__()
        self._actual_value = actual_value

    def to_be(self, expected_value):
        self.assertEqual(self._actual_value, expected_value)

    def to_not_be(self, expected_value):
        self.assertNotEqual(self._actual_value, expected_value)

    def to_be_of_type(self, expected_type):
        self.assertIsInstance(self._actual_value, expected_type)

    def to_equal_list(self, expected_list):
        self.assertListEqual(self._actual_value, expected_list)

    def to_contain(self, expected_element):
        self.assertTrue(expected_element in self._actual_value)

    def to_contain_all(self, expected_elements):
        is_contained = True
        for element in expected_elements:
            if element not in self._actual_value:
                is_contained = False
                break
        self.assertTrue(is_contained)

    def to_be_true(self):
        self.assertTrue(self._actual_value)

    def to_be_false(self):
        self.assertFalse(self._actual_value)

    def to_be_none(self):
        self.assertIsNone(self._actual_value)

    def to_not_be_none(self):
        self.assertIsNotNone(self._actual_value)

    def to_be_a_list(self):
        self.to_be_of_type(list)

    def to_be_a_dict(self):
        self.to_be_of_type(dict)

    def to_be_a_set(self):
        self.to_be_of_type(set)

    def to_raise(self, expected_exception, *args, **kwargs):
        with self.assertRaises(expected_exception=expected_exception):
            self._actual_value(*args, **kwargs)

    def to_be_of_length(self, expected_length: int):
        """
        Asserts whether the previously provided value's length matches expected_length. The length is determined by
        using the BIF len().
        
        :param expected_length: the expected value of len(actual_value)
        """
        self.assertEqual(len(self._actual_value), expected_length)
