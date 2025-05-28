import json
from typing import Dict, Any, Optional
import os
from pathlib import Path
from src.core.mcp_tool import MCPTool

class OutputGenerator:
    """
    Generates MCP-compatible JSON files and Python tool classes from validated, mapped responses.
    Optionally validates output against a provided MCP schema.
    """
    @staticmethod
    def write_json(data: Dict[str, Any], path: str, schema: Optional[Dict[str, Any]] = None) -> None:
        """
        Write data to a JSON file at the given path. Optionally validate against schema.
        Raises ValueError if validation fails.
        """
        if schema:
            # Simple schema validation: check required fields
            required = schema.get("required", [])
            missing = [field for field in required if field not in data or data[field] is None]
            if missing:
                raise ValueError(f"Missing required fields for MCP output: {missing}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2) 

    def generate_tool_class(self, name: str, description: str, parameters_schema: Dict[str, Any], 
                          sample_response: Dict[str, Any], usage_code: str, output_file: str) -> None:
        """
        Generate a complete MCP tool class file
        
        Args:
            name: Name of the tool class
            description: Description of the tool
            parameters_schema: Schema for input parameters
            sample_response: Sample API response for reference
            usage_code: Original usage code for reference
            output_file: Path to write the generated tool class
        """
        # Extract main function from usage code to use as implementation
        main_function = self._extract_main_function(usage_code)
        
        # Format the sample response as a proper comment
        sample_response_comment = self._format_sample_response_comment(sample_response)
        
        tool_code = f'''"""
Generated MCP Tool: {name}
Description: {description}

Auto-generated from API usage code.
"""
import os
import json
import requests
from typing import Any, Dict
from src.core.mcp_tool import MCPTool

{main_function}

class {name}(MCPTool):
    name = "{name}"
    description = "{description}"
    parameters_schema = {json.dumps(parameters_schema, indent=4)}

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
            return {{
                "error": str(e),
                "message": f"Failed to get weather data: {{str(e)}}"
            }}

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

{sample_response_comment}
'''
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the tool class file
        with open(output_file, 'w') as f:
            f.write(tool_code)
    
    def _format_sample_response_comment(self, sample_response: Dict[str, Any]) -> str:
        """Format sample response as a proper Python comment"""
        response_json = json.dumps(sample_response, indent=2)
        lines = response_json.split('\n')
        comment_lines = ['# Sample response structure for reference:']
        for line in lines:
            comment_lines.append(f'# {line}')
        return '\n'.join(comment_lines)

    def generate_wrapper(self, tool_name: str, tool_class_path: Path, output_file: str) -> None:
        """
        Generate a simple wrapper function for the tool
        
        Args:
            tool_name: Name of the tool
            tool_class_path: Path to the tool class file
            output_file: Path to write the wrapper
        """
        class_module = tool_class_path.stem  # Get filename without extension
        
        wrapper_code = f'''"""
Wrapper for {tool_name}
Provides a simple function interface for the MCP tool
"""
import sys
import os
from pathlib import Path

# Add the tool directory to the path
tool_dir = Path(__file__).parent
if str(tool_dir) not in sys.path:
    sys.path.insert(0, str(tool_dir))

from {class_module} import {tool_name}

def run_{tool_name.lower()}(**kwargs):
    """
    Run {tool_name} with the given parameters
    
    Args:
        **kwargs: Parameters for the tool
        
    Returns:
        Result from the tool execution
    """
    tool = {tool_name}()
    
    if not tool.validate(kwargs):
        raise ValueError(f"Invalid parameters for {tool_name}: {{kwargs}}")
    
    return tool.run(kwargs)

# Example usage:
if __name__ == "__main__":
    try:
        result = run_{tool_name.lower()}(city="London")
        print(f"Result: {{result}}")
    except Exception as e:
        print(f"Error: {{e}}")
'''
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the wrapper file
        with open(output_file, 'w') as f:
            f.write(wrapper_code)
    
    def _extract_main_function(self, usage_code: str) -> str:
        """Extract the main function from usage code"""
        lines = usage_code.split('\n')
        function_lines = []
        in_function = False
        
        for line in lines:
            if line.strip().startswith('def '):
                in_function = True
                function_lines.append(line)
            elif in_function:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    # End of function
                    break
                function_lines.append(line)
        
        if function_lines:
            return '\n'.join(function_lines)
        else:
            # If no function found, create a basic one
            return '''
def get_weather(city: str, api_key: str = None, units: str = "metric") -> dict:
    """
    Basic weather function - replace with actual implementation
    """
    import requests
    import os
    
    if api_key is None:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("API key required. Set OPENWEATHER_API_KEY env var or pass api_key parameter")
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    return response.json()
''' 