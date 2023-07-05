import unittest
from unittest.mock import MagicMock


# The class we want to test
class Calculator:
    def add(self, x, y):
        return x + y


# The unit test class
class TestCalculator(unittest.TestCase):
    def test_add(self):
        # Create an instance of the Calculator class
        calculator = Calculator()

        # Create a mock object for the add method
        calculator.add = MagicMock(return_value=10)

        # Call the add method with some values
        result = calculator.add(2, 3)

        # Verify that the add method was called with the correct arguments
        calculator.add.assert_called_once_with(2, 3)

        # Verify that the result is as expected
        self.assertEqual(result, 10)


if __name__ == "__main__":
    unittest.main()
