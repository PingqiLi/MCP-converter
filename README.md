# API-to-MCP Transformation Tool v0.3.0

🤖 **LLM-Powered API Analysis** - Convert any API into MCP (Model Context Protocol) compatible modules using intelligent documentation analysis. This tool automates the process of generating new MCP tools from comprehensive API documentation, leveraging LLM capabilities for accurate parameter extraction and tool generation.

---

## 🚀 Quick Start

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
pip install -r requirements.txt
```

### 2. **Generate a Tool with One Command**
```bash
python main.py \
  --name WeatherTool \
  --api-docs "OpenWeatherMap API: Get current weather data. Base URL: https://api.openweathermap.org/data/2.5/weather. Parameters: q (city name), appid (API key). Returns JSON with temperature, humidity, weather description."
```

### 3. **Use Your Generated Tool**
```python
from generated_tools.weathertool.wrapper import run_weathertool
result = run_weathertool(q="London", appid="your_api_key")
print(result)
```

---

## 💡 Key Features

### ✨ **Simplified Workflow**
- **Single input**: API documentation only (text or file)
- **LLM-powered**: Intelligent analysis of any API documentation
- **One command**: Generate complete MCP tools instantly
- **Clean architecture**: Modular package structure with clear separation

### 🎯 **Enhanced Accuracy**
- **Smart parameter extraction**: LLM understands complex API docs
- **Authentication detection**: Automatically identifies auth methods
- **Response modeling**: Creates accurate data structures
- **High confidence**: 95%+ accuracy with comprehensive docs

### 🔧 **Complete Tool Generation**
- **MCP-compatible**: Full Model Context Protocol support
- **Rich metadata**: Detailed tool information and configuration
- **Clean structure**: Organized codebase with proper package hierarchy

---

## 📖 Usage Examples

### Example 1: Weather API
```bash
python main.py \
  --name WeatherTool \
  --api-docs "OpenWeatherMap Current Weather API. Base URL: https://api.openweathermap.org/data/2.5/weather. Authentication: API key as 'appid' parameter. Parameters: q (city), units (metric/imperial). Returns JSON with temperature, humidity, weather conditions."
```

### Example 2: News API
```bash
python main.py \
  --name NewsTool \
  --api-docs "NewsAPI Everything Endpoint. URL: https://newsapi.org/v2/everything. Authentication: X-API-Key header. Parameters: q (query), sources, language, sortBy, pageSize. Returns articles array with title, description, url."
```

### Example 3: From Documentation File
```bash
python main.py \
  --name GitHubTool \
  --api-docs examples/github_api_docs.txt
```

---

## 📁 Project Structure

```
src/
├── core/                        # Core functionality
│   ├── tool_generator.py        # Main orchestrator
│   ├── mcp_tool.py              # Base MCP tool class
│   └── apiclient.py             # Base API client class
├── llm/                         # LLM providers and parsing
│   └── input_parser.py          # LLM-powered API analysis
├── generators/                  # Code generation
│   └── output_generator.py      # Tool and wrapper generation
├── utils/                       # Utility functions
│   ├── normalizer.py            # Data normalization
│   ├── validator.py             # Input validation
│   ├── field_mapper.py          # Field mapping
│   └── sandbox.py               # Safe code execution
└── server/                      # Server components
    ├── mcp_server.py            # MCP protocol server
    └── langgraph_adapter.py     # LangGraph integration
```

### Generated Tool Structure

```
generated_tools/
├── tool_registry.json           # Central registry
└── yourtool/
    ├── tool.py                  # Main MCP tool class
    ├── wrapper.py               # Function wrapper
    └── metadata.json            # Tool metadata
```

---

## 🤖 LLM Configuration

The tool uses external configuration for prompts and models in `config/llm_prompts.json`:

```json
{
  "api_analysis_prompt": {
    "system_message": "You are an expert API analyst...",
    "user_prompt_template": "Analyze the following API documentation..."
  },
  "models": {
    "openai": {"model": "gpt-4o-mini", "temperature": 0.1},
    "anthropic": {"model": "claude-3-haiku-20240307", "temperature": 0.1}
  }
}
```

---

## 🔧 Advanced Features

### MCP Server Integration
```python
# Start MCP server with generated tools
from src.server.mcp_server import MCPServer
server = MCPServer()
server.discover_tools()  # Load all tools from generated_tools/
```

### LangGraph Compatibility
```python
# Convert MCP tools to LangGraph functions
from src.server.langgraph_adapter import LangGraphAdapter
adapter = LangGraphAdapter()
langgraph_tools = adapter.convert_all_tools()
```

---

## 📊 What's New in v0.3.0

### ✅ **Simplified**
- **Removed**: Non-conventional `install.py` script
- **Removed**: Subparser complexity - direct command interface
- **Removed**: Redundant dependencies and files
- **Added**: Clean package structure with logical organization

### 🏗️ **Better Architecture**
- **Core**: Main functionality (`tool_generator`, `mcp_tool`, `apiclient`)
- **LLM**: AI providers and parsing (`input_parser`)
- **Generators**: Code generation utilities (`output_generator`)
- **Utils**: Data processing (`normalizer`, `validator`, `field_mapper`, `sandbox`)
- **Server**: MCP server and adapters (`mcp_server`, `langgraph_adapter`)

### 📦 **Minimal Dependencies**
```txt
# Core dependencies only
requests>=2.25.0
PyYAML>=6.0.0

# LLM providers (install at least one)
openai>=1.0.0
anthropic>=0.18.0
google-generativeai>=0.3.0
mistralai>=0.1.0
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the new package structure
4. Test with `python main.py --help`
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details. 