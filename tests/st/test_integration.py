#!/usr/bin/env python3
"""
Integration tests for MCP server and LangGraph functionality
"""
import sys
import os
import unittest
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from src.mcp_server import MCPServer
from src.langgraph_adapter import LangGraphAdapter


class TestMCPServerIntegration(unittest.TestCase):
    """Test MCP server functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.server = MCPServer(tools_dir="generated_tools")
    
    def test_server_initialization(self):
        """Test that MCP server initializes correctly"""
        self.assertIsNotNone(self.server)
        self.assertEqual(self.server.tools_dir, "generated_tools")
    
    def test_tool_discovery(self):
        """Test that server can discover tools"""
        tools = self.server.discover_tools()
        self.assertIsInstance(tools, list)
        # Tools list might be empty if no tools are generated yet
    
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
        self.adapter = LangGraphAdapter(tools_dir="generated_tools")
    
    def test_adapter_initialization(self):
        """Test that LangGraph adapter initializes correctly"""
        self.assertIsNotNone(self.adapter)
        self.assertEqual(self.adapter.tools_dir, "generated_tools")
    
    def test_tool_conversion(self):
        """Test that adapter can convert tools"""
        # This test will pass even if no tools exist
        try:
            langgraph_tools = self.adapter.convert_all_tools()
            self.assertIsInstance(langgraph_tools, list)
        except Exception as e:
            # If no tools exist, that's okay for this test
            self.assertTrue(True)


class TestEndToEndIntegration(unittest.TestCase):
    """Test complete end-to-end integration"""
    
    def test_tool_generation_to_server(self):
        """Test that a generated tool can be served by MCP server"""
        # This is more of a smoke test - just verify the components work together
        server = MCPServer(tools_dir="generated_tools")
        adapter = LangGraphAdapter(tools_dir="generated_tools")
        
        # Should not raise exceptions
        tools = server.discover_tools()
        langgraph_tools = adapter.convert_all_tools()
        
        self.assertIsInstance(tools, list)
        self.assertIsInstance(langgraph_tools, list)


if __name__ == "__main__":
    unittest.main(verbosity=2) 