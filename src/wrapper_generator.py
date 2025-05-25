import os

def generate_wrapper(tool_class, output_path):
    """
    Generate a Python wrapper module for the given MCPTool class.
    The wrapper exposes a simple function interface and includes usage documentation.
    """
    tool_name = tool_class.__name__
    wrapper_code = f'''"""
Python wrapper for {tool_name}.

Usage:
    from generated_tools.{tool_name.lower()}_wrapper import run_{tool_name.lower()}
    result = run_{tool_name.lower()}(city="London")
"""
from generated_tools.{tool_name.lower()} import {tool_name}

def run_{tool_name.lower()}(**kwargs):
    """Run the {tool_name} tool with the given parameters."""
    tool = {tool_name}()
    if not tool.validate(kwargs):
        raise ValueError("Invalid parameters for {tool_name}: {{}}".format(kwargs))
    return tool.run(kwargs)
'''
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(wrapper_code) 