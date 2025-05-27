# LLM Provider Support

The API-to-MCP Transformation Tool supports multiple LLM providers for intelligent API documentation analysis. This document provides detailed information about each supported provider.

## Supported Providers

### 1. OpenAI (Recommended)
- **Model**: `gpt-4o-mini`
- **API Key**: `OPENAI_API_KEY`
- **Installation**: `pip install openai`
- **Strengths**: Excellent JSON parsing, consistent output format
- **Best for**: Production use, reliable results

**Setup:**
```bash
export OPENAI_API_KEY="your_openai_api_key"
pip install openai
```

### 2. Anthropic Claude
- **Model**: `claude-3-haiku-20240307`
- **API Key**: `ANTHROPIC_API_KEY`
- **Installation**: `pip install anthropic`
- **Strengths**: Strong reasoning, detailed analysis
- **Best for**: Complex API documentation, nuanced understanding

**Setup:**
```bash
export ANTHROPIC_API_KEY="your_anthropic_api_key"
pip install anthropic
```

### 3. Google Gemini
- **Model**: `gemini-1.5-flash`
- **API Key**: `GOOGLE_API_KEY`
- **Installation**: `pip install google-generativeai`
- **Strengths**: Fast processing, good parameter extraction
- **Best for**: Quick analysis, cost-effective processing

**Setup:**
```bash
export GOOGLE_API_KEY="your_google_api_key"
pip install google-generativeai
```

### 4. Mistral AI
- **Model**: `mistral-large-latest`
- **API Key**: `MISTRAL_API_KEY`
- **Installation**: `pip install mistralai`
- **Strengths**: European provider, good multilingual support
- **Best for**: Privacy-conscious users, European compliance

**Setup:**
```bash
export MISTRAL_API_KEY="your_mistral_api_key"
pip install mistralai
```

### 5. Perplexity Sonar
- **Model**: `llama-3.1-sonar-large-128k-online`
- **API Key**: `PERPLEXITY_API_KEY`
- **Installation**: `pip install openai` (uses OpenAI-compatible API)
- **Strengths**: Real-time web search, up-to-date information
- **Best for**: APIs requiring current information, research-backed analysis

**Setup:**
```bash
export PERPLEXITY_API_KEY="your_perplexity_api_key"
pip install openai
```

## Provider Selection Priority

The tool automatically selects the first available provider in this order:
1. OpenAI (if `OPENAI_API_KEY` is set)
2. Anthropic (if `ANTHROPIC_API_KEY` is set)
3. Google Gemini (if `GOOGLE_API_KEY` is set)
4. Perplexity Sonar (if `PERPLEXITY_API_KEY` is set)
5. Mistral AI (if `MISTRAL_API_KEY` is set)

## Configuration

All providers use the same configuration structure in `config/llm_prompts.json`:

```json
{
  "models": {
    "openai": {
      "model": "gpt-4o-mini",
      "temperature": 0.1,
      "max_tokens": 4000
    },
    "anthropic": {
      "model": "claude-3-haiku-20240307",
      "temperature": 0.1,
      "max_tokens": 4000
    },
    "google": {
      "model": "gemini-1.5-flash",
      "temperature": 0.1,
      "max_tokens": 4000
    },
    "mistral": {
      "model": "mistral-large-latest",
      "temperature": 0.1,
      "max_tokens": 4000
    },
    "perplexity": {
      "model": "llama-3.1-sonar-large-128k-online",
      "temperature": 0.1,
      "max_tokens": 4000
    }
  }
}
```

## Error Handling

Each provider has specific error handling:

### OpenAI Errors
- Rate limiting: Automatic retry with exponential backoff
- Invalid API key: Clear error message with setup instructions
- Model not found: Falls back to available model

### Anthropic Errors
- Rate limiting: Detailed quota information
- Content policy: Specific policy violation details
- API errors: Structured error responses

### Google Gemini Errors
- Safety filters: Detailed safety feedback
- Quota exceeded: Clear quota limit information
- Blocked content: Specific blocking reasons

### Mistral Errors
- Authentication: Clear API key validation
- Rate limits: Detailed limit information
- Model availability: Alternative model suggestions

### Perplexity Errors
- Rate limiting: Quota and rate limit detection
- Authentication: API key validation
- Search failures: Web search timeout or blocking

## Performance Comparison

| Provider | Speed | Cost | Accuracy | JSON Quality | Special Features |
|----------|-------|------|----------|--------------|------------------|
| OpenAI   | Fast  | Medium | High | Excellent | Reliable, consistent |
| Anthropic| Medium| High | Very High | Excellent | Best reasoning |
| Google   | Very Fast | Low | High | Good | Cost-effective |
| Perplexity| Medium | Medium | Very High | Good | Real-time web data |
| Mistral  | Fast  | Medium | High | Good | EU compliance |

## Best Practices

### For Production Use
- Use OpenAI for consistent, reliable results
- Set up multiple providers as fallbacks
- Monitor API usage and costs

### For Development
- Use Google Gemini for fast iteration
- Switch providers to test consistency
- Use Anthropic for complex documentation

### For Cost Optimization
- Start with Google Gemini (lowest cost)
- Use OpenAI for final production tools
- Monitor token usage across providers

## Troubleshooting

### Common Issues

1. **No API Key Found**
   ```bash
   ❌ No LLM API key found! Set OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, or MISTRAL_API_KEY
   ```
   **Solution**: Set at least one API key environment variable

2. **Import Error**
   ```bash
   ❌ Google Generative AI library not installed. Install with: pip install google-generativeai
   ```
   **Solution**: Install the required provider library

3. **API Quota Exceeded**
   ```bash
   ❌ LLM parsing failed: API quota exceeded
   ```
   **Solution**: Check your API usage limits or switch providers

4. **Safety Filter Triggered (Gemini)**
   ```bash
   ❌ Google Gemini safety filter triggered
   ```
   **Solution**: Rephrase the API documentation or use a different provider

### Testing Provider Setup

Use the included test scripts to verify your setup:

```bash
# Test all providers comprehensively
python test_providers.py

# Test specific provider (legacy)
python test_gemini.py

# Quick setup verification
python -c "from src.input_parser import InputParser; print('✅ Setup successful')"
```

## Advanced Configuration

### Custom Models

You can modify the model configuration in `config/llm_prompts.json`:

```json
{
  "models": {
    "openai": {
      "model": "gpt-4",  // Use GPT-4 for higher accuracy
      "temperature": 0.05,  // Lower temperature for more consistent output
      "max_tokens": 6000    // Higher token limit for complex APIs
    }
  }
}
```

### Custom Prompts

The system prompt and user prompt template can be customized for specific use cases:

```json
{
  "api_analysis_prompt": {
    "system_message": "Your custom system message...",
    "user_prompt_template": "Your custom template with {api_documentation}..."
  }
}
```

## Future Enhancements

- **Provider-specific optimizations**: Tailored prompts for each provider
- **Automatic fallback**: Switch providers on failure
- **Cost tracking**: Monitor usage across providers
- **Performance benchmarking**: Compare provider accuracy
- **Custom model support**: Support for fine-tuned models 