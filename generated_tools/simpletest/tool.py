"""
Generated MCP Tool: SimpleTest
Description: Generated API tool

Auto-generated from API usage code.
"""
import os
import json
import requests
from typing import Any, Dict
from src.mcp_tool import MCPTool

def test_func(input_param): return {'result': input_param}

class SimpleTest(MCPTool):
    name = "SimpleTest"
    description = "Generated API tool"
    parameters_schema = {
    "input": {
        "type": "string",
        "description": "Input parameter for the API",
        "required": true
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
#   "message": "Code executed successfully"
# }
