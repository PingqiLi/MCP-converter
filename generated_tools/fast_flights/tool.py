from src.mcp_tool import MCPTool
from src.normalizer import Normalizer
from typing import Any, Dict
from datetime import datetime

class FastFlightsTool(MCPTool):
    name = "FastFlightsTool"
    description = "Query Google Flights data using the fast-flights API. Only future flights are allowed."
    parameters_schema = {
        "from_airport": {"type": "string", "description": "IATA code of departure airport", "required": True},
        "to_airport": {"type": "string", "description": "IATA code of arrival airport", "required": True},
        "date": {"type": "string", "description": "Departure date (YYYY-MM-DD), must be in the future", "required": True},
        "trip": {"type": "string", "default": "one-way", "enum": ["one-way", "round-trip"]},
        "seat": {"type": "string", "default": "economy", "enum": ["economy", "premium-economy", "business", "first"]},
        "adults": {"type": "integer", "default": 1},
        "children": {"type": "integer", "default": 0},
        "infants_in_seat": {"type": "integer", "default": 0},
        "infants_on_lap": {"type": "integer", "default": 0},
        "fetch_mode": {"type": "string", "default": "fallback", "enum": ["common", "fallback", "force-fallback"]}
    }

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Validate date is in the future
        date_str = params.get("date")
        if not date_str:
            raise ValueError("'date' parameter is required.")
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            raise ValueError("'date' must be in YYYY-MM-DD format.")
        if date_obj.date() <= datetime.now().date():
            raise ValueError("'date' must be in the future.")

        # Import fast-flights only when needed
        try:
            from fast_flights import FlightData, Passengers, get_flights
        except ImportError:
            raise ImportError("fast-flights package is not installed. Please install it via pip.")

        flight_data = [
            FlightData(
                date=date_str,
                from_airport=params["from_airport"],
                to_airport=params["to_airport"]
            )
        ]
        passengers = Passengers(
            adults=params.get("adults", 1),
            children=params.get("children", 0),
            infants_in_seat=params.get("infants_in_seat", 0),
            infants_on_lap=params.get("infants_on_lap", 0)
        )
        result = get_flights(
            flight_data=flight_data,
            trip=params.get("trip", "one-way"),
            seat=params.get("seat", "economy"),
            passengers=passengers,
            fetch_mode=params.get("fetch_mode", "fallback")
        )
        return Normalizer.to_dict(result)

    def validate(self, params: Dict[str, Any]) -> bool:
        required = ["from_airport", "to_airport", "date"]
        for r in required:
            if r not in params or not isinstance(params[r], str) or not params[r].strip():
                return False
        # Validate date format and future
        try:
            date_obj = datetime.strptime(params["date"], "%Y-%m-%d")
            if date_obj.date() <= datetime.now().date():
                return False
        except Exception:
            return False
        return True 