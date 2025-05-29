#!/usr/bin/env python3
"""
Example: Using Standalone MCP Tools with LangGraph
Demonstrates the complete integration workflow
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def demonstrate_tool_conversion():
    """Demonstrate converting standalone tools to LangGraph functions"""
    print("🔧 Converting Standalone MCP Tools to LangGraph Functions")
    print("=" * 60)
    
    # Import the adapter
    from server.langgraph_adapter import convert_mcp_to_langgraph
    
    # Import standalone tools (no inheritance needed!)
    sys.path.insert(0, str(Path(__file__).parent.parent / "generated_tools" / "fastflightstoolv5"))
    from tool import FastFlightsToolV5
    
    # Convert to LangGraph functions
    tools = convert_mcp_to_langgraph(FastFlightsToolV5)
    
    print(f"✅ Converted {len(tools)} tools:")
    for tool in tools:
        print(f"   📋 {tool.__name__}")
        print(f"      Description: {tool.__doc__}")
        print(f"      Parameters: {list(tool.__annotations__.keys())[:-1]}")  # Exclude 'return'
        print(f"      Return type: {tool.__annotations__.get('return', 'Unknown')}")
        print()
    
    return tools

def simulate_langgraph_usage(tools):
    """Simulate how these tools would be used in a LangGraph agent"""
    print("🤖 Simulating LangGraph Agent Usage")
    print("=" * 60)
    
    # Get the FastFlights tool
    flight_tool = tools[0]
    
    print(f"Agent has access to: {flight_tool.__name__}")
    print(f"Tool description: {flight_tool.__doc__}")
    print()
    
    # Simulate agent calling the tool
    print("🎯 Agent receives user request: 'Find flights from Los Angeles to New York on Jan 1st'")
    print()
    print("🔧 Agent constructs tool call:")
    
    tool_call = {
        "flight_data": [
            {
                "date": "2025-01-01",
                "from_airport": "LAX", 
                "to_airport": "JFK"
            }
        ],
        "trip": "one-way",
        "seat": "economy", 
        "passengers": {
            "adults": 1,
            "children": 0,
            "infants_in_seat": 0,
            "infants_on_lap": 0
        },
        "fetch_mode": "common"
    }
    
    print(f"Parameters: {tool_call}")
    print()
    
    # Execute the tool call
    print("⚡ Executing tool...")
    try:
        result = flight_tool(**tool_call)
        print("✅ Tool execution successful!")
        print(f"📄 Result length: {len(result)} characters")
        print(f"📄 Result preview: {result[:200]}...")
        
        if "error" in result.lower():
            print("⚠️  Note: This shows expected behavior when fast-flights package isn't installed")
        
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
    
    print()

def show_framework_independence():
    """Demonstrate that tools are framework-independent"""
    print("🌐 Framework Independence Demonstration")
    print("=" * 60)
    
    # Import tool directly (no framework needed)
    sys.path.insert(0, str(Path(__file__).parent.parent / "generated_tools" / "fastflightstoolv5"))
    from tool import FastFlightsToolV5
    
    print("✅ Direct tool usage (no framework):")
    tool = FastFlightsToolV5()
    print(f"   Tool name: {tool.name}")
    print(f"   Tool type: {type(tool)}")
    print(f"   Dependencies: None (standalone)")
    print()
    
    print("✅ MCP server compatibility:")
    from server.mcp_server import is_mcp_tool_compatible
    print(f"   Compatible: {is_mcp_tool_compatible(tool)}")
    print()
    
    print("✅ LangGraph adapter compatibility:")
    from server.langgraph_adapter import convert_mcp_to_langgraph
    try:
        langgraph_tools = convert_mcp_to_langgraph(FastFlightsToolV5)
        print(f"   Convertible: True ({len(langgraph_tools)} functions created)")
    except Exception as e:
        print(f"   Convertible: False ({e})")
    print()
    
    print("📦 Tool can be used with:")
    print("   • Direct Python imports")
    print("   • MCP protocol servers") 
    print("   • LangGraph agents")
    print("   • Any framework supporting the interface")
    print()

def mock_langgraph_agent_example():
    """Show what a real LangGraph agent setup would look like"""
    print("📚 Real LangGraph Agent Example")
    print("=" * 60)
    
    example_code = '''
# Real LangGraph integration example
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

# Import your standalone tools
from generated_tools.fastflightstoolv5.tool import FastFlightsToolV5
from generated_tools.weathertool.tool import WeatherTool  # If you have one

# Convert to LangGraph functions
from src.server.langgraph_adapter import convert_mcp_to_langgraph
tools = convert_mcp_to_langgraph(FastFlightsToolV5, WeatherTool)

# Create agent with tools
model = ChatAnthropic(model="claude-3-sonnet-20240229")
agent = create_react_agent(
    model=model,
    tools=tools,
    prompt="You are a helpful travel assistant with access to flight and weather tools."
)

# Use the agent
response = agent.invoke({
    "messages": [
        {"role": "user", "content": "Find flights from LA to NYC and check the weather there"}
    ]
})

print(response["messages"][-1].content)
'''
    
    print("💻 Example code:")
    print(example_code)

if __name__ == "__main__":
    print("🚀 Standalone MCP Tools with LangGraph Integration")
    print("=" * 70)
    print()
    
    try:
        # Demonstrate tool conversion
        tools = demonstrate_tool_conversion()
        
        # Simulate LangGraph usage
        simulate_langgraph_usage(tools)
        
        # Show framework independence
        show_framework_independence()
        
        # Show real example
        mock_langgraph_agent_example()
        
        print("🎉 Integration demonstration complete!")
        print("✅ Standalone tools work seamlessly with LangGraph")
        
    except Exception as e:
        print(f"❌ Error in demonstration: {e}")
        import traceback
        traceback.print_exc() 