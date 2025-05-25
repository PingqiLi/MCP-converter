import unittest
from src.validator import MCPFieldValidator

class TestMCPFieldValidator(unittest.TestCase):
    def setUp(self):
        self.required = ["location", "temp", "description"]

    def test_valid(self):
        mapped = {"location": "London", "temp": 20.5, "description": "Cloudy"}
        is_valid, errors = MCPFieldValidator.validate(mapped, self.required)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_missing_field(self):
        mapped = {"location": "London", "temp": 20.5}
        is_valid, errors = MCPFieldValidator.validate(mapped, self.required)
        self.assertFalse(is_valid)
        self.assertIn("Missing or null required field: 'description'", errors)

    def test_null_field(self):
        mapped = {"location": "London", "temp": None, "description": "Cloudy"}
        is_valid, errors = MCPFieldValidator.validate(mapped, self.required)
        self.assertFalse(is_valid)
        self.assertIn("Missing or null required field: 'temp'", errors)

if __name__ == "__main__":
    unittest.main() 