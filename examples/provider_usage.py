#!/usr/bin/env python3
"""
Example: Using the LLM Provider System Programmatically

This example demonstrates how to:
1. Check available providers
2. Use a specific provider
3. Handle provider fallbacks
4. Parse API documentation with different providers
"""

import os
import sys
from pathlib import Path

# Add src to path for this example
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def example_check_available_providers():
    """Example: Check which providers are available"""
    print("🔍 Checking Available Providers...")
    
    from input_parser import LLMProviderRegistry
    
    registry = LLMProviderRegistry()
    available = registry.get_available_providers()
    
    print(f"Available providers: {available}")
    
    if not available:
        print("⚠️  No providers available. Set an API key:")
        for provider_name in registry.priority_order:
            provider_class = registry.providers[provider_name]
            temp_provider = provider_class({})
            print(f"   export {temp_provider.api_key_env_var}='your_key_here'")
    
    return available

def example_use_specific_provider(provider_name: str):
    """Example: Force use of a specific provider"""
    print(f"\n🎯 Using Specific Provider: {provider_name}")
    
    from input_parser import LLMProviderRegistry
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "llm_prompts.json"
    import json
    with open(config_path) as f:
        llm_config = json.load(f)
    
    registry = LLMProviderRegistry()
    
    try:
        # Check if provider is available
        available = registry.get_available_providers()
        if provider_name not in available:
            print(f"❌ Provider {provider_name} not available (API key not set)")
            return False
        
        # Create specific provider
        provider_config = llm_config["models"][provider_name]
        provider = registry.create_provider(provider_name, provider_config)
        
        # Test with simple documentation
        test_doc = "Simple API: GET /users - Returns list of users. No authentication required."
        
        system_msg = "Extract API information and return as JSON."
        user_prompt = f"API Documentation: {test_doc}\n\nReturn JSON with api_name, description, endpoints."
        
        response = provider.call(system_msg, user_prompt)
        print(f"✅ Response from {provider_name}:")
        print(f"   {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error using {provider_name}: {e}")
        return False

def example_automatic_fallback():
    """Example: Automatic provider selection with fallback"""
    print("\n🔄 Automatic Provider Selection...")
    
    from input_parser import InputParser
    
    try:
        # This will automatically select the best available provider
        parser = InputParser()
        
        print(f"✅ Selected provider: {parser.llm_provider_name}")
        
        # Simple API documentation
        api_doc = """
        GitHub API - Get User Info
        
        Endpoint: GET /users/{username}
        Base URL: https://api.github.com
        
        Parameters:
        - username (required): GitHub username
        
        Authentication: Optional Bearer token
        
        Response: JSON with user profile information
        """
        
        result = parser.parse(api_doc)
        
        print("✅ Parsed API documentation:")
        print(f"   API Name: {result.get('api_name', 'N/A')}")
        print(f"   Provider Used: {result.get('llm_provider', 'N/A')}")
        print(f"   Endpoints Found: {len(result.get('endpoints', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with automatic selection: {e}")
        return False

def example_provider_comparison():
    """Example: Compare responses from different providers"""
    print("\n⚖️  Provider Comparison...")
    
    from input_parser import LLMProviderRegistry
    import json
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config" / "llm_prompts.json"
    with open(config_path) as f:
        llm_config = json.load(f)
    
    registry = LLMProviderRegistry()
    available = registry.get_available_providers()
    
    if len(available) < 2:
        print("⚠️  Need at least 2 providers for comparison")
        return False
    
    test_doc = "Weather API: GET /weather?city={city}&units={units}. Returns temperature and conditions."
    system_msg = "Extract API info as JSON with api_name, endpoints, parameters."
    user_prompt = f"Documentation: {test_doc}"
    
    results = {}
    
    for provider_name in available[:3]:  # Test up to 3 providers
        try:
            provider_config = llm_config["models"][provider_name]
            provider = registry.create_provider(provider_name, provider_config)
            
            response = provider.call(system_msg, user_prompt)
            results[provider_name] = response[:150] + "..." if len(response) > 150 else response
            
            print(f"✅ {provider_name}: {results[provider_name]}")
            
        except Exception as e:
            print(f"❌ {provider_name}: Error - {e}")
    
    return len(results) > 0

def main():
    """Run all examples"""
    print("🚀 LLM Provider System Examples\n")
    
    # Check available providers
    available = example_check_available_providers()
    
    if not available:
        print("\n❌ No providers available. Set an API key to run examples.")
        return 1
    
    # Test automatic fallback
    example_automatic_fallback()
    
    # Test specific provider (use first available)
    example_use_specific_provider(available[0])
    
    # Compare providers if multiple available
    if len(available) > 1:
        example_provider_comparison()
    
    print("\n🎉 Examples completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 