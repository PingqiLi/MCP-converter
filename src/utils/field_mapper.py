import json
from typing import Dict, Any, Optional
import difflib

class FieldMapper:
    """
    Maps API response fields to required MCP fields using configurable or inferable mapping.
    """
    def __init__(self, mapping: Optional[Dict[str, str]] = None):
        self.mapping = mapping or {}

    def map_fields(self, normalized_response: Dict[str, Any], parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map API response fields to MCP schema format
        
        Args:
            normalized_response: The normalized API response
            parsed_data: Parsed data from input parser
            
        Returns:
            Dict containing MCP-compatible mapping
        """
        # Create MCP-compatible mapping
        mcp_mapping = {
            "input_schema": parsed_data.get("parameters", {}),
            "output_schema": self._create_output_schema(normalized_response),
            "field_mapping": self._create_field_mapping(normalized_response)
        }
        
        return mcp_mapping
    
    def _create_output_schema(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Create output schema from API response"""
        schema = {
            "type": "object",
            "properties": {}
        }
        
        for key, value in response.items():
            schema["properties"][key] = self._infer_json_schema_type(value)
        
        return schema
    
    def _create_field_mapping(self, response: Dict[str, Any]) -> Dict[str, str]:
        """Create field mapping for API response"""
        mapping = {}
        
        # Create direct mappings for now
        for key in response.keys():
            mapping[key] = key
        
        return mapping
    
    def _infer_json_schema_type(self, value: Any) -> Dict[str, Any]:
        """Infer JSON schema type from a value"""
        if isinstance(value, str):
            return {"type": "string"}
        elif isinstance(value, int):
            return {"type": "integer"}
        elif isinstance(value, float):
            return {"type": "number"}
        elif isinstance(value, bool):
            return {"type": "boolean"}
        elif isinstance(value, list):
            return {"type": "array", "items": {"type": "object"} if value and isinstance(value[0], dict) else {"type": "string"}}
        elif isinstance(value, dict):
            properties = {}
            for k, v in value.items():
                properties[k] = self._infer_json_schema_type(v)
            return {"type": "object", "properties": properties}
        else:
            return {"type": "string"}

    def map_fields_legacy(self, data: Dict[str, Any], infer: bool = True, mcp_fields: Optional[list] = None) -> Dict[str, Any]:
        """
        Legacy method: Map fields in data to MCP fields using config or inference.
        If infer is True, try to match fields by name similarity if not in mapping.
        mcp_fields: list of required MCP field names (for inference).
        """
        result = {}
        for mcp_field in (mcp_fields or []):
            # Configurable mapping
            if mcp_field in self.mapping:
                src_field = self.mapping[mcp_field]
                result[mcp_field] = data.get(src_field)
            elif infer:
                # Infer mapping by closest match
                candidates = list(data.keys())
                match = difflib.get_close_matches(mcp_field, candidates, n=1)
                if match:
                    result[mcp_field] = data[match[0]]
                else:
                    result[mcp_field] = None
            else:
                result[mcp_field] = None
        return result

    def save_mapping(self, path: str):
        """Save mapping config to a JSON file."""
        with open(path, 'w') as f:
            json.dump(self.mapping, f, indent=2)

    @classmethod
    def load_mapping(cls, path: str) -> 'FieldMapper':
        """Load mapping config from a JSON file."""
        with open(path, 'r') as f:
            mapping = json.load(f)
        return cls(mapping) 