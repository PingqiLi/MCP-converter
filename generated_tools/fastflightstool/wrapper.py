"""
Wrapper for FastFlightsTool
Provides a simple function interface for the MCP tool
"""
import sys
import os
from pathlib import Path

# Add the tool directory to the path
tool_dir = Path(__file__).parent
if str(tool_dir) not in sys.path:
    sys.path.insert(0, str(tool_dir))

from tool import FastFlightsTool

def run_fastflightstool(**kwargs):
    """
    Run FastFlightsTool with the given parameters
    
    Args:
        **kwargs: Parameters for the tool
        
    Returns:
        Result from the tool execution
    """
    tool = FastFlightsTool()
    
    if not tool.validate(kwargs):
        raise ValueError(f"Invalid parameters for FastFlightsTool: {kwargs}")
    
    return tool.run(kwargs)

# Example usage:
if __name__ == "__main__":
    try:
        result = run_fastflightstool(city="London")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
