---
name: fastmcp-builder
description: Guide for creating FastMCP-based MCP servers in Python. Use when building MCP servers with tools, resources, and prompts using the FastMCP framework. Covers decorators, context injection, structured output, authentication, and deployment. Python-only implementation.
license: Complete terms in LICENSE.txt
---

# FastMCP Server Development Guide

## Overview

FastMCP is a Pythonic framework that simplifies MCP server creation through decorators and type hints, eliminating boilerplate code while providing powerful features.

**Key Features:**
- **Decorator-based API** - `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`
- **Automatic schema generation** - Type hints create JSON schemas
- **Context injection** - Built-in logging, progress, LLM sampling
- **Structured output** - Automatic structured content (v2.10.0+)
- **Production-ready** - Authentication, deployment, CLI tools

**FastMCP vs Traditional MCP:**
```python
# FastMCP: Concise and Pythonic
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Traditional: Verbose and low-level
# (50+ lines of boilerplate code)
```

---

# Process

## 🚀 High-Level Workflow

### Phase 1: Planning

**1.1 Understand Requirements**
- What tools (actions) should the LLM perform?
- What resources (data) should be accessible?
- What prompts (templates) are needed?
- Is authentication required?

**1.2 Plan Tool Design**

Consider two patterns for tools:

**API-Wrapper Pattern:**
- Many small tools, each does one operation
- Agent orchestrates multiple calls
- Best for: Simple CRUD, rapid prototyping

**Intention-Based Pattern:**
- Fewer powerful tools that complete workflows
- Tool orchestrates internal steps
- Best for: Complex workflows, ≥3 sequential operations

**For intention-based tool design, load:**
[🎯 Intention-Based Tools](../../mcp-builder/reference/intention_based_tool_design.md) - Learn workflow-centric design

**1.3 Plan Infrastructure**
- Dependencies needed
- Database/API connections (lifespan)
- Authentication provider
- Deployment target (stdio or HTTP)

---

### Phase 2: Implementation

#### 2.1 Initialize Server

**Quick start with script:**
```bash
python scripts/init_fastmcp_server.py my_server
cd my_server
```

**Or manually:**
```python
from fastmcp import FastMCP

mcp = FastMCP("my-server", dependencies=["requests"])
```

#### 2.2 Implement Tools

**Basic tool:**
```python
@mcp.tool()
def greet(name: str) -> str:
    """Greet a user"""
    return f"Hello, {name}!"
```

**Tool with validation:**
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@mcp.tool()
async def create_user(user: User, ctx: Context) -> dict:
    """Create user with logging"""
    await ctx.info(f"Creating: {user.name}")
    return {"id": 123, "name": user.name}
```

**📘 Complete Documentation:**
- [Tools Basics](./references/tools_basics.md) - Decorator, parameters, type hints
- [Tools Validation](./references/tools_validation.md) - Pydantic, Field(), strict mode
- [Tools Output](./references/tools_output.md) - ToolResult, structured content
- [Tools Patterns](./references/tools_patterns.md) - Common patterns & examples
- [Tools Troubleshooting](./references/tools_troubleshooting.md) - Error handling

#### 2.3 Implement Resources

**Static resource:**
```python
@mcp.resource("config://version")
def version() -> str:
    return "1.0.0"
```

**Dynamic resource:**
```python
@mcp.resource("users://{user_id}/profile")
def user_profile(user_id: int) -> dict:
    return {"id": user_id, "name": f"User {user_id}"}
```

**📘 Complete Documentation:**
[Resources Guide](./references/resources_complete.md) - URIs, templates, content types

#### 2.4 Implement Prompts

```python
@mcp.prompt()
def review_code(code: str, focus: str = "all") -> str:
    """Generate code review prompt"""
    return f"Review this code focusing on {focus}:\n\n{code}"
```

**📘 Complete Documentation:**
[Prompts Guide](./references/prompts_complete.md) - Templates, arguments, messages

#### 2.5 Add Context Injection

```python
from fastmcp import Context

@mcp.tool()
async def process(query: str, ctx: Context) -> dict:
    """Process with logging and progress"""
    await ctx.info(f"Processing: {query}")
    await ctx.report_progress(0.5, 1.0)

    # LLM sampling
    summary = await ctx.sample("Summarize this", max_tokens=100)

    return {"status": "success", "summary": summary}
```

**📘 Complete Documentation:**
[Context Patterns](./references/context_patterns.md) - Logging, progress, sampling

#### 2.6 Add Structured Output (v2.10.0+)

```python
# Automatic for dict/Pydantic models
@mcp.tool()
def get_data() -> dict:
    return {"name": "Alice", "age": 30}  # Auto-structured

# Manual with ToolResult
from fastmcp.utilities.types import ToolResult

@mcp.tool()
def advanced() -> ToolResult:
    return ToolResult(
        content=["Human-readable summary"],
        structured_content={"result": 100},
        meta={"execution_time_ms": 150}
    )
```

#### 2.7 Add Error Handling

```python
from fastmcp import ToolError

@mcp.tool()
def fetch_data(api_key: str) -> dict:
    if not api_key:
        raise ToolError("API key required", code="MISSING_KEY")
    return {"status": "success"}
```

#### 2.8 Configure Lifespan (Optional)

```python
@mcp.lifespan()
async def setup():
    db = await connect_database()
    yield {"db": db}
    await db.close()
```

#### 2.9 Add Authentication (Optional)

```python
from fastmcp.auth import AuthProvider

mcp = FastMCP(
    "my-server",
    auth=AuthProvider.google(client_id="...")
)

@mcp.tool(protected=True)  # Requires auth
def protected_op() -> str:
    return "Protected data"
```

#### 2.10 Add Run Method

```python
if __name__ == "__main__":
    mcp.run()  # stdio for Claude Desktop
    # Or: mcp.run(transport="http", port=8000)
```

---

### Phase 3: Testing & Validation

#### 3.1 Validate Code

```bash
python scripts/validate_fastmcp.py my_server.py
```

Checks: syntax, type hints, docstrings, FastMCP patterns

#### 3.2 Test Interactively

```bash
fastmcp dev my_server.py
```

Opens inspector to test tools, resources, and prompts.

#### 3.3 Write Tests

```python
import pytest
from my_server import mcp

@pytest.mark.asyncio
async def test_tool():
    result = await mcp.call_tool("greet", {"name": "Alice"})
    assert "Alice" in result
```

#### 3.4 Run Tests

```bash
pytest tests/
```

---

### Phase 4: Deployment

#### 4.1 Deploy to Claude Desktop

```bash
fastmcp install my_server.py --name "My Server"
```

#### 4.2 Deploy via HTTP

```python
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8000)
```

**Run with uvicorn:**
```bash
uvicorn my_server:mcp --host 0.0.0.0 --port 8000
```

**📘 Complete Deployment Documentation:**
[Deployment Guide](./references/deployment.md) - stdio, HTTP, Cloud, Docker

---

## Reference Files

### Core Implementation
- [📘 Tools Basics](./references/tools_basics.md) - Decorator, parameters, types
- [📘 Tools Validation](./references/tools_validation.md) - Pydantic, constraints
- [📘 Tools Output](./references/tools_output.md) - ToolResult, structured output
- [📘 Tools Patterns](./references/tools_patterns.md) - Common examples
- [📘 Tools Troubleshooting](./references/tools_troubleshooting.md) - Debugging
- [📘 Resources Complete](./references/resources_complete.md) - URIs, templates
- [📘 Prompts Complete](./references/prompts_complete.md) - Templates, messages
- [📘 Context Patterns](./references/context_patterns.md) - Logging, progress, sampling

### Advanced Features
- [📘 Structured Output](./references/structured_output.md) - Schemas, media
- [📘 Error Handling](./references/error_handling.md) - ToolError, recovery
- [📘 Media Handling](./references/media_handling.md) - Image, Audio, File
- [📘 Pydantic Patterns](./references/pydantic_patterns.md) - Models, validation
- [📘 Authentication](./references/authentication.md) - OAuth, JWT, API keys
- [📘 Deployment](./references/deployment.md) - Production setup
- [📘 Best Practices](./references/best_practices.md) - Agent-centric design
- [📘 CLI Reference](./references/cli_reference.md) - fastmcp commands

---

## Quick Start Example

```python
from fastmcp import FastMCP, Context
from pydantic import BaseModel

mcp = FastMCP("example")

class User(BaseModel):
    name: str
    age: int

@mcp.tool()
async def create_user(user: User, ctx: Context) -> dict:
    """Create user with logging"""
    await ctx.info(f"Creating: {user.name}")
    return {"id": 123, "name": user.name}

@mcp.resource("config://version")
def version() -> str:
    return "1.0.0"

@mcp.prompt()
def greet(name: str) -> str:
    return f"Greet {name} warmly"

if __name__ == "__main__":
    mcp.run()
```

**Test it:**
```bash
fastmcp dev example.py
fastmcp install example.py --name "Example"
```

---

## Scripts & Templates

### Initialize Server
```bash
python scripts/init_fastmcp_server.py my_server
```

Creates: server.py, pyproject.toml, .env.example, .gitignore

### Validate Server
```bash
python scripts/validate_fastmcp.py my_server.py
```

### Templates
See `assets/` for:
- **server_template.py** - Minimal template
- **tool_examples/** - 6 complete examples:
  - `01_simple_tool.py` - Basic patterns
  - `02_api_wrapper_tool.py` - Async HTTP
  - `03_database_tool.py` - CRUD operations
  - `04_file_operations_tool.py` - File system
  - `05_async_parallel_tool.py` - Concurrency
  - `06_structured_output_tool.py` - ToolResult patterns

---

## Common Patterns

### Tool with Validation
```python
from pydantic import Field
from typing import Annotated

@mcp.tool()
def search(
    query: Annotated[str, Field(min_length=3, max_length=100)],
    limit: Annotated[int, Field(ge=1, le=50)] = 10
) -> list:
    return []
```

### Tool with Progress
```python
@mcp.tool()
async def process_batch(items: list, ctx: Context) -> dict:
    total = len(items)
    for i, item in enumerate(items):
        await ctx.report_progress((i+1)/total, 1.0)
        process(item)
    return {"processed": total}
```

### Tool with Media
```python
from fastmcp.utilities.types import Image

@mcp.tool()
def generate_chart(data: list) -> list:
    chart_path = create_chart(data)
    return ["Chart created:", Image(path=chart_path)]
```

---

## Resources

- **FastMCP Docs**: https://gofastmcp.com/
- **GitHub**: https://github.com/jlowin/fastmcp
- **MCP Spec**: https://modelcontextprotocol.io/

---

## Version Notes

- **v2.10.0+**: Structured output introduced
- **v2.0+**: Decorator-based API
- This skill documents FastMCP 2.0+ features
