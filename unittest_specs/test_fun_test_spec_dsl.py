import unittest

from inspect import getmodule, currentframe
from typing import Callable

from unittest_specs.fun_test_spec import describe, it, expect


class FunTestDSL(unittest.TestCase):
    def test_it_should_return_correct_name(self):
        actual_name, _ = it("a test name", lambda: 1)
        self.assertEqual(actual_name, "test_a_test_name")

    def test_it_should_return_passed_function(self):
        _, actual_def = it("", lambda: 1)
        self.assertEqual(actual_def(), 1)

    def test_describe_should_register_class(self):
        describe("Test Class")
        module = getmodule(currentframe())
        self.assertEqual(module.__dict__["TestClass"].__name__, "TestClass")

    def test_exception_interception(self):
        def exception_raiser(_):
            raise Exception()

        _, wrapped_interception_def = it("", exception_raiser, intercept=Exception)
        wrapped_interception_def(self)


class FunAsserterSpec(unittest.TestCase):
    def setUp(self) -> None:
        self.five_asserter = expect(5)
        self.list_asserter = expect([1, 2, 3])
        self.dict_asserter = expect({1: 3, 2: 2, 3: 1})
        self.set_asserter = expect({1, 2, 3})
        self.none_asserter = expect(None)
        self.true_asserter = expect(True)
        self.false_asserter = expect(False)

    def test_should_create_asserter(self):
        self.assertIsInstance(expect(''), unittest.TestCase)

    def test_asserter_should_return_callable(self):
        self.assertIsInstance(expect('').to_be(''), Callable)

    def test_asserter_should_detect_equality_correctly(self):
        self.five_asserter.to_be(5)(self)

    def test_asserter_should_detect_inequality_correctly(self):
        self.five_asserter.to_not_be(2)(self)

    def test_asserter_should_detect_type_correctly(self):
        self.five_asserter.to_be_of_type(int)(self)

    def test_asserter_should_detect_list_equality_correctly(self):
        self.list_asserter.to_equal_list([1, 2, 3])(self)

    def test_asserter_should_detect_list_contains_correctly(self):
        self.list_asserter.to_contain(2)(self)

    def test_asserter_should_detect_list_contains_all_correctly(self):
        self.list_asserter.to_contain_all([3, 1, 2])(self)

    def test_asserter_should_detect_true_correctly(self):
        self.true_asserter.to_be_true()(self)

    def test_asserter_should_detect_false_correctly(self):
        self.false_asserter.to_be_false()(self)

    def test_asserter_should_detect_none_correctly(self):
        self.none_asserter.to_be_none()(self)

    def test_asserter_should_detect_not_none_correctly(self):
        self.five_asserter.to_not_be_none()(self)

    def test_asserter_should_detect_list_type_correctly(self):
        self.list_asserter.to_be_a_list()(self)

    def test_asserter_should_detect_dict_type_correctly(self):
        self.dict_asserter.to_be_a_dict()(self)

    def test_asserter_should_detect_set_type_correctly(self):
        self.set_asserter.to_be_a_set()(self)

    def test_asserter_should_detect_list_length_correctly(self):
        self.list_asserter.to_be_of_length(3)(self)


describe("Python numbers",

         it("5 should be of type int",
            expect(5).to_be_of_type(int)
            )

         )
