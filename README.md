# RCA MCP Tools (Python)

This package defines two MCP-style tools for streamlining incident RCAs:

- `build_incident_timeline`: Fetches data from SIM, Jira, and observability backends,
  normalizes events, and generates an incident timeline + narrative via an LLM.
- `generate_5_whys_questions`: Prepares structured context and task instructions for
  a unified 5 Whys table based on the incident problem statement and timeline.

The code is LLM-agnostic. Implement `LLMClient` for your provider (Anthropic, OpenAI,
local models, etc.), then wire `server.py` into your MCP transport.

The MCP server returns structured tool output, so clients can read `structuredContent`
directly instead of parsing JSON from a text block.

## Files

- `llm_interface.py`: Abstract LLM client interface.
- `prompts.py`: System prompts used for the two tools.
- `tools_schema.py`: JSON Schema definitions for the MCP tools.
- `handlers.py`: Tool call implementations that use the LLM.
- `server.py`: MCP transport entrypoint exposing the RCA tools over stdio.
- `mcp_server.py`: Minimal server facade exposing `list_tools` and `call_tool`.

## Next steps

- Add SIM, Jira, and Logz.io clients in `handlers.py` to replace stub data.
- Integrate with a Python MCP SDK or your own transport to expose these tools to
  MCP-compatible clients (Claude Desktop, Cursor, etc.).
