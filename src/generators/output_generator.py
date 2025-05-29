import json
from typing import Dict, Any, Optional
import os
from pathlib import Path

class OutputGenerator:
    """
    Generates MCP-compatible JSON files and Python tool classes from validated, mapped responses.
    Uses LLM-generated field mappings and templates to create decoupled tools.
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
                          sample_response: Dict[str, Any], usage_code: str, output_file: str,
                          parsed_data: Dict[str, Any] = None) -> None:
        """
        Generate a complete MCP tool class file using LLM-generated field mappings
        
        Args:
            name: Name of the tool class
            description: Description of the tool
            parameters_schema: Schema for input parameters
            sample_response: Sample API response for reference
            usage_code: Generated usage code based on LLM analysis
            output_file: Path to write the generated tool class
            parsed_data: LLM-parsed API data containing field mappings
        """
        if parsed_data is None:
            parsed_data = {}
        
        # Determine API type and generate appropriate implementation
        api_type = parsed_data.get('api_type', 'rest')
        
        if api_type == 'python_package':
            tool_code = self._generate_python_package_tool(name, description, parameters_schema, 
                                                         sample_response, parsed_data)
        else:
            tool_code = self._generate_rest_api_tool(name, description, parameters_schema, 
                                                   sample_response, parsed_data)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the tool class file
        with open(output_file, 'w') as f:
            f.write(tool_code)
    
    def _generate_python_package_tool(self, name: str, description: str, parameters_schema: Dict[str, Any],
                                    sample_response: Dict[str, Any], parsed_data: Dict[str, Any]) -> str:
        """Generate tool for Python package APIs"""
        
        package_name = parsed_data.get('package_name', 'unknown_package')
        main_function = parsed_data.get('main_function', {})
        import_statement = main_function.get('import_statement', f'from {package_name} import main_function')
        function_name = main_function.get('name', 'main_function')
        
        # Generate parameter extraction code
        param_extraction = self._generate_parameter_extraction(parameters_schema)
        
        # Generate function call code
        function_call = self._generate_function_call(function_name, parameters_schema, parsed_data)
        
        # Generate response transformation code
        response_transform = self._generate_response_transformation(parsed_data)
        
        # Generate validation code
        validation_code = self._generate_validation_code(parameters_schema)
        
        # Format sample response comment
        sample_response_comment = self._format_sample_response_comment(sample_response)
        
        tool_code = f'''"""
Generated MCP Tool: {name}
Description: {description}

Auto-generated from API documentation analysis.
"""
import json
from typing import Any, Dict, List

def call_{function_name.lower()}({self._generate_function_signature(parameters_schema)}):
    """
    Function to call {package_name}
    Generated from LLM analysis of API documentation
    
    This is a Python package, not a REST API
    """
    try:
        {import_statement}
        
{function_call}
        
{response_transform}
        
    except ImportError:
        return {{
            "error": "{package_name} package not installed",
            "message": "Please install {package_name}: pip install {package_name}"
        }}
    except Exception as e:
        return {{
            "error": str(e),
            "message": f"Failed to get data: {{str(e)}}"
        }}


class {name}:
    """MCP Tool for {description}"""
    name = "{name}"
    description = "{description}"
    parameters_schema = {json.dumps(parameters_schema, indent=4)}

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        try:
{param_extraction}
            
            # Call the function
            result = call_{function_name.lower()}({self._generate_function_args(parameters_schema)})
            
            return result
        except Exception as e:
            return {{
                "error": str(e),
                "message": f"Failed to execute {name}: {{str(e)}}"
            }}

    def validate(self, params: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        if not isinstance(params, dict):
            return False
        
{validation_code}
        
        return True

{sample_response_comment}
'''
        return tool_code
    
    def _generate_rest_api_tool(self, name: str, description: str, parameters_schema: Dict[str, Any],
                              sample_response: Dict[str, Any], parsed_data: Dict[str, Any]) -> str:
        """Generate tool for REST APIs"""
        
        base_url = parsed_data.get('base_url', 'https://api.example.com')
        endpoints = parsed_data.get('endpoints', [])
        authentication = parsed_data.get('authentication', {})
        
        # Generate parameter extraction code
        param_extraction = self._generate_parameter_extraction(parameters_schema)
        
        # Generate API call code
        api_call = self._generate_api_call(base_url, endpoints, authentication, parameters_schema)
        
        # Generate validation code
        validation_code = self._generate_validation_code(parameters_schema)
        
        # Format sample response comment
        sample_response_comment = self._format_sample_response_comment(sample_response)
        
        tool_code = f'''"""
Generated MCP Tool: {name}
Description: {description}

Auto-generated from API documentation analysis.
"""
import requests
import json
from typing import Any, Dict

def call_api({self._generate_function_signature(parameters_schema)}):
    """
    Function to call {parsed_data.get('api_name', 'API')}
    Generated from LLM analysis of API documentation
    """
    try:
        {api_call}
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return response.json()
        
    except Exception as e:
        return {{
            "error": str(e),
            "message": f"Failed to call API: {{str(e)}}"
        }}


class {name}:
    """MCP Tool for {description}"""
    name = "{name}"
    description = "{description}"
    parameters_schema = {json.dumps(parameters_schema, indent=4)}

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        try:
            {param_extraction}
            
            # Call the API
            result = call_api({self._generate_function_args(parameters_schema)})
            
            return result
        except Exception as e:
            return {{
                "error": str(e),
                "message": f"Failed to execute {name}: {{str(e)}}"
            }}

    def validate(self, params: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        if not isinstance(params, dict):
            return False
        
        {validation_code}
        
        return True

{sample_response_comment}
'''
        return tool_code
    
    def _generate_function_signature(self, parameters_schema: Dict[str, Any]) -> str:
        """Generate function signature from parameters schema"""
        params = []
        for param_name, param_info in parameters_schema.items():
            param_type = self._get_python_type(param_info.get('type', 'str'))
            is_required = param_info.get('required', True)
            default_value = param_info.get('default', 'None')
            
            if is_required and default_value == 'None':
                params.append(f"{param_name}: {param_type}")
            else:
                if default_value == 'None' or default_value is None:
                    params.append(f"{param_name}: {param_type} = None")
                elif isinstance(default_value, str):
                    params.append(f'{param_name}: {param_type} = "{default_value}"')
                else:
                    params.append(f"{param_name}: {param_type} = {default_value}")
        
        return ", ".join(params)
    
    def _generate_parameter_extraction(self, parameters_schema: Dict[str, Any]) -> str:
        """Generate parameter extraction code"""
        extractions = []
        for param_name, param_info in parameters_schema.items():
            default_value = param_info.get('default', 'None')
            if isinstance(default_value, str) and default_value != 'None':
                default_value = f'"{default_value}"'
            extractions.append(f'            {param_name} = params.get("{param_name}", {default_value})')
        
        return "\n".join(extractions)
    
    def _generate_function_args(self, parameters_schema: Dict[str, Any]) -> str:
        """Generate function call arguments"""
        args = []
        for param_name in parameters_schema.keys():
            args.append(f"{param_name}={param_name}")
        
        return ", ".join(args)
    
    def _generate_function_call(self, function_name: str, parameters_schema: Dict[str, Any], 
                              parsed_data: Dict[str, Any]) -> str:
        """Generate the actual function call code for Python packages"""
        
        # Generate object construction code for complex parameters
        object_constructions = []
        function_args = []
        
        for param_name, param_info in parameters_schema.items():
            param_type = param_info.get('type', 'string')
            
            if param_type == 'object' and 'class_structure' in param_info:
                # This is a custom class object
                class_name = param_info.get('class_name', param_name.title())
                object_constructions.append(f"        # Convert {param_name} dict to {class_name} object")
                object_constructions.append(f"        {param_name}_obj = {class_name}(")
                
                class_structure = param_info.get('class_structure', {})
                for field_name, field_desc in class_structure.items():
                    object_constructions.append(f"            {field_name}={param_name}.get('{field_name}', {self._get_default_for_type(field_desc)}),")
                
                object_constructions.append("        )")
                function_args.append(f"{param_name}={param_name}_obj")
                
            elif param_type == 'array' and 'class_structure' in param_info:
                # This is an array of objects
                item_class = param_info.get('item_class', 'FlightData')  # Use FlightData as default
                object_constructions.append(f"        # Convert {param_name} list to {item_class} objects")
                object_constructions.append(f"        {param_name}_objects = []")
                object_constructions.append(f"        for item in {param_name}:")
                object_constructions.append(f"            {param_name}_objects.append({item_class}(")
                
                class_structure = param_info.get('class_structure', {})
                for field_name, field_desc in class_structure.items():
                    object_constructions.append(f"                {field_name}=item['{field_name}'],")
                
                object_constructions.append("            ))")
                function_args.append(f"{param_name}={param_name}_objects")
            else:
                function_args.append(f"{param_name}={param_name}")
        
        construction_code = "\n".join(object_constructions)
        call_code = f"        # Call the actual function\n        result = {function_name}(\n            {', '.join(function_args)}\n        )"
        
        return f"{construction_code}\n\n{call_code}" if construction_code else call_code
    
    def _generate_response_transformation(self, parsed_data: Dict[str, Any]) -> str:
        """Generate response transformation code based on LLM analysis"""
        response_format = parsed_data.get('response_format', {})
        response_type = response_format.get('type', 'dict')
        
        if response_type == 'object' or response_type == 'dataclass':
            # Need to convert object to dict
            structure = response_format.get('structure', {})
            transform_code = ["        # Convert result to dictionary format"]
            transform_code.append("        response = {}")
            
            for attr_name, attr_info in structure.items():
                attr_type = attr_info.get('type', 'string')
                if attr_type == 'list':
                    # Handle list of objects
                    transform_code.append(f"        response['{attr_name}'] = []")
                    transform_code.append(f"        for item in result.{attr_name}:")
                    transform_code.append("            item_dict = {}")
                    
                    item_structure = attr_info.get('item_structure', {})
                    for field_name, field_desc in item_structure.items():
                        transform_code.append(f"                item_dict['{field_name}'] = item.{field_name}")
                    
                    transform_code.append(f"            response['{attr_name}'].append(item_dict)")
                else:
                    transform_code.append(f"        response['{attr_name}'] = result.{attr_name}")
            
            transform_code.append("        return response")
            return "\n".join(transform_code)
        else:
            return "        return result"
    
    def _generate_api_call(self, base_url: str, endpoints: list, authentication: Dict[str, Any], 
                         parameters_schema: Dict[str, Any]) -> str:
        """Generate API call code for REST APIs"""
        
        # Use first endpoint if available
        endpoint = endpoints[0] if endpoints else {"path": "/", "method": "GET"}
        method = endpoint.get('method', 'GET').upper()
        path = endpoint.get('path', '/')
        
        # Generate URL construction
        url_code = f'        url = "{base_url}{path}"'
        
        # Generate parameters
        params_code = "        params = {}"
        for param_name in parameters_schema.keys():
            params_code += f'\n        if {param_name} is not None:\n            params["{param_name}"] = {param_name}'
        
        # Generate headers for authentication
        auth_code = "        headers = {}"
        auth_type = authentication.get('type', 'none')
        if auth_type == 'api_key':
            location = authentication.get('location', 'header')
            param_name = authentication.get('parameter_name', 'X-API-Key')
            if location == 'header':
                auth_code += f'\n        if api_key:\n            headers["{param_name}"] = api_key'
            else:
                auth_code += f'\n        if api_key:\n            params["{param_name}"] = api_key'
        
        return f"{url_code}\n{params_code}\n{auth_code}"
    
    def _generate_validation_code(self, parameters_schema: Dict[str, Any]) -> str:
        """Generate validation code for parameters"""
        validations = []
        
        for param_name, param_info in parameters_schema.items():
            is_required = param_info.get('required', True)
            param_type = param_info.get('type', 'string')
            enum_values = param_info.get('enum')
            
            if is_required:
                validations.append(f"        # Check {param_name}")
                validations.append(f"        {param_name} = params.get('{param_name}')")
                
                if param_type == 'array':
                    validations.append(f"        if not {param_name} or not isinstance({param_name}, list) or len({param_name}) == 0:")
                    validations.append("            return False")
                    
                    # Validate array items if structure is defined
                    if 'class_structure' in param_info:
                        validations.append(f"        for item in {param_name}:")
                        validations.append("            if not isinstance(item, dict):")
                        validations.append("                return False")
                        
                        class_structure = param_info.get('class_structure', {})
                        required_fields = list(class_structure.keys())
                        validations.append(f"            if not all(key in item for key in {required_fields}):")
                        validations.append("                return False")
                        
                elif param_type == 'object':
                    validations.append(f"        if not {param_name} or not isinstance({param_name}, dict):")
                    validations.append("            return False")
                    
                elif param_type == 'string':
                    validations.append(f"        if not {param_name} or not isinstance({param_name}, str):")
                    validations.append("            return False")
                    
                    if enum_values:
                        validations.append(f"        if {param_name} not in {enum_values}:")
                        validations.append("            return False")
        
        return "\n".join(validations) if validations else "        # No specific validation required"
    
    def _get_python_type(self, json_type: str) -> str:
        """Convert JSON schema type to Python type hint"""
        type_mapping = {
            'string': 'str',
            'integer': 'int', 
            'number': 'float',
            'boolean': 'bool',
            'array': 'List[Dict]',
            'object': 'Dict[str, Any]'
        }
        return type_mapping.get(json_type, 'str')
    
    def _get_default_for_type(self, type_desc: str) -> str:
        """Get default value for a type description"""
        if 'integer' in type_desc.lower():
            return '0'
        elif 'boolean' in type_desc.lower():
            return 'False'
        elif 'list' in type_desc.lower() or 'array' in type_desc.lower():
            return '[]'
        elif 'dict' in type_desc.lower() or 'object' in type_desc.lower():
            return '{}'
        else:
            return '""'
    
    def _format_sample_response_comment(self, sample_response: Dict[str, Any]) -> str:
        """Format sample response as a proper Python comment"""
        response_json = json.dumps(sample_response, indent=2)
        lines = response_json.split('\n')
        comment_lines = ['# Sample response structure based on API analysis:']
        for line in lines:
            comment_lines.append(f'# {line}')
        return '\n'.join(comment_lines)

    def generate_wrapper(self, tool_name: str, tool_class_path: Path, output_file: str) -> None:
        """
        Generate a simple wrapper function for the tool (decoupled from src)
        
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
        # Example usage - replace with actual parameters
        result = run_{tool_name.lower()}()
        print(f"Result: {{result}}")
    except Exception as e:
        print(f"Error: {{e}}")
'''
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the wrapper file
        with open(output_file, 'w') as f:
            f.write(wrapper_code) 