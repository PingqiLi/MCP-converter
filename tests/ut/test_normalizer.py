import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.normalizer import Normalizer
from dataclasses import dataclass

@dataclass
class Weather:
    city: str
    temp: float

class CustomType:
    def __init__(self, value):
        self.value = value

class TestNormalizer(unittest.TestCase):
    def test_dict_normalization(self):
        normalizer = Normalizer()
        data = {"key": "value"}
        result = normalizer.normalize(data)
        self.assertEqual(result, data)

    def test_object_normalization(self):
        class TestObj:
            def __init__(self):
                self.attr = "value"
        
        normalizer = Normalizer()
        obj = TestObj()
        result = normalizer.normalize(obj)
        self.assertEqual(result, {"attr": "value"})

    def test_json_string_normalization(self):
        normalizer = Normalizer()
        json_str = '{"key": "value"}'
        result = normalizer.normalize(json_str)
        self.assertEqual(result, {"key": "value"})

    def test_to_dict_from_dataclass(self):
        w = Weather(city="London", temp=20.5)
        result = Normalizer.to_dict(w)
        self.assertEqual(result, {"city": "London", "temp": 20.5})

    def test_to_dict_from_dict(self):
        d = {"foo": "bar"}
        result = Normalizer.to_dict(d)
        self.assertEqual(result, d)

    def test_to_dict_from_json_str(self):
        s = '{"foo": "bar"}'
        result = Normalizer.to_dict(s)
        self.assertEqual(result, {"foo": "bar"})

    def test_to_dict_from_list(self):
        l = [Weather(city="London", temp=20.5), Weather(city="Paris", temp=22.0)]
        result = Normalizer.to_dict(l)
        self.assertEqual(result, [
            {"city": "London", "temp": 20.5},
            {"city": "Paris", "temp": 22.0}
        ])

    def test_to_dict_from_object(self):
        class Dummy:
            def __init__(self):
                self.x = 1
        d = Dummy()
        result = Normalizer.to_dict(d)
        self.assertEqual(result, {"x": 1})

    def test_to_json(self):
        w = Weather(city="London", temp=20.5)
        json_str = Normalizer.to_json(w)
        self.assertIn('"city": "London"', json_str)
        self.assertIn('"temp": 20.5', json_str)

    def test_to_json_nonserializable(self):
        class Dummy:
            def __str__(self):
                return "dummy"
        d = Dummy()
        json_str = Normalizer.to_json(d)
        self.assertIn('"dummy"', json_str)

    def test_plugin_extensibility(self):
        def custom_normalizer(obj):
            return {"custom": obj.value}
        Normalizer.register("CustomType", custom_normalizer)
        c = CustomType("foo")
        result = Normalizer.to_dict(c)
        self.assertEqual(result, {"custom": "foo"})

if __name__ == "__main__":
    unittest.main() 