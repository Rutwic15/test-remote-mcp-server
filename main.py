import random
import json
from fastmcp import FastMCP

mcp = FastMCP(name="Simple Calculator Server")

@mcp.tool()
def add_numbers(a:int, b:int) -> int:
    "Add two numbers"
    return a+b

## Generate random number
@mcp.tool()
def generate_random(min_val:int = 1, max_val:int = 100) -> int:
    """Generate a random within a range"""
    return random.randint(min_val,max_val)


## Resource: Server Info
@mcp.resource("info://server")
def server_info() -> str:
    """Get info about the server"""
    info = {
        "name": "A simple calculator server",
        "Version": "1.0.0",
        "description": "A basic MCP server with math tools",
        "tools": ["add_numbers", "generate_random"],
        "author": "Achanti Rutwick"
    }
    return json.dumps(info, indent=2)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
