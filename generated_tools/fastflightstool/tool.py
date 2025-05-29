"""
Generated MCP Tool: FastFlightsTool
Description: An API for scraping Google Flights data using Base64-encoded Protobuf strings. It provides structured flight information, prices, and availability without requiring an API key.

Auto-generated from API usage code.
"""
import os
import json
import requests
from typing import Any, Dict
from src.core.mcp_tool import MCPTool

def call_fastflightsapi(flight_data: str, trip: str, seat: str, passengers: str, fetch_mode: str = None):
    """
    Function to call Fast Flights API
    Generated from LLM analysis of API documentation
    
    Base URL: Not applicable (local Python package)
    Authentication: none
    """
    """
    Usage examples from API documentation:
        - {'description': 'Retrieve one-way flight data from Taipei to Matsuyama', 'parameters': {'flight_data': [{'date': '2025-01-01', 'from_airport': 'TPE', 'to_airport': 'MYJ'}], 'trip': 'one-way', 'seat': 'economy', 'passengers': {'adults': 2, 'children': 1, 'infants_in_seat': 0, 'infants_on_lap': 0}, 'fetch_mode': 'fallback'}, 'expected_response': 'A Result object containing flight information, prices, and availability.'}
    """
    import requests
    
    
    params = {
        "flight_data": "flight_data_value",
        "trip": "trip_value",
        "seat": "seat_value",
        "passengers": "passengers_value",
        "fetch_mode": fetch_mode or "fetch_mode_value"
    }
    
    response = requests.get("Not applicable (local Python package)", params=params)
    return response.json()


class FastFlightsTool(MCPTool):
    name = "FastFlightsTool"
    description = "An API for scraping Google Flights data using Base64-encoded Protobuf strings. It provides structured flight information, prices, and availability without requiring an API key."
    parameters_schema = {
    "flight_data": {
        "type": "array",
        "description": "A list of FlightData objects containing flight details.",
        "required": true,
        "default": null,
        "enum": null,
        "pattern": null,
        "minimum": null,
        "maximum": null,
        "example": [
            {
                "date": "2025-01-01",
                "from_airport": "TPE",
                "to_airport": "MYJ"
            }
        ]
    },
    "trip": {
        "type": "string",
        "description": "The type of trip. Can be 'one-way' or 'round-trip'.",
        "required": true,
        "default": null,
        "enum": [
            "one-way",
            "round-trip"
        ],
        "pattern": null,
        "minimum": null,
        "maximum": null,
        "example": "one-way"
    },
    "seat": {
        "type": "string",
        "description": "The class of seat. Can be 'economy', 'premium-economy', 'business', or 'first'.",
        "required": true,
        "default": null,
        "enum": [
            "economy",
            "premium-economy",
            "business",
            "first"
        ],
        "pattern": null,
        "minimum": null,
        "maximum": null,
        "example": "economy"
    },
    "passengers": {
        "type": "object",
        "description": "An object containing the number of passengers.",
        "required": true,
        "default": null,
        "enum": null,
        "pattern": null,
        "minimum": null,
        "maximum": null,
        "example": {
            "adults": 2,
            "children": 1,
            "infants_in_seat": 0,
            "infants_on_lap": 0
        }
    },
    "fetch_mode": {
        "type": "string",
        "description": "The data fetching method. Can be 'common', 'fallback', or 'force-fallback'.",
        "required": false,
        "default": "common",
        "enum": [
            "common",
            "fallback",
            "force-fallback"
        ],
        "pattern": null,
        "minimum": null,
        "maximum": null,
        "example": "fallback"
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
#   "flights": [
#     {
#       "airline": "Example Air",
#       "flight_number": "EX123",
#       "departure": "2024-01-01T10:00:00Z",
#       "arrival": "2024-01-01T14:00:00Z",
#       "price": 299.99
#     }
#   ]
# }
