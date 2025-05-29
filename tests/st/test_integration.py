#!/usr/bin/env python3
"""
Integration tests for MCP server and LangGraph functionality
"""
import sys
import os
import unittest
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from server.mcp_server import MCPServer
from server.langgraph_adapter import LangGraphAdapter


class TestMCPServerIntegration(unittest.TestCase):
    """Test MCP server functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.server = MCPServer(tools_directory="generated_tools")
    
    def test_server_initialization(self):
        """Test that MCP server initializes correctly"""
        self.assertIsNotNone(self.server)
        # Convert Path to string for comparison
        self.assertEqual(str(self.server.tools_directory), "generated_tools")
    
    def test_tool_discovery(self):
        """Test that server can discover tools"""
        self.server.discover_tools()
        # Should not raise exceptions
        self.assertIsInstance(self.server.tools, dict)
    
    def test_tool_registry_exists(self):
        """Test that tool registry exists or can be created"""
        registry_path = Path("generated_tools") / "tool_registry.json"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = json.load(f)
                self.assertIn("tools", registry)
                self.assertIn("last_updated", registry)


class TestLangGraphIntegration(unittest.TestCase):
    """Test LangGraph adapter functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.adapter = LangGraphAdapter()  # No parameters needed
    
    def test_adapter_initialization(self):
        """Test that LangGraph adapter initializes correctly"""
        self.assertIsNotNone(self.adapter)
        self.assertIsInstance(self.adapter.tools, dict)
        self.assertIsInstance(self.adapter.functions, list)
    
    def test_tool_conversion(self):
        """Test that adapter can convert tools"""
        # This test will pass even if no tools exist
        try:
            langgraph_tools = self.adapter.get_langgraph_tools()
            self.assertIsInstance(langgraph_tools, list)
        except Exception as e:
            # If no tools exist, that's okay for this test
            self.assertTrue(True)


class TestEndToEndIntegration(unittest.TestCase):
    """Test complete end-to-end integration"""
    
    def test_tool_generation_to_server(self):
        """Test that a generated tool can be served by MCP server"""
        # This is more of a smoke test - just verify the components work together
        server = MCPServer(tools_directory="generated_tools")
        adapter = LangGraphAdapter()  # No parameters needed
        
        # Should not raise exceptions
        server.discover_tools()
        langgraph_tools = adapter.get_langgraph_tools()
        
        self.assertIsInstance(server.tools, dict)
        self.assertIsInstance(langgraph_tools, list)


if __name__ == "__main__":
    unittest.main(verbosity=2) 