import unittest

from unittest_specs.simple_test_spec import SimpleFlatSpec

parameterize = SimpleFlatSpec.parameterize
intercept = SimpleFlatSpec.intercept


def get_empty_test_case():
    def __(i):
        pass

    return type('', (unittest.TestCase,), {'subTest': __})


class SimpleTestDSL(unittest.TestCase):

    def test_param_decorator_should_execute_without_error(self):
        @parameterize(params=[])
        def empty_function(_):
            return 1

        empty_function(get_empty_test_case())

    @parameterize(params=[
        (1, 1),
        (2, 2),
    ])
    def test_should_decorate_class_member(self, left_param, right_param):
        self.assertEqual(left_param, right_param)

    def test_should_handle_exceptions_with_args_correctly(self):
        def exception_raiser(some_arg, another_arg=0):
            if some_arg == 1 and another_arg == 32:
                raise Exception()

        SimpleFlatSpec().expect(exception_raiser).to_raise(Exception, 1, another_arg=32)

    @parameterize(params=[
        ([1, 2, 3], 3),
        ('abcde', 'd'),
        ({0: 1}, 0),
        ((0, 1, 2, 3), 0),
    ])
    def test_should_detect_contained_correctly(self, given_input, expected_element):
        SimpleFlatSpec().expect(given_input).to_contain(expected_element)

    @parameterize(params=[
        ([1, 2, 3], [1, 3]),
        ({0: 1}, [0]),
        ((0, 1, 2, 3), [1, 3, 0]),
    ])
    def test_should_detect_contained_correctly(self, given_input, expected_elements):
        SimpleFlatSpec().expect(given_input).to_contain_all(expected_elements)


class SimpleAsserterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_case = SimpleFlatSpec()

    def test_asserter_should_store_value_correctly(self):
        actual = self.test_case.expect(1)._actual_value
        self.assertEqual(1, actual)

    def test_asserter_should_detect_equality_correctly(self):
        self.test_case.expect('test').to_be('test')

    def test_asserter_should_detect_difference_correctly(self):
        self.test_case.expect('test').to_not_be('Test')

    def test_asserter_should_detect_type_correctly(self):
        self.test_case.expect('test').to_be_of_type(str)

    def test_asserter_should_test_list_equality_correctly(self):
        self.test_case.expect([1, 2, 3]).to_equal_list([1, 2, 3])

    def test_asserter_should_test_contains_correctly(self):
        self.test_case.expect([1, 2, 3]).to_contain(1)

    def test_asserter_should_test_contains_all_correctly(self):
        self.test_case.expect([1, 2, 3]).to_contain_all((2, 3, 1,))

    def test_asserter_should_test_true_correctly(self):
        self.test_case.expect(True).to_be_true()

    def test_asserter_should_test_false_correctly(self):
        self.test_case.expect(False).to_be_false()

    def test_asserter_should_test_none_correctly(self):
        self.test_case.expect(None).to_be_none()

    def test_asserter_should_test_not_none_correctly(self):
        self.test_case.expect('some').to_not_be_none()

    def test_asserter_should_recognize_set_correctly(self):
        self.test_case.expect({1, 2}).to_be_a_set()

    def test_asserter_should_recognize_list_correctly(self):
        self.test_case.expect([]).to_be_a_list()

    def test_asserter_should_recognize_dict_correctly(self):
        self.test_case.expect({}).to_be_a_dict()

    def test_asserter_should_check_length_correctly(self):
        self.test_case.expect({}).to_be_of_length(0)

    def test_should_handle_exceptions_correctly(self):
        def exception_raiser():
            raise Exception()

        self.test_case.expect(exception_raiser).to_raise(Exception)

    @intercept(Exception)
    def test_should_intercept_exceptions(self):
        def exception_raiser():
            raise Exception()

        exception_raiser()
