import unittest
from datetime import datetime, timedelta
from generated_tools.fast_flights.wrapper import run_fastflightstool

class TestFastFlightsToolWrapper(unittest.TestCase):
    def setUp(self):
        # Use a date 10 days in the future
        self.future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

    def test_run_valid(self):
        result = run_fastflightstool(
            from_airport="TPE",
            to_airport="MYJ",
            date=self.future_date,
            adults=1
        )
        print("Returned result:", result)
        self.assertIsInstance(result, dict)
        # Check for at least one expected top-level key (MCP style)
        self.assertTrue(any(k in result for k in ["flights", "results", "data", "itineraries", "trips"]),
                        f"Returned dict keys: {list(result.keys())}")

    def test_run_invalid_date(self):
        with self.assertRaises(ValueError):
            run_fastflightstool(
                from_airport="TPE",
                to_airport="MYJ",
                date="2000-01-01"
            )

    def test_run_missing_param(self):
        with self.assertRaises(ValueError):
            run_fastflightstool(
                from_airport="TPE",
                date=self.future_date
            )

if __name__ == "__main__":
    unittest.main() 