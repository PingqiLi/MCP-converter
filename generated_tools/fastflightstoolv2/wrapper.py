"""
Wrapper for FastFlightsToolV2
Provides a simple function interface for the MCP tool
"""
import sys
import os
from pathlib import Path

# Add the tool directory to the path
tool_dir = Path(__file__).parent
if str(tool_dir) not in sys.path:
    sys.path.insert(0, str(tool_dir))

from tool import FastFlightsToolV2

def run_fastflightstoolv2(**kwargs):
    """
    Run FastFlightsToolV2 with the given parameters
    
    Args:
        **kwargs: Parameters for the tool
        
    Returns:
        Result from the tool execution
    """
    tool = FastFlightsToolV2()
    
    if not tool.validate(kwargs):
        raise ValueError(f"Invalid parameters for FastFlightsToolV2: {kwargs}")
    
    return tool.run(kwargs)

# Example usage:
if __name__ == "__main__":
    try:
        # Example flight search from LAX to JFK
        result = run_fastflightstoolv2(
            flight_data=[
                {
                    "date": "2025-07-01",
                    "from_airport": "LAX",
                    "to_airport": "JFK"
                }
            ],
            trip="one-way",
            seat="economy",
            passengers={
                "adults": 1,
                "children": 0,
                "infants_in_seat": 0,
                "infants_on_lap": 0
            },
            fetch_mode="fallback"
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
