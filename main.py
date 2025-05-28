#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API-to-MCP Transformation Tool
Convert any API into MCP-compatible modules using LLM-powered analysis.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.tool_generator import ToolGenerator


def main():
    parser = argparse.ArgumentParser(
        description="API-to-MCP Transformation Tool: Convert any API into MCP-compatible modules using LLM-powered analysis.",
        epilog="""
Examples:
  python main.py --name WeatherTool --api-docs "OpenWeatherMap API provides..."
  python main.py --name FlightTool --api-docs ./api_docs.txt
        """
    )
    
    parser.add_argument('--version', action='version', version='API-to-MCP Tool 0.3.0')
    
    parser.add_argument(
        '--name',
        required=True,
        help='Name for the new tool (e.g., WeatherTool, FlightTool)'
    )
    
    parser.add_argument(
        '--api-docs',
        required=True,
        help='API documentation (file path or direct text). Comprehensive API description for LLM analysis.'
    )
    
    parser.add_argument(
        '--output-dir',
        default='generated_tools',
        help='Output directory for generated tools (default: generated_tools)'
    )
    
    args = parser.parse_args()
    
    print("🚀 Generating tool: {}".format(args.name))
    print("📝 Using LLM-powered API analysis...")
    
    # Handle API documentation input - either file or direct text
    api_documentation = ""
    
    if os.path.exists(args.api_docs):
        print("📖 Reading API documentation from file: {}".format(args.api_docs))
        with open(args.api_docs, 'r', encoding='utf-8') as f:
            api_documentation = f.read()
    else:
        # Treat as direct text input
        api_documentation = args.api_docs
        print("📝 Using provided API documentation text")
    
    if not api_documentation.strip():
        print("❌ Error: API documentation cannot be empty")
        return 1
    
    try:
        generator = ToolGenerator()
        generator.generate_tool_from_documentation(
            name=args.name,
            api_documentation=api_documentation,
            output_dir=args.output_dir
        )
        print("✅ Tool '{}' generated successfully!".format(args.name))
        print("📁 Location: {}/{}/".format(args.output_dir, args.name.lower()))
        return 0
    except Exception as e:
        print("❌ Error generating tool: {}".format(e))
        return 1


if __name__ == "__main__":
    sys.exit(main()) 