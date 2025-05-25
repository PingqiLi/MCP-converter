import unittest
from src.input_parser import InputParser

class TestInputParser(unittest.TestCase):
    def setUp(self):
        self.parser = InputParser()

    def test_parse_json(self):
        data = '{"foo": "bar"}'
        result = self.parser.parse_json(data)
        self.assertEqual(result, {"foo": "bar"})

    def test_parse_yaml(self):
        yaml_data = 'foo: bar'
        result = self.parser.parse_yaml(yaml_data)
        self.assertEqual(result, {"foo": "bar"})

    def test_parse_python_usage(self):
        code = 'result = get_weather(city="London")'
        result = self.parser.parse_python_usage(code)
        self.assertTrue("functions" in result)
        self.assertTrue(any(f["function"] == "get_weather" for f in result["functions"]))

    def test_extract_endpoints(self):
        api_dict = {"paths": {"/weather": {"get": {}}}}
        endpoints = self.parser.extract_endpoints(api_dict)
        self.assertEqual(endpoints, {"/weather": {"get": {}}})

    def test_extract_schemas(self):
        api_dict = {"components": {"schemas": {"Weather": {"type": "object"}}}}
        schemas = self.parser.extract_schemas(api_dict)
        self.assertEqual(schemas, {"Weather": {"type": "object"}})

if __name__ == "__main__":
    unittest.main() 