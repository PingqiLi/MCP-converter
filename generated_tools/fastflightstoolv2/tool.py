"""
Generated MCP Tool: FastFlightsToolV2
Description: A Python package for scraping Google Flights data using Base64-encoded Protobuf strings.

Auto-generated from API usage code.
"""
import os
import json
from typing import Any, Dict, List
from src.core.mcp_tool import MCPTool

def call_fastflights(flight_data: List[Dict], trip: str, seat: str, passengers: Dict, fetch_mode: str = "common"):
    """
    Function to call Fast Flights API
    Generated from LLM analysis of API documentation
    
    This is a Python package, not a REST API
    """
    try:
        from fast_flights import FlightData, Passengers, get_flights
        
        # Convert flight_data list to FlightData objects
        flight_data_objects = []
        for flight in flight_data:
            flight_data_objects.append(FlightData(
                date=flight["date"],
                from_airport=flight["from_airport"],
                to_airport=flight["to_airport"]
            ))
        
        # Convert passengers dict to Passengers object
        passengers_obj = Passengers(
            adults=passengers.get("adults", 1),
            children=passengers.get("children", 0),
            infants_in_seat=passengers.get("infants_in_seat", 0),
            infants_on_lap=passengers.get("infants_on_lap", 0)
        )
        
        # Call the actual Fast Flights API
        result = get_flights(
            flight_data=flight_data_objects,
            trip=trip,
            seat=seat,
            passengers=passengers_obj,
            fetch_mode=fetch_mode
        )
        
        # Convert result to dictionary format
        response = {
            "current_price": result.current_price,
            "flights": []
        }
        
        # Convert each flight object to dictionary
        for flight in result.flights:
            flight_dict = {
                "is_best": flight.is_best,
                "name": flight.name,
                "departure": flight.departure,
                "arrival": flight.arrival,
                "arrival_time_ahead": flight.arrival_time_ahead,
                "duration": flight.duration,
                "stops": flight.stops,
                "delay": flight.delay,
                "price": flight.price
            }
            response["flights"].append(flight_dict)
        
        return response
        
    except ImportError:
        return {
            "error": "fast-flights package not installed",
            "message": "Please install fast-flights: pip install fast-flights"
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": f"Failed to get flight data: {str(e)}"
        }


class FastFlightsToolV2(MCPTool):
    name = "FastFlightsToolV2"
    description = "A Python package for scraping Google Flights data using Base64-encoded Protobuf strings."
    parameters_schema = {
        "flight_data": {
            "type": "array",
            "description": "A list of FlightData objects containing flight details.",
            "required": True,
            "default": None,
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
            "description": "Type of trip.",
            "required": True,
            "default": None,
            "enum": [
                "one-way",
                "round-trip"
            ],
            "example": "one-way"
        },
        "seat": {
            "type": "string",
            "description": "Seat class.",
            "required": True,
            "default": None,
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
            "description": "Passengers object containing details about the passengers.",
            "required": True,
            "default": None,
            "example": {
                "adults": 2,
                "children": 1,
                "infants_in_seat": 0,
                "infants_on_lap": 0
            }
        },
        "fetch_mode": {
            "type": "string",
            "description": "Data fetching method.",
            "required": False,
            "default": "common",
            "enum": [
                "common",
                "fallback",
                "force-fallback"
            ],
            "example": "fallback"
        }
    }

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        try:
            # Extract parameters
            flight_data = params.get("flight_data", [])
            trip = params.get("trip", "one-way")
            seat = params.get("seat", "economy")
            passengers = params.get("passengers", {"adults": 1, "children": 0, "infants_in_seat": 0, "infants_on_lap": 0})
            fetch_mode = params.get("fetch_mode", "common")
            
            # Call the Fast Flights function
            result = call_fastflights(
                flight_data=flight_data,
                trip=trip,
                seat=seat,
                passengers=passengers,
                fetch_mode=fetch_mode
            )
            
            return result
        except Exception as e:
            return {
                "error": str(e),
                "message": f"Failed to get flight data: {str(e)}"
            }

    def validate(self, params: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        # Check required parameters
        if not isinstance(params, dict):
            return False
        
        # Check flight_data
        flight_data = params.get("flight_data")
        if not flight_data or not isinstance(flight_data, list) or len(flight_data) == 0:
            return False
        
        # Validate each flight in flight_data
        for flight in flight_data:
            if not isinstance(flight, dict):
                return False
            if not all(key in flight for key in ["date", "from_airport", "to_airport"]):
                return False
        
        # Check trip
        trip = params.get("trip")
        if not trip or trip not in ["one-way", "round-trip"]:
            return False
        
        # Check seat
        seat = params.get("seat")
        if not seat or seat not in ["economy", "premium-economy", "business", "first"]:
            return False
        
        # Check passengers
        passengers = params.get("passengers")
        if not passengers or not isinstance(passengers, dict):
            return False
        
        return True

# Sample response structure based on ground truth:
# {
#   "current_price": "typical",
#   "flights": [
#     {
#       "is_best": true,
#       "name": "JetBlue",
#       "departure": "4:20 PM on Sat, Jun 28",
#       "arrival": "12:55 AM on Sun, Jun 29",
#       "arrival_time_ahead": "+1",
#       "duration": "5 hr 35 min",
#       "stops": 0,
#       "delay": null,
#       "price": "HK$1438"
#     }
#   ]
# }
