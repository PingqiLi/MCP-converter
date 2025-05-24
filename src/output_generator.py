import json
from typing import Dict, Any, Optional
import os

class OutputGenerator:
    """
    Generates MCP-compatible JSON files from validated, mapped responses.
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