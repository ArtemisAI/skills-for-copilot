# Tools Basics

FastMCP tools basics covering decorator syntax, parameters, type annotations, and required vs optional arguments.

**Topics covered:**
1. The @tool Decorator
2. Decorator Parameters Reference
3. Type Annotations
4. Required vs Optional Arguments

**For more advanced topics, see:**
- [Tools Validation](./tools_validation.md) - Validation modes, parameter metadata, error handling
- [Tools Output](./tools_output.md) - Return values, structured output, ToolResult
- [Tools Advanced](./tools_advanced.md) - MCP annotations, context, async, tool management
- [Tools Patterns](./tools_patterns.md) - Common patterns and troubleshooting

---

# Tools Complete Guide

## Overview

This is the comprehensive guide to FastMCP tools covering all decorator options, type annotations, validation modes, structured output, and advanced patterns. Tools are Python functions decorated with `@mcp.tool()` that LLMs can execute.

**What makes FastMCP tools powerful:**
- Automatic JSON schema generation from type hints
- Built-in validation (flexible or strict mode)
- Automatic structured output (v2.10.0+)
- Context injection for logging and progress
- Rich error handling with `ToolError`
- Media output support (images, audio, files)
- Full control with `ToolResult`

---

## Table of Contents

1. [The @tool Decorator](#1-the-tool-decorator)
2. [Decorator Parameters Reference](#2-decorator-parameters-reference)
3. [Type Annotations](#3-type-annotations)
4. [Required vs Optional Arguments](#4-required-vs-optional-arguments)
5. [Validation Modes](#5-validation-modes)
6. [Parameter Metadata](#6-parameter-metadata)
7. [Return Values & Content Blocks](#7-return-values--content-blocks)
8. [Structured Output](#8-structured-output)
9. [Output Schemas](#9-output-schemas)
10. [ToolResult for Full Control](#10-toolresult-for-full-control)
11. [Error Handling](#11-error-handling)
12. [MCP Annotations](#12-mcp-annotations)
13. [Context Injection](#13-context-injection)
14. [Async vs Sync](#14-async-vs-sync)
15. [Tool Management](#15-tool-management)
16. [Common Patterns](#16-common-patterns)
17. [Troubleshooting](#17-troubleshooting)

---

## 1. The @tool Decorator

### Basic Usage

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
def function_name(param: type) -> return_type:
    """Docstring becomes tool description shown to LLM"""
    return result
```

### Key Features

- **Type hints required** - Used to generate JSON schemas
- **Docstring becomes description** - First line shown to LLM
- **Automatic validation** - Input validated against type hints
- **Automatic schema** - JSON schema generated from types
- **Flexible by default** - Coercion enabled (e.g., `"10"` → `10`)

### Minimal Example

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

---

## 2. Decorator Parameters Reference

### Complete Signature

```python
@mcp.tool(
    name: str | None = None,
    description: str | None = None,
    enabled: bool = True,
    strict_input_validation: bool = False,
    output_schema: dict | None = None,
    icons: list[Icon] | None = None,
    exclude_args: list[str] | None = None,
    annotations: ToolAnnotations | dict | None = None,
    _meta: dict | None = None
)
```

---

### 2.1 Parameter: `name`

**Type:** `str | None`
**Default:** Function name
**Purpose:** Override tool name shown to LLM

**Example:**
```python
@mcp.tool(name="calculate_sum")
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# LLM sees tool named "calculate_sum" instead of "add"
```

**When to use:**
- Function name not user-friendly
- Want to namespace tools (e.g., `"db.query"`)
- Following naming conventions

---

### 2.2 Parameter: `description`

**Type:** `str | None`
**Default:** Function docstring
**Purpose:** Override tool description shown to LLM

**Example:**
```python
@mcp.tool(description="Adds two integers and returns their sum")
def add(a: int, b: int) -> int:
    """Internal documentation for developers"""
    return a + b

# LLM sees custom description, not docstring
```

**When to use:**
- Docstring for internal documentation only
- Need different wording for LLM vs developers
- Docstring contains implementation details

---

### 2.3 Parameter: `enabled`

**Type:** `bool`
**Default:** `True`
**Purpose:** Control tool visibility and availability

**Behavior:**
- `enabled=False`: Tool doesn't appear in `list_tools()` and cannot be called
- Can toggle at runtime with `mcp.enable_tool()` / `mcp.disable_tool()`

**Example:**
```python
@mcp.tool(enabled=False)
def beta_feature() -> str:
    """Beta feature not ready for production"""
    return "Beta data"

# Later, enable it:
mcp.enable_tool("beta_feature")
```

**Use cases:**
- Feature flags
- Beta features
- Maintenance mode
- A/B testing

---

### 2.4 Parameter: `strict_input_validation`

**Type:** `bool`
**Default:** `False`
**Purpose:** Toggle between flexible (coercion) and strict validation

**Flexible Mode (default: `False`):**
```python
@mcp.tool(strict_input_validation=False)  # Default
def add(a: int, b: int) -> int:
    return a + b

# Client sends: {"a": "10", "b": "20"}
# ✅ Pydantic coerces to: {"a": 10, "b": 20}
```

**Strict Mode (`True`):**
```python
@mcp.tool(strict_input_validation=True)
def add_strict(a: int, b: int) -> int:
    return a + b

# Client sends: {"a": "10", "b": "20"}
# ❌ Validation error - strings not accepted
```

**Comparison Table:**

| Input Type | Flexible (default) | Strict |
|-----------|-------------------|--------|
| String integers (`"10"` for int) | ✅ Coerced to integer | ❌ Validation error |
| String floats (`"3.14"` for float) | ✅ Coerced to float | ❌ Validation error |
| String booleans (`"true"` for bool) | ✅ Coerced to boolean | ❌ Validation error |
| Lists with string elements (`["1"]` for list[int]) | ✅ Elements coerced | ❌ Validation error |
| Invalid values (`"abc"` for int) | ❌ Validation error | ❌ Validation error |

**When to use strict:**
- Need exact type matching
- Security-sensitive inputs
- Want to catch client errors early

---

### 2.5 Parameter: `output_schema`

**Type:** `dict | None`
**Default:** Auto-generated from return type hint
**Purpose:** Override automatic schema generation

**Rules:**
- MUST be object type: `{"type": "object", ...}`
- If provided, tool MUST return structured output matching it
- Used for structured output feature (v2.10.0+)

**Example:**
```python
@mcp.tool(
    output_schema={
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "result": {"type": "integer"},
            "timestamp": {"type": "string", "format": "date-time"}
        },
        "required": ["status", "result"]
    }
)
def process() -> dict:
    return {
        "status": "success",
        "result": 42,
        "timestamp": "2025-10-29T10:00:00Z"
    }
```

**When to use:**
- Need precise schema control
- Complex nested objects
- Want to enforce specific structure

---

### 2.6 Parameter: `icons`

**Type:** `list[Icon] | None`
**Default:** None
**Purpose:** Provide icons for UI display

**Example:**
```python
from fastmcp import Icon

@mcp.tool(
    icons=[
        Icon(
            src="icon.png",
            mimeType="image/png",
            sizes="64x64"
        )
    ]
)
def my_tool() -> str:
    """Tool with custom icon"""
    return "result"
```

**Icon Fields:**
- `src`: Icon source (URL or path)
- `mimeType`: MIME type (e.g., "image/png")
- `sizes`: Icon size (e.g., "64x64")

---

### 2.7 Parameter: `exclude_args`

**Type:** `list[str] | None`
**Default:** None
**Purpose:** Hide arguments from LLM schema (runtime injection)

**Restriction:** Only arguments with default values can be excluded

**Example:**
```python
@mcp.tool(exclude_args=["api_key", "user_id"])
def fetch_data(
    query: str,
    api_key: str = "",    # Hidden from LLM, set at runtime
    user_id: str = ""     # Hidden from LLM, set at runtime
) -> dict:
    """Fetch data (api_key injected by server)"""
    return {"query": query, "user": user_id}

# LLM only sees "query" parameter
# Server injects api_key and user_id at runtime
```

**Use cases:**
- API keys
- User IDs from authentication
- Internal configuration
- Server-side secrets

---

### 2.8 Parameter: `annotations`

**Type:** `ToolAnnotations | dict | None`
**Default:** None
**Purpose:** Add MCP metadata about tool behavior

**Example:**
```python
from fastmcp.annotations import ToolAnnotations

@mcp.tool(
    annotations=ToolAnnotations(
        title="Fetch User Profile",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True
    )
)
def get_user(id: int) -> dict:
    """Get user profile from database"""
    return {"id": id, "name": "Alice"}
```

**Annotations Reference:**

| Field | Type | Default | Meaning |
|-------|------|---------|---------|
| `title` | str | - | User-friendly display name for UIs |
| `readOnlyHint` | bool | false | Tool only reads data, doesn't modify |
| `destructiveHint` | bool | true | For non-readonly: changes are irreversible |
| `idempotentHint` | bool | false | Multiple identical calls = single call effect |
| `openWorldHint` | bool | true | Interacts with external systems (APIs, files) |

**See [Section 12: MCP Annotations](#12-mcp-annotations) for detailed examples.**

---

### 2.9 Parameter: `_meta`

**Type:** `dict | None`
**Default:** None
**Purpose:** Custom metadata for MCP client (not shown to LLM)

**Example:**
```python
@mcp.tool(_meta={"version": "1.0", "author": "team", "category": "data"})
def process_data() -> str:
    """Process data"""
    return "done"

# Metadata available to client application but not LLM
```

**Use cases:**
- Tool versioning
- Internal categorization
- Audit metadata
- Client-specific data

---

## 3. Type Annotations

Type annotations are **REQUIRED** for all tool parameters. FastMCP uses them to generate JSON schemas automatically.

### Supported Type Annotations

| Type Annotation | Example | Description | Behavior Notes |
|----------------|---------|-------------|----------------|
| **Basic Types** | `int, float, str, bool` | Scalar values | Most common types |
| **Binary Data** | `bytes` | Binary content | Raw strings, NO auto base64 decode |
| **Date/Time** | `datetime, date, timedelta` | Temporal objects | ISO format strings expected |
| **Collections** | `list[str], dict[str, int], set[int]` | Collections | Nested types supported |
| **Optional** | `float \| None, Optional[float]` | Nullable values | Can be omitted by LLM |
| **Union** | `str \| int, Union[str, int]` | Multiple types | LLM can send either type |
| **Literal** | `Literal["A", "B", "C"]` | Specific values | Enum-like, limited choices |
| **Enum** | `Color` (Enum class) | Enumerated values | Client sends value, receives member |
| **Path** | `Path` | File paths | Auto-converted from strings |
| **UUID** | `UUID` | UUIDs | Auto-converted from strings |
| **Pydantic** | `UserData` (BaseModel) | Complex data | Rich validation, nested models |

---

### 3.1 Basic Types

```python
@mcp.tool()
def example(
    count: int,
    price: float,
    name: str,
    active: bool
) -> str:
    """All basic types"""
    return f"{name}: {count} items at ${price}, active={active}"
```

---

### 3.2 Binary Data (bytes)

**Important:** `bytes` receives raw string, NOT auto-decoded base64

```python
@mcp.tool()
def process_binary(data: bytes) -> str:
    """Process binary data"""
    # Receives raw string from client
    # For base64, use str type and decode manually:
    # import base64
    # decoded = base64.b64decode(data_string)
    return f"Processed {len(data)} bytes"
```

---

### 3.3 Date/Time Types

```python
from datetime import datetime, date, timedelta

@mcp.tool()
def schedule_event(
    start: datetime,
    end_date: date,
    duration: timedelta
) -> str:
    """Schedule event with datetime handling"""
    # Client sends: ISO format strings
    # FastMCP auto-converts to Python datetime objects
    return f"Event from {start} to {end_date}, duration: {duration}"
```

---

### 3.4 Collections

```python
@mcp.tool()
def process_collections(
    tags: list[str],
    scores: dict[str, int],
    unique_ids: set[int]
) -> dict:
    """Collections with nested types"""
    return {
        "tag_count": len(tags),
        "score_total": sum(scores.values()),
        "unique_count": len(unique_ids)
    }
```

---

### 3.5 Optional and Union Types

```python
@mcp.tool()
def search(
    query: str,
    limit: int | None = None,           # Optional with Union syntax
    category: str | None = None          # Can be omitted
) -> list[dict]:
    """Search with optional parameters"""
    return []

# Alternative Optional syntax:
from typing import Optional

@mcp.tool()
def search_alt(
    query: str,
    limit: Optional[int] = None         # Optional with typing.Optional
) -> list[dict]:
    return []
```

---

### 3.6 Literal Types

```python
from typing import Literal

@mcp.tool()
def set_priority(
    task_id: int,
    priority: Literal["low", "medium", "high"]
) -> str:
    """Set task priority (limited choices)"""
    return f"Task {task_id} priority set to {priority}"

# LLM must send one of: "low", "medium", "high"
```

---

### 3.7 Enum Types

```python
from enum import Enum

class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

@mcp.tool()
def set_color(color: Color) -> str:
    """Set color using Enum"""
    # Client sends: "red" (the value)
    # Function receives: Color.RED (enum member)
    return f"Color set to {color.value}"
```

**Important:** Client sends the **value**, function receives the **enum member**.

---

### 3.8 Path and UUID

```python
from pathlib import Path
from uuid import UUID

@mcp.tool()
def read_file(path: Path) -> str:
    """Read file (Path auto-converted from string)"""
    # Client sends: "/path/to/file"
    # Function receives: Path("/path/to/file")
    return path.read_text()

@mcp.tool()
def get_record(id: UUID) -> dict:
    """Get record by UUID"""
    # Client sends: "123e4567-e89b-12d3-a456-426614174000"
    # Function receives: UUID object
    return {"id": str(id), "status": "active"}
```

---

### 3.9 Pydantic Models

```python
from pydantic import BaseModel, Field

class UserData(BaseModel):
    name: str
    age: int
    email: str | None = None

@mcp.tool()
def create_user(user: UserData) -> dict:
    """Create user with Pydantic validation"""
    # ✅ Client sends: {"user": {"name": "Alice", "age": 30}}
    # ❌ INVALID: {"user": '{"name": "Alice", "age": 30}'}
    #    (stringified JSON not accepted even with flexible validation)
    return {"id": 123, "name": user.name}
```

**Important:** Pydantic models require actual objects, not stringified JSON.

---

## 4. Required vs Optional Arguments

Python convention: parameters **without defaults are required**, **with defaults are optional**.

```python
@mcp.tool()
def search_products(
    query: str,                    # REQUIRED (no default)
    max_results: int = 10,         # OPTIONAL (has default)
    sort_by: str = "relevance",    # OPTIONAL (has default)
    category: str | None = None    # OPTIONAL (can be None)
) -> list[dict]:
    """Search products"""
    return []
```

**Schema generation:**
- LLM MUST provide `query`
- LLM can omit `max_results`, `sort_by`, `category` (defaults used)

---

