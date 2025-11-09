# Tools Advanced Features

FastMCP tools advanced features including MCP annotations, context injection, async patterns, and tool management.

**Topics covered:**
12. MCP Annotations (readOnlyHint, destructiveHint, etc.)
13. Context Injection (logging, progress, sampling)
14. Async vs Sync
15. Tool Management (enable/disable/remove)

**See also:**
- [Tools Basics](./tools_basics.md) - Decorator syntax and types
- [Tools Validation](./tools_validation.md) - Validation and error handling
- [Tools Output](./tools_output.md) - Return values and structured output
- [Tools Patterns](./tools_patterns.md) - Common patterns and troubleshooting

---

## 12. MCP Annotations

Annotations provide metadata about tool behavior to clients **without consuming LLM token context**.

```python
from fastmcp.annotations import ToolAnnotations

@mcp.tool(
    annotations=ToolAnnotations(
        title="Calculate User Engagement Score",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False
    )
)
def calculate_score(user_id: int) -> int:
    """Calculate engagement score for user"""
    # Read-only calculation, no side effects
    return 100
```

---

### 12.1 Annotation Reference

| Annotation | Type | Default | Meaning | Use When |
|-----------|------|---------|---------|----------|
| `title` | string | - | User-friendly display name | Tool name not clear to users |
| `readOnlyHint` | boolean | false | Tool only reads, doesn't modify | GET-like operations |
| `destructiveHint` | boolean | true | For non-readonly: irreversible changes | DELETE, data loss possible |
| `idempotentHint` | boolean | false | Multiple calls = single call effect | Safe to retry, no accumulation |
| `openWorldHint` | boolean | true | Interacts with external systems | API calls, file I/O, databases |

---

### 12.2 Annotation Examples

#### Read-only, Local Computation

```python
@mcp.tool(
    annotations=ToolAnnotations(
        title="Add Two Numbers",
        readOnlyHint=True,        # No modification
        idempotentHint=True,      # Safe to retry
        openWorldHint=False       # No external systems
    )
)
def add(a: int, b: int) -> int:
    """Pure function, no side effects"""
    return a + b
```

#### External API, Idempotent Read

```python
@mcp.tool(
    annotations=ToolAnnotations(
        title="Fetch User Profile",
        readOnlyHint=True,        # Just reads
        idempotentHint=True,      # Same result on retry
        openWorldHint=True        # Calls external API
    )
)
async def get_user(id: int) -> dict:
    """Fetch from external API"""
    return await api.get_user(id)
```

#### Destructive Write

```python
@mcp.tool(
    annotations=ToolAnnotations(
        title="Delete User Account",
        readOnlyHint=False,       # Modifies data
        destructiveHint=True,     # Cannot be undone
        idempotentHint=False,     # First call matters
        openWorldHint=True        # External database
    )
)
async def delete_account(id: int) -> dict:
    """Permanently delete account"""
    return await db.delete(id)
```

#### Non-destructive Write

```python
@mcp.tool(
    annotations=ToolAnnotations(
        title="Update User Email",
        readOnlyHint=False,       # Modifies data
        destructiveHint=False,    # Can be changed again
        idempotentHint=True,      # Same result on retry
        openWorldHint=True        # External database
    )
)
async def update_email(id: int, email: str) -> dict:
    """Update user email (can be changed later)"""
    return await db.update(id, email=email)
```

---

## 13. Context Injection

Access MCP capabilities by injecting `Context` parameter.

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("My Server")

@mcp.tool()
async def comprehensive_tool(
    query: str,
    ctx: Context  # Type hint required, parameter name flexible
) -> str:
    """Tool demonstrating all Context features"""

    # 1. Logging
    await ctx.debug("Debug-level message")
    await ctx.info(f"Processing query: {query}")
    await ctx.warning("Warning message if needed")
    await ctx.error("Error message for serious issues")

    # 2. Progress reporting
    await ctx.report_progress(
        progress=0.5,
        total=1.0,
        message="Halfway through processing"
    )

    # 3. Read resources
    config = await ctx.read_resource("config://settings")
    data = await ctx.read_resource("file://data.json")

    # 4. LLM sampling (call LLM from within tool)
    summary = await ctx.sample(
        prompt="Summarize this data briefly",
        max_tokens=100
    )

    # 5. Request metadata
    request_id = ctx.request_id
    client_id = ctx.client_id

    # 6. Access FastMCP server instance
    server_name = ctx.fastmcp.name

    # 7. Access session for advanced features
    await ctx.session.send_resource_updated("file://data.json")

    # 8. Access lifespan context
    db = ctx.request_context.lifespan_context.get("db")

    return f"Processed {query} with summary: {summary}"
```

---

### 13.1 Context Methods Reference

**Logging:**
- `await ctx.debug(message: str)` - Debug-level log
- `await ctx.info(message: str)` - Info-level log
- `await ctx.warning(message: str)` - Warning-level log
- `await ctx.error(message: str)` - Error-level log
- `await ctx.log(level: str, message: str, logger_name: str = None)` - Custom level

**Progress:**
- `await ctx.report_progress(progress: float, total: float = None, message: str = None)`
  - `progress`: Current progress value
  - `total`: Total expected progress (optional)
  - `message`: Progress message (optional)

**Resources:**
- `await ctx.read_resource(uri: str)` - Read resource by URI

**LLM Sampling:**
- `await ctx.sample(prompt: str, max_tokens: int = 100)` - Request LLM completion

**Elicitation (User Interaction):**
- `await ctx.elicit(message: str, schema: Type[BaseModel])` - Request user input with validation

**Request Info:**
- `ctx.request_id` - Unique request ID
- `ctx.client_id` - Client ID if available

**Server Access:**
- `ctx.fastmcp` - FastMCP server instance
- `ctx.session` - MCP session for advanced operations
- `ctx.request_context` - Request-specific data including lifespan context

---

## 14. Async vs Sync

FastMCP supports both async and sync functions.

### 14.1 Async (Recommended for I/O)

```python
import aiohttp

@mcp.tool()
async def fetch_data(url: str) -> dict:
    """Async tool for I/O operations"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

**Benefits:**
- Non-blocking execution
- Server stays responsive
- Handles concurrent requests efficiently
- Best for I/O operations (network, file, database)

---

### 14.2 Sync (Acceptable for CPU-bound)

```python
@mcp.tool()
def calculate(numbers: list[int]) -> int:
    """Sync tool for CPU-bound work"""
    # CPU-intensive calculation
    return sum(n ** 2 for n in numbers)
```

**Drawbacks:**
- Blocks event loop during execution
- Can reduce server responsiveness
- Not ideal for I/O operations

---

### 14.3 Wrapping Blocking Operations

For CPU-intensive sync operations, wrap them to avoid blocking:

```python
import asyncio
import time

def blocking_operation(data: str) -> str:
    """Expensive CPU work (synchronous)"""
    time.sleep(5)  # Simulating heavy computation
    return f"Processed {data}"

@mcp.tool()
async def wrapped_blocking(data: str) -> str:
    """Async wrapper for blocking sync operation"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,  # Uses default ThreadPoolExecutor
        blocking_operation,
        data
    )
    return result
```

---

## 15. Tool Management

### 15.1 Enable/Disable Tools

```python
# Disable at creation
@mcp.tool(enabled=False)
def beta_feature() -> str:
    """Beta feature disabled by default"""
    return "Beta data"

# Enable/disable at runtime
mcp.enable_tool("beta_feature")
mcp.disable_tool("beta_feature")
```

**Behavior:**
- Disabled tools don't appear in `list_tools()` response
- Calling disabled tool returns "Unknown tool" error
- Useful for feature flags, maintenance, A/B testing

---

### 15.2 Remove Tools

```python
# Remove tool completely
mcp.remove_tool("old_feature")
```

**Use cases:**
- Dynamic toolset changes
- Cleanup temporary tools
- Runtime configuration

---

### 15.3 Duplicate Tool Handling

```python
# Configure on server creation
mcp = FastMCP(
    "My Server",
    on_duplicate_tools="warn"  # Options: "warn" | "error" | "replace" | "ignore"
)

@mcp.tool()
def my_tool() -> str:
    return "First version"

@mcp.tool()
def my_tool() -> str:  # Duplicate!
    return "Second version"
```

**Modes:**
- `"warn"` (default): Log warning, replace old with new
- `"error"`: Raise ValueError, prevent duplicate
- `"replace"`: Silently replace old with new
- `"ignore"`: Keep original, ignore new registration

---

### 15.4 Tool Notifications

FastMCP automatically sends `notifications/tools/list_changed` to clients when:
- Tool added
- Tool removed
- Tool enabled
- Tool disabled

Clients can listen for these notifications to update their tool lists.

---

## 16. Common Patterns
