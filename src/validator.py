from typing import Dict, List, Tuple

class MCPFieldValidator:
    """
    Validates that all required MCP fields are present in the mapped response.
    Returns (is_valid, errors) tuple.
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