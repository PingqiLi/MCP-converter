"""
Python wrapper for WeatherTool.

Usage:
    from generated_tools.weathertool_wrapper import run_weathertool
    result = run_weathertool(city="London")
"""
from generated_tools.weather_tool import WeatherTool

def run_weathertool(**kwargs):
    """Run the WeatherTool tool with the given parameters."""
    tool = WeatherTool()
    if not tool.validate(kwargs):
        raise ValueError("Invalid parameters for WeatherTool: {}".format(kwargs))
    return tool.run(kwargs) 