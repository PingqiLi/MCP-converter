"""
Generated MCP Tool: FastFlightsOriginal
Description: A Python package for scraping Google Flights data using Base64-encoded Protobuf strings.

Auto-generated from API usage code.
"""
import os
import json
import requests
from typing import Any, Dict
from src.core.mcp_tool import MCPTool

def call_fastflights(flight_data: str, trip: str, seat: str, passengers: str, fetch_mode: str = None):
    """
    Function to call Fast Flights
    Generated from LLM analysis of API documentation
    
    Base URL: None
    Authentication: none
    """
    """
    Usage examples from API documentation:
        - {'description': 'Example usage for a one-way flight search.', 'parameters': {'flight_data': "[FlightData(date='2025-01-01', from_airport='TPE', to_airport='MYJ')]", 'trip': 'one-way', 'seat': 'economy', 'passengers': 'Passengers(adults=2, children=1, infants_in_seat=0, infants_on_lap=0)', 'fetch_mode': 'fallback'}, 'expected_response': 'A Result object containing flight information, prices, and availability.'}
    """
    import requests
    
    
    params = {
        "flight_data": "flight_data_value",
        "trip": "trip_value",
        "seat": "seat_value",
        "passengers": "passengers_value",
        "fetch_mode": fetch_mode or "fetch_mode_value"
    }
    
    response = requests.get("None", params=params)
    return response.json()


class FastFlightsOriginal(MCPTool):
    name = "FastFlightsOriginal"
    description = "A Python package for scraping Google Flights data using Base64-encoded Protobuf strings."
    parameters_schema = {
    "flight_data": {
        "type": "array",
        "description": "A list of FlightData objects containing flight details.",
        "required": true,
        "class_structure": {
            "date": "string - Flight date in YYYY-MM-DD format (e.g., '2025-01-01')",
            "from_airport": "string - 3-letter departure airport code (e.g., 'TPE')",
            "to_airport": "string - 3-letter arrival airport code (e.g., 'MYJ')"
        },
        "example": "[FlightData(date='2025-01-01', from_airport='TPE', to_airport='MYJ')]"
    },
    "trip": {
        "type": "string",
        "description": "Trip type.",
        "required": true,
        "enum": [
            "one-way",
            "round-trip"
        ],
        "example": "one-way"
    },
    "seat": {
        "type": "string",
        "description": "Seat class.",
        "required": true,
        "enum": [
            "economy",
            "premium-economy",
            "business",
            "first"
        ],
        "example": "economy"
    },
    "passengers": {
        "type": "object",
        "description": "Passengers object containing passenger details.",
        "required": true,
        "class_structure": {
            "adults": "integer - Number of adult passengers",
            "children": "integer - Number of child passengers",
            "infants_in_seat": "integer - Number of infants with seats",
            "infants_on_lap": "integer - Number of lap infants"
        },
        "example": "Passengers(adults=2, children=1, infants_in_seat=0, infants_on_lap=0)"
    },
    "fetch_mode": {
        "type": "string",
        "description": "Data fetching method.",
        "required": false,
        "enum": [
            "common",
            "fallback",
            "force-fallback"
        ],
        "default": "common",
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
