import json
from typing import Any, Callable, Dict, Type
from dataclasses import is_dataclass, asdict

class Normalizer:
    """
    Normalizes API responses (dataclass, dict, JSON string) into Python dictionaries and serializes to JSON.
    Supports plugin-based extensibility for new response formats.
    """
    _registry: Dict[str, Callable[[Any], Any]] = {}

    def normalize(self, obj: Any) -> Dict[str, Any]:
        """
        Main normalize method that converts any object to a normalized dictionary
        
        Args:
            obj: Object to normalize (dataclass, dict, JSON string, etc.)
            
        Returns:
            Normalized dictionary representation
        """
        normalized = self.to_dict(obj)
        if not isinstance(normalized, dict):
            # If the result is not a dict, wrap it
            return {"result": normalized}
        return normalized

    @classmethod
    def register(cls, type_name: str, normalizer_fn: Callable[[Any], Any]):
        """Register a new normalizer function for a given type name."""
        cls._registry[type_name] = normalizer_fn

    @classmethod
    def to_dict(cls, obj: Any) -> Any:
        """
        Convert dataclass, dict, or JSON string to a Python dictionary.
        Handles nested dataclasses and lists. Uses plugins if registered.
        """
        # Plugin/registry dispatch
        obj_type = type(obj).__name__
        if obj_type in cls._registry:
            return cls._registry[obj_type](obj)
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, dict):
            return obj
        if isinstance(obj, str):
            try:
                return json.loads(obj)
            except Exception:
                pass  # Not a JSON string
        if isinstance(obj, list):
            return [cls.to_dict(item) for item in obj]
        if hasattr(obj, "__dict__") and obj.__dict__:
            return dict(obj.__dict__)
        return obj  # Return as-is if cannot normalize

    @staticmethod
    def to_json(obj: Any) -> str:
        """
        Serialize normalized object to JSON string.
        Handles non-serializable objects by converting them to strings.
        """
        def default(o):
            if is_dataclass(o):
                return asdict(o)
            if hasattr(o, "__dict__") and o.__dict__:
                return dict(o.__dict__)
            return str(o)
        try:
            return json.dumps(obj, default=default)
        except Exception as e:
            raise ValueError(f"Could not serialize object to JSON: {e}") 