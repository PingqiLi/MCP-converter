# API-to-MCP Transformation Tool

Convert any API (Python or otherwise) into a format compatible with the MCP (Modular Command Platform) system. This tool automates the process of generating new MCP tools from API descriptions and usage code, supporting a wide range of response formats, and outputting standardized JSON and Python classes for MCP.

---

## 🚀 How to Generate a New MCP Tool (Step-by-Step)

### 0. **Environment Setup**
- Copy `.env.example` to `.env` and fill in your LLM/API keys (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.).
- Install dependencies in your virtual environment:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  # For FastFlightsTool or similar, also:
  pip install fast-flights
  ```

### 1. **Prepare Your API Description and Example Usage**
- Write or collect:
  - An API description (YAML, JSON, OpenAPI, or text)
  - Example usage code (Python snippet or HTTP request)

### 2. **Run the CLI to Start Tool Generation**
```bash
python main.py generate-tool --name <YourToolName> --api-description <path/to/description.txt> --usage-code <path/to/usage.py>
```
- `--name`: Your desired tool name (e.g., `WeatherTool`, `FastFlightsTool`)
- `--api-description`: Path to the API description file
- `--usage-code`: Path to the example usage code

### 3. **Follow the Interactive Prompts**
- The CLI will:
  - Parse your API description and usage code (using LLM inference)
  - Guide you through mapping API response fields to MCP-required fields
  - Validate required MCP fields
  - Confirm the tool name and output locations

### 4. **Review the Generated Tool**
- The new MCP tool will be created in `generated_tools/<your_tool_name>/tool.py`
- A wrapper will be generated in `generated_tools/<your_tool_name>/wrapper.py` for function-style usage
- Example usage:
  ```python
  from generated_tools.mycustomtool.wrapper import run_mycustomtool
  result = run_mycustomtool(param1=..., param2=...)
  print(result)
  ```

### 5. **Test Your Tool**
- A test file will be generated in `tests/test_<your_tool_name>.py`
- Run tests:
  ```bash
  .venv/bin/python -m unittest -v tests/test_<your_tool_name>.py
  ```

---

## Example: Generating a Custom Flights Tool

Suppose you want to generate a tool called `MyFlightsTool` for a new flights API:

1. Prepare your API usage code in `scripts/my_flights_usage.py` and description in `scripts/my_flights_description.txt`
2. Run:
   ```bash
   python main.py generate-tool --name MyFlightsTool --api-description scripts/my_flights_description.txt --usage-code scripts/my_flights_usage.py
   ```
3. Follow the prompts to map fields and confirm output
4. Use your tool:
   ```python
   from generated_tools.myflightstool.wrapper import run_myflightstool
   result = run_myflightstool(from_airport="JFK", to_airport="LAX", date="2025-01-01")
   print(result)
   ```
5. Run the generated test:
   ```bash
   .venv/bin/python -m unittest -v tests/test_myflightstool.py
   ```

---

## Features
- Command-line interface (CLI) for user interaction
- Parse API descriptions and example usage code
- Execute API calls in a secure, sandboxed environment
- Normalize API responses (dataclass, dict, JSON) into Python dictionaries
- Serialize normalized responses into JSON
- Map API response fields to required MCP fields (configurable/inferable mapping)
- Validate that all required MCP fields are present in the output
- Output MCP-compatible JSON files
- Generate standardized Python tool classes for each API, following a base abstraction (`MCPTool`)
- Extensible: add new API types/response formats via plugin hooks
- Example tools: WeatherTool (mock), FastFlightsTool (real API)

---

## Project Structure
- `main.py` — CLI entry point
- `src/` — Core modules (parser, sandbox, normalizer, field_mapper, validator, etc.)
- `generated_tools/` — Generated MCP tool classes and wrappers
- `tests/` — Unit and system-level tests

---

## License
MIT 