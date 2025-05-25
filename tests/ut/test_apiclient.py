import unittest
from src.apiclient import APIClient

class DummyClient(APIClient):
    name = "Dummy"
    description = "A dummy API client."
    def execute(self, *args, **kwargs):
        return "executed"
    def get_schema(self):
        return {"info": "dummy schema"}

class TestAPIClient(unittest.TestCase):
    def test_abstract_methods(self):
        with self.assertRaises(TypeError):
            APIClient()
    def test_subclass(self):
        client = DummyClient()
        self.assertEqual(client.execute(), "executed")
        self.assertEqual(client.get_schema(), {"info": "dummy schema"})
        self.assertEqual(client.name, "Dummy")
        self.assertEqual(client.description, "A dummy API client.")

if __name__ == "__main__":
    unittest.main() 