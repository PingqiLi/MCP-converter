import json
import os
from typing import Any, Dict, Optional, Type, Tuple
from pathlib import Path
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        self._initialize_client()
    
    @abstractmethod
    def _initialize_client(self):
        """Initialize the LLM client"""
        pass
    
    @abstractmethod
    def call(self, system_message: str, user_prompt: str) -> str:
        """Make a call to the LLM API"""
        pass
    
    @property
    @abstractmethod
    def api_key_env_var(self) -> str:
        """Environment variable name for API key"""
        pass
    
    @property
    @abstractmethod
    def required_packages(self) -> list:
        """Required packages for this provider"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation"""
    
    @property
    def api_key_env_var(self) -> str:
        return "OPENAI_API_KEY"
    
    @property
    def required_packages(self) -> list:
        return ["openai"]
    
    def _initialize_client(self):
        try:
            import openai
            self.client = openai.OpenAI()
        except ImportError:
            raise ImportError("OpenAI library not installed. Install with: pip install openai")
    
    def call(self, system_message: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.config["model"],
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"]
        )
        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    """Anthropic provider implementation"""
    
    @property
    def api_key_env_var(self) -> str:
        return "ANTHROPIC_API_KEY"
    
    @property
    def required_packages(self) -> list:
        return ["anthropic"]
    
    def _initialize_client(self):
        try:
            import anthropic
            self.client = anthropic.Anthropic()
        except ImportError:
            raise ImportError("Anthropic library not installed. Install with: pip install anthropic")
    
    def call(self, system_message: str, user_prompt: str) -> str:
        response = self.client.messages.create(
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.content[0].text


class GoogleProvider(LLMProvider):
    """Google Gemini provider implementation"""
    
    @property
    def api_key_env_var(self) -> str:
        return "GOOGLE_API_KEY"
    
    @property
    def required_packages(self) -> list:
        return ["google-generativeai"]
    
    def _initialize_client(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv(self.api_key_env_var))
            self.client = genai.GenerativeModel(self.config["model"])
        except ImportError:
            raise ImportError("Google Generative AI library not installed. Install with: pip install google-generativeai")
    
    def call(self, system_message: str, user_prompt: str) -> str:
        # Combine system message and user prompt for Gemini
        combined_prompt = f"{system_message}\n\n{user_prompt}"
        
        # Configure generation parameters
        generation_config = {
            'temperature': self.config["temperature"],
            'max_output_tokens': self.config["max_tokens"],
        }
        
        try:
            response = self.client.generate_content(
                combined_prompt,
                generation_config=generation_config
            )
            
            # Check if response was blocked or empty
            if not response.text:
                if hasattr(response, 'prompt_feedback'):
                    raise RuntimeError(f"Google Gemini blocked the request: {response.prompt_feedback}")
                else:
                    raise RuntimeError("Google Gemini returned empty response")
            
            return response.text
            
        except Exception as e:
            if "quota" in str(e).lower():
                raise RuntimeError(f"Google Gemini API quota exceeded: {e}")
            elif "safety" in str(e).lower():
                raise RuntimeError(f"Google Gemini safety filter triggered: {e}")
            else:
                raise RuntimeError(f"Google Gemini API error: {e}")


class MistralProvider(LLMProvider):
    """Mistral AI provider implementation"""
    
    @property
    def api_key_env_var(self) -> str:
        return "MISTRAL_API_KEY"
    
    @property
    def required_packages(self) -> list:
        return ["mistralai"]
    
    def _initialize_client(self):
        try:
            from mistralai.client import MistralClient
            self.client = MistralClient(api_key=os.getenv(self.api_key_env_var))
        except ImportError:
            raise ImportError("Mistral AI library not installed. Install with: pip install mistralai")
    
    def call(self, system_message: str, user_prompt: str) -> str:
        from mistralai.models.chat_completion import ChatMessage
        
        messages = [
            ChatMessage(role="system", content=system_message),
            ChatMessage(role="user", content=user_prompt)
        ]
        
        response = self.client.chat(
            model=self.config["model"],
            messages=messages,
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"]
        )
        return response.choices[0].message.content


class PerplexityProvider(LLMProvider):
    """Perplexity Sonar provider implementation"""
    
    @property
    def api_key_env_var(self) -> str:
        return "PERPLEXITY_API_KEY"
    
    @property
    def required_packages(self) -> list:
        return ["openai"]  # Perplexity uses OpenAI-compatible API
    
    def _initialize_client(self):
        try:
            import openai
            self.client = openai.OpenAI(
                api_key=os.getenv(self.api_key_env_var),
                base_url="https://api.perplexity.ai"
            )
        except ImportError:
            raise ImportError("OpenAI library not installed (required for Perplexity). Install with: pip install openai")
    
    def call(self, system_message: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"]
            )
            return response.choices[0].message.content
        except Exception as e:
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                raise RuntimeError(f"Perplexity API quota/rate limit exceeded: {e}")
            elif "unauthorized" in str(e).lower():
                raise RuntimeError(f"Perplexity API authentication failed: {e}")
            else:
                raise RuntimeError(f"Perplexity API error: {e}")


class LLMProviderRegistry:
    """Registry for managing LLM providers"""
    
    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "google": GoogleProvider,
            "mistral": MistralProvider,
            "perplexity": PerplexityProvider,
        }
        # Priority order for provider selection
        self.priority_order = ["openai", "anthropic", "google", "perplexity", "mistral"]
    
    def get_available_providers(self) -> list:
        """Get list of providers with available API keys"""
        available = []
        for provider_name in self.priority_order:
            provider_class = self.providers[provider_name]
            # Check API key without initializing the client
            try:
                # Create a dummy instance just to get the API key env var name
                dummy_config = {"model": "dummy", "temperature": 0.1, "max_tokens": 1000}
                temp_provider = object.__new__(provider_class)
                temp_provider.config = dummy_config
                
                api_key = os.getenv(temp_provider.api_key_env_var)
                if api_key:
                    print(f"✅ Found API key for {provider_name}: {temp_provider.api_key_env_var}")
                    available.append(provider_name)
                else:
                    print(f"❌ No API key found for {provider_name}: {temp_provider.api_key_env_var}")
            except Exception as e:
                print(f"❌ Error checking {provider_name}: {e}")
        return available
    
    def create_provider(self, provider_name: str, config: Dict[str, Any]) -> LLMProvider:
        """Create and initialize a provider instance"""
        if provider_name not in self.providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        provider_class = self.providers[provider_name]
        return provider_class(config)
    
    def get_first_available_provider(self, llm_config: Dict[str, Any]) -> Tuple[str, LLMProvider]:
        """Get the first available provider based on priority"""
        available_providers = self.get_available_providers()
        
        if not available_providers:
            api_keys = [self.providers[name]({}).api_key_env_var for name in self.priority_order]
            raise RuntimeError(
                "❌ No LLM API key found! This tool requires LLM-based parsing.\n"
                "Please set one of the following environment variables:\n" +
                "\n".join(f"  - {key}" for key in api_keys) +
                f"\n\nExample: export {api_keys[0]}='your_key_here'"
            )
        
        provider_name = available_providers[0]
        provider_config = llm_config["models"][provider_name]
        provider = self.create_provider(provider_name, provider_config)
        
        return provider_name, provider


class InputParser:
    """
    LLM-based parser for API documentation.
    Requires LLM API key - raises error if not available.
    """

    def __init__(self):
        self.llm_config = self._load_llm_config()
        self.provider_registry = LLMProviderRegistry()
        self.llm_provider_name, self.llm_provider = self.provider_registry.get_first_available_provider(self.llm_config)

    def _load_llm_config(self) -> Dict[str, Any]:
        """Load LLM prompts and configuration from external file"""
        config_path = Path(__file__).parent.parent / "config" / "llm_prompts.json"
        
        if not config_path.exists():
            raise FileNotFoundError(f"LLM configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parse(self, api_documentation: str) -> Dict[str, Any]:
        """
        Parse API documentation using LLM analysis
        
        Args:
            api_documentation: API documentation text (comprehensive description)
            
        Returns:
            Dict containing parsed API information
        """
        if not api_documentation.strip():
            raise ValueError("API documentation cannot be empty")
        
        return self._parse_with_llm(api_documentation)

    def _parse_with_llm(self, api_documentation: str) -> Dict[str, Any]:
        """Use LLM to intelligently parse the API documentation"""
        
        # Create prompt using configuration
        prompt_config = self.llm_config["api_analysis_prompt"]
        user_prompt = prompt_config["user_prompt_template"].format(
            api_documentation=api_documentation
        )
        
        try:
            response = self.llm_provider.call(prompt_config["system_message"], user_prompt)
            
            # Parse LLM response
            parsed_info = self._parse_llm_response(response)
            parsed_info["parsing_method"] = "llm"
            parsed_info["confidence_score"] = 0.95  # High confidence with LLM
            parsed_info["llm_provider"] = self.llm_provider_name
            
            return parsed_info
            
        except Exception as e:
            raise RuntimeError(f"LLM parsing failed: {e}")

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate LLM response"""
        try:
            # Extract JSON from response (in case there's extra text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                parsed = json.loads(json_str)
                
                # Validate and standardize the response
                return self._standardize_llm_response(parsed)
            else:
                print(f"❌ LLM Response (no JSON found):\n{response}")
                raise ValueError("No valid JSON found in LLM response")
                
        except json.JSONDecodeError as e:
            print(f"❌ LLM Response (invalid JSON):\n{response}")
            print(f"❌ Extracted JSON:\n{json_str if 'json_str' in locals() else 'N/A'}")
            raise ValueError(f"Invalid JSON in LLM response: {e}")

    def _standardize_llm_response(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize LLM response to match our expected format"""
        return {
            "api_name": parsed.get("api_name", "Unknown API"),
            "description": parsed.get("description", "Generated API tool"),
            "base_url": parsed.get("base_url"),
            "endpoints": parsed.get("endpoints", []),
            "parameters": parsed.get("parameters", {}),
            "authentication": parsed.get("authentication"),
            "response_format": parsed.get("response_format"),
            "error_handling": parsed.get("error_handling", {}),
            "usage_examples": parsed.get("usage_examples", []),
            "tool_metadata": parsed.get("tool_metadata", {}),
            "usage_info": {"llm_extracted": True}
        }



 