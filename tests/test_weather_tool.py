import unittest
from generated_tools.weather_tool import WeatherTool

class TestWeatherTool(unittest.TestCase):
    def setUp(self):
        self.tool = WeatherTool()

    def test_attributes(self):
        self.assertEqual(self.tool.name, "WeatherTool")
        self.assertIn("city", self.tool.parameters_schema)

    def test_validate(self):
        self.assertTrue(self.tool.validate({"city": "London"}))
        self.assertFalse(self.tool.validate({}))
        self.assertFalse(self.tool.validate({"city": ""}))
        self.assertFalse(self.tool.validate({"city": 123}))

    def test_run_valid(self):
        result = self.tool.run({"city": "London"})
        self.assertEqual(result["location"], "London")
        self.assertIn("temp", result)
        self.assertIn("description", result)

    def test_run_invalid(self):
        with self.assertRaises(ValueError):
            self.tool.run({})

if __name__ == "__main__":
    unittest.main() 