#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installation script for MCP-converter
Helps users install the correct dependencies based on their needs.
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 MCP-converter Installation Script")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Warning: Not in a virtual environment")
        response = input("Continue anyway? (y/N): ").lower()
        if response != 'y':
            print("Please create and activate a virtual environment first:")
            print("  python -m venv venv")
            print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
            return
    
    print("\nSelect installation type:")
    print("1. Core only (basic functionality)")
    print("2. Core + LangGraph (full functionality)")
    print("3. Core + specific LLM providers")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n📦 Installing core dependencies...")
        success = run_command("pip install -r requirements.txt")
        
    elif choice == "2":
        print("\n📦 Installing core dependencies...")
        success1 = run_command("pip install -r requirements.txt")
        print("\n📦 Installing LangGraph dependencies...")
        success2 = run_command("pip install -r requirements-langgraph.txt")
        success = success1 and success2
        
    elif choice == "3":
        print("\n📦 Installing core dependencies...")
        success = run_command("pip install -r requirements.txt")
        
        if success:
            print("\nSelect LLM providers to install:")
            print("1. OpenAI")
            print("2. Anthropic")
            print("3. Google Gemini")
            print("4. Mistral AI")
            print("5. All providers")
            
            provider_choice = input("Enter your choice (1-5): ").strip()
            
            providers = {
                "1": "openai",
                "2": "anthropic",
                "3": "google-generativeai",
                "4": "mistralai",
                "5": "openai anthropic google-generativeai mistralai"
            }
            
            if provider_choice in providers:
                print(f"\n📦 Installing {providers[provider_choice]}...")
                success = run_command(f"pip install {providers[provider_choice]}")
    else:
        print("❌ Invalid choice")
        return
    
    if success:
        print("\n🎉 Installation completed successfully!")
        print("\nNext steps:")
        print("1. Set your API key(s):")
        print("   export OPENAI_API_KEY='your_key'")
        print("   export ANTHROPIC_API_KEY='your_key'")
        print("   export GOOGLE_API_KEY='your_key'")
        print("   export MISTRAL_API_KEY='your_key'")
        print("   export PERPLEXITY_API_KEY='your_key'")
        print("\n2. Test the installation:")
        print("   python main.py --help")
        print("\n3. Generate your first tool:")
        print("   python main.py generate-tool --name TestTool --api-documentation 'Your API docs here'")
    else:
        print("\n❌ Installation failed. Please check the errors above.")

if __name__ == "__main__":
    main() 