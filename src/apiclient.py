from abc import ABC, abstractmethod
from typing import Any, Dict

class APIClient(ABC):
    """
    Abstract base class for all API integrations.
    Subclasses must implement execute and get_schema methods.
    Required attributes: name, description
    """
    name: str
    description: str

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute an API call with given arguments.
        Returns the API response.
        """
        pass

    @abstractmethod
    def get_schema(self) -> Dict:
        """
        Return the API schema or description as a dictionary.
        """
        pass 