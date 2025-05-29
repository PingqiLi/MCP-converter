"""
LangGraph Adapter for MCP Tools
Converts MCP tool classes to LangGraph-compatible functions
"""
import inspect
from typing import Any, Callable, Dict, List, Union


def is_mcp_tool_compatible(obj: Any) -> bool:
    """
    Check if an object is MCP tool compatible (duck typing).
    A tool is compatible if it has the required attributes and methods.
    """
    required_attributes = ['name', 'description', 'parameters_schema']
    required_methods = ['run', 'validate']
    
    # Check if all required attributes exist
    for attr in required_attributes:
        if not hasattr(obj, attr):
            return False
    
    # Check if all required methods exist and are callable
    for method in required_methods:
        if not hasattr(obj, method) or not callable(getattr(obj, method)):
            return False
    
    return True


class LangGraphAdapter:
    """Adapter to convert MCP tools to LangGraph-compatible functions"""
    
    def __init__(self):
        self.tools: Dict[str, Any] = {}  # Changed from MCPTool to Any
        self.functions: List[Callable] = []
    
    def register_mcp_tool(self, tool_class: type) -> None:
        """Register an MCP tool class"""
        # Try to instantiate the tool to check compatibility
        try:
            tool_instance = tool_class()
        except Exception as e:
            raise ValueError(f"Could not instantiate {tool_class.__name__}: {e}")
        
        if not is_mcp_tool_compatible(tool_instance):
            raise ValueError(f"{tool_class.__name__} is not MCP tool compatible. "
                           f"It must have attributes: name, description, parameters_schema "
                           f"and methods: run, validate")
        
        self.tools[tool_instance.name] = tool_instance
        
        # Create LangGraph-compatible function
        langgraph_func = self._create_langgraph_function(tool_instance)
        self.functions.append(langgraph_func)
    
    def _create_langgraph_function(self, tool: Any) -> Callable:  # Changed from MCPTool to Any
        """Create a LangGraph-compatible function from an MCP tool"""
        
        def langgraph_wrapper(**kwargs) -> str:
            """Wrapper function for LangGraph"""
            try:
                # Validate parameters using MCP tool's validation
                if not tool.validate(kwargs):
                    return f"Error: Invalid parameters for {tool.name}"
                
                # Run the MCP tool
                result = tool.run(kwargs)
                
                # Convert result to string for LangGraph
                if isinstance(result, dict):
                    import json
                    return json.dumps(result, indent=2)
                elif isinstance(result, str):
                    return result
                else:
                    return str(result)
                    
            except Exception as e:
                return f"Error executing {tool.name}: {str(e)}"
        
        # Set function metadata for LangGraph
        langgraph_wrapper.__name__ = tool.name.lower()
        langgraph_wrapper.__doc__ = tool.description
        
        # Add type annotations dynamically based on tool schema
        self._add_function_annotations(langgraph_wrapper, tool.parameters_schema)
        
        return langgraph_wrapper
    
    def _add_function_annotations(self, func: Callable, schema: Dict[str, Any]) -> None:
        """Add type annotations to function based on MCP tool schema"""
        from typing import List, Dict, Union
        
        annotations = {}
        
        for param_name, param_info in schema.items():
            param_type = param_info.get('type', 'string')
            
            if param_type == 'string':
                annotations[param_name] = str
            elif param_type == 'integer':
                annotations[param_name] = int
            elif param_type == 'number':
                annotations[param_name] = float
            elif param_type == 'boolean':
                annotations[param_name] = bool
            elif param_type == 'array':
                annotations[param_name] = List[Dict[str, Any]]  # Most arrays in our context are lists of objects
            elif param_type == 'object':
                annotations[param_name] = Dict[str, Any]
            else:
                annotations[param_name] = str  # Fallback to string
        
        annotations['return'] = str
        func.__annotations__ = annotations
    
    def get_langgraph_tools(self) -> List[Callable]:
        """Get all LangGraph-compatible tools"""
        return self.functions
    
    def get_tool_by_name(self, name: str) -> Callable:
        """Get a specific LangGraph tool by name"""
        for func in self.functions:
            if func.__name__ == name.lower():
                return func
        raise ValueError(f"Tool {name} not found")


def convert_mcp_to_langgraph(*tool_classes) -> List[Callable]:
    """
    Convenience function to convert MCP tool classes to LangGraph functions
    
    Usage:
        from generated_tools.weather_tool import WeatherTool
        tools = convert_mcp_to_langgraph(WeatherTool)
    """
    adapter = LangGraphAdapter()
    
    for tool_class in tool_classes:
        adapter.register_mcp_tool(tool_class)
    
    return adapter.get_langgraph_tools() 