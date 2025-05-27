#!/usr/bin/env python3
"""
Test script for all LLM provider integrations with InputParser
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_provider_integration(provider_name: str, api_key_env: str):
    """Test a specific provider integration"""
    
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

def test_provider_registry():
    """Test the provider registry functionality"""
    
    try:
        from input_parser import LLMProviderRegistry
        
        print("🧪 Testing LLM Provider Registry...")
        
        registry = LLMProviderRegistry()
        
        # Test provider list
        print(f"📋 Registered providers: {list(registry.providers.keys())}")
        print(f"📋 Priority order: {registry.priority_order}")
        
        # Test available providers
        available = registry.get_available_providers()
        print(f"✅ Available providers: {available}")
        
        if not available:
            print("⚠️  No providers available (no API keys set)")
            return True
        
        # Test provider creation
        for provider_name in available:
            try:
                # Get a dummy config for testing
                config = {"model": "test", "temperature": 0.1, "max_tokens": 100}
                provider = registry.create_provider(provider_name, config)
                print(f"✅ Successfully created {provider_name} provider")
            except Exception as e:
                print(f"❌ Failed to create {provider_name} provider: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing provider registry: {e}")
        return False

def main():
    """Run all provider tests"""
    
    print("🚀 Starting LLM Provider Integration Tests\n")
    
    # Test provider registry first
    registry_success = test_provider_registry()
    print()
    
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
    print(f"   Registry: {'✅ PASS' if registry_success else '❌ FAIL'}")
    
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
    if failed_tests or not registry_success:
        print(f"\n❌ Some tests failed: {failed_tests}")
        return 1
    else:
        print("\n🎉 All tests passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 