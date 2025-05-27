"""
Example: Using MCP Tools with LangGraph
Demonstrates how to integrate your generated MCP tools with LangGraph
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.langgraph_adapter import convert_mcp_to_langgraph
from generated_tools.weather_tool import WeatherTool

# Convert MCP tools to LangGraph-compatible functions
tools = convert_mcp_to_langgraph(WeatherTool)

# Example usage with mock LangGraph-style execution
def demo_langgraph_integration():
    """Demo showing how the tools work in LangGraph style"""
    
    print("=== LangGraph Integration Demo ===")
    print(f"Available tools: {[tool.__name__ for tool in tools]}")
    
    # Get the weather tool
    weather_tool = tools[0]  # WeatherTool becomes 'weathertool'
    
    print(f"\nTool name: {weather_tool.__name__}")
    print(f"Tool description: {weather_tool.__doc__}")
    print(f"Tool annotations: {weather_tool.__annotations__}")
    
    # Test the tool
    result = weather_tool(city="San Francisco")
    print(f"\nResult: {result}")


def langgraph_agent_example():
    """
    Example of how you would use this with actual LangGraph
    (Requires: pip install langgraph langchain-anthropic)
    """
    try:
        from langgraph.prebuilt import create_react_agent
        from langchain_anthropic import ChatAnthropic
        
        # Initialize the model
        model = ChatAnthropic(model="claude-3-sonnet-20240229")
        
        # Convert MCP tools to LangGraph tools
        langgraph_tools = convert_mcp_to_langgraph(WeatherTool)
        
        # Create the agent
        agent = create_react_agent(
            model=model,
            tools=langgraph_tools,
            prompt="You are a helpful assistant with access to tools."
        )
        
        # Run the agent
        response = agent.invoke({
            "messages": [{"role": "user", "content": "What's the weather in Tokyo?"}]
        })
        
        print("=== LangGraph Agent Response ===")
        print(response["messages"][-1].content)
        
    except ImportError:
        print("LangGraph not installed. To run this example:")
        print("pip install langgraph langchain-anthropic")
    except Exception as e:
        print(f"Error running LangGraph agent: {e}")
        print("Make sure you have ANTHROPIC_API_KEY set in your environment")


if __name__ == "__main__":
    demo_langgraph_integration()
    print("\n" + "="*50 + "\n")
    langgraph_agent_example() 