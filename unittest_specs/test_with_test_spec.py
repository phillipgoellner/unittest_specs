import unittest

from inspect import getmodule, currentframe

from unittest_specs import expect
from unittest_specs.with_test_spec import scenario, setup, run, teardown, assertion


class TestWithScenarioDSL(unittest.TestCase):
    def setUp(self) -> None:
        def increment():
            self.test_value += 1

        self.test_value = 0
        self.increment = increment

    def tearDown(self) -> None:
        module = getmodule(currentframe())
        if "TestSuite" in module.__dict__:
            if "test_scenario" in module.__dict__["TestSuite"].__dict__:
                module.__dict__["TestSuite"] = type("TestSuite", (unittest.TestCase,), {})

    def test_with_statement_registers_class_in_module(self):
        with scenario("test scenario"):
            pass

        module = getmodule(currentframe())
        self.assertEqual(module.__dict__["TestSuite"].__name__, "TestSuite")

    def test_with_statement_registers_scenario_function_in_class(self):
        with scenario("test scenario"):
            pass

        module = getmodule(currentframe())
        self.assertEqual(module.__dict__["TestSuite"].__dict__["test_scenario"].__name__, "test_scenario")

    def test_with_statement_registers_two_scenario_function_in_class(self):
        with scenario("first test scenario"):
            pass

        with scenario("second test scenario"):
            pass

        module = getmodule(currentframe())
        self.assertEqual(module.__dict__["TestSuite"].__dict__["test_first_test_scenario"].__name__, "test_first_test_scenario")
        self.assertEqual(module.__dict__["TestSuite"].__dict__["test_second_test_scenario"].__name__, "test_second_test_scenario")

    def test_execution_throws_exception_when_no_run_action_is_defined(self):
        with scenario("test scenario"):
            pass

        module = getmodule(currentframe())
        test_run = module.__dict__["TestSuite"].__dict__["test_scenario"]

        self.assertRaises(Exception, test_run)

    def test_setup_adds_setup_action_to_test_execution(self):
        with scenario("test scenario") as test_scenario:
            test_scenario @ setup << self.increment
            test_scenario @ run << (lambda: print(""))

        module = getmodule(currentframe())
        module.__dict__["TestSuite"].__dict__["test_scenario"]()
        self.assertEqual(1, self.test_value)

    def test_setup_adds_two_setup_actions_to_test_execution(self):
        with scenario("test scenario") as test_scenario:
            test_scenario @ setup << self.increment
            test_scenario @ setup << self.increment
            test_scenario @ run << (lambda: print(""))

        module = getmodule(currentframe())
        module.__dict__["TestSuite"].__dict__["test_scenario"]()
        self.assertEqual(2, self.test_value)

    def test_run_sets_test_execution_action(self):
        with scenario("test scenario") as test_scenario:
            test_scenario @ run << self.increment

        module = getmodule(currentframe())
        module.__dict__["TestSuite"].__dict__["test_scenario"]()
        self.assertEqual(1, self.test_value)

    def test_setting_a_second_run_action_throws_an_exception(self):
        def create_scenario():
            with scenario("test scenario") as test_scenario:
                test_scenario @ run << self.increment
                test_scenario @ run << self.increment

        self.assertRaises(Exception, create_scenario)

    def test_teardown_adds_teardown_action_to_test_execution(self):
        with scenario("test scenario") as test_scenario:
            test_scenario @ run << (lambda: print(""))
            test_scenario @ teardown << self.increment

        module = getmodule(currentframe())
        module.__dict__["TestSuite"].__dict__["test_scenario"]()
        self.assertEqual(1, self.test_value)

    def test_teardown_adds_two_teardown_actions_to_test_execution(self):
        with scenario("test scenario") as test_scenario:
            test_scenario @ run << (lambda: print(""))
            test_scenario @ teardown << self.increment
            test_scenario @ teardown << self.increment

        module = getmodule(currentframe())
        module.__dict__["TestSuite"].__dict__["test_scenario"]()
        self.assertEqual(2, self.test_value)


with scenario("free standing scenario") as standalone_test_scenario:

    class Adder:
        def __init__(self):
            self.__result = 0

        def perform_addition(self, a, b):
            self.__result = a + b

        def reset_result(self):
            self.__result = 0

        @property
        def result(self):
            return self.__result

    adder = Adder()

    standalone_test_scenario @ setup << (lambda: adder.reset_result())
    standalone_test_scenario @ run << (lambda: adder.perform_addition(1, 4))
    standalone_test_scenario @ assertion << expect(lambda: adder.result).to_be(5)
    standalone_test_scenario @ teardown << (lambda: adder.reset_result())
