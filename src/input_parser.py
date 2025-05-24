import json
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:
    yaml = None

class InputParser:
    """
    Parses API descriptions (YAML/JSON/OpenAPI) and usage code (Python scripts or snippets).
    Extracts endpoints, request/response schemas, and example data.
    """

    def parse_json(self, json_str: str) -> Optional[Dict[str, Any]]:
        """Parse a JSON string and return a dictionary."""
        try:
            return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return None

    def parse_yaml(self, yaml_str: str) -> Optional[Dict[str, Any]]:
        """Parse a YAML string and return a dictionary."""
        if not yaml:
            print("PyYAML is not installed. Cannot parse YAML.")
            return None
        try:
            return yaml.safe_load(yaml_str)
        except Exception as e:
            print(f"Error parsing YAML: {e}")
            return None

    def parse_python_usage(self, code_str: str) -> Dict[str, Any]:
        """
        Naive parser for Python usage code. Extracts function calls and arguments as example data.
        This is a placeholder for more advanced static analysis.
        """
        import ast
        result = {"functions": []}
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func_name = getattr(node.func, 'id', None) or getattr(getattr(node.func, 'attr', None), 'id', None)
                    args = [ast.dump(arg) for arg in node.args]
                    result["functions"].append({"function": func_name, "args": args})
        except Exception as e:
            print(f"Error parsing Python code: {e}")
        return result

    def extract_endpoints(self, api_dict: Dict[str, Any]) -> Any:
        """
        Extract endpoints from a parsed API description (OpenAPI-style or similar).
        """
        if 'paths' in api_dict:
            return api_dict['paths']
        # Add more heuristics as needed
        return None

    def extract_schemas(self, api_dict: Dict[str, Any]) -> Any:
        """
        Extract request/response schemas from a parsed API description.
        """
        if 'components' in api_dict and 'schemas' in api_dict['components']:
            return api_dict['components']['schemas']
        # Add more heuristics as needed
        return None 