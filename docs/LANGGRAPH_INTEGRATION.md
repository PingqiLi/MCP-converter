# LangGraph Integration Guide

This guide explains how to use your generated MCP tools with LangGraph, enabling your tools to work seamlessly with LangGraph agents.

## Overview

Your current MCP tool system can be easily integrated with LangGraph through the provided adapter. This allows you to:

1. **Convert MCP tools to LangGraph functions**: Use the `LangGraphAdapter` to convert your MCP tool classes into LangGraph-compatible functions
2. **Run an MCP server**: Serve your tools via the Model Context Protocol for use with AI assistants and agents
3. **Maintain compatibility**: Keep using your existing MCP tool generation workflow

## Quick Start

### 1. Install LangGraph Dependencies

```bash
# Install LangGraph and related packages
pip install langgraph langchain-core langchain-anthropic

# Or add to your requirements.txt:
# langgraph>=0.2.0
# langchain-core>=0.3.0
# langchain-anthropic>=0.2.0
```

### 2. Convert MCP Tools to LangGraph

```python
from src.langgraph_adapter import convert_mcp_to_langgraph
from generated_tools.weather_tool import WeatherTool
from generated_tools.fast_flights.tool import FastFlightsTool  # If you have it

# Convert your MCP tools to LangGraph functions
tools = convert_mcp_to_langgraph(WeatherTool, FastFlightsTool)

# Now you can use these tools with LangGraph
print(f"Available tools: {[tool.__name__ for tool in tools]}")
```

### 3. Use with LangGraph Agent

```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

# Initialize the model
model = ChatAnthropic(model="claude-3-sonnet-20240229")

# Create agent with your tools
agent = create_react_agent(
    model=model,
    tools=tools,  # Your converted MCP tools
    prompt="You are a helpful assistant with access to tools."
)

# Use the agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in Tokyo?"}]
})

print(response["messages"][-1].content)
```

## LangGraph Adapter Details

The `LangGraphAdapter` class handles the conversion from MCP tools to LangGraph-compatible functions:

### Features:
- **Automatic conversion**: Converts MCP tool classes to Python functions
- **Parameter validation**: Uses your MCP tool's validation logic
- **Type annotations**: Automatically adds type hints based on your tool's schema
- **Error handling**: Graceful error handling and reporting
- **JSON serialization**: Converts complex results to JSON strings for LangGraph

### Usage:

```python
from src.langgraph_adapter import LangGraphAdapter

# Create adapter
adapter = LangGraphAdapter()

# Register your tools
adapter.register_mcp_tool(WeatherTool)
adapter.register_mcp_tool(YourCustomTool)

# Get LangGraph-compatible functions
tools = adapter.get_langgraph_tools()

# Or use the convenience function
tools = convert_mcp_to_langgraph(WeatherTool, YourCustomTool)
```

## MCP Server

Your project also includes an MCP server that can serve your tools via the Model Context Protocol.

### Running the MCP Server

```bash
# Start the MCP server
python src/mcp_server.py

# The server will automatically discover and load all tools from generated_tools/
```

### MCP Server Features:
- **Auto-discovery**: Automatically finds all `*_tool.py` files in `generated_tools/`
- **Dynamic loading**: Loads MCP tool classes dynamically
- **Protocol compliance**: Implements MCP protocol for tool serving
- **Error handling**: Robust error handling and logging

### Using the MCP Server

The server communicates via stdio and implements these MCP methods:

- `tools/list`: List all available tools
- `tools/call`: Execute a specific tool

Example MCP client interaction:
```json
// List tools
{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}

// Call a tool
{
  "jsonrpc": "2.0", 
  "id": 2, 
  "method": "tools/call", 
  "params": {
    "name": "WeatherTool",
    "arguments": {"city": "San Francisco"}
  }
}
```

## Comparison: LangGraph vs MCP Server

| Feature | LangGraph Integration | MCP Server |
|---------|----------------------|------------|
| **Use Case** | Direct integration with LangGraph agents | Standard MCP protocol for AI assistants |
| **Setup** | Import adapter, convert tools | Run server process |
| **Protocol** | Python function calls | JSON-RPC over stdio |
| **Target** | LangGraph applications | Any MCP-compatible client |
| **Performance** | Direct function calls | Network/IPC overhead |

## Examples

### Example 1: Weather Tool with LangGraph

```python
# File: examples/weather_langgraph.py
from src.langgraph_adapter import convert_mcp_to_langgraph
from generated_tools.weather_tool import WeatherTool
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

# Convert tools
tools = convert_mcp_to_langgraph(WeatherTool)

# Create agent
model = ChatAnthropic(model="claude-3-sonnet-20240229")
agent = create_react_agent(model, tools)

# Query weather
response = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in Paris?"}]
})
```

### Example 2: Custom API Tool

```python
# After generating a custom tool with your CLI:
# python main.py generate-tool --name MyAPITool --api-description desc.txt --usage-code usage.py

from src.langgraph_adapter import convert_mcp_to_langgraph
from generated_tools.myapitool.tool import MyAPITool

# Convert and use
tools = convert_mcp_to_langgraph(MyAPITool)
# ... use with LangGraph as above
```

## Best Practices

1. **Error Handling**: Your MCP tools should implement robust validation and error handling
2. **Type Safety**: Define clear parameter schemas in your MCP tools
3. **Documentation**: Use descriptive tool names and descriptions for better LLM understanding
4. **Testing**: Test both MCP tools individually and their LangGraph integration

## Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure your `generated_tools` directory is in Python path
2. **Tool Not Found**: Check that your tool files follow the `*_tool.py` naming convention
3. **Validation Errors**: Verify your tool's `validate()` method works correctly
4. **LangGraph Errors**: Ensure tool functions have proper type annotations

### Debug Mode:

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test tool conversion
from src.langgraph_adapter import convert_mcp_to_langgraph
tools = convert_mcp_to_langgraph(YourTool)
print(f"Converted tool: {tools[0].__name__}")
print(f"Annotations: {tools[0].__annotations__}")
```

## Next Steps

1. **Generate more tools**: Use your CLI to create tools for different APIs
2. **Extend the adapter**: Add custom logic for specific tool types
3. **Integrate with agents**: Build complex multi-tool agents with LangGraph
4. **Deploy MCP server**: Use the MCP server for production AI assistant integrations 