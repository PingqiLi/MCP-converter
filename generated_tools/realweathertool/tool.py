"""
Generated MCP Tool: RealWeatherTool
Description: Tool for getting weather information

Auto-generated from API usage code.
"""
import os
import json
import requests
from typing import Any, Dict
from src.mcp_tool import MCPTool

def get_weather(city: str, api_key: str = None, units: str = "metric") -> dict:
    """
    Get current weather for a city using OpenWeatherMap API
    
    Args:
        city: City name (e.g., "London", "New York", "Tokyo,JP")
        api_key: OpenWeatherMap API key (defaults to env OPENWEATHER_API_KEY)
        units: Temperature units - "metric", "imperial", or "standard"
    
    Returns:
        dict: Weather data from API
    """
    if api_key is None:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("API key required. Set OPENWEATHER_API_KEY env var or pass api_key parameter")
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raises exception for bad status codes
    
    return response.json()


class RealWeatherTool(MCPTool):
    name = "RealWeatherTool"
    description = "Tool for getting weather information"
    parameters_schema = {
    "city": {
        "type": "string",
        "description": "city parameter"
    },
    "api_key": {
        "type": "string",
        "description": "api_key parameter"
    },
    "units": {
        "type": "string",
        "description": "units parameter"
    }
}

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        try:
            # Extract parameters
            city = params.get("city", "London")
            units = params.get("units", "metric")
            api_key = params.get("api_key") or os.getenv("OPENWEATHER_API_KEY")
            
            # Call the extracted function
            result = get_weather(city=city, api_key=api_key, units=units)
            
            return result
        except Exception as e:
            return {
                "error": str(e),
                "message": f"Failed to get weather data: {str(e)}"
            }

    def validate(self, params: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        # Check required parameters
        if not isinstance(params, dict):
            return False
            
        # For weather tool, city is typically required
        if "city" in self.parameters_schema:
            city = params.get("city")
            if not city or not isinstance(city, str) or not city.strip():
                return False
        
        return True

# Sample response structure for reference:
# {
#   "name": "London",
#   "sys": {
#     "country": "GB"
#   },
#   "main": {
#     "temp": 15.5,
#     "humidity": 72
#   },
#   "weather": [
#     {
#       "main": "Clouds",
#       "description": "overcast clouds"
#     }
#   ],
#   "wind": {
#     "speed": 3.2
#   }
# }
