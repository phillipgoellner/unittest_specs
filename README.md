# unittest_specs

## SimpleFlatSpec

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

## Parameterizing Tests

Instead of writing several test function covering the same functionality with different parameters, one can use
parameterization to provide an arbitrarily long list of test data sets. This is implemented using the `unittest.TestCase.subTest`
function, with the first element in each being used as the label.

A parameterized test might look like the following:

```python
from unittest_specs import SimpleFlatSpec, parameterized


class MyTest(SimpleFlatSpec):
    
    @parameterized(params=[
        ('hello',  5),
        ('world!', 6),
    ])
    def test_should_check_string_length(self, given_string, expected_length):
        self.expect(given_string).to_be_of_length(expected_length)
```
