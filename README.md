# unittest_specs

This package provides different styles, with which you can construct test specifications. Since it uses
Python's `unittest` package for the actual test execution, `unittest_specs` can be regarded as merely a nicer
front to a native package.

## Table of content
* [SimpleFlatSpec](#SimpleFlatSpec)
* [FunSpec](#FunSpec)

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

### Intercepting Exceptions

When a function is supposed to raise an exception under a certain circumstance, this can also be tested by specifying
the intercept option of an `it()` block.

```python
from unittest_specs import describe, it


def dangerous_function():
    raise Exception()


describe("Python arithmatic",
         
         it("should intercept an exception", dangerous_function, intercept=Exception)
         
         )
```

This requires a function reference to be passed to `it()`, since an interception requires to be set up before
the actual execution. If the function you want to test requires parameters to reach an error state, this can easily
set up by passing a parameter-less lambda:

```python
from unittest_specs import describe, it


def divide(divisor, dividend):
    return divisor / dividend


describe("Python arithmatic",
         
         it("dividing by zero should throw an error", lambda: divide(42, 0), intercept=ZeroDivisionError)
         
         )
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
| `to_be_of_length()` | checks for an expected length of an object supporting len()          | `assertEqual(len(actual_value), expected_value)`     |


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

