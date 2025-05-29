import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))

from server.mcp_server import is_mcp_tool_compatible

class DummyTool:
    """A dummy tool for testing MCP compatibility without inheritance"""
    name = "DummyTool"
    description = "A dummy MCP tool."
    parameters_schema = {"param": {"type": "string"}}
    
    def run(self, params):
        return "ran"
    
    def validate(self, params):
        return "param" in params

class IncompleteTool:
    """A tool missing required methods/attributes"""
    name = "IncompleteTool"
    # Missing description, parameters_schema, and methods

class TestMCPToolCompatibility(unittest.TestCase):
    def test_compatible_tool(self):
        """Test that a properly structured tool is compatible"""
        tool = DummyTool()
        self.assertTrue(is_mcp_tool_compatible(tool))
    
    def test_incompatible_tool(self):
        """Test that an incomplete tool is not compatible"""
        tool = IncompleteTool()
        self.assertFalse(is_mcp_tool_compatible(tool))
    
    def test_tool_functionality(self):
        """Test that a compatible tool works correctly"""
        tool = DummyTool()
        self.assertEqual(tool.run({}), "ran")
        self.assertTrue(tool.validate({"param": "x"}))
        self.assertFalse(tool.validate({}))
        self.assertEqual(tool.name, "DummyTool")
        self.assertEqual(tool.description, "A dummy MCP tool.")
        self.assertEqual(tool.parameters_schema, {"param": {"type": "string"}})

if __name__ == '__main__':
    unittest.main() 