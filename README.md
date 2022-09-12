# unittest_specs

## Table of content
* [FunSpec](#FunSpec)
* [SimpleFlatSpec](#SimpleFlatSpec)
* [WithSpec](#WithSpec)

## FunSpec

This style can be used to write highly readable test cases helpful for good documentation in code. 

Due to its [limitations](#limitations), this style is mostly suited for compact unit tests, since no elaborate
test structure can be written.

### Usage

`FunSpec` provides the three functions `describe()`, `it()` and `expect()` to construct [RSpec](http://rspec.info/) inspired test cases,
which might feel more familiar to e.g. TypeScript developers. Specifications written this way are picked up by
`unittest`'s auto-discovery (`python3 -m unittest <directory>`), since they are converted into `unittest.TestCase`
sub-classes and are therefore valid `unittest` tests.

Setting up test cases is pretty straight forward:

```python
from unittest_specs import describe, it, expect

describe("Python numbers",
         
         it("5 should be of type int",
            expect(5).to_be_of_type(int)
            )
         
         )
```

Above example dynamically creates a type equivalent to:

```python
import unittest


class PythonNumbers(unittest.TestCase):
    def test_5_should_be_of_type_int(self):
        self.assertIsInstance(5, int)
```

The constructed type is hooked into the executing module (the one calling `describe()`), so that unittest
picks it up while performing its auto-discovery.

For every `describe()` block an arbitrary amount of `it()` statements can be defined, with each resulting in a
separate test function. Keep in mind that each `it()` should have a description unique to its `describe()` block
(see [Limitations](#limitations) for further detail). This might look something like this:

```python
from unittest_specs import describe, it, expect

describe("Python arithmatic",
         
         it("should multiply correctly",
            expect(2 * 5).to_be(10)
            ),
         
         it("should square correctly",
            expect(4 ** 2).to_be(16)
            ),
         
         it("should subtract correctly",
            expect(1340 - 3).to_be(1337)
            ),
         
         )
```

Which, again, translates to an equivalent of:

```python
import unittest


class PythonArithmatic(unittest.TestCase):
    def test_should_multiply_correctly(self):
        self.assertEqual(2 * 5, 10)
        
    def test_should_square_correctly(self):
        self.assertEqual(4 ** 2, 16)
        
    def test_should_subtract_correctly(self):
        self.assertEqual(1340 - 3, 1337)
```

### Limitations

**Descriptions and Identifiers**

The descriptions provided in `describe()` and `it()` are used to dynamically generate test classes based on
`unittest.TestCase`, with the description specified in `describe()` being converted into the class name and all
following `it()` descriptions being used for test function names. Since both are identifiers, which Python requires
to be unique in their appropriate context, some unexpected behaviour might occur when violating this requirement.

**it() and Blocks**

As of now, there is no way to specify anonymous blocks in Python syntax. This means that, unfortunately, in the
current implementation, every test case specified in `it()` needs to only consist of one single evaluation.
Therefore, the recommended usage is to utilize `expect()` and its assertions to formulate the test.

## SimpleFlatSpec

The simple flat spec style is visually very close to plain `unittest.TestCase` code and can, in fact be used
as a drop-in replacement. Its main advantage is a set of more readable assertions, as well as some utility
decorators.

### Usage

The `SimpleFlatSpec` class provides an easy and readable way to write tests. Much like in 
`unittest` itself, each test case should be specified in a separate test function with a name
outlining the expected behaviour. In the function body, any required setup can be performed, before
calling `self.expect()` to provide the computed actual value. This declaration should be followed by
an assertion, of which there is a range to choose from (see the following section for a complete list).

A very simple test case could look something like this:

```python
from unittest_specs import SimpleFlatSpec


class MyTest(SimpleFlatSpec):
    def test_should_identify_even_number(self):
        is_even_number = 4 % 2 == 0
        
        self.expect(is_even_number).to_be_true()
```

### Available Assertions

| Assertion Function  | Description                                                          | Equivalent unittest function                         |
|---------------------|----------------------------------------------------------------------|------------------------------------------------------|
| `to_be()`           | checks for equality between actual and expected value                | `assertEqual()`                                      |
| `to_not_be()`       | checks for inequality between actual and expected value              | `assertNotEqual()`                                   |
| `to_be_of_type()`   | checks whether the actual value is of a specified type               | `assertIsInstance()`                                 |
| `to_equal_list()`   | checks an actual and expected list for equality                      | `assertListEqual()`                                  |
| `to_contain()`      | checks whether the actual collection contains an expected value      | `assertTrue(expected_element in self._actual_value)` |
| `to_contain_all()`  | checks whether the actual collection contains all expected values    | custom implementation                                |
| `to_be_true()`      | checks whether the actual value is of value `True`                   | `assertTrue()`                                       |
| `to_be_false()`     | checks whether the actual value is of value `False`                  | `assertFalse()`                                      |
| `to_be_none()`      | checks whether the actual value is `None`                            | `assertIsNone()`                                     |
| `to_not_be_none()`  | checks whether the actual value is not `None`                        | `assertIsNotNone()`                                  |
| `to_be_a_list()`    | checks whether the actual value is of type `list`                    | `assertIsInstance(actual_value, list)`               |
| `to_be_a_dict()`    | checks whether the actual value is of type `dict`                    | `assertIsInstance(actual_value, dict)`               |
| `to_be_a_set()`     | checks whether the actual value is of type `set`                     | `assertIsInstance(actual_value, set)`                |
| `to_raise()`        | intercepts an `Exception` expected to be raised in the test function | `assertRaises()`                                     |
| `to_be_of_length()` | checks for an expected length of an object supporting len()          | `assertEqual(len(actual_value), expected_value)`     |

### Parameterizing Tests

Instead of writing several test function covering the same functionality with different parameters, one can use
parameterization to provide an arbitrarily long list of test data sets. This is implemented using the `unittest.TestCase.subTest`
function, with the first element in each being used as the label.

A parameterized test might look like the following:

```python
from unittest_specs import SimpleFlatSpec


class MyTest(SimpleFlatSpec):
    
    @SimpleFlatSpec.parameterize(params=[
        ('hello',  5),
        ('world!', 6),
    ])
    def test_should_check_string_length(self, given_string, expected_length):
        self.expect(given_string).to_be_of_length(expected_length)
```

## WithSpec

The `WithSpec` provides a structure to set up multi-step test scenarios optionally including setup and/or teardown.

### Usage

Similar to [FunSpec](#FunSpec) `WithSpec` also utilizes a strongly modified DSL to construct test cases. They, too,
are dynamically converted into valid `unittest` test cases and executed by the  auto-discovery
(`python3 -m unittest <directory>`). A `WithSpec` test scenario does not require any class to be set up.

There are four building blocks that help you construct `WithSpec` test scenarios:

#### setup

With the optional `setup` step(s) one or more actions can be defined in order to set up the
actual test run. For instance, if your test case is to delete a table row, you might want to create it
first.

#### run

This is the only mandatory step for a test scenario. Sets up the actual action to be tested.

#### assertion

Optionally run an assertion statement after the `run` step. This step is compatible with
`unittest.expect`, but instead of passing a value, a value providing lambda needs to be passed
instead, since Python always evaluates function arguments eagerly.

`WithSpec` enforces the philosophy of only having a single assertion statement per test case. Therefore
trying to define multiple `assertion` steps in the same scenario will result in an exception.

#### teardown

In case your test case produces any side effects, you might want to clean them up afterwards. This 
can be done by defining one or more `teardown` steps. Since not every test needs a cleanup, this step
is optional.

A complete scenario might look something like this:

```python
from unittest_specs import scenario, setup, run, teardown, assertion, expect

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


with scenario("adding 1 and 4 together results in 5") as test_scenario:

    adder = Adder()

    test_scenario @ setup << (lambda: adder.reset_result())
    
    test_scenario @ run << (lambda: adder.perform_addition(1, 4))
    
    test_scenario @ assertion << expect(lambda: adder.result).to_be(5)
    
    test_scenario @ teardown << (lambda: adder.reset_result())
```
