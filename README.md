# RCA MCP Tools (Python)

This package defines two MCP-style tools for streamlining incident RCAs:

- `build_incident_timeline`: Fetches data from SIM, Jira, and observability backends,
  normalizes events, and generates an incident timeline + narrative via an LLM.
- `generate_5_whys_questions`: Generates 5 Whys starter question chains based on the
  incident problem statement and timeline.

The code is LLM-agnostic. Implement `LLMClient` for your provider (Anthropic, OpenAI,
local models, etc.), then wire `RcaMcpServer` into your MCP transport.

## Files

- `llm_interface.py`: Abstract LLM client interface.
- `prompts.py`: System prompts used for the two tools.
- `tools_schema.py`: JSON Schema definitions for the MCP tools.
- `handlers.py`: Tool call implementations that use the LLM.
- `mcp_server.py`: Minimal server facade exposing `list_tools` and `call_tool`.

## Next steps

- Add SIM, Jira, and Logz.io clients in `handlers.py` to replace stub data.
- Integrate with a Python MCP SDK or your own transport to expose these tools to
  MCP-compatible clients (Claude Desktop, Cursor, etc.).
