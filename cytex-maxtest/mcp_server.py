"""
MCP surface for cisco-aibom's mcp_detector. Code-path detection is the most
reliable trigger (python files are always scanned, unlike a hidden .mcp.json).
Static fixture — imports won't resolve at runtime, that's fine.
"""
from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from langchain_mcp_adapters.client import MultiServerMCPClient

# FastMCP server (matches "FastMCP(" and "from mcp.server.fastmcp")
app = FastMCP("cytex-maxtest")


@app.tool()
def lookup(term: str) -> str:
    return term


# Low-level MCP server (matches "Server(" + "from mcp.server import")
server = Server("cytex-maxtest")

# MCP client to multiple servers (matches "MultiServerMCPClient(" +
# "from langchain_mcp_adapters")
client = MultiServerMCPClient({
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data"],
        "transport": "stdio",
    },
    "remote": {"url": "https://mcp.example.com/sse", "transport": "sse"},
})
