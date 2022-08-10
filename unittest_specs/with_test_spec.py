import unittest
from inspect import getmodule, stack


setup = 0
run = 1
assertion = 2
teardown = 3


def scenario(scenario_name: str):
    """
    Creates a ScenarioBuilder to construct a test case. ScenarioBuilder objects are technically context managers and
    should therefore be used in with constructs:

    ``with scenario("name") as test_scenario:``

    A test scenario can have up to four different parts:

    * ``setup`` *(optional)* - one or more steps to set up the actual test action
    * ``run`` - the action to be taken for the test case execution
    * ``assertion`` *(optional)* - a single assertion for the test case
    * ``teardown`` *(optional)* - one or more steps to clean up after the test case

    All parts take

    :param scenario_name: description of the test case, should be unique since it is converted to a function name
    :return: a ScenarioBuilder object, which can be used to construct test cases
    """
    class ScenarioBuilder:
        class ActionAdder:
            def __init__(self, scenario_builder, action):
                self.scenario_builder = scenario_builder
                self.action = action

            def __lshift__(self, other):
                if self.action == setup:
                    self.scenario_builder.add_setup_action(other)
                if self.action == run:
                    self.scenario_builder.set_run_action(other)
                if self.action == assertion:
                    self.scenario_builder.add_assertion(other)
                if self.action == teardown:
                    self.scenario_builder.add_teardown_action(other)

        def __init__(self, scenario_name_for_builder: str):
            self.scenario_name = scenario_name_for_builder.lower().replace(" ", "_")

            if not self.scenario_name.startswith("test_"):
                self.scenario_name = f"test_{self.scenario_name}"

            self.setup = []
            self.run = None
            self.assertion = None
            self.teardown = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            def scenario_execution(_=None):
                list(map(lambda action: action(), self.setup))

                if self.run:
                    self.run()
                else:
                    raise Exception("No run action defined!")

                if self.assertion:
                    self.assertion(_)

                list(map(lambda action: action(), self.teardown))

            class_members = {
                self.scenario_name: scenario_execution
            }

            for key, value in zip(class_members, class_members.values()):
                value.__name__ = key

            module = getmodule(stack()[1][0])

            if "TestSuite" in module.__dict__:
                existing_members = module.__dict__["TestSuite"].__dict__
                for key, value in zip(existing_members, existing_members.values()):
                    class_members[key] = value

            test_class = type("TestSuite", (unittest.TestCase,), class_members)
            module.__dict__["TestSuite"] = test_class

        def __matmul__(self, other):
            return self.ActionAdder(self, other)

        def add_setup_action(self, action):
            self.setup.append(action)

        def set_run_action(self, action):
            if self.run:
                raise Exception("Multiple run actions defined! Only one can be defined per scenario")
            self.run = action

        def add_assertion(self, action):
            if self.assertion:
                raise Exception("Multiple assertions actions defined! Only one can be defined per scenario")
            self.assertion = action

        def add_teardown_action(self, action):
            self.teardown.append(action)

    return ScenarioBuilder(scenario_name)
