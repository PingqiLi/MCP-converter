import unittest
import os
from src.field_mapper import FieldMapper

class TestFieldMapper(unittest.TestCase):
    def setUp(self):
        self.data = {
            "city": "London",
            "temperature": 20.5,
            "desc": "Cloudy"
        }
        self.mcp_fields = ["location", "temp", "description"]
        self.mapping = {
            "location": "city",
            "temp": "temperature",
            "description": "desc"
        }

    def test_configurable_mapping(self):
        mapper = FieldMapper(self.mapping)
        result = mapper.map_fields(self.data, infer=False, mcp_fields=self.mcp_fields)
        self.assertEqual(result, {
            "location": "London",
            "temp": 20.5,
            "description": "Cloudy"
        })

    def test_inferable_mapping(self):
        # No config, should infer by name similarity
        mapper = FieldMapper()
        result = mapper.map_fields(self.data, infer=True, mcp_fields=["city", "temperature", "desc"])
        self.assertEqual(result, self.data)

    def test_partial_infer(self):
        # Only some fields match
        mapper = FieldMapper()
        result = mapper.map_fields(self.data, infer=True, mcp_fields=["city", "humidity"])
        self.assertEqual(result, {"city": "London", "humidity": None})

    def test_save_and_load_mapping(self):
        mapper = FieldMapper(self.mapping)
        path = "test_mapping.json"
        mapper.save_mapping(path)
        loaded = FieldMapper.load_mapping(path)
        self.assertEqual(loaded.mapping, self.mapping)
        os.remove(path)

if __name__ == "__main__":
    unittest.main() 