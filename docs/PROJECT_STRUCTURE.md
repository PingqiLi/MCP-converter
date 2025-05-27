# Project Structure

This document outlines the organized structure of the API-to-MCP Transformation Tool project.

## 📁 Root Directory

```
api-to-mcp-converter/
├── 📄 main.py                    # CLI entry point
├── 📄 run_tests.py               # Test runner script
├── 📄 pyproject.toml             # Modern Python project configuration
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # Project documentation
├── 📄 .gitignore                 # Git ignore rules
└── 📄 __init__.py                # Python package marker
```

## 📁 Core Source Code (`src/`)

```
src/
├── 📄 tool_generator.py          # Main orchestrator class
├── 📄 input_parser.py            # LLM-powered API documentation parser
├── 📄 sandbox.py                 # Safe code execution environment
├── 📄 normalizer.py              # Response format standardization
├── 📄 field_mapper.py            # API-to-MCP field mapping
├── 📄 validator.py               # MCP schema validation
├── 📄 output_generator.py        # Tool file generation
├── 📄 wrapper_generator.py       # Wrapper class generation
├── 📄 mcp_server.py              # MCP server implementation
├── 📄 langgraph_adapter.py       # LangGraph integration
├── 📄 mcp_tool.py                # Base MCP tool class
└── 📄 apiclient.py               # Generic API client
```

## 📁 Configuration (`config/`)

```
config/
└── 📄 llm_prompts.json           # LLM prompts for API analysis
```

## 📁 Tests (`tests/`)

```
tests/
├── 📁 ut/                            # Unit Tests
│   ├── 📄 __init__.py                # Unit tests package
│   ├── 📄 test_input_parser.py       # Input parser unit tests
│   ├── 📄 test_sandbox.py            # Sandbox execution tests
│   ├── 📄 test_normalizer.py         # Response normalization tests
│   ├── 📄 test_field_mapper.py       # Field mapping tests
│   ├── 📄 test_validator.py          # Validation tests
│   ├── 📄 test_output_generator.py   # Output generation tests
│   ├── 📄 test_mcp_tool.py           # MCP tool base class tests
│   └── 📄 test_apiclient.py          # API client tests
└── 📁 st/                            # System Tests
    ├── 📄 __init__.py                # System tests package
    ├── 📄 test_simplified_workflow.py # End-to-end workflow tests
    └── 📄 test_integration.py        # MCP server & LangGraph tests
```

## 📁 Documentation (`docs/`)

```
docs/
├── 📄 PROJECT_STRUCTURE.md       # This file
└── 📄 SIMPLIFIED_WORKFLOW_GUIDE.md # Workflow documentation
```

## 📁 Examples (`examples/`)

```
examples/
├── 📄 weather_api_docs.txt       # OpenWeatherMap API documentation
├── 📄 news_api_docs.txt          # NewsAPI documentation
└── 📄 langgraph_integration.py   # LangGraph usage example
```

## 📁 Scripts (`scripts/`)

```
scripts/
├── 📄 example_prd.txt            # Example Product Requirements Document
└── 📄 prd.txt                    # Project PRD
```

## 📁 Generated Tools (`generated_tools/`)

```
generated_tools/
├── 📄 tool_registry.json         # Central tool registry
└── 📁 [tool_directories]/        # Individual tool directories
    ├── 📄 tool.py                # Main tool implementation
    ├── 📄 wrapper.py             # Tool wrapper class
    └── 📄 metadata.json          # Tool metadata
```

## 🔧 Key Design Principles

### 1. **Separation of Concerns**
- Each module has a single, well-defined responsibility
- Clear interfaces between components
- Minimal coupling between modules

### 2. **LLM-First Architecture**
- All parsing is LLM-powered for maximum accuracy
- Configurable prompts in separate configuration files
- Graceful error handling when LLM is unavailable

### 3. **Extensible Design**
- Plugin-style architecture for new API types
- Configurable field mappings
- Support for multiple LLM providers

### 4. **Testing Strategy**
- **Unit Tests (ut/)**: Individual component tests in isolation
- **System Tests (st/)**: End-to-end workflows and integration tests
- Clear separation between unit and system testing
- Organized test runner with selective execution by test type

### 5. **Modern Python Practices**
- Type hints throughout the codebase
- Modern project configuration with `pyproject.toml`
- Proper package structure
- Code formatting and linting configuration

## 🚀 Workflow Overview

1. **Input**: API documentation text
2. **Parse**: LLM analyzes and extracts key information
3. **Generate**: Create usage code from parsed data
4. **Execute**: Run code in sandboxed environment
5. **Normalize**: Convert response to standard format
6. **Map**: Map fields to MCP schema
7. **Validate**: Ensure MCP compliance
8. **Output**: Generate tool files and registry entry

## 📊 File Organization Benefits

- **Clear separation** between core logic, tests, and examples
- **Easy navigation** with logical directory structure
- **Maintainable** with focused, single-purpose modules
- **Extensible** with plugin-style architecture
- **Professional** with modern Python project standards

## 🔄 Development Workflow

1. **Make changes** to source code in `src/`
2. **Run unit tests** with `python run_tests.py --type ut`
3. **Run system tests** with `python run_tests.py --type st` (requires LLM API key)
4. **Run all tests** with `python run_tests.py --type all`
5. **Generate tools** with `python main.py generate-tool`
6. **Serve tools** via MCP server or LangGraph adapter

This structure provides a solid foundation for maintaining and extending the API-to-MCP transformation tool. 