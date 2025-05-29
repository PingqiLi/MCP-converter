"""
Generated MCP Tool: FastFlightsToolV5
Description: A Python package for scraping Google Flights data using Base64-encoded Protobuf strings.

Auto-generated from API documentation analysis.
"""
import json
from typing import Any, Dict, List

def call_get_flights(flight_data: List[Dict], trip: str, seat: str, passengers: Dict[str, Any], fetch_mode: str = "common"):
    """
    Function to call fast-flights
    Generated from LLM analysis of API documentation
    
    This is a Python package, not a REST API
    """
    try:
        from fast_flights import FlightData, Passengers, Result, get_flights
        
        # Convert flight_data list to FlightData objects
        flight_data_objects = []
        for item in flight_data:
            flight_data_objects.append(FlightData(
                date=item['date'],
                from_airport=item['from_airport'],
                to_airport=item['to_airport'],
            ))
        # Convert passengers dict to Passengers object
        passengers_obj = Passengers(
            adults=passengers.get('adults', 0),
            children=passengers.get('children', 0),
            infants_in_seat=passengers.get('infants_in_seat', 0),
            infants_on_lap=passengers.get('infants_on_lap', 0),
        )

        # Call the actual function
        result = get_flights(
            flight_data=flight_data_objects, trip=trip, seat=seat, passengers=passengers_obj, fetch_mode=fetch_mode
        )
        
        # Convert result to dictionary format
        response = {}
        response['current_price'] = result.current_price
        response['flights'] = []
        for flight in result.flights:
            flight_dict = {
                'arrival': flight.arrival,
                'arrival_time_ahead': flight.arrival_time_ahead,
                'delay': flight.delay,
                'departure': flight.departure,
                'duration': flight.duration,
                'is_best': flight.is_best,
                'name': flight.name,
                'price': flight.price,
                'stops': flight.stops
            }
            response['flights'].append(flight_dict)
        return response
        
    except ImportError:
        return {
            "error": "fast-flights package not installed",
            "message": "Please install fast-flights: pip install fast-flights"
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": f"Failed to get data: {str(e)}"
        }


class FastFlightsToolV5:
    """MCP Tool for A Python package for scraping Google Flights data using Base64-encoded Protobuf strings."""
    name = "FastFlightsToolV5"
    description = "A Python package for scraping Google Flights data using Base64-encoded Protobuf strings."
    parameters_schema = {
        "flight_data": {
            "type": "array",
            "description": "A list of FlightData objects containing flight details.",
            "required": True,
            "class_structure": {
                "date": "string - Flight date in YYYY-MM-DD format (e.g., '2025-01-01')",
                "from_airport": "string - 3-letter departure airport code (e.g., 'TPE')",
                "to_airport": "string - 3-letter arrival airport code (e.g., 'MYJ')"
            },
            "example": "[FlightData(date='2025-01-01', from_airport='TPE', to_airport='MYJ')]"
        },
        "trip": {
            "type": "string",
            "description": "Type of trip.",
            "required": True,
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
            "required": False,
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
            flight_data = params.get("flight_data", None)
            trip = params.get("trip", None)
            seat = params.get("seat", None)
            passengers = params.get("passengers", None)
            fetch_mode = params.get("fetch_mode", "common")
            
            # Call the function
            result = call_get_flights(flight_data=flight_data, trip=trip, seat=seat, passengers=passengers, fetch_mode=fetch_mode)
            
            return result
        except Exception as e:
            return {
                "error": str(e),
                "message": f"Failed to execute FastFlightsToolV5: {str(e)}"
            }

    def validate(self, params: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        if not isinstance(params, dict):
            return False
        
        # Check flight_data
        flight_data = params.get('flight_data')
        if not flight_data or not isinstance(flight_data, list) or len(flight_data) == 0:
            return False
        for item in flight_data:
            if not isinstance(item, dict):
                return False
            if not all(key in item for key in ['date', 'from_airport', 'to_airport']):
                return False
        # Check trip
        trip = params.get('trip')
        if not trip or not isinstance(trip, str):
            return False
        if trip not in ['one-way', 'round-trip']:
            return False
        # Check seat
        seat = params.get('seat')
        if not seat or not isinstance(seat, str):
            return False
        if seat not in ['economy', 'premium-economy', 'business', 'first']:
            return False
        # Check passengers
        passengers = params.get('passengers')
        if not passengers or not isinstance(passengers, dict):
            return False
        
        return True

# Sample response structure based on API analysis:
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
