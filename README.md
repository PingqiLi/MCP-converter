# API-to-MCP Transformation Tool v0.3.0

🤖 **LLM-Powered API Analysis** - Convert any API into MCP (Model Context Protocol) compatible modules using intelligent documentation analysis. This tool automates the process of generating new MCP tools from comprehensive API documentation, leveraging LLM capabilities for accurate parameter extraction and tool generation.

**🔗 LangChain Compatible**: Generated tools work seamlessly with [LangChain's official MCP adapters](https://github.com/langchain-ai/langchain-mcp-adapters) for instant LangGraph integration.

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

#### Option A: Direct Usage
```python
from generated_tools.weathertool.wrapper import run_weathertool
result = run_weathertool(q="London", appid="your_api_key")
print(result)
```

#### Option B: With LangChain MCP Adapters
```python
# Install: pip install langchain-mcp-adapters langgraph
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# Start MCP server
# python launch_mcp_server.py --transport langchain --port 3000

client = MultiServerMCPClient({
    "generated_tools": {
        "url": "http://localhost:3000/mcp",
        "transport": "streamable_http"
    }
})

tools = await client.get_tools()
agent = create_react_agent("openai:gpt-4", tools)
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
- **LangChain ready**: Works with official LangChain MCP adapters
- **Rich metadata**: Detailed tool information and configuration
- **Clean structure**: Organized codebase with proper package hierarchy

### 🌐 **Multiple Integration Options**
- **Standalone**: Use tools directly in Python
- **MCP Server**: Host tools via MCP protocol (stdio/HTTP)
- **LangChain**: Integrate with LangGraph agents
- **Multi-framework**: Support for any framework using the interface

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

## 🔗 LangChain MCP Adapters Integration

This project generates tools that are **fully compatible** with [LangChain's official MCP adapters](https://github.com/langchain-ai/langchain-mcp-adapters). Your generated tools can be used directly in LangGraph agents and LangChain workflows.

### Quick LangChain Setup

1. **Install LangChain MCP Adapters**:
   ```bash
   pip install langchain-mcp-adapters langgraph "langchain[openai]"
   ```

2. **Start MCP Server**:
   ```bash
   # Stdio transport
   python launch_mcp_server.py
   
   # HTTP transport (recommended for LangChain)
   python launch_mcp_server.py --transport langchain --port 3000
   ```

3. **Use with LangGraph**:
   ```python
   import asyncio
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client
   from langchain_mcp_adapters.tools import load_mcp_tools
   from langgraph.prebuilt import create_react_agent
   from langchain_openai import ChatOpenAI

   async def main():
       server_params = StdioServerParameters(
           command="python", args=["launch_mcp_server.py"]
       )
       
       async with stdio_client(server_params) as (read, write):
           async with ClientSession(read, write) as session:
               await session.initialize()
               tools = await load_mcp_tools(session)
               
               model = ChatOpenAI(model="gpt-4")
               agent = create_react_agent(model=model, tools=tools)
               
               response = await agent.ainvoke({
                   "messages": [{"role": "user", "content": "Use the tools to help me"}]
               })
               print(response)

   asyncio.run(main())
   ```

📚 **Full Documentation**: See [`LANGCHAIN_MCP_INTEGRATION.md`](LANGCHAIN_MCP_INTEGRATION.md) for comprehensive examples, multi-server setup, FastMCP integration, and troubleshooting.

---

## 📁 Project Structure

```