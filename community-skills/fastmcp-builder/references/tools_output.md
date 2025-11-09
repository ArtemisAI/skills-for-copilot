# Tools Output & Structured Content

FastMCP tools output patterns, structured content, output schemas, and ToolResult.

**Topics covered:**
7. Return Values & Content Blocks
8. Structured Output (v2.10.0+)
9. Output Schemas
10. ToolResult for Full Control

**See also:**
- [Tools Basics](./tools_basics.md) - Decorator syntax and types
- [Tools Validation](./tools_validation.md) - Validation and error handling
- [Tools Advanced](./tools_advanced.md) - MCP annotations, context, async
- [Tools Patterns](./tools_patterns.md) - Common patterns and troubleshooting

---

## 7. Return Values & Content Blocks

FastMCP automatically converts return values to appropriate MCP content blocks.

### Automatic Conversion Table

| Return Type | Converts To | Example |
|------------|-------------|---------|
| `str` | `TextContent` | `"Hello world"` |
| `bytes` | `BlobResourceContents` in `EmbeddedResource` (base64) | `b"\x89PNG..."` |
| `Image` | `ImageContent` | `Image(path="chart.png")` |
| `Audio` | `AudioContent` | `Audio(data=wav_bytes, format="wav")` |
| `File` | `EmbeddedResource` (base64) | `File(path="report.pdf")` |
| MCP content blocks | Pass through as-is | `TextContent(...)` |
| `list[any above]` | List of content blocks | `["text", Image(...)]` |
| `None` | Empty response | `None` |

---

### 7.1 Simple String Return

```python
@mcp.tool()
def greet(name: str) -> str:
    """Simple string return"""
    return f"Hello, {name}!"

# Returns: TextContent(type="text", text="Hello, Alice!")
```

---

### 7.2 Media Helper Classes

```python
from fastmcp.utilities.types import Image, Audio, File
from pathlib import Path

@mcp.tool()
def generate_chart(data: list[int]) -> Image:
    """Generate and return chart image"""
    # Generate chart (creates chart.png)
    create_chart(data, "chart.png")

    # From path (MIME type auto-detected from extension)
    return Image(path="chart.png")

    # Or from bytes (format required):
    # return Image(data=png_bytes, format="png")

@mcp.tool()
def generate_audio(text: str) -> Audio:
    """Generate audio from text"""
    # From path
    return Audio(path="speech.wav")

    # Or from bytes (format required):
    # return Audio(data=wav_bytes, format="wav")

@mcp.tool()
def generate_report(data: dict) -> File:
    """Generate PDF report"""
    # From path
    return File(path="report.pdf")

    # Or from bytes (format and name required):
    # return File(data=pdf_bytes, format="pdf", name="report.pdf")
```

---

### 7.3 Media Class Parameters

**Common to all (Image, Audio, File):**
- **`path=` OR `data=`** (mutually exclusive)
  - `path`: File path (string or Path) - MIME type auto-detected from extension
  - `data`: Raw bytes - requires `format=` parameter
- **`format=`**: Optional format override (e.g., "png", "wav", "pdf")
- **`annotations=`**: Optional MCP annotations

**File only:**
- **`name=`**: Required when using `data=`, filename for the embedded resource

---

### 7.4 Multiple Outputs

```python
@mcp.tool()
def comprehensive_report(topic: str) -> list:
    """Generate multi-part report"""
    return [
        "Analysis complete. See attached files:",
        Image(path="chart.png"),
        File(path="data.csv"),
        Audio(path="summary.wav")
    ]

# Returns list of content blocks
```

---

## 8. Structured Output

**New in version:** 2.10.0

FastMCP automatically generates **structured output** alongside traditional content blocks. This provides machine-readable data in addition to human-readable text.

---

### 8.1 Automatic Structured Content Rules

**Rule 1: Object-like results ALWAYS become structured content**

```python
@mcp.tool()
def get_user() -> dict:
    """Get user data (dict is object-like)"""
    return {"name": "Alice", "age": 30}
    # ✅ Automatically generates:
    # Content: TextContent with JSON string
    # Structured: {"name": "Alice", "age": 30}

@mcp.tool()
def get_profile() -> UserData:  # Pydantic model
    """Get user profile"""
    return UserData(name="Bob", age=25)
    # ✅ Automatically generates structured content
```

**Object-like types:**
- `dict`
- Pydantic `BaseModel`
- `dataclass`
- `TypedDict`

---

**Rule 2: Non-object results ONLY become structured content with `output_schema`**

```python
@mcp.tool()
def get_count() -> int:
    """Get count (primitive type)"""
    return 42
    # ❌ NO structured content (only content block)
    # Content: TextContent("42")

@mcp.tool(
    output_schema={
        "type": "object",
        "properties": {"result": {"type": "integer"}}
    }
)
def get_count_structured() -> int:
    """Get count with schema"""
    return 42
    # ✅ Generates structured content:
    # Content: TextContent("42")
    # Structured: {"result": 42}  # Auto-wrapped
```

---

### 8.2 Automatic Primitive Wrapping

When you return primitive types with an `output_schema`, FastMCP automatically wraps them under a `"result"` key:

```python
@mcp.tool()
def get_temperature() -> int:
    return 25
    # Auto-wrapped as: {"result": 25}

@mcp.tool()
def get_cities() -> list[str]:
    return ["London", "Paris", "Tokyo"]
    # Auto-wrapped as: {"result": ["London", "Paris", "Tokyo"]}

@mcp.tool()
def get_message() -> str:
    return "Hello"
    # Auto-wrapped as: {"result": "Hello"}
```

---

### 8.3 Object-like Results (No Schema Needed)

```python
from pydantic import BaseModel
from dataclasses import dataclass

# Dict
@mcp.tool()
def get_data() -> dict[str, int]:
    return {"count": 42, "status": 200}
    # Structured: {"count": 42, "status": 200}

# Pydantic model
class User(BaseModel):
    name: str
    age: int

@mcp.tool()
def get_user() -> User:
    return User(name="Alice", age=30)
    # Structured: {"name": "Alice", "age": 30}

# Dataclass
@dataclass
class Product:
    id: int
    name: str

@mcp.tool()
def get_product() -> Product:
    return Product(id=1, name="Widget")
    # Structured: {"id": 1, "name": "Widget"}
```

---

### 8.4 Complex Type Example

```python
from typing import TypedDict

class SearchResult(TypedDict):
    query: str
    results: list[str]
    count: int

@mcp.tool()
def search(query: str) -> SearchResult:
    """Search with typed result"""
    results = ["result1", "result2", "result3"]
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }
    # Automatically generates:
    # Content: TextContent with JSON
    # Structured: {"query": "...", "results": [...], "count": 3}
```

---

## 9. Output Schemas

### 9.1 Automatic Schema Generation

FastMCP generates output schemas from return type hints:

```python
from pydantic import BaseModel, Field

class WeatherData(BaseModel):
    temperature: float = Field(description="Temperature in Celsius")
    condition: str = Field(description="Weather condition")
    humidity: float = Field(ge=0, le=100)

@mcp.tool()
def get_weather(city: str) -> WeatherData:
    """Get weather (schema auto-generated from WeatherData)"""
    return WeatherData(
        temperature=22.5,
        condition="sunny",
        humidity=65.0
    )
```

---

### 9.2 Manual Schema Override

```python
@mcp.tool(
    output_schema={
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["success", "error"]
            },
            "data": {
                "type": "array",
                "items": {"type": "integer"}
            },
            "timestamp": {
                "type": "string",
                "format": "date-time"
            }
        },
        "required": ["status", "data"]
    }
)
def process() -> dict:
    """Process with manual schema"""
    return {
        "status": "success",
        "data": [1, 2, 3],
        "timestamp": "2025-10-29T10:00:00Z"
    }
```

---

### 9.3 Schema Rules

- **Output schemas MUST be object type:** `{"type": "object", ...}`
- **If you provide a schema, tool MUST return matching structured output**
- **Structured output can be provided WITHOUT a schema** (using `ToolResult`)
- **Validation occurs automatically** when schema is present

---

## 10. ToolResult for Full Control

For complete control over content blocks, structured output, and metadata:

```python
from fastmcp.utilities.types import ToolResult, Image

@mcp.tool()
def advanced_analysis(query: str) -> ToolResult:
    """Complete control over response"""
    return ToolResult(
        # Traditional content blocks (shown to LLM)
        content=[
            "Analysis complete. Key findings:",
            "- Finding 1: Data shows upward trend",
            "- Finding 2: No anomalies detected",
            Image(path="visualization.png")
        ],

        # Structured output (machine-readable)
        structured_content={
            "query": query,
            "findings": ["Finding 1", "Finding 2"],
            "confidence": 0.95,
            "data_points": 1000,
            "trend": "upward"
        },

        # Metadata (NOT shown to LLM, only to client app)
        meta={
            "execution_time_ms": 150,
            "cache_hit": True,
            "model_version": "2.0",
            "cost": 0.001
        }
    )
```

---

### ToolResult Fields

**`content`**: List of content blocks
- Accepts: `str`, `Image`, `Audio`, `File`, MCP content blocks
- Shown to LLM

**`structured_content`**: Dict or Pydantic model
- Machine-readable data
- Accessed by client applications

**`meta`**: Dict
- Metadata for client app
- NOT exposed to LLM
- Use for telemetry, debugging, etc.

---

### When to Use ToolResult

- **Need precise control** over both content and structured output
- **Returning multiple media types** (text + images + files)
- **Adding metadata** not for LLM (execution time, costs, etc.)
- **Bypassing automatic conversion** to customize response

**Note:** Using `ToolResult` bypasses all automatic conversions. You must construct the complete response yourself.

---

## 11. Error Handling
