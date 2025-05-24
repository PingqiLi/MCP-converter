from src.mcp_tool import MCPTool
from typing import Any, Dict

class WeatherTool(MCPTool):
    name = "WeatherTool"
    description = "A tool to fetch weather information for a given city."
    parameters_schema = {
        "city": {"type": "string", "description": "City name to fetch weather for."}
    }

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        city = params.get("city")
        # Dummy implementation: returns static weather data
        if not city:
            raise ValueError("City parameter is required.")
        return {
            "location": city,
            "temp": 20.5,
            "description": "Cloudy"
        }

    def validate(self, params: Dict[str, Any]) -> bool:
        return "city" in params and isinstance(params["city"], str) and params["city"].strip() != "" 