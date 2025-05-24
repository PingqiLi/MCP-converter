import unittest
from generated_tools.weathertool_wrapper import run_weathertool

class TestWeatherToolWrapper(unittest.TestCase):
    def test_run_valid(self):
        result = run_weathertool(city="London")
        self.assertEqual(result["location"], "London")
        self.assertIn("temp", result)
        self.assertIn("description", result)

    def test_run_invalid(self):
        with self.assertRaises(ValueError):
            run_weathertool()
        with self.assertRaises(ValueError):
            run_weathertool(city="")

if __name__ == "__main__":
    unittest.main() 