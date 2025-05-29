"""
Tool Generator - Main orchestrator for generating MCP tools from API descriptions
"""
import os
import json
from pathlib import Path
from typing import Dict, Any

from ..llm.input_parser import InputParser
from ..utils.sandbox import Sandbox
from ..utils.normalizer import Normalizer
from ..utils.field_mapper import FieldMapper
from ..utils.validator import Validator
from ..generators.output_generator import OutputGenerator


class ToolGenerator:
    """Main class that orchestrates the tool generation process"""
    
    def __init__(self):
        self.input_parser = InputParser()
        self.sandbox = Sandbox()
        self.normalizer = Normalizer()
        self.field_mapper = FieldMapper()
        self.validator = Validator()
        self.output_generator = OutputGenerator()
    
    def generate_tool_from_documentation(self, name: str, api_documentation: str, 
                                        output_dir: str = "generated_tools") -> None:
        """
        Generate a complete MCP tool from API documentation using LLM analysis
        
        Args:
            name: Name of the tool (e.g., "WeatherTool")
            api_documentation: Comprehensive API documentation text
            output_dir: Directory to output the generated tool
        """
        print(f"🔄 Starting LLM-powered tool generation for '{name}'...")
        
        # Step 1: Parse API documentation with LLM
        print("🧠 Analyzing API documentation with LLM...")
        parsed_data = self.input_parser.parse(api_documentation)
        
        print(f"📋 Parsed API: {parsed_data.get('api_name', 'Unknown')}")
        print(f"🎯 Confidence: {parsed_data.get('confidence_score', 0.5):.1%}")
        print(f"🤖 Provider: {parsed_data.get('llm_provider', 'unknown')}")
        
        # Step 2: Create mock response based on API analysis
        print("📝 Creating sample response from API structure...")
        sample_response = self._create_mock_response(parsed_data)
        
        # Step 3: Normalize the response
        print("🔧 Normalizing API response structure...")
        normalized_response = self.normalizer.normalize(sample_response)
        print(f"✅ Normalized response with {len(normalized_response)} fields")
        
        # Step 4: Map to MCP fields
        print("🗺️  Mapping API fields to MCP schema...")
        mcp_mapping = self.field_mapper.map_fields(normalized_response, parsed_data)
        print("✅ Field mapping completed")
        
        # Step 5: Validate required MCP fields
        print("🔍 Validating MCP field requirements...")
        validation_result = self.validator.validate_mcp_fields(mcp_mapping)
        if not validation_result.is_valid:
            raise ValueError(f"Validation failed: {validation_result.errors}")
        print("✅ MCP validation passed")
        
        # Step 6: Generate output files
        print("📁 Generating tool files...")
        tool_dir = Path(output_dir) / name.lower()
        tool_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate the main tool class
        tool_class_path = tool_dir / "tool.py"
        wrapper_path = tool_dir / "wrapper.py"
        metadata_path = tool_dir / "metadata.json"
        
        self.output_generator.generate_tool_class(
            name=name,
            description=parsed_data.get('description', f"Tool for {name}"),
            parameters_schema=mcp_mapping.get('input_schema', {}),
            sample_response=normalized_response,
            usage_code=self._generate_usage_code_from_parsed_data(parsed_data),
            output_file=str(tool_class_path),
            parsed_data=parsed_data
        )
        
        self.output_generator.generate_wrapper(
            tool_name=name,
            tool_class_path=tool_class_path,
            output_file=str(wrapper_path)
        )
        
        # Generate enhanced metadata file
        metadata = {
            "name": name,
            "description": parsed_data.get('description', f"Tool for {name}"),
            "version": "1.0.0",
            "api_info": {
                "api_name": parsed_data.get('api_name'),
                "base_url": parsed_data.get('base_url'),
                "authentication": parsed_data.get('authentication'),
                "response_format": parsed_data.get('response_format'),
                "endpoints": parsed_data.get('endpoints', [])
            },
            "parsing_info": {
                "method": parsed_data.get('parsing_method', 'llm'),
                "confidence_score": parsed_data.get('confidence_score', 0.95),
                "llm_provider": parsed_data.get('llm_provider', 'unknown'),
                "llm_enhanced": True
            },
            "generated_at": self._get_current_timestamp(),
            "files": {
                "tool": "tool.py",
                "wrapper": "wrapper.py",
                "metadata": "metadata.json"
            },
            "mcp_schema": mcp_mapping,
            "input_sources": {
                "api_documentation_provided": True,
                "documentation_length": len(api_documentation)
            }
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📁 Generated files:")
        print(f"  - {tool_class_path}")
        print(f"  - {wrapper_path}")
        print(f"  - {metadata_path}")
        
        # Update tool registry
        self._update_tool_registry(output_dir, name, metadata)
        
        print(f"🎉 Tool '{name}' generation completed successfully!")
        print(f"🤖 Enhanced with {parsed_data.get('llm_provider', 'LLM')} analysis (confidence: {parsed_data.get('confidence_score', 0.95):.1%})")

    def _create_mock_response(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a mock response based on parsed API information"""
        api_name = parsed_data.get('api_name', '').lower()
        
        if 'weather' in api_name:
            return {
                "name": "London",
                "sys": {"country": "GB"},
                "main": {"temp": 15.5, "humidity": 72, "pressure": 1013},
                "weather": [{"main": "Clouds", "description": "overcast clouds"}],
                "wind": {"speed": 3.2, "deg": 245}
            }
        elif 'flight' in api_name:
            return {
                "flights": [
                    {
                        "airline": "Example Air",
                        "flight_number": "EX123",
                        "departure": "2024-01-01T10:00:00Z",
                        "arrival": "2024-01-01T14:00:00Z",
                        "price": 299.99
                    }
                ]
            }
        else:
            # Generic response
            return {
                "status": "success",
                "data": "Sample response data",
                "timestamp": "2024-01-01T12:00:00Z"
            }

    def _generate_usage_code_from_parsed_data(self, parsed_data: Dict[str, Any]) -> str:
        """Generate usage code from LLM-parsed API data"""
        api_name = parsed_data.get('api_name', 'API').replace(' ', '').replace('-', '').replace('_', '')
        base_url = parsed_data.get('base_url', 'https://api.example.com')
        parameters = parsed_data.get('parameters', {})
        authentication = parsed_data.get('authentication', {})
        usage_examples = parsed_data.get('usage_examples', [])
        
        # Generate function parameters from parsed schema
        param_list = []
        param_usage = {}
        
        for param_name, param_info in parameters.items():
            param_type = param_info.get('type', 'str')
            is_required = param_info.get('required', True)
            
            if param_type == 'string':
                type_hint = 'str'
                default_val = f'"{param_name}_value"'
            elif param_type == 'integer':
                type_hint = 'int'
                default_val = '1'
            elif param_type == 'boolean':
                type_hint = 'bool'
                default_val = 'True'
            else:
                type_hint = 'str'
                default_val = f'"{param_name}_value"'
            
            if is_required:
                param_list.append(f"{param_name}: {type_hint}")
                param_usage[param_name] = default_val
            else:
                param_list.append(f"{param_name}: {type_hint} = None")
                param_usage[param_name] = f"{param_name} or {default_val}"
        
        # Create the function signature
        params_str = ", ".join(param_list) if param_list else ""
        
        # Determine how to handle authentication
        auth_code = ""
        if authentication:
            auth_type = authentication.get('type', 'api_key')
            if auth_type == 'api_key':
                location = authentication.get('location', 'header')
                param_name = authentication.get('parameter_name', 'api_key')
                
                if location == 'header':
                    auth_code = f'''
    headers = {{"{param_name}": api_key}} if "api_key" in locals() else {{}}'''
                elif location == 'query':
                    auth_code = f'''
    if "api_key" in locals():
        params["{param_name}"] = api_key'''
        
        # Build parameter dict for the request
        param_dict_items = []
        for param_name, default in param_usage.items():
            if param_name != 'api_key':  # Skip API key as it's handled in auth
                param_dict_items.append(f'        "{param_name}": {default}')
        
        params_dict = "{\n" + ",\n".join(param_dict_items) + "\n    }" if param_dict_items else "{}"
        
        # Use usage examples if available
        example_comment = ""
        if usage_examples:
            example_comment = f'''
    """
    Usage examples from API documentation:
    {chr(10).join(f"    - {example}" for example in usage_examples[:3])}
    """'''
        
        return f'''
def call_{api_name.lower()}({params_str}):
    """
    Function to call {parsed_data.get('api_name', 'API')}
    Generated from LLM analysis of API documentation
    
    Base URL: {base_url}
    Authentication: {authentication.get('type', 'None')}
    """{example_comment}
    import requests
    {auth_code}
    
    params = {params_dict}
    
    response = requests.get("{base_url}", params=params{', headers=headers' if 'headers' in auth_code else ''})
    return response.json()

# Example usage
if __name__ == "__main__":
    # Replace with actual values
    result = call_{api_name.lower()}({", ".join(f"{k}={v}" for k, v in list(param_usage.items())[:3])})
    print(result)
'''

    # Keep the original method for backward compatibility
    def generate_tool(self, name: str, api_description_file: str, usage_code_file: str, output_dir: str = "generated_tools") -> None:
        """
        Original method - kept for backward compatibility
        Generate a complete MCP tool from API description and usage code files
        """
        print(f"🔄 Starting tool generation for '{name}' (legacy mode)...")
        
        # Read files
        api_description = self._read_file(api_description_file)
        usage_code = self._read_file(usage_code_file)
        
        # Call the enhanced method
        return self.generate_tool_flexible(
            name=name,
            api_description=api_description,
            usage_code=usage_code,
            output_dir=output_dir
        )
    
    def _read_file(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _update_tool_registry(self, output_dir: str, tool_name: str, metadata: Dict[str, Any]) -> None:
        """Update the central tool registry"""
        registry_path = Path(output_dir) / "tool_registry.json"
        
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = json.load(f)
        else:
            registry = {"tools": {}, "last_updated": None}
        
        registry["tools"][tool_name] = {
            "directory": tool_name.lower(),
            "metadata": metadata
        }
        registry["last_updated"] = self._get_current_timestamp()
        
        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
        
        print(f"📝 Updated tool registry: {registry_path}") 