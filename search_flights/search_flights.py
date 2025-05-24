from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fast_flights import FlightData, Passengers, Result, get_flights

class FlightSearchInput(BaseModel):
    origin: str = Field(..., description="IATA code of the departure airport")
    destination: str = Field(..., description="IATA code of the arrival airport")
    depart_date: str = Field(..., description="Departure date in YYYY-MM-DD format")
    return_date: Optional[str] = Field(None, description="Return date in YYYY-MM-DD format (optional)")
    adults: int = Field(1, description="Number of adult passengers")
    children: int = Field(0, description="Number of child passengers")
    infants_in_seat: int = Field(0, description="Number of infants in seat")
    infants_on_lap: int = Field(0, description="Number of infants on lap")
    cabin_class: Optional[str] = Field("economy", description="Cabin class: economy, premium-economy, business, first")
    trip: str = Field("one-way", description="Trip type: one-way or round-trip")

class FlightInfo(BaseModel):
    price: Optional[float]
    currency: Optional[str]
    airline: Optional[str]
    flight_number: Optional[str]
    departure_time: Optional[str]
    arrival_time: Optional[str]
    duration: Optional[str]
    booking_link: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None

class FlightSearchResult(BaseModel):
    flights: List[FlightInfo]
    meta: Optional[Dict[str, Any]] = None

class SearchFlightsTool:
    """MCP Tool: Search for flights using fast-flights (Google Flights scraper)."""
    def __init__(self):
        pass

    async def search_flights(self, params: FlightSearchInput) -> FlightSearchResult:
        # Prepare flight data for fast-flights
        flight_data = [
            FlightData(
                date=params.depart_date,
                from_airport=params.origin,
                to_airport=params.destination,
            )
        ]
        if params.trip == "round-trip" and params.return_date:
            flight_data.append(
                FlightData(
                    date=params.return_date,
                    from_airport=params.destination,
                    to_airport=params.origin,
                )
            )
        passengers = Passengers(
            adults=params.adults,
            children=params.children,
            infants_in_seat=params.infants_in_seat,
            infants_on_lap=params.infants_on_lap,
        )
        # fast-flights is synchronous, so run in thread executor for async compatibility
        import asyncio
        loop = asyncio.get_event_loop()
        result: Result = await loop.run_in_executor(
            None,
            lambda: get_flights(
                flight_data=flight_data,
                trip=params.trip,
                seat=params.cabin_class,
                passengers=passengers,
                fetch_mode="fallback",
            ),
        )
        # Parse results into FlightInfo
        flights = []
        for f in result.flights:
            flights.append(
                FlightInfo(
                    price=f.price,
                    currency=f.currency,
                    airline=f.airline,
                    flight_number=f.flight_number,
                    departure_time=f.departure_time,
                    arrival_time=f.arrival_time,
                    duration=f.duration,
                    booking_link=f.booking_link,
                    raw=f.dict() if hasattr(f, 'dict') else None,
                )
            )
        return FlightSearchResult(flights=flights, meta={"raw": result.dict() if hasattr(result, 'dict') else None}) 