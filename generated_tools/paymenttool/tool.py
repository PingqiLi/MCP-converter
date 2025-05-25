"""
Generated MCP Tool: PaymentTool
Description: Tool for payment processing

Auto-generated from API usage code.
"""
import os
import json
import requests
from typing import Any, Dict
from src.mcp_tool import MCPTool

def create_payment(amount: int, currency: str = "usd"):
    stripe.api_key = "your_stripe_key"
    return stripe.PaymentIntent.create(
        amount=amount,
        currency=currency
    )


class PaymentTool(MCPTool):
    name = "PaymentTool"
    description = "Tool for payment processing"
    parameters_schema = {
    "amount": {
        "type": "integer",
        "description": "amount parameter",
        "required": true
    },
    "currency": {
        "type": "string",
        "description": "currency parameter",
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
#   "status": "success",
#   "data": "Sample response data",
#   "timestamp": "2024-01-01T12:00:00Z"
# }
