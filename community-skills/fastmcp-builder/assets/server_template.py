#!/usr/bin/env python3
"""
Minimal FastMCP Server Template

This template provides a basic FastMCP server structure with examples of:
- Tools (functions that agents can call)
- Resources (dynamic data sources)
- Prompts (reusable prompt templates)
"""

import os
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("my-server")

# Environment variables for API keys (if needed)
# API_KEY = os.getenv("MY_API_KEY")


# ============================================================================
# TOOLS - Functions that agents can call to perform actions
# ============================================================================

@mcp.tool()
async def greet(name: str) -> str:
    """
    Greet a user by name.

    Args:
        name: The name of the person to greet

    Returns:
        A personalized greeting message
    """
    return f"Hello, {name}! Welcome to FastMCP."


# ============================================================================
# RESOURCES - Dynamic data sources that provide context
# ============================================================================

@mcp.resource("info://server/status")
def server_status() -> str:
    """
    Provide current server status information.

    Returns:
        Server status as formatted text
    """
    return "Server Status: Running\nVersion: 1.0.0\nTools Available: 1"


# ============================================================================
# PROMPTS - Reusable prompt templates with dynamic arguments
# ============================================================================

@mcp.prompt()
def help_prompt() -> str:
    """
    Generate a help message explaining server capabilities.

    Returns:
        Formatted help text
    """
    return """This server provides the following capabilities:

Tools:
- greet(name): Greet a user by name

Resources:
- info://server/status: View server status

Use these tools to interact with the server."""


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    # Run the server using stdio transport (for Claude Desktop)
    mcp.run()
