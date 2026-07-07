import asyncio
import json
from typing import Any, Dict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from handlers import call_build_incident_timeline, call_generate_5_whys_questions
from tools_schema import ALL_TOOLS

server = Server("rca-tools")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name=t["name"],
            description=t["description"],
            inputSchema=t["inputSchema"],
        )
        for t in ALL_TOOLS
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    if name == "build_incident_timeline":
        result = call_build_incident_timeline(arguments)
    elif name == "generate_5_whys_questions":
        result = call_generate_5_whys_questions(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
