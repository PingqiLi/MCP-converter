import unittest
from src.mcp_tool import MCPTool

class DummyTool(MCPTool):
    name = "DummyTool"
    description = "A dummy MCP tool."
    parameters_schema = {"param": {"type": "string"}}
    def run(self, *args, **kwargs):
        return "ran"
    def validate(self, params):
        return "param" in params

class TestMCPTool(unittest.TestCase):
    def test_abstract_methods(self):
        with self.assertRaises(TypeError):
            MCPTool()
    def test_subclass(self):
        tool = DummyTool()
        self.assertEqual(tool.run(), "ran")
        self.assertTrue(tool.validate({"param": "x"}))
        self.assertFalse(tool.validate({}))
        self.assertEqual(tool.name, "DummyTool")
        self.assertEqual(tool.description, "A dummy MCP tool.")
        self.assertEqual(tool.parameters_schema, {"param": {"type": "string"}})

if __name__ == "__main__":
    unittest.main() 