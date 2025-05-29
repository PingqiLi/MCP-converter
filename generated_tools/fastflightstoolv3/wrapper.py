"""
Wrapper for FastFlightsToolV3
Provides a simple function interface for the MCP tool
"""
import sys
import os
from pathlib import Path

# Add the tool directory to the path
tool_dir = Path(__file__).parent
if str(tool_dir) not in sys.path:
    sys.path.insert(0, str(tool_dir))

from tool import FastFlightsToolV3

def run_fastflightstoolv3(**kwargs):
    """
    Run FastFlightsToolV3 with the given parameters
    
    Args:
        **kwargs: Parameters for the tool
        
    Returns:
        Result from the tool execution
    """
    tool = FastFlightsToolV3()
    
    if not tool.validate(kwargs):
        raise ValueError(f"Invalid parameters for FastFlightsToolV3: {kwargs}")
    
    return tool.run(kwargs)

# Example usage:
if __name__ == "__main__":
    try:
        # Example usage - replace with actual parameters
        result = run_fastflightstoolv3()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
