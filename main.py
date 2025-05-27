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

from src.tool_generator import ToolGenerator


def generate_tool_command(args):
    """Handle the generate-tool command"""
    print("🚀 Generating tool: {}".format(args.name))
    print("📝 Using LLM-powered API analysis...")
    
    # Handle API documentation input - either file or direct text
    api_documentation = ""
    
    if args.api_documentation:
        if os.path.exists(args.api_documentation):
            print("📖 Reading API documentation from file: {}".format(args.api_documentation))
            with open(args.api_documentation, 'r', encoding='utf-8') as f:
                api_documentation = f.read()
        else:
            # Treat as direct text input
            api_documentation = args.api_documentation
            print("📝 Using provided API documentation text")
    else:
        raise ValueError("API documentation is required (either file path or text)")
    
    if not api_documentation.strip():
        raise ValueError("API documentation cannot be empty")
    
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


def main():
    parser = argparse.ArgumentParser(
        description="API-to-MCP Transformation Tool: Convert any API into MCP-compatible modules using LLM-powered analysis."
    )
    parser.add_argument('--version', action='version', version='API-to-MCP Tool 0.3.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # generate-tool subcommand
    generate_parser = subparsers.add_parser(
        'generate-tool',
        help='Generate a new MCP tool from API documentation using LLM analysis'
    )
    generate_parser.add_argument(
        '--name',
        required=True,
        help='Name for the new tool (e.g., WeatherTool, FlightTool)'
    )
    generate_parser.add_argument(
        '--api-documentation',
        required=True,
        help='API documentation (file path or direct text). Comprehensive API description for LLM analysis.'
    )
    generate_parser.add_argument(
        '--output-dir',
        default='generated_tools',
        help='Output directory for generated tools (default: generated_tools)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'generate-tool':
        return generate_tool_command(args)
    else:
        parser.print_help()
        print("\n" + "="*60)
        print("🤖 LLM-Powered API-to-MCP Tool v0.3.0")
        print("="*60)
        print("💡 Features:")
        print("  📝 Converts API documentation into working MCP tools")
        print("  🧠 Uses LLM for intelligent API analysis")
        print("  🔧 Generates complete tool with validation & docs")
        print("  📋 Supports both file paths and direct text input")
        print("\n🔑 Required:")
        print("  Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        print("\n📖 Example:")
        print('  python main.py generate-tool --name WeatherTool \\')
        print('    --api-documentation "OpenWeatherMap API provides..."')
        print("="*60)
        return 0


if __name__ == "__main__":
    sys.exit(main()) 