# Tools Common Patterns & Troubleshooting

FastMCP tools common patterns, real-world examples, and troubleshooting guide.

**Topics covered:**
16. Common Patterns (6+ real-world examples)
17. Troubleshooting (8+ common issues and solutions)

**See also:**
- [Tools Basics](./tools_basics.md) - Decorator syntax and types
- [Tools Validation](./tools_validation.md) - Validation and error handling
- [Tools Output](./tools_output.md) - Return values and structured output
- [Tools Advanced](./tools_advanced.md) - MCP annotations, context, async

---

## 16. Common Patterns

### 16.1 Pattern: Simple CRUD Tool

```python
from pydantic import BaseModel, Field
from typing import Annotated

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(ge=18, le=120)

@mcp.tool(
    annotations=ToolAnnotations(
        title="Create New User",
        readOnlyHint=False,
        destructiveHint=False
    )
)
async def create_user(user: UserCreate) -> dict:
    """Create a new user account"""
    created = await db.create_user(
        name=user.name,
        email=user.email,
        age=user.age
    )
    return {"id": created.id, "name": created.name}
```

---

### 16.2 Pattern: Tool with Progress Reporting

```python
@mcp.tool()
async def process_large_dataset(
    dataset_id: str,
    ctx: Context
) -> dict:
    """Process large dataset with progress updates"""
    await ctx.info(f"Starting processing of dataset {dataset_id}")

    data = await load_dataset(dataset_id)
    total_items = len(data)

    results = []
    for i, item in enumerate(data):
        # Process item
        result = await process_item(item)
        results.append(result)

        # Report progress every 10 items
        if (i + 1) % 10 == 0 or i == total_items - 1:
            progress = (i + 1) / total_items
            await ctx.report_progress(
                progress=progress,
                total=1.0,
                message=f"Processed {i + 1}/{total_items} items"
            )

    await ctx.info("Processing complete")
    return {
        "dataset_id": dataset_id,
        "processed_items": total_items,
        "results_summary": len(results)
    }
```

---

### 16.3 Pattern: Tool with Error Recovery

```python
import asyncio

@mcp.tool()
async def resilient_api_call(
    url: str,
    retries: int = 3,
    ctx: Context = None
) -> dict:
    """Make API call with automatic retries"""
    for attempt in range(retries):
        try:
            if ctx:
                await ctx.debug(f"Attempt {attempt + 1}/{retries}")

            result = await make_api_call(url)

            if ctx:
                await ctx.info("API call successful")

            return {"status": "success", "data": result}

        except RequestTimeout:
            if attempt < retries - 1:
                if ctx:
                    await ctx.warning(f"Timeout, retrying...")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise ToolError(
                    f"API call failed after {retries} attempts",
                    code="API_TIMEOUT"
                )

        except Exception as e:
            if ctx:
                await ctx.error(f"Unexpected error: {e}")
            raise ToolError(
                f"API call failed: {str(e)}",
                code="API_ERROR"
            )
```

---

### 16.4 Pattern: Tool with Multiple Media Outputs

```python
from fastmcp.utilities.types import Image, File

@mcp.tool()
async def generate_report(
    topic: str,
    include_chart: bool = True,
    ctx: Context = None
) -> list:
    """Generate comprehensive report with visualizations"""
    if ctx:
        await ctx.info(f"Generating report on {topic}")

    # Generate text content
    text_content = await generate_text_report(topic)

    outputs = [f"Report on {topic}:\n\n{text_content}"]

    # Add chart if requested
    if include_chart:
        if ctx:
            await ctx.report_progress(0.5, 1.0, "Generating chart...")
        chart_path = await generate_chart(topic)
        outputs.append(Image(path=chart_path))

    # Add data file
    if ctx:
        await ctx.report_progress(0.75, 1.0, "Generating data file...")
    data_path = await export_data(topic)
    outputs.append(File(path=data_path))

    if ctx:
        await ctx.info("Report generation complete")

    return outputs
```

---

### 16.5 Pattern: Tool with Structured Output and Validation

```python
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    summary: str = Field(description="Brief summary of findings")
    score: float = Field(ge=0, le=100, description="Quality score")
    recommendations: list[str] = Field(description="List of recommendations")
    data_points: int = Field(ge=0, description="Number of data points analyzed")

@mcp.tool(
    annotations=ToolAnnotations(
        title="Analyze Dataset",
        readOnlyHint=True,
        idempotentHint=True
    )
)
async def analyze_data(
    dataset_id: str,
    ctx: Context = None
) -> AnalysisResult:
    """Analyze dataset and return structured results"""
    if ctx:
        await ctx.info(f"Analyzing dataset {dataset_id}")

    data = await load_dataset(dataset_id)
    analysis = perform_analysis(data)

    return AnalysisResult(
        summary=analysis['summary'],
        score=analysis['score'],
        recommendations=analysis['recommendations'],
        data_points=len(data)
    )
```

---

### 16.6 Pattern: Tool with External Resource Reading

```python
@mcp.tool()
async def process_with_config(
    input_data: str,
    ctx: Context
) -> dict:
    """Process data using configuration from resources"""
    # Read configuration from resource
    config_content = await ctx.read_resource("config://settings")
    config = json.loads(config_content)

    # Read data from file resource
    ref_data = await ctx.read_resource("file://reference_data.json")
    reference = json.loads(ref_data)

    # Process using config and reference data
    result = process(input_data, config, reference)

    return {
        "status": "success",
        "result": result,
        "config_used": config["version"]
    }
```

---

## 17. Troubleshooting

### 17.1 Issue: Schema Generation Fails

**Problem:** Tool registers but schema is incorrect or missing.

**Solutions:**
```python
# ❌ Missing type hints
@mcp.tool()
def bad(data):  # No type hints!
    return data

# ✅ Add type hints
@mcp.tool()
def good(data: str) -> str:
    return data
```

---

### 17.2 Issue: Validation Errors

**Problem:** Client sends valid data but tool rejects it.

**Solutions:**
```python
# Check validation mode
@mcp.tool(strict_input_validation=False)  # Allow coercion
def flexible(num: int) -> int:
    return num

# For Pydantic models, ensure dict (not stringified JSON)
# ❌ Client: {"user": '{"name": "Alice"}'}
# ✅ Client: {"user": {"name": "Alice"}}
```

---

### 17.3 Issue: Tool Not Appearing in list_tools

**Problem:** Tool defined but not visible to client.

**Solutions:**
```python
# Check if disabled
@mcp.tool(enabled=True)  # Ensure enabled
def my_tool() -> str:
    return "result"

# Check duplicate handling
mcp = FastMCP("Server", on_duplicate_tools="warn")
# Check logs for warnings about duplicates
```

---

### 17.4 Issue: Context Not Injected

**Problem:** Context parameter is None or missing.

**Solutions:**
```python
# ❌ Missing type hint
@mcp.tool()
async def bad(query: str, ctx) -> str:  # No Context type hint!
    return "result"

# ✅ Add Context type hint
from fastmcp import Context

@mcp.tool()
async def good(query: str, ctx: Context) -> str:
    await ctx.info("Working!")
    return "result"
```

---

### 17.5 Issue: Async/Await Errors

**Problem:** Sync tool trying to await, or async tool not awaited.

**Solutions:**
```python
# ❌ Sync tool trying to await
@mcp.tool()
def bad(ctx: Context) -> str:
    await ctx.info("Oops!")  # Error: can't await in sync function
    return "result"

# ✅ Make tool async
@mcp.tool()
async def good(ctx: Context) -> str:
    await ctx.info("Works!")
    return "result"
```

---

### 17.6 Issue: Structured Output Not Generated

**Problem:** Tool returns data but no structured content.

**Solutions:**
```python
# For primitives, add output schema
@mcp.tool(
    output_schema={
        "type": "object",
        "properties": {"result": {"type": "integer"}}
    }
)
def get_count() -> int:
    return 42  # Now generates structured content

# For objects, it's automatic
@mcp.tool()
def get_user() -> dict:
    return {"name": "Alice"}  # Auto-generates structured content
```

---

### 17.7 Issue: Error Details Not Visible

**Problem:** Errors happening but LLM sees generic message.

**Solutions:**
```python
# Check mask_error_details setting
mcp = FastMCP("Server", mask_error_details=False)  # Show details

# Or use ToolError for user-friendly messages
from fastmcp import ToolError

@mcp.tool()
def my_tool() -> str:
    raise ToolError(
        "User-friendly error message",
        code="ERROR_CODE"
    )
```

---

### 17.8 Issue: Media Not Displaying

**Problem:** Image/Audio/File not showing to client.

**Solutions:**
```python
from fastmcp.utilities.types import Image

# ❌ Wrong: returning path string
@mcp.tool()
def bad() -> str:
    return "chart.png"  # Just returns text

# ✅ Correct: using Image class
@mcp.tool()
def good() -> Image:
    return Image(path="chart.png")

# For bytes, specify format
@mcp.tool()
def from_bytes() -> Image:
    return Image(data=image_bytes, format="png")
```

---

## Summary Checklist

When creating a tool, ensure:

- [ ] **Type hints on ALL parameters** (required)
- [ ] **Docstring or description** provided
- [ ] **Return type hint** specified
- [ ] **Appropriate validation mode** selected (flexible vs strict)
- [ ] **Parameter metadata** added where needed (`Field()`)
- [ ] **Error handling** implemented (try/except, `ToolError`)
- [ ] **MCP annotations** set (readOnlyHint, destructiveHint, etc.)
- [ ] **Context injected** if needed (logging, progress, sampling)
- [ ] **Async for I/O**, sync acceptable for CPU-bound
- [ ] **Structured output** considered (Pydantic models for complex data)
- [ ] **Output schema** if returning primitives that need structured content
- [ ] **Media helper classes** used for images/audio/files
- [ ] **Progress reporting** for long operations
- [ ] **Logging with Context** for debugging
- [ ] **Tool enabled** (enabled=True or not explicitly disabled)

---

## Next Steps

For related topics, see:
- [Context Patterns Guide](./context_patterns.md) - Complete Context API reference
- [Structured Output Guide](./structured_output.md) - Deep dive into structured output
- [Error Handling Guide](./error_handling.md) - Comprehensive error patterns
- [Pydantic Patterns Guide](./pydantic_patterns.md) - Advanced Pydantic usage
- [Media Handling Guide](./media_handling.md) - Image, Audio, File classes

---

**End of Tools Complete Guide**
