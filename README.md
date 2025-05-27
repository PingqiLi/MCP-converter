# API-to-MCP Transformation Tool v0.3.0

🤖 **LLM-Powered API Analysis** - Convert any API into MCP (Model Context Protocol) compatible modules using intelligent documentation analysis. This tool automates the process of generating new MCP tools from comprehensive API documentation, leveraging LLM capabilities for accurate parameter extraction and tool generation.

---

## 🚀 Quick Start (Simplified Workflow)

### 1. **Environment Setup**
Set your LLM API key (required - choose one):
```bash
# OpenAI (recommended)
export OPENAI_API_KEY="your_openai_api_key"

# OR Anthropic Claude
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# OR Google Gemini
export GOOGLE_API_KEY="your_google_api_key"

# OR Mistral AI
export MISTRAL_API_KEY="your_mistral_api_key"

# OR Perplexity Sonar
export PERPLEXITY_API_KEY="your_perplexity_api_key"
```

Install dependencies:
```bash
# Option 1: Use the interactive installation script (recommended)
python install.py

# Option 2: Manual installation
# Install core dependencies
pip install -r requirements.txt

# Optional: Install LangGraph support (if needed)
pip install -r requirements-langgraph.txt

# Or install specific LLM providers only:
pip install openai                    # For OpenAI
pip install anthropic                 # For Anthropic
pip install google-generativeai       # For Google Gemini
pip install mistralai                 # For Mistral AI
# Note: Perplexity uses OpenAI-compatible API, so just install openai
```

### 2. **Generate a Tool with One Command**
```bash
python main.py generate-tool \
  --name WeatherTool \
  --api-documentation "OpenWeatherMap API: Get current weather data. Base URL: https://api.openweathermap.org/data/2.5/weather. Parameters: q (city name), appid (API key). Returns JSON with temperature, humidity, weather description."
```

### 3. **Use Your Generated Tool**
```python
from generated_tools.weathertool.wrapper import run_weathertool
result = run_weathertool(q="London", appid="your_api_key")
print(result)
```

---

## 💡 Key Features (v0.3.0)

### ✨ **Simplified Workflow**
- **Single input**: API documentation only (text or file)
- **LLM-powered**: Intelligent analysis of any API documentation
- **One command**: Generate complete MCP tools instantly
- **Clean architecture**: Modular provider system with automatic fallback

### 🎯 **Enhanced Accuracy**
- **Smart parameter extraction**: LLM understands complex API docs
- **Authentication detection**: Automatically identifies auth methods
- **Response modeling**: Creates accurate data structures
- **High confidence**: 95%+ accuracy with comprehensive docs

### 🔧 **Complete Tool Generation**
- **MCP-compatible**: Full Model Context Protocol support
- **LangGraph ready**: Automatic conversion for AI agents
- **MCP server**: Built-in server for tool hosting
- **Rich metadata**: Detailed tool information and configuration

---

## 📖 Usage Examples

### Example 1: Weather API
```bash
python main.py generate-tool \
  --name WeatherTool \
  --api-documentation "OpenWeatherMap Current Weather API. Base URL: https://api.openweathermap.org/data/2.5/weather. Authentication: API key as 'appid' parameter. Parameters: q (city), units (metric/imperial). Returns JSON with temperature, humidity, weather conditions."
```

### Example 2: News API
```bash
python main.py generate-tool \
  --name NewsTool \
  --api-documentation "NewsAPI Everything Endpoint. URL: https://newsapi.org/v2/everything. Authentication: X-API-Key header. Parameters: q (query), sources, language, sortBy, pageSize. Returns articles array with title, description, url."
```

### Example 3: From Documentation File
```bash
python main.py generate-tool \
  --name GitHubTool \
  --api-documentation scripts/github_api_docs.txt
```

---

## 🤖 LLM Configuration

The tool uses external configuration for prompts and models:

**`config/llm_prompts.json`**:
```json
{
  "api_analysis_prompt": {
    "system_message": "You are an expert API analyst...",
    "user_prompt_template": "Analyze the following API documentation..."
  },
  "models": {
    "openai": {"model": "gpt-3.5-turbo", "temperature": 0.1},
    "anthropic": {"model": "claude-3-haiku-20240307", "temperature": 0.1}
  }
}
```

---

## 📁 Generated Tool Structure

```
generated_tools/
├── tool_registry.json           # Central registry
└── yourtool/
    ├── tool.py                  # Main MCP tool class
    ├── wrapper.py               # Function wrapper
    └── metadata.json            # Tool metadata
```

### Enhanced Metadata
```json
{
  "name": "WeatherTool",
  "parsing_info": {
    "method": "llm",
    "confidence_score": 0.95,
    "llm_provider": "openai"
  },
  "api_info": {
    "api_name": "OpenWeatherMap API",
    "base_url": "https://api.openweathermap.org/data/2.5/weather",
    "authentication": {"type": "api_key", "location": "query"}
  }
}
```

---

## 🔧 Advanced Features

### MCP Server Integration
```python
# Start MCP server with generated tools
from src.mcp_server import MCPServer
server = MCPServer()
server.start()  # Serves all tools in generated_tools/
```

### LangGraph Compatibility
```python
# Convert MCP tools to LangGraph functions
from src.langgraph_adapter import LangGraphAdapter
adapter = LangGraphAdapter()
langgraph_tools = adapter.convert_all_tools()
```

### Tool Registry Management
```python
# Access tool registry
from src.tool_registry import ToolRegistry
registry = ToolRegistry()
tools = registry.list_tools()
```

---

## 📊 Migration from v0.2.0

### What Changed
- ❌ **Removed**: `--usage-code`, `--context`, `--no-llm` arguments
- ❌ **Removed**: Rule-based parsing fallback (400+ lines)
- ✅ **Added**: Single `--api-documentation` input
- ✅ **Added**: External LLM prompt configuration
- ✅ **Added**: Enhanced metadata and confidence scoring

### Migration Guide
**Old (v0.2.0)**:
```bash
python main.py generate-tool \
  --name WeatherTool \
  --api-description weather.txt \
  --usage-code usage.py \
  --context "Additional notes"
```

**New (v0.3.0)**:
```bash
python main.py generate-tool \
  --name WeatherTool \
  --api-documentation "Complete API documentation here..."
```

---

## 🚨 Requirements & Error Handling

### Required Environment
- **LLM API Key**: OpenAI, Anthropic, Google Gemini, Perplexity Sonar, or Mistral AI (mandatory)
- **Python 3.8+**: Modern Python version
- **Dependencies**: Corresponding provider package (`openai`, `anthropic`, `google-generativeai`, or `mistralai`)

### Common Errors
```bash
# No API key
❌ No LLM API key found! Set OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, PERPLEXITY_API_KEY, or MISTRAL_API_KEY

# Empty documentation
❌ API documentation cannot be empty

# Missing dependencies
❌ Google Generative AI library not installed. Install with: pip install google-generativeai

# API quota exceeded
❌ LLM parsing failed: API quota exceeded
```

---

## 📚 Documentation

- **[Simplified Workflow Guide](docs/SIMPLIFIED_WORKFLOW_GUIDE.md)** - Complete usage guide
- **[LLM Provider Support](docs/LLM_PROVIDERS.md)** - Comprehensive guide to all supported LLM providers
- **[LLM Configuration](config/llm_prompts.json)** - Prompt customization
- **[Tool Registry](generated_tools/tool_registry.json)** - Generated tools index

---

## 🎯 Project Structure

```
api-to-mcp-converter/
├── main.py                      # CLI entry point
├── config/
│   └── llm_prompts.json        # LLM configuration
├── src/
│   ├── input_parser.py         # LLM-powered API analysis
│   ├── tool_generator.py       # Tool generation pipeline
│   ├── mcp_server.py          # MCP server implementation
│   └── langgraph_adapter.py   # LangGraph integration
├── generated_tools/            # Generated MCP tools
│   ├── tool_registry.json     # Central tool registry
│   └── [toolname]/            # Individual tool directories
└── docs/                      # Documentation
```

---

## 🔮 Future Enhancements

- **Specialized prompts** for different API types (REST, GraphQL, gRPC)
- **Batch processing** for multiple APIs
- **Integration templates** for common frameworks
- **Automatic testing** of generated tools
- **Advanced error handling** and retry mechanisms

---

## 📄 License

MIT - See LICENSE file for details.

---

**🚀 The simplified workflow makes API-to-MCP tool generation fast, accurate, and reliable. One input, one command, one great result!** 