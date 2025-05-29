#!/usr/bin/env python3
"""
MCP Server Launcher
Supports both stdio and HTTP transport for LangChain MCP adapters compatibility
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from server.mcp_server import MCPServer, SimpleStdioMCPServer


async def run_stdio_server():
    """Run MCP server with stdio transport"""
    print("🚀 Starting MCP Server (stdio transport)", file=sys.stderr)
    
    # Create and configure MCP server
    mcp_server = MCPServer(tools_directory="generated_tools")
    mcp_server.discover_tools()
    
    print(f"📡 Loaded {len(mcp_server.tools)} tools", file=sys.stderr)
    for tool_name in mcp_server.tools.keys():
        print(f"   • {tool_name}", file=sys.stderr)
    
    # Create stdio wrapper and run
    stdio_server = SimpleStdioMCPServer(mcp_server)
    await stdio_server.run()


async def run_http_server(port: int = 3000):
    """Run MCP server with HTTP transport for LangChain compatibility"""
    try:
        # Try to import FastMCP for HTTP support
        from mcp.server.fastmcp import FastMCP
        import uvicorn
        
        print(f"🌐 Starting MCP HTTP Server on port {port}", file=sys.stderr)
        
        # Create FastMCP server
        mcp = FastMCP("GeneratedTools")
        
        # Load tools from our MCP server
        tool_server = MCPServer(tools_directory="generated_tools")
        tool_server.discover_tools()
        
        print(f"📡 Loaded {len(tool_server.tools)} tools for HTTP server", file=sys.stderr)
        
        # Convert our tools to FastMCP format
        for tool_name, tool_instance in tool_server.tools.items():
            print(f"   • Converting {tool_name}", file=sys.stderr)
            
            # Create FastMCP tool function
            def create_fastmcp_tool(tool_inst):
                @mcp.tool()
                def converted_tool(**kwargs) -> str:
                    """Converted MCP tool for HTTP transport"""
                    if not tool_inst.validate(kwargs):
                        return f"Error: Invalid parameters for {tool_inst.name}"
                    
                    result = tool_inst.run(kwargs)
                    
                    # Convert result to string for FastMCP
                    if isinstance(result, dict):
                        import json
                        return json.dumps(result, indent=2)
                    elif isinstance(result, str):
                        return result
                    else:
                        return str(result)
                
                # Set metadata
                converted_tool.__name__ = tool_inst.name.lower().replace(' ', '_')
                converted_tool.__doc__ = tool_inst.description
                return converted_tool
            
            # Add tool to FastMCP server
            fastmcp_tool = create_fastmcp_tool(tool_instance)
            
        print(f"✅ HTTP server ready at http://localhost:{port}/mcp", file=sys.stderr)
        
        # Run HTTP server
        config = uvicorn.Config(
            app=mcp.get_app(),
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
        
    except ImportError as e:
        print(f"❌ HTTP server requires additional dependencies:", file=sys.stderr)
        print(f"   pip install fastmcp uvicorn", file=sys.stderr)
        print(f"   Error: {e}", file=sys.stderr)
        sys.exit(1)


async def run_langchain_compatible_server(port: int = 3000):
    """
    Run a server specifically optimized for LangChain MCP adapters
    This uses the streamable HTTP transport that LangChain adapters expect
    """
    try:
        from mcp.server.fastmcp import FastMCP
        
        print(f"🔗 Starting LangChain-compatible MCP Server on port {port}", file=sys.stderr)
        print("📖 Compatible with: https://github.com/langchain-ai/langchain-mcp-adapters", file=sys.stderr)
        
        # Create FastMCP server with streamable HTTP
        mcp = FastMCP("GeneratedToolsForLangChain")
        
        # Load and convert tools
        tool_server = MCPServer(tools_directory="generated_tools") 
        tool_server.discover_tools()
        
        print(f"📡 Converting {len(tool_server.tools)} tools for LangChain", file=sys.stderr)
        
        for tool_name, tool_instance in tool_server.tools.items():
            print(f"   🔧 {tool_name}", file=sys.stderr)
            
            # Create LangChain-optimized tool function
            def create_langchain_tool(tool_inst):
                async def langchain_compatible_tool(**kwargs):
                    """LangChain-compatible async tool"""
                    try:
                        # Validate parameters
                        if not tool_inst.validate(kwargs):
                            return {"error": f"Invalid parameters for {tool_inst.name}"}
                        
                        # Execute tool
                        result = tool_inst.run(kwargs)
                        
                        # Return structured response for LangChain
                        if isinstance(result, dict):
                            return result
                        elif isinstance(result, str):
                            return {"result": result}
                        else:
                            return {"result": str(result)}
                            
                    except Exception as e:
                        return {"error": f"Tool execution failed: {str(e)}"}
                
                # Set function metadata for MCP/LangChain
                langchain_compatible_tool.__name__ = tool_inst.name.lower().replace(' ', '_')
                langchain_compatible_tool.__doc__ = tool_inst.description
                return langchain_compatible_tool
            
            # Register with FastMCP
            tool_func = create_langchain_tool(tool_instance)
            mcp._tools[tool_func.__name__] = tool_func
        
        print(f"✅ LangChain-compatible server ready", file=sys.stderr)
        print(f"🌐 Access at: http://localhost:{port}/mcp", file=sys.stderr)
        print(f"📚 Usage example:", file=sys.stderr)
        print(f"   from langchain_mcp_adapters.client import MultiServerMCPClient", file=sys.stderr)
        print(f"   client = MultiServerMCPClient({{", file=sys.stderr)
        print(f"       \"generated_tools\": {{", file=sys.stderr)
        print(f"           \"url\": \"http://localhost:{port}/mcp\",", file=sys.stderr)
        print(f"           \"transport\": \"streamable_http\"", file=sys.stderr)
        print(f"       }}", file=sys.stderr)
        print(f"   }})", file=sys.stderr)
        
        # Run with streamable HTTP transport
        mcp.run(transport="streamable-http", port=port)
        
    except ImportError as e:
        print(f"❌ LangChain server requires FastMCP:", file=sys.stderr)
        print(f"   pip install fastmcp", file=sys.stderr)
        print(f"   Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="MCP Server for generated tools - Compatible with LangChain MCP Adapters"
    )
    parser.add_argument(
        "--transport", 
        choices=["stdio", "http", "langchain"],
        default="stdio",
        help="Transport type (default: stdio)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port for HTTP transport (default: 3000)"
    )
    parser.add_argument(
        "--tools-dir",
        default="generated_tools",
        help="Directory containing generated tools (default: generated_tools)"
    )
    
    args = parser.parse_args()
    
    if args.transport == "stdio":
        asyncio.run(run_stdio_server())
    elif args.transport == "http":
        asyncio.run(run_http_server(args.port))
    elif args.transport == "langchain":
        asyncio.run(run_langchain_compatible_server(args.port))


if __name__ == "__main__":
    main() 