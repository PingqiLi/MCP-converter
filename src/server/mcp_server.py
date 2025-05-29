"""
MCP Server Implementation
Serves generated MCP tools via the Model Context Protocol
Compatible with LangChain MCP Adapters: https://github.com/langchain-ai/langchain-mcp-adapters
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
import importlib.util
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

logger = logging.getLogger(__name__)


def is_mcp_tool_compatible(obj: Any) -> bool:
    """
    Check if an object is MCP tool compatible (duck typing).
    A tool is compatible if it has the required attributes and methods.
    """
    required_attributes = ['name', 'description', 'parameters_schema']
    required_methods = ['run', 'validate']
    
    # Check if all required attributes exist
    for attr in required_attributes:
        if not hasattr(obj, attr):
            return False
    
    # Check if all required methods exist and are callable
    for method in required_methods:
        if not hasattr(obj, method) or not callable(getattr(obj, method)):
            return False
    
    return True


class MCPServer:
    """
    MCP Server that dynamically loads and serves generated MCP tools using the tool registry.
    Works with any tool class that has the required interface (duck typing).
    
    Compatible with LangChain MCP Adapters for both stdio and HTTP transport.
    """
    
    def __init__(self, tools_directory: str = "generated_tools"):
        self.tools_directory = Path(tools_directory)
        self.tools: Dict[str, Any] = {}  # Changed from MCPTool to Any
        self.tool_schemas: Dict[str, Dict[str, Any]] = {}
        
    def discover_tools(self) -> None:
        """Discover and load all MCP tools from the tool registry"""
        registry_path = self.tools_directory / "tool_registry.json"
        
        if not registry_path.exists():
            logger.warning(f"Tool registry not found at {registry_path}")
            logger.info("Falling back to file scanning...")
            self._discover_tools_by_scanning()
            return
        
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)
            
            tools_info = registry.get("tools", {})
            logger.info(f"Found {len(tools_info)} tools in registry")
            
            for tool_name, tool_info in tools_info.items():
                try:
                    self._load_tool_from_registry(tool_name, tool_info)
                except Exception as e:
                    logger.error(f"Failed to load tool {tool_name}: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to read tool registry: {e}")
            logger.info("Fallback to file scanning...")
            self._discover_tools_by_scanning()
    
    def _load_tool_from_registry(self, tool_name: str, tool_info: Dict[str, Any]) -> None:
        """Load a single MCP tool from registry information"""
        tool_dir = self.tools_directory / tool_info["directory"]
        tool_file = tool_dir / "tool.py"
        
        if not tool_file.exists():
            raise FileNotFoundError(f"Tool file not found: {tool_file}")
        
        # Import the module
        module_name = f"{tool_info['directory']}_tool"
        spec = importlib.util.spec_from_file_location(module_name, tool_file)
        if spec is None or spec.loader is None:
            raise ValueError(f"Could not load spec for {tool_file}")
            
        module = importlib.util.module_from_spec(spec)
        
        # Add the tool directory to sys.path temporarily
        tool_dir_str = str(tool_dir)
        if tool_dir_str not in sys.path:
            sys.path.insert(0, tool_dir_str)
        
        try:
            spec.loader.exec_module(module)
        finally:
            # Remove from sys.path
            if tool_dir_str in sys.path:
                sys.path.remove(tool_dir_str)
        
        # Find the tool class (should match the tool name)
        tool_class = getattr(module, tool_name, None)
        if tool_class is None:
            # Try to find any compatible tool class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):
                    # Try to instantiate and check compatibility
                    try:
                        test_instance = attr()
                        if is_mcp_tool_compatible(test_instance):
                            tool_class = attr
                            break
                    except Exception:
                        continue
        
        if tool_class is None:
            raise ValueError(f"No compatible MCP tool class found in {tool_file}")
        
        # Instantiate the tool
        tool_instance = tool_class()
        
        # Validate that the instance is MCP compatible
        if not is_mcp_tool_compatible(tool_instance):
            raise ValueError(f"Tool {tool_name} is not MCP compatible")
        
        self.tools[tool_instance.name] = tool_instance
        
        # Store the schema for MCP protocol - enhanced for LangChain compatibility
        self.tool_schemas[tool_instance.name] = {
            "name": tool_instance.name,
            "description": tool_instance.description,
            "inputSchema": {
                "type": "object",
                "properties": self._convert_schema_for_langchain(tool_instance.parameters_schema),
                "required": list(tool_instance.parameters_schema.keys())
            }
        }
        
        logger.info(f"Loaded tool from registry: {tool_instance.name}")
    
    def _convert_schema_for_langchain(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert tool parameter schema to be fully compatible with LangChain MCP adapters
        """
        converted = {}
        for param_name, param_info in schema.items():
            converted_param = param_info.copy()
            
            # Ensure type is specified
            if 'type' not in converted_param:
                converted_param['type'] = 'string'
            
            # Add description if missing
            if 'description' not in converted_param:
                converted_param['description'] = f"Parameter {param_name}"
            
            # Handle array types specifically for LangChain
            if converted_param['type'] == 'array':
                if 'items' not in converted_param:
                    converted_param['items'] = {'type': 'object'}
            
            # Handle object types
            elif converted_param['type'] == 'object':
                if 'properties' not in converted_param:
                    converted_param['properties'] = {}
            
            converted[param_name] = converted_param
        
        return converted
    
    def _discover_tools_by_scanning(self) -> None:
        """Fallback method: Discover tools by scanning for tool.py files"""
        if not self.tools_directory.exists():
            logger.warning(f"Tools directory {self.tools_directory} does not exist")
            return
            
        for tool_file in self.tools_directory.rglob("tool.py"):
            try:
                self._load_tool_from_file(tool_file)
            except Exception as e:
                logger.error(f"Failed to load tool from {tool_file}: {e}")
    
    def _load_tool_from_file(self, tool_file: Path) -> None:
        """Load a single MCP tool from a Python file (legacy method)"""
        # Import the module
        module_name = f"{tool_file.parent.name}_tool"
        spec = importlib.util.spec_from_file_location(module_name, tool_file)
        if spec is None or spec.loader is None:
            raise ValueError(f"Could not load spec for {tool_file}")
            
        module = importlib.util.module_from_spec(spec)
        
        # Add the tool directory to sys.path temporarily
        tool_dir_str = str(tool_file.parent)
        if tool_dir_str not in sys.path:
            sys.path.insert(0, tool_dir_str)
        
        try:
            spec.loader.exec_module(module)
        finally:
            # Remove from sys.path
            if tool_dir_str in sys.path:
                sys.path.remove(tool_dir_str)
        
        # Find MCP tool classes in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type):
                try:
                    # Try to instantiate and check compatibility
                    tool_instance = attr()
                    if is_mcp_tool_compatible(tool_instance):
                        self.tools[tool_instance.name] = tool_instance
                        
                        # Store the schema for MCP protocol - enhanced for LangChain compatibility
                        self.tool_schemas[tool_instance.name] = {
                            "name": tool_instance.name,
                            "description": tool_instance.description,
                            "inputSchema": {
                                "type": "object",
                                "properties": self._convert_schema_for_langchain(tool_instance.parameters_schema),
                                "required": list(tool_instance.parameters_schema.keys())
                            }
                        }
                        
                        logger.info(f"Loaded tool from file: {tool_instance.name}")
                        break  # Only load one tool per file
                except Exception as e:
                    logger.debug(f"Could not instantiate {attr_name}: {e}")
                    continue
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools for MCP protocol"""
        return list(self.tool_schemas.values())
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with given arguments"""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        
        tool = self.tools[name]
        
        # Validate arguments
        if not tool.validate(arguments):
            raise ValueError(f"Invalid arguments for tool '{name}'")
        
        # Execute the tool
        try:
            result = tool.run(arguments)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error executing tool '{name}': {e}")
            raise
    
    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool"""
        return self.tool_schemas.get(name)


class SimpleStdioMCPServer:
    """
    Simple MCP server that communicates via stdio
    Implements basic MCP protocol for tool serving
    """
    
    def __init__(self, mcp_server: MCPServer):
        self.mcp_server = mcp_server
        self.request_id = 0
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "tools/list":
                result = self.mcp_server.list_tools()
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = await self.mcp_server.call_tool(tool_name, arguments)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
    
    async def run(self):
        """Run the stdio-based MCP server"""
        logger.info("Starting MCP server on stdio...")
        
        # Discover tools
        self.mcp_server.discover_tools()
        logger.info(f"Loaded {len(self.mcp_server.tools)} tools: {list(self.mcp_server.tools.keys())}")
        
        try:
            while True:
                # Read from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                try:
                    request = json.loads(line.strip())
                    response = await self.handle_request(request)
                    print(json.dumps(response), flush=True)
                except json.JSONDecodeError:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")


async def main():
    """Main entry point for the MCP server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]  # Log to stderr to avoid interfering with stdio
    )
    
    # Create and run the server
    mcp_server = MCPServer()
    stdio_server = SimpleStdioMCPServer(mcp_server)
    await stdio_server.run()


if __name__ == "__main__":
    asyncio.run(main()) 