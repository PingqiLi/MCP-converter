import unittest
import os
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from generators.output_generator import OutputGenerator

class TestOutputGenerator(unittest.TestCase):
    def setUp(self):
        self.data = {"location": "London", "temp": 20.5, "description": "Cloudy"}
        self.schema = {"required": ["location", "temp", "description"]}
        self.path = "tests/tmp/test_output.json"
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_write_json_valid(self):
        OutputGenerator.write_json(self.data, self.path, self.schema)
        self.assertTrue(os.path.exists(self.path))
        with open(self.path) as f:
            loaded = json.load(f)
        self.assertEqual(loaded, self.data)

    def test_write_json_missing_required(self):
        bad_data = {"location": "London", "temp": 20.5}
        with self.assertRaises(ValueError) as ctx:
            OutputGenerator.write_json(bad_data, self.path, self.schema)
        self.assertIn("Missing required fields", str(ctx.exception))

    def test_write_json_no_schema(self):
        OutputGenerator.write_json(self.data, self.path)
        self.assertTrue(os.path.exists(self.path))
        with open(self.path) as f:
            loaded = json.load(f)
        self.assertEqual(loaded, self.data)

if __name__ == "__main__":
    unittest.main() 