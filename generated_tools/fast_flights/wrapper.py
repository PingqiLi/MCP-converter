"""
Python wrapper for FastFlightsTool.

Usage:
    from generated_tools.fast_flights.wrapper import run_fastflightstool
    result = run_fastflightstool(
        from_airport="TPE",
        to_airport="MYJ",
        date="2025-01-01",
        adults=1
    )
"""
from generated_tools.fast_flights.tool import FastFlightsTool

def run_fastflightstool(**kwargs):
    """Run the FastFlightsTool tool with the given parameters."""
    tool = FastFlightsTool()
    if not tool.validate(kwargs):
        raise ValueError("Invalid parameters for FastFlightsTool: {}".format(kwargs))
    return tool.run(kwargs) 