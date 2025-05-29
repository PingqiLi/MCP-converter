#!/usr/bin/env python3
"""
Test script for the simplified LLM-only workflow
Tests the new API documentation input method
"""
import sys
import os
import unittest
from pathlib import Path

# Add src to path (same approach as main.py)
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root / "src"))

from src.core.tool_generator import ToolGenerator


class TestSimplifiedWorkflow(unittest.TestCase):
    """Test cases for the simplified LLM-only workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Check if LLM is available
        self.llm_available = any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"])
        if not self.llm_available:
            self.skipTest("No LLM API key found - skipping LLM-dependent tests")
    
    def test_simple_weather_api(self):
        """Test 1: Generate tool from simple weather API documentation"""
        api_documentation = """
        OpenWeatherMap Current Weather API
        
        This API provides current weather data for any location worldwide. 
        
        Base URL: https://api.openweathermap.org/data/2.5/weather
        
        Authentication: API key required, passed as 'appid' query parameter
        
        Parameters:
        - q (required): City name, e.g., "London", "New York"
        - appid (required): Your API key from OpenWeatherMap
        - units (optional): Temperature units - "metric", "imperial", or "kelvin" (default)
        
        Response Format: JSON
        Example response:
        {
            "name": "London",
            "sys": {"country": "GB"},
            "main": {"temp": 15.5, "humidity": 65, "pressure": 1013},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "wind": {"speed": 3.6, "deg": 180}
        }
        
        Rate Limits: 1000 calls/day for free tier
        """
        
        generator = ToolGenerator()
        
        # This should not raise an exception
        generator.generate_tool_from_documentation(
            name="TestWeatherTool",
            api_documentation=api_documentation,
            output_dir="test_generated_tools"
        )
        
        # Verify the tool was generated
        tool_dir = os.path.join("test_generated_tools", "testweathertool")
        self.assertTrue(os.path.exists(tool_dir))
        self.assertTrue(os.path.exists(os.path.join(tool_dir, "tool.py")))
        self.assertTrue(os.path.exists(os.path.join(tool_dir, "wrapper.py")))
        self.assertTrue(os.path.exists(os.path.join(tool_dir, "metadata.json")))

    def test_news_api(self):
        """Test 2: Generate tool from news API documentation"""
        api_documentation = """
        NewsAPI.org - Everything Endpoint
        
        Search through millions of articles from over 80,000 large and small news sources and blogs.
        
        URL: https://newsapi.org/v2/everything
        Method: GET
        
        Authentication: 
        - Type: API Key
        - Location: Header
        - Header Name: X-API-Key
        
        Required Parameters:
        - q: Keywords or phrases to search for in the article title and body
        - apiKey: Your API key (can also be passed as X-API-Key header)
        
        Optional Parameters:
        - sources: Comma-separated string of news sources or blogs
        - language: Language to search for articles in (e.g., 'en', 'es', 'fr')
        - sortBy: How to sort articles ('relevancy', 'popularity', 'publishedAt')
        
        Response:
        Returns a JSON object with 'status', 'totalResults', and 'articles' array.
        Each article contains title, description, url, urlToImage, publishedAt, source, etc.
        """
        
        generator = ToolGenerator()
        
        # This should not raise an exception
        generator.generate_tool_from_documentation(
            name="TestNewsTool",
            api_documentation=api_documentation,
            output_dir="test_generated_tools"
        )
        
        # Verify the tool was generated
        tool_dir = os.path.join("test_generated_tools", "testnewstool")
        self.assertTrue(os.path.exists(tool_dir))

    def test_minimal_api(self):
        """Test 3: Generate tool from minimal API documentation"""
        api_documentation = """
        Simple Quote API
        
        Get random inspirational quotes.
        
        URL: https://api.quotegarden.com/quotes/random
        No authentication required.
        Returns JSON with quote text and author.
        """
        
        generator = ToolGenerator()
        
        # This should not raise an exception
        generator.generate_tool_from_documentation(
            name="TestQuoteTool",
            api_documentation=api_documentation,
            output_dir="test_generated_tools"
        )
        
        # Verify the tool was generated
        tool_dir = os.path.join("test_generated_tools", "testquotetool")
        self.assertTrue(os.path.exists(tool_dir))

    def test_empty_documentation_error(self):
        """Test error handling for empty documentation"""
        generator = ToolGenerator()
        
        with self.assertRaises(ValueError) as context:
            generator.generate_tool_from_documentation(
                name="TestTool",
                api_documentation="",
                output_dir="test_generated_tools"
            )
        
        self.assertIn("cannot be empty", str(context.exception))

    def tearDown(self):
        """Clean up after tests"""
        # Clean up test generated tools
        import shutil
        if os.path.exists("test_generated_tools"):
            shutil.rmtree("test_generated_tools")


def run_simplified_workflow_tests():
    """Run the simplified workflow tests"""
    print("🧪 Running Simplified Workflow Tests")
    print("=" * 50)
    
    # Check if LLM is available
    llm_available = any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"])
    if not llm_available:
        print("❌ NO LLM API KEY FOUND!")
        print("⚠️  Simplified workflow tests require an LLM API key.")
        print("💡 Set one of these environment variables:")
        print("   - OPENAI_API_KEY (recommended)")
        print("   - ANTHROPIC_API_KEY")
        return False
    else:
        provider = "OpenAI" if os.getenv("OPENAI_API_KEY") else "Anthropic"
        print(f"🤖 LLM API key detected - Using {provider} for tests")
    
    # Run the tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    return True


if __name__ == "__main__":
    run_simplified_workflow_tests() 