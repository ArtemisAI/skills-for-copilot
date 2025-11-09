# Tools Validation & Error Handling

FastMCP tools validation modes, parameter metadata, and error handling patterns.

**Topics covered:**
5. Validation Modes (flexible vs strict)
6. Parameter Metadata (Field constraints)
11. Error Handling (ToolError)

**See also:**
- [Tools Basics](./tools_basics.md) - Decorator syntax and type annotations
- [Tools Output](./tools_output.md) - Return values and structured output
- [Tools Advanced](./tools_advanced.md) - MCP annotations, context, async
- [Tools Patterns](./tools_patterns.md) - Common patterns and troubleshooting

---

## 5. Validation Modes

### 5.1 Flexible Validation (Default)

**Default behavior:** `strict_input_validation=False`

```python
@mcp.tool()  # strict_input_validation=False by default
def add(a: int, b: int) -> int:
    return a + b

# Client sends: {"a": "10", "b": "20"}
# ✅ Pydantic coerces to: {"a": 10, "b": 20}
```

**Coercion rules:**
- String integers → int
- String floats → float
- String booleans → bool
- Nested coercion in lists/dicts

---

### 5.2 Strict Validation

**Opt-in:** `strict_input_validation=True`

```python
@mcp.tool(strict_input_validation=True)
def add_strict(a: int, b: int) -> int:
    return a + b

# Client sends: {"a": "10", "b": "20"}
# ❌ Validation error - strings not accepted, must be actual integers
```

---

### 5.3 Validation Comparison Table

| Input Type | Flexible (default) | Strict |
|-----------|-------------------|--------|
| String integers (`"10"` for `int`) | ✅ Coerced to `10` | ❌ Error |
| String floats (`"3.14"` for `float`) | ✅ Coerced to `3.14` | ❌ Error |
| String booleans (`"true"` for `bool`) | ✅ Coerced to `True` | ❌ Error |
| Lists with string elements (`["1", "2"]` for `list[int]`) | ✅ Coerced to `[1, 2]` | ❌ Error |
| Pydantic model fields with type mismatches | ✅ Fields coerced | ❌ Error |
| Invalid values (`"abc"` for `int`) | ❌ Error | ❌ Error |

---

### 5.4 When to Use Each Mode

**Use Flexible (default):**
- Most general-purpose tools
- LLM-facing tools (LLMs might send string representations)
- User-friendly error handling

**Use Strict:**
- Security-sensitive operations
- Need exact type matching
- Catching client errors early
- API compliance requirements

---

## 6. Parameter Metadata

### 6.1 Simple String Descriptions

Use `Annotated` with a single string for parameter descriptions:

```python
from typing import Annotated

@mcp.tool()
def search(
    query: Annotated[str, "Search query to execute"],
    limit: Annotated[int, "Maximum number of results to return"] = 10
) -> list[str]:
    """Search with annotated parameters"""
    return []
```

**Equivalent to `Field(description=...)` but more concise.**

---

### 6.2 Advanced Metadata with Field()

Use `Field()` for constraints and detailed metadata:

```python
from pydantic import Field
from typing import Annotated

@mcp.tool()
def create_user(
    name: Annotated[
        str,
        Field(
            description="User's full name",
            min_length=1,
            max_length=100,
            pattern="^[a-zA-Z ]+$"  # Letters and spaces only
        )
    ],
    age: Annotated[
        int,
        Field(
            description="User's age in years",
            ge=18,    # Greater or equal to 18
            le=120,   # Less or equal to 120
            default=25
        )
    ] = 25,
    email: Annotated[
        str,
        Field(
            description="User's email address",
            pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
        )
    ] | None = None
) -> dict:
    """Create user with validated inputs"""
    return {"name": name, "age": age, "email": email}
```

---

### 6.3 Available Field() Parameters

| Parameter | Type | Purpose | Example |
|-----------|------|---------|---------|
| `description` | str | Human-readable description | `"User's age in years"` |
| `ge` / `gt` | numeric | Greater or equal / Greater than | `ge=18` (≥ 18) |
| `le` / `lt` | numeric | Less or equal / Less than | `le=120` (≤ 120) |
| `min_length` | int | Minimum string/collection length | `min_length=3` |
| `max_length` | int | Maximum string/collection length | `max_length=100` |
| `pattern` | str | Regex pattern for strings | `pattern="^[A-Z]+$"` |
| `default` | any | Default value | `default=25` |
| `examples` | list | Example values | `examples=[18, 25, 30]` |
| `title` | str | Short title | `title="Age"` |

---

### 6.4 Validation Examples

```python
@mcp.tool()
def advanced_validation(
    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=20,
            pattern="^[a-zA-Z0-9_]+$"  # Alphanumeric + underscore
        )
    ],
    score: Annotated[
        float,
        Field(
            ge=0.0,
            le=100.0,
            description="Score between 0 and 100"
        )
    ],
    tags: Annotated[
        list[str],
        Field(
            min_length=1,
            max_length=5,
            description="1-5 tags"
        )
    ]
) -> dict:
    """Tool with comprehensive validation"""
    return {"username": username, "score": score, "tags": tags}
```

---

## 7. Return Values & Content Blocks
## 11. Error Handling

### 11.1 Standard Python Exceptions

```python
@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Result: Error logged and converted to MCP error response
```

---

### 11.2 ToolError for Custom Errors

```python
from fastmcp import ToolError

@mcp.tool()
def fetch_data(api_key: str) -> dict:
    """Fetch data from API"""
    if not api_key:
        raise ToolError(
            "API key is required",
            code="MISSING_API_KEY"
        )

    if not validate_key(api_key):
        raise ToolError(
            "Invalid API key format. Expected format: 'sk-...'",
            code="INVALID_API_KEY"
        )

    try:
        data = fetch_from_api(api_key)
        return {"status": "success", "data": data}
    except APITimeout:
        raise ToolError(
            "API request timed out after 30 seconds",
            code="API_TIMEOUT"
        )
```

---

### 11.3 ToolError Parameters

**`message`**: Error message (required)
- User-friendly description of what went wrong
- Shown to LLM

**`code`**: Error code (optional)
- Programmatic error identifier
- Used for error handling logic
- Examples: `"MISSING_API_KEY"`, `"TIMEOUT"`, `"INVALID_INPUT"`

---

### 11.4 Masking Error Details

For security, mask internal error details from LLM:

```python
# On server initialization
mcp = FastMCP("My Server", mask_error_details=True)

@mcp.tool()
def sensitive_operation() -> str:
    """Operation that might expose secrets in errors"""

    # Standard exception
    raise Exception("Internal DB error: postgres://user:pass@host/db")
    # LLM receives: "An error occurred" (details masked)

    # ToolError still shows details
    raise ToolError("User-friendly error message", code="ERROR_CODE")
    # LLM receives: "User-friendly error message" (not masked)
```

---

### 11.5 Masking Behavior

**`mask_error_details=False` (default):**
- All exceptions show full details to LLM
- Good for development and debugging

**`mask_error_details=True`:**
- Standard exceptions: Generic message shown (`"An error occurred"`)
- `ToolError`: Original message shown (not masked)
- Prevents leaking sensitive information

---

### 11.6 Error Handling Best Practices

```python
@mcp.tool()
async def robust_operation(input: str, ctx: Context) -> dict:
    """Robust tool with comprehensive error handling"""
    try:
        await ctx.info("Starting operation")

        # Validate input
        if not input:
            raise ToolError("Input cannot be empty", code="EMPTY_INPUT")

        if len(input) > 1000:
            raise ToolError(
                "Input too long (max 1000 characters)",
                code="INPUT_TOO_LONG"
            )

        # Perform operation
        result = await perform_operation(input)

        await ctx.info("Operation completed successfully")
        return {"status": "success", "result": result}

    except ToolError:
        # Re-raise ToolError as-is
        raise

    except ValueError as e:
        # Convert to ToolError with context
        await ctx.error(f"Validation error: {e}")
        raise ToolError(
            f"Invalid input: {e}",
            code="VALIDATION_ERROR"
        )

    except TimeoutError as e:
        await ctx.warning("Operation timed out, will retry")
        # Retry logic here
        raise ToolError(
            "Operation timed out after 30 seconds",
            code="TIMEOUT"
        )

    except Exception as e:
        # Log unexpected errors
        await ctx.error(f"Unexpected error: {e}")
        raise ToolError(
            "An unexpected error occurred. Please try again.",
            code="INTERNAL_ERROR"
        )
```

---

## 12. MCP Annotations
