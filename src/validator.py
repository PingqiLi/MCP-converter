from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of validation"""
    is_valid: bool
    errors: List[str]

class Validator:
    """
    Validates that all required MCP fields are present in the mapped response.
    """
    
    def validate_mcp_fields(self, mcp_mapping: Dict[str, Any]) -> ValidationResult:
        """
        Validate MCP field mapping
        
        Args:
            mcp_mapping: The MCP mapping dict from field_mapper
            
        Returns:
            ValidationResult with is_valid flag and any errors
        """
        errors = []
        
        # Check for required top-level keys
        required_keys = ["input_schema", "output_schema"]
        for key in required_keys:
            if key not in mcp_mapping:
                errors.append(f"Missing required key: '{key}'")
        
        # Validate input schema
        if "input_schema" in mcp_mapping:
            input_schema = mcp_mapping["input_schema"]
            if not isinstance(input_schema, dict):
                errors.append("input_schema must be a dictionary")
            elif not input_schema:
                errors.append("input_schema cannot be empty - at least one parameter required")
        
        # Validate output schema
        if "output_schema" in mcp_mapping:
            output_schema = mcp_mapping["output_schema"]
            if not isinstance(output_schema, dict):
                errors.append("output_schema must be a dictionary")
            elif "type" not in output_schema:
                errors.append("output_schema must have a 'type' field")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, errors=errors)

class MCPFieldValidator:
    """
    Legacy validator class - kept for backwards compatibility
    """
    @staticmethod
    def validate(mapped_response: Dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
        """
        Check for missing or invalid MCP fields in the mapped response.
        Returns (is_valid, list of error messages).
        """
        errors = []
        for field in required_fields:
            if field not in mapped_response or mapped_response[field] is None:
                errors.append(f"Missing or null required field: '{field}'")
        is_valid = len(errors) == 0
        return is_valid, errors 