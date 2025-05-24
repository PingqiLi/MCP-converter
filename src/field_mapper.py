import json
from typing import Dict, Any, Optional
import difflib

class FieldMapper:
    """
    Maps API response fields to required MCP fields using configurable or inferable mapping.
    """
    def __init__(self, mapping: Optional[Dict[str, str]] = None):
        self.mapping = mapping or {}

    def map_fields(self, data: Dict[str, Any], infer: bool = True, mcp_fields: Optional[list] = None) -> Dict[str, Any]:
        """
        Map fields in data to MCP fields using config or inference.
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