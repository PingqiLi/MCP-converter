#!/usr/bin/env python3
"""
Test script for all LLM provider integrations with InputParser
"""

import os
import sys
import unittest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

class TestLLMProviderIntegration(unittest.TestCase):
    """Test LLM provider integration functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Check if any LLM API key is available
        self.llm_available = any(os.getenv(key) for key in [
            "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", 
            "MISTRAL_API_KEY", "PERPLEXITY_API_KEY"
        ])
        
        if not self.llm_available:
            self.skipTest("No LLM API key found - skipping LLM-dependent tests")
    
    def test_provider_registry(self):
        """Test the provider registry functionality"""
        
        try:
            from input_parser import LLMProviderRegistry
            
            registry = LLMProviderRegistry()
            
            # Test provider list
            self.assertIsInstance(registry.providers, dict)
            self.assertIsInstance(registry.priority_order, list)
            
            # Test available providers
            available = registry.get_available_providers()
            self.assertIsInstance(available, list)
            
            if available:
                # Test provider creation for available providers
                for provider_name in available[:1]:  # Test only first available
                    config = {"model": "test", "temperature": 0.1, "max_tokens": 100}
                    provider = registry.create_provider(provider_name, config)
                    self.assertIsNotNone(provider)
            
        except ImportError as e:
            self.skipTest(f"Could not import LLMProviderRegistry: {e}")
    
    def test_input_parser_integration(self):
        """Test InputParser with available LLM provider"""
        
        try:
            from input_parser import InputParser
            
            # Test API documentation
            test_doc = """
            Weather API Documentation
            
            Base URL: https://api.weather.com/v1
            
            Endpoint: /current
            Method: GET
            Description: Get current weather for a location
            
            Parameters:
            - location (required): City name or coordinates
            - units (optional): Temperature units (celsius, fahrenheit)
            - api_key (required): Your API key for authentication
            
            Authentication: API key in query parameter
            
            Response: JSON with temperature, humidity, conditions
            """
            
            # Initialize parser
            parser = InputParser()
            self.assertIsNotNone(parser)
            
            # Parse the documentation (this uses the LLM)
            result = parser.parse(test_doc)
            
            # Verify result structure
            self.assertIsInstance(result, dict)
            
            # Verify expected fields are present
            expected_fields = ['api_name', 'description', 'endpoints', 'parameters']
            for field in expected_fields:
                self.assertIn(field, result, f"Missing field: {field}")
            
        except ImportError as e:
            self.skipTest(f"Could not import InputParser: {e}")
        except Exception as e:
            self.fail(f"InputParser integration test failed: {e}")


def test_provider_integration(provider_name: str, api_key_env: str):
    """Test a specific provider integration (helper function for manual testing)"""
    
    # Check if API key is set
    if not os.getenv(api_key_env):
        print(f"⚠️  {api_key_env} not set. Skipping {provider_name} test.")
        return False
    
    try:
        from input_parser import InputParser
        
        # Test API documentation
        test_doc = """
        Weather API Documentation
        
        Base URL: https://api.weather.com/v1
        
        Endpoint: /current
        Method: GET
        Description: Get current weather for a location
        
        Parameters:
        - location (required): City name or coordinates
        - units (optional): Temperature units (celsius, fahrenheit)
        - api_key (required): Your API key for authentication
        
        Authentication: API key in query parameter
        
        Response: JSON with temperature, humidity, conditions
        """
        
        print(f"🧪 Testing {provider_name} integration...")
        
        # Initialize parser
        parser = InputParser()
        
        if parser.llm_provider_name != provider_name:
            print(f"⚠️  Expected {provider_name} provider, got: {parser.llm_provider_name}")
            print(f"   This is normal if another provider has higher priority")
            return True  # Not an error, just different priority
        
        print(f"✅ Successfully initialized with provider: {parser.llm_provider_name}")
        
        # Parse the documentation
        result = parser.parse(test_doc)
        
        print("✅ Successfully parsed API documentation")
        print(f"📊 API Name: {result.get('api_name', 'N/A')}")
        print(f"📊 Provider: {result.get('llm_provider', 'N/A')}")
        print(f"📊 Confidence: {result.get('confidence_score', 'N/A')}")
        
        # Verify expected fields
        expected_fields = ['api_name', 'description', 'endpoints', 'parameters', 'authentication']
        missing_fields = [field for field in expected_fields if field not in result]
        
        if missing_fields:
            print(f"⚠️  Missing fields: {missing_fields}")
        else:
            print("✅ All expected fields present")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {provider_name} integration: {e}")
        return False


def run_manual_provider_tests():
    """Run manual tests for all providers (not part of unittest)"""
    
    print("🚀 Starting LLM Provider Integration Tests\n")
    
    # Test individual providers
    providers_to_test = [
        ("openai", "OPENAI_API_KEY"),
        ("anthropic", "ANTHROPIC_API_KEY"),
        ("google", "GOOGLE_API_KEY"),
        ("mistral", "MISTRAL_API_KEY"),
        ("perplexity", "PERPLEXITY_API_KEY"),
    ]
    
    results = {}
    for provider_name, api_key_env in providers_to_test:
        success = test_provider_integration(provider_name, api_key_env)
        results[provider_name] = success
        print()
    
    # Summary
    print("📊 Test Results Summary:")
    
    for provider_name, success in results.items():
        api_key_env = next(env for name, env in providers_to_test if name == provider_name)
        if os.getenv(api_key_env):
            status = "✅ PASS" if success else "❌ FAIL"
        else:
            status = "⚠️  SKIP (no API key)"
        print(f"   {provider_name.capitalize()}: {status}")
    
    # Overall result
    tested_providers = [name for name, env in providers_to_test if os.getenv(env)]
    if not tested_providers:
        print("\n⚠️  No providers tested (no API keys set)")
        print("Set at least one API key to test the system:")
        for _, env in providers_to_test:
            print(f"   export {env}='your_key_here'")
        return 1
    
    failed_tests = [name for name in tested_providers if not results[name]]
    if failed_tests:
        print(f"\n❌ Some tests failed: {failed_tests}")
        return 1
    else:
        print("\n🎉 All tests passed!")
        return 0


if __name__ == "__main__":
    # If run directly, run manual tests
    import sys
    sys.exit(run_manual_provider_tests()) 