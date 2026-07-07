from typing import Any, Dict

from handlers import call_build_incident_timeline, call_generate_5_whys_questions
from tools_schema import ALL_TOOLS


class RcaMcpServer:
    """Minimal MCP-like server facade for RCA tools.

    Wire this into your actual MCP transport (stdio/WebSocket/HTTP) according to the
    Python MCP SDK or your own implementation.
    """

    def __init__(self, llm: object | None = None):
        self.llm = llm

    def list_tools(self) -> Dict[str, Any]:
        """Return the tool list and schemas (for tools/list)."""
        return {"tools": ALL_TOOLS}

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch a tool call (for tools/call)."""
        if name == "build_incident_timeline":
            data = call_build_incident_timeline(arguments)
            return {
                "content": [
                    {
                        "type": "structured",
                        "data": data,
                    }
                ]
            }

        if name == "generate_5_whys_questions":
            data = call_generate_5_whys_questions(arguments)
            return {
                "content": [
                    {
                        "type": "structured",
                        "data": data,
                    }
                ]
            }

        return {
            "isError": True,
            "content": [
                {
                    "type": "text",
                    "text": f"Unknown tool: {name}",
                }
            ],
        }
