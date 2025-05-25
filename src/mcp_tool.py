from abc import ABC, abstractmethod
from typing import Any, Dict

class MCPTool(ABC):
    """
    Abstract base class for all MCP tool definitions.
    Subclasses must implement run and validate methods.
    Required class attributes: name, description, parameters_schema
    """
    name: str
    description: str
    parameters_schema: Dict[str, Any]

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        Execute the tool's main logic.
        Returns the result of the tool's operation.
        """
        pass

    @abstractmethod
    def validate(self, params: Dict[str, Any]) -> bool:
        """
        Validate the input parameters against the tool's schema.
        Returns True if valid, False otherwise.
        """
        pass 