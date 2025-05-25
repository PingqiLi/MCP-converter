import json
import os
from typing import Any, Dict
from pathlib import Path

class InputParser:
    """
    LLM-based parser for API documentation.
    Requires LLM API key - raises error if not available.
    """

    def __init__(self):
        self.llm_client = None
        self.llm_config = self._load_llm_config()
        self._initialize_llm_client()

    def _load_llm_config(self) -> Dict[str, Any]:
        """Load LLM prompts and configuration from external file"""
        config_path = Path(__file__).parent.parent / "config" / "llm_prompts.json"
        
        if not config_path.exists():
            raise FileNotFoundError(f"LLM configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _has_llm_api_key(self) -> bool:
        """Check if any LLM API key is available"""
        api_keys = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY", 
            "GOOGLE_API_KEY",
            "MISTRAL_API_KEY"
        ]
        return any(os.getenv(key) for key in api_keys)

    def _initialize_llm_client(self):
        """Initialize the appropriate LLM client based on available API keys - required for operation"""
        if not self._has_llm_api_key():
            raise RuntimeError(
                "❌ No LLM API key found! This tool requires LLM-based parsing.\n"
                "Please set one of the following environment variables:\n"
                "  - OPENAI_API_KEY (recommended)\n"
                "  - ANTHROPIC_API_KEY\n"
                "  - GOOGLE_API_KEY\n"
                "  - MISTRAL_API_KEY\n"
                "\nExample: export OPENAI_API_KEY='your_key_here'"
            )
        
        if os.getenv("OPENAI_API_KEY"):
            try:
                import openai
                self.llm_client = openai.OpenAI()
                self.llm_provider = "openai"
                return
            except ImportError:
                raise ImportError("OpenAI library not installed. Install with: pip install openai")
        
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                self.llm_client = anthropic.Anthropic()
                self.llm_provider = "anthropic"
                return
            except ImportError:
                raise ImportError("Anthropic library not installed. Install with: pip install anthropic")
        
        raise RuntimeError("Failed to initialize any LLM client despite API key being available")

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
            if self.llm_provider == "openai":
                response = self._call_openai(prompt_config["system_message"], user_prompt)
            elif self.llm_provider == "anthropic":
                response = self._call_anthropic(user_prompt)
            else:
                raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
            
            # Parse LLM response
            parsed_info = self._parse_llm_response(response)
            parsed_info["parsing_method"] = "llm"
            parsed_info["confidence_score"] = 0.95  # High confidence with LLM
            parsed_info["llm_provider"] = self.llm_provider
            
            return parsed_info
            
        except Exception as e:
            raise RuntimeError(f"LLM parsing failed: {e}")

    def _call_openai(self, system_message: str, user_prompt: str) -> str:
        """Call OpenAI API using configuration"""
        model_config = self.llm_config["models"]["openai"]
        
        response = self.llm_client.chat.completions.create(
            model=model_config["model"],
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"]
        )
        return response.choices[0].message.content

    def _call_anthropic(self, user_prompt: str) -> str:
        """Call Anthropic API using configuration"""
        model_config = self.llm_config["models"]["anthropic"]
        
        response = self.llm_client.messages.create(
            model=model_config["model"],
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.content[0].text

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
                raise ValueError("No valid JSON found in LLM response")
                
        except json.JSONDecodeError as e:
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
            "usage_examples": parsed.get("usage_examples", []),
            "usage_info": {"llm_extracted": True}
        }



 