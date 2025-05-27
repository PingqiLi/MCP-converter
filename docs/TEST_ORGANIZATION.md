# Test Organization

This document explains the organized test structure for the API-to-MCP Transformation Tool.

## 📁 Test Directory Structure

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

## 🔧 Test Categories

### Unit Tests (`tests/ut/`)

**Purpose**: Test individual components in isolation with minimal dependencies.

**Characteristics**:
- Fast execution
- No external dependencies (APIs, files, etc.)
- Mock external services when needed
- Focus on single module functionality
- Can run without LLM API keys (for most tests)

**Test Types**:
- Component functionality validation
- Input/output validation
- Error handling verification
- Edge case testing
- Mock-based testing for external dependencies

**Examples**:
- `test_sandbox.py`: Tests code execution in isolation
- `test_normalizer.py`: Tests data format conversion
- `test_validator.py`: Tests MCP schema validation
- `test_mcp_tool.py`: Tests base class functionality

### System Tests (`tests/st/`)

**Purpose**: Test end-to-end workflows and integration between components.

**Characteristics**:
- Slower execution
- May require external dependencies (LLM API keys)
- Test complete workflows
- Integration between multiple components
- Real API interactions when possible

**Test Types**:
- End-to-end workflow testing
- Component integration testing
- MCP server functionality
- LangGraph adapter testing
- Real API interaction testing

**Examples**:
- `test_simplified_workflow.py`: Complete tool generation workflow
- `test_integration.py`: MCP server and LangGraph integration

## 🚀 Running Tests

### Command Options

```bash
# Run all tests (unit + system)
python run_tests.py --type all

# Run only unit tests (fast, no LLM required)
python run_tests.py --type ut
python run_tests.py --type unit

# Run only system tests (requires LLM API key)
python run_tests.py --type st
python run_tests.py --type system

# Legacy support for specific tests
python run_tests.py --type integration
python run_tests.py --type simplified

# List available test types
python run_tests.py --list
```

### Test Execution Flow

1. **Development Phase**: Run unit tests frequently
   ```bash
   python run_tests.py --type ut
   ```

2. **Integration Phase**: Run system tests before commits
   ```bash
   python run_tests.py --type st
   ```

3. **Release Phase**: Run all tests
   ```bash
   python run_tests.py --type all
   ```

## 📊 Test Dependencies

### Unit Tests Requirements
- ✅ No external API keys required (for most tests)
- ✅ Fast execution (< 5 seconds)
- ✅ Minimal setup required
- ⚠️ Some tests may require LLM keys due to simplified workflow

### System Tests Requirements
- 🔑 **LLM API Key Required**: Set one of:
  - `OPENAI_API_KEY` (recommended)
  - `ANTHROPIC_API_KEY`
- ⏱️ Slower execution (may take 1-2 minutes)
- 🌐 Internet connection required
- 📁 May create temporary files/directories

## 🎯 Test Strategy Benefits

### 1. **Clear Separation**
- Unit tests focus on individual components
- System tests focus on integration and workflows
- Easy to identify which tests to run during development

### 2. **Faster Development**
- Run unit tests quickly during development
- Run system tests only when needed
- Parallel execution possible

### 3. **Better CI/CD**
- Unit tests can run in basic environments
- System tests can run in environments with API keys
- Different test stages for different purposes

### 4. **Easier Debugging**
- Unit test failures point to specific components
- System test failures indicate integration issues
- Clear test scope and purpose

## 🔄 Adding New Tests

### For Unit Tests (`tests/ut/`)
1. Create test file: `test_[component_name].py`
2. Test single component functionality
3. Use mocks for external dependencies
4. Ensure fast execution
5. Add to unit test suite

### For System Tests (`tests/st/`)
1. Create test file: `test_[workflow_name].py`
2. Test end-to-end functionality
3. Use real dependencies when possible
4. Document any special requirements
5. Add to system test suite

## 📝 Test Naming Conventions

- **File naming**: `test_[component/workflow].py`
- **Class naming**: `Test[ComponentName]` or `Test[WorkflowName]`
- **Method naming**: `test_[specific_functionality]`
- **Descriptive docstrings**: Explain what the test validates

## 🛠️ Test Utilities

Both test directories include `__init__.py` files that can contain:
- Common test utilities
- Shared fixtures
- Test configuration
- Helper functions

This organized structure provides clear separation between different types of tests, making the codebase more maintainable and the testing process more efficient. 