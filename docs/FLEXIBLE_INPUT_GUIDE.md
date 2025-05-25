# Flexible Input Guide: LLM-Enhanced API Tool Generation

The API-to-MCP Transformation Tool now supports **flexible, intelligent input parsing** that dramatically reduces the friction of creating MCP tools from APIs.

## 🚀 What's New

### Before (v0.1)
- Required formal, well-structured API description files
- Needed complete usage code files
- Manual parameter extraction

### Now (v0.2)
- ✨ **Informal descriptions**: "This weather API takes a city and returns temp/humidity"
- 🤖 **LLM-powered analysis**: Automatically extracts structure and parameters
- 🔧 **Code-only generation**: Just paste example code, get a working tool
- 📝 **Direct text input**: No need to create files for simple APIs
- 🎯 **Smart fallback**: Works without LLM using enhanced rule-based parsing

## 🔑 Setup

### Enable LLM Enhancement (Optional but Recommended)

Set one of these environment variables:

```bash
# OpenAI (recommended for accuracy)
export OPENAI_API_KEY="your_openai_key"

# Anthropic Claude (also excellent)
export ANTHROPIC_API_KEY="your_anthropic_key"

# Install dependencies
pip install openai anthropic
```

### Without LLM (Rule-based only)
The tool works without any API keys using enhanced rule-based parsing.

## 💡 Usage Examples

### 1. Informal Description Only

**What you provide:**
```bash
python main.py generate-tool \
  --name WeatherTool \
  --api-description "Simple weather API. Give it a city, get back temperature and conditions. Uses OpenWeatherMap, needs API key in 'appid' parameter."
```

**What the LLM figures out:**
- API name and description
- Parameter structure (city, appid)
- Response format (JSON with weather data)
- Authentication method (API key)

### 2. Code-Only Generation

**What you provide:**
```python
# Just paste this as --usage-code
import requests

def get_news(query: str, api_key: str, country: str = "us") -> dict:
    url = "https://newsapi.org/v2/everything"
    headers = {"X-API-Key": api_key}
    params = {"q": query, "country": country}
    return requests.get(url, headers=headers, params=params).json()
```

**What gets generated:**
- Complete MCP tool with proper schema
- Parameter validation
- Error handling
- Documentation

### 3. Mixed Informal Inputs

```bash
python main.py generate-tool \
  --name FlightTool \
  --api-description "Flight search API" \
  --usage-code "import amadeus; client = amadeus.Client(); flights = client.shopping.flight_offers_search.get(origin='NYC', destination='LAX')" \
  --context "Uses Amadeus API, requires client ID/secret, returns flight offers with prices"
```

### 4. Direct Text (No Files)

```bash
# Description as text (not file)
python main.py generate-tool \
  --name SimpleCalc \
  --api-description "Calculator API for basic math" \
  --usage-code "def add(a, b): return {'result': a + b}"
```

### 5. File-based (Legacy Support)

```bash
# Still works with files
python main.py generate-tool \
  --name WeatherTool \
  --api-description scripts/weather_description.txt \
  --usage-code scripts/weather_usage.py
```

## 🧠 How LLM Enhancement Works

### Input Analysis
The LLM analyzes whatever you provide and extracts:

```json
{
  "api_name": "OpenWeatherMap API",
  "description": "Tool for getting current weather information",
  "base_url": "https://api.openweathermap.org/data/2.5/weather",
  "parameters": {
    "city": {
      "type": "string", 
      "description": "City name to get weather for",
      "required": true
    },
    "api_key": {
      "type": "string",
      "description": "OpenWeatherMap API key", 
      "required": true
    }
  },
  "authentication": {
    "type": "api_key",
    "location": "query",
    "parameter_name": "appid"
  }
}
```

### Confidence Scoring
- **LLM parsing**: 90% confidence
- **Rule-based parsing**: 60% confidence
- **Hybrid approach**: Uses best available method

## 🎯 Best Practices

### For Best Results with LLM

1. **Be descriptive but natural**:
   ```
   ✅ "Weather API that takes city names and returns current conditions"
   ❌ "API"
   ```

2. **Include key details**:
   ```
   ✅ "Uses bearer token authentication, returns JSON with articles array"
   ❌ "News API"
   ```

3. **Mention authentication**:
   ```
   ✅ "Requires API key in header as 'X-API-Key'"
   ❌ (no auth info)
   ```

### What the LLM Understands

- **API patterns**: REST, GraphQL, WebSocket endpoints
- **Auth methods**: API keys, Bearer tokens, OAuth, Basic auth
- **Parameter types**: Query params, headers, request body
- **Response formats**: JSON, XML, plain text
- **Common APIs**: Weather, news, payments, social media, etc.

## 📊 Comparison: Before vs After

| Aspect | Before (v0.1) | After (v0.2) |
|--------|---------------|-------------|
| **Input Requirements** | Formal description file + usage file | Any combination of text/code |
| **Setup Time** | 10-15 minutes writing docs | 30 seconds pasting code |
| **API Knowledge Needed** | Full understanding required | Basic idea sufficient |
| **Documentation Quality** | Manual, error-prone | LLM-generated, comprehensive |
| **Parameter Extraction** | Manual analysis | Automatic detection |
| **Error Handling** | Basic | Enhanced with validation |

## 🔧 Advanced Usage

### Custom Context
```bash
python main.py generate-tool \
  --name CustomTool \
  --usage-code "$(cat my_api_code.py)" \
  --context "Rate limited to 1000/hour. Returns paginated results. Webhook support available."
```

### Disable LLM (Rule-based only)
```bash
python main.py generate-tool \
  --name SimpleTool \
  --api-description "Basic API description" \
  --no-llm
```

### Multiple Input Sources
```bash
python main.py generate-tool \
  --name ComprehensiveTool \
  --api-description "$(curl -s https://api.example.com/docs)" \
  --usage-code "$(cat examples/usage.py)" \
  --context "Additional notes about rate limits and authentication"
```

## 🎉 Benefits

### For Users
- **⚡ Faster**: Generate tools in seconds, not minutes
- **🎯 Easier**: No need to write formal documentation
- **🧠 Smarter**: LLM understands context and nuance
- **🔄 Flexible**: Use whatever information you have

### For Developers
- **📝 Better docs**: LLM generates comprehensive documentation
- **🔍 More accurate**: Better parameter detection and validation
- **🛡️ Safer**: Enhanced error handling and validation
- **🎨 Consistent**: Standardized output format

## 🚨 Troubleshooting

### LLM Not Working?
```bash
# Check API key
echo $OPENAI_API_KEY

# Test without LLM
python main.py generate-tool --name TestTool --api-description "Simple API" --no-llm
```

### Poor Results?
1. **Add more context**: Include authentication, response format, common use cases
2. **Provide code examples**: Even incomplete code helps immensely
3. **Use specific terminology**: "REST API", "JSON response", "Bearer token"

### Still Having Issues?
- Check the confidence score in output
- Try different LLM providers (OpenAI vs Anthropic)
- Use `--no-llm` flag for rule-based parsing
- Provide more detailed input

## 🎭 Examples in Action

### Real-World Example: Stripe Payments

**Input (30 seconds to write):**
```bash
python main.py generate-tool \
  --name StripePayments \
  --usage-code "import stripe; stripe.api_key='sk_test_...'; stripe.PaymentIntent.create(amount=2000, currency='usd')" \
  --context "Stripe payments API, amounts in cents, supports multiple currencies"
```

**Generated Tool Features:**
- ✅ Proper parameter validation (amount, currency)
- ✅ Error handling for API failures
- ✅ Type hints and documentation
- ✅ MCP-compatible interface
- ✅ LangGraph compatibility

**Time Saved:** 10+ minutes of manual tool creation

---

The enhanced API-to-MCP tool makes it trivially easy to convert any API into a working MCP tool. Just describe what you want or paste some code, and let the LLM figure out the rest! 🚀 