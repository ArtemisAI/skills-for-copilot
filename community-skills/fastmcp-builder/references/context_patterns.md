# Context Injection Patterns

This guide provides comprehensive documentation for using `Context` injection in FastMCP, which enables tools, resources, and prompts to access logging, progress reporting, LLM sampling, and request metadata.

---

## Table of Contents

1. [Overview](#overview)
2. [Injecting Context](#injecting-context)
3. [Logging Methods](#logging-methods)
4. [Progress Reporting](#progress-reporting)
5. [Sampling (LLM Calls)](#sampling-llm-calls)
6. [Request Metadata](#request-metadata)
7. [Common Patterns](#common-patterns)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Overview

**Context** is a special object that FastMCP can automatically inject into your tools, resources, and prompts. It provides access to:

- **Logging**: Send log messages to the client (info, warn, error, debug)
- **Progress**: Report progress updates for long-running operations
- **Sampling**: Call the LLM from within your tool
- **Metadata**: Access request information

**Why Use Context:**
- **Observability**: Track what your tools are doing
- **User feedback**: Keep users informed during long operations
- **LLM integration**: Let tools make LLM calls for complex decisions
- **Debugging**: Detailed logging for troubleshooting

---

## Injecting Context

### Basic Injection

Add a parameter with type hint `Context` to any tool, resource, or prompt function.

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("my-server")

@mcp.tool()
async def my_tool(query: str, ctx: Context) -> str:
    """
    Example tool with context injection.

    Args:
        query: User query
        ctx: Request context (automatically injected)

    Returns:
        Result
    """
    await ctx.info(f"Processing query: {query}")
    result = process_query(query)
    await ctx.info("Query processed successfully")
    return result
```

**Key Points:**
- Parameter name can be anything, but `ctx` is conventional
- Type hint **must** be `Context` for injection to work
- Context is automatically provided by FastMCP
- Don't include context in function calls - it's injected
- Works with tools, resources, and prompts

### Parameter Position

Context can be at any position in the parameter list.

```python
# Context first
@mcp.tool()
async def tool1(ctx: Context, query: str) -> str:
    await ctx.info("Starting")
    return query

# Context last (most common)
@mcp.tool()
async def tool2(query: str, ctx: Context) -> str:
    await ctx.info("Starting")
    return query

# Context in middle
@mcp.tool()
async def tool3(query: str, ctx: Context, limit: int = 10) -> str:
    await ctx.info("Starting")
    return query
```

### Async Requirement

Context methods are async and must be awaited.

```python
# ✓ Correct - Async function, await context methods
@mcp.tool()
async def correct_tool(query: str, ctx: Context) -> str:
    await ctx.info("Processing")
    return "Done"

# ✗ Wrong - Sync function can't await
@mcp.tool()
def wrong_tool(query: str, ctx: Context) -> str:
    await ctx.info("This won't work")  # SyntaxError
    return "Done"

# ✓ Workaround - If you must use sync, don't inject Context
@mcp.tool()
def sync_tool(query: str) -> str:
    # No logging available in sync functions
    return "Done"
```

---

## Logging Methods

Context provides four logging levels for different message types.

### ctx.info()

**Use for:** General informational messages about normal operation.

```python
@mcp.tool()
async def fetch_data(url: str, ctx: Context) -> dict:
    """Fetch data from API with logging."""
    await ctx.info(f"Fetching data from {url}")

    response = await http_client.get(url)

    await ctx.info(f"Received {len(response.data)} items")

    return response.data
```

### ctx.warn()

**Use for:** Warnings about potential issues that don't prevent operation.

```python
@mcp.tool()
async def process_items(items: list[str], ctx: Context) -> dict:
    """Process items with warnings for issues."""
    results = []
    errors = []

    for item in items:
        try:
            result = process_item(item)
            results.append(result)
        except ValueError as e:
            await ctx.warn(f"Skipping invalid item '{item}': {e}")
            errors.append(item)

    if errors:
        await ctx.warn(f"Skipped {len(errors)} invalid items")

    return {"results": results, "errors": errors}
```

### ctx.error()

**Use for:** Error messages for failures that prevent normal operation.

```python
@mcp.tool()
async def critical_operation(id: str, ctx: Context) -> str:
    """Perform critical operation with error handling."""
    await ctx.info(f"Starting critical operation for ID: {id}")

    try:
        result = await perform_operation(id)
        await ctx.info("Operation completed successfully")
        return result

    except DatabaseError as e:
        await ctx.error(f"Database error: {e}")
        raise

    except Exception as e:
        await ctx.error(f"Unexpected error: {e}")
        raise
```

### ctx.debug()

**Use for:** Detailed debugging information (verbose mode).

```python
@mcp.tool()
async def complex_calculation(data: dict, ctx: Context) -> float:
    """Complex calculation with debug logging."""
    await ctx.debug(f"Input data: {data}")

    step1 = calculate_step1(data)
    await ctx.debug(f"Step 1 result: {step1}")

    step2 = calculate_step2(step1)
    await ctx.debug(f"Step 2 result: {step2}")

    final = calculate_final(step2)
    await ctx.debug(f"Final result: {final}")

    await ctx.info(f"Calculation complete: {final}")

    return final
```

### Logging Levels in Practice

```python
@mcp.tool()
async def data_sync(source: str, destination: str, ctx: Context) -> dict:
    """
    Sync data between source and destination with comprehensive logging.

    Args:
        source: Source location
        destination: Destination location
        ctx: Request context

    Returns:
        Sync statistics
    """
    await ctx.info(f"Starting sync: {source} → {destination}")
    await ctx.debug(f"Sync configuration: {get_config()}")

    # Fetch source data
    try:
        source_data = await fetch_data(source)
        await ctx.info(f"Fetched {len(source_data)} items from source")
        await ctx.debug(f"Source data sample: {source_data[:2]}")
    except Exception as e:
        await ctx.error(f"Failed to fetch source data: {e}")
        raise

    # Validate data
    invalid_items = validate_data(source_data)
    if invalid_items:
        await ctx.warn(f"Found {len(invalid_items)} invalid items - skipping")
        await ctx.debug(f"Invalid items: {invalid_items}")

    # Sync to destination
    try:
        synced_count = await sync_to_destination(source_data, destination)
        await ctx.info(f"Successfully synced {synced_count} items")
    except Exception as e:
        await ctx.error(f"Sync failed: {e}")
        raise

    return {
        "total": len(source_data),
        "synced": synced_count,
        "skipped": len(invalid_items)
    }
```

---

## Progress Reporting

Use `ctx.report_progress()` to provide progress updates for long-running operations.

### Basic Progress Reporting

```python
@mcp.tool()
async def process_large_dataset(items: list[str], ctx: Context) -> dict:
    """
    Process large dataset with progress reporting.

    Args:
        items: Items to process
        ctx: Request context

    Returns:
        Processing results
    """
    total = len(items)
    results = []

    await ctx.info(f"Processing {total} items")

    for i, item in enumerate(items, start=1):
        # Report progress
        await ctx.report_progress(
            progress=i,
            total=total
        )

        # Process item
        result = await process_item(item)
        results.append(result)

        # Log milestone
        if i % 100 == 0:
            await ctx.info(f"Processed {i}/{total} items")

    await ctx.info("Processing complete")

    return {"processed": len(results), "results": results}
```

### Progress with Status Messages

```python
@mcp.tool()
async def multi_stage_operation(data: dict, ctx: Context) -> str:
    """Multi-stage operation with progress and status."""

    # Stage 1: Validation
    await ctx.report_progress(progress=1, total=4)
    await ctx.info("Stage 1/4: Validating data")
    validate(data)

    # Stage 2: Processing
    await ctx.report_progress(progress=2, total=4)
    await ctx.info("Stage 2/4: Processing data")
    processed = process(data)

    # Stage 3: Saving
    await ctx.report_progress(progress=3, total=4)
    await ctx.info("Stage 3/4: Saving results")
    save(processed)

    # Stage 4: Cleanup
    await ctx.report_progress(progress=4, total=4)
    await ctx.info("Stage 4/4: Cleanup")
    cleanup()

    return "Operation complete"
```

### Progress for Batch Operations

```python
import asyncio

@mcp.tool()
async def batch_api_calls(urls: list[str], ctx: Context) -> list[dict]:
    """
    Make batch API calls with progress tracking.

    Args:
        urls: URLs to fetch
        ctx: Request context

    Returns:
        Fetched data
    """
    total = len(urls)
    completed = 0
    results = []

    await ctx.info(f"Fetching data from {total} URLs")

    # Process in batches of 10
    batch_size = 10
    for i in range(0, total, batch_size):
        batch = urls[i:i + batch_size]

        # Fetch batch concurrently
        batch_results = await asyncio.gather(
            *[fetch_url(url) for url in batch],
            return_exceptions=True
        )

        results.extend(batch_results)
        completed += len(batch)

        # Report progress
        await ctx.report_progress(progress=completed, total=total)
        await ctx.info(f"Completed {completed}/{total} requests")

    return results
```

---

## Sampling (LLM Calls)

Use `ctx.sample()` to make LLM calls from within your tools. This enables tools to use the LLM's reasoning capabilities for complex decisions.

### Basic Sampling

```python
@mcp.tool()
async def analyze_text(text: str, ctx: Context) -> str:
    """
    Analyze text using LLM.

    Args:
        text: Text to analyze
        ctx: Request context

    Returns:
        Analysis result
    """
    await ctx.info("Analyzing text with LLM")

    # Call the LLM
    response = await ctx.sample(
        messages=[
            {
                "role": "user",
                "content": f"Analyze the sentiment of this text: {text}"
            }
        ],
        max_tokens=100
    )

    analysis = response.content
    await ctx.info("Analysis complete")

    return analysis
```

### Sampling with System Prompts

```python
@mcp.tool()
async def code_review(code: str, language: str, ctx: Context) -> str:
    """
    Review code using LLM.

    Args:
        code: Code to review
        language: Programming language
        ctx: Request context

    Returns:
        Code review
    """
    await ctx.info(f"Reviewing {language} code")

    response = await ctx.sample(
        messages=[
            {
                "role": "system",
                "content": f"You are an expert {language} code reviewer."
            },
            {
                "role": "user",
                "content": f"Review this code:\n\n```{language}\n{code}\n```"
            }
        ],
        max_tokens=500
    )

    return response.content
```

### Multi-Turn Sampling

```python
@mcp.tool()
async def interactive_analysis(topic: str, ctx: Context) -> dict:
    """
    Perform interactive analysis with multiple LLM calls.

    Args:
        topic: Topic to analyze
        ctx: Request context

    Returns:
        Comprehensive analysis
    """
    results = {}

    # Step 1: Initial analysis
    await ctx.info("Step 1: Initial analysis")
    response1 = await ctx.sample(
        messages=[
            {"role": "user", "content": f"What are the key aspects of {topic}?"}
        ],
        max_tokens=200
    )
    results["key_aspects"] = response1.content

    # Step 2: Deep dive based on initial analysis
    await ctx.info("Step 2: Deep dive")
    response2 = await ctx.sample(
        messages=[
            {"role": "user", "content": f"What are the key aspects of {topic}?"},
            {"role": "assistant", "content": response1.content},
            {"role": "user", "content": "Explain the most important aspect in detail."}
        ],
        max_tokens=300
    )
    results["deep_dive"] = response2.content

    # Step 3: Recommendations
    await ctx.info("Step 3: Recommendations")
    response3 = await ctx.sample(
        messages=[
            {"role": "user", "content": f"Based on the analysis of {topic}, provide 3 actionable recommendations."}
        ],
        max_tokens=200
    )
    results["recommendations"] = response3.content

    return results
```

### Sampling for Decision Making

```python
@mcp.tool()
async def smart_categorize(items: list[str], ctx: Context) -> dict[str, list[str]]:
    """
    Categorize items using LLM intelligence.

    Args:
        items: Items to categorize
        ctx: Request context

    Returns:
        Categorized items
    """
    await ctx.info(f"Categorizing {len(items)} items using LLM")

    # Ask LLM to categorize
    items_text = "\n".join(f"- {item}" for item in items)

    response = await ctx.sample(
        messages=[
            {
                "role": "system",
                "content": "You categorize items into logical groups."
            },
            {
                "role": "user",
                "content": f"""Categorize these items into logical groups.
Return JSON with categories as keys and arrays of items as values.

Items:
{items_text}"""
            }
        ],
        max_tokens=500
    )

    # Parse LLM response
    import json
    categories = json.loads(response.content)

    await ctx.info(f"Created {len(categories)} categories")

    return categories
```

---

## Request Metadata

Access metadata about the current request through the Context object.

### Available Metadata

```python
@mcp.tool()
async def request_info(ctx: Context) -> dict:
    """
    Display available request metadata.

    Args:
        ctx: Request context

    Returns:
        Request information
    """
    # Note: Available metadata depends on FastMCP version
    # and may include:
    # - Request ID
    # - Client information
    # - Timestamp
    # - Server info

    info = {
        "context_available": ctx is not None,
        "context_type": type(ctx).__name__
    }

    await ctx.info(f"Request metadata: {info}")

    return info
```

---

## Common Patterns

### Pattern 1: Comprehensive Logging

```python
@mcp.tool()
async def data_pipeline(
    input_file: str,
    output_file: str,
    ctx: Context
) -> dict:
    """
    Data processing pipeline with comprehensive logging.

    Args:
        input_file: Input file path
        output_file: Output file path
        ctx: Request context

    Returns:
        Pipeline statistics
    """
    await ctx.info(f"Starting pipeline: {input_file} → {output_file}")
    start_time = time.time()

    try:
        # Load data
        await ctx.info("Loading input data")
        await ctx.debug(f"Input file: {input_file}")
        data = load_data(input_file)
        await ctx.info(f"Loaded {len(data)} records")

        # Validate
        await ctx.info("Validating data")
        invalid = validate_data(data)
        if invalid:
            await ctx.warn(f"Found {len(invalid)} invalid records")
            await ctx.debug(f"Invalid records: {invalid[:5]}")

        # Transform
        await ctx.info("Transforming data")
        transformed = transform_data(data)
        await ctx.debug(f"Transformation complete: {len(transformed)} records")

        # Save
        await ctx.info(f"Saving to {output_file}")
        save_data(transformed, output_file)

        elapsed = time.time() - start_time
        await ctx.info(f"Pipeline complete in {elapsed:.2f}s")

        return {
            "input_records": len(data),
            "output_records": len(transformed),
            "invalid_records": len(invalid),
            "duration_seconds": elapsed
        }

    except Exception as e:
        await ctx.error(f"Pipeline failed: {e}")
        await ctx.debug(f"Stack trace: {traceback.format_exc()}")
        raise
```

### Pattern 2: Progress for Long Operations

```python
@mcp.tool()
async def generate_reports(
    report_ids: list[str],
    ctx: Context
) -> list[str]:
    """
    Generate multiple reports with progress tracking.

    Args:
        report_ids: Report IDs to generate
        ctx: Request context

    Returns:
        Generated report paths
    """
    total = len(report_ids)
    generated = []

    await ctx.info(f"Generating {total} reports")

    for i, report_id in enumerate(report_ids, start=1):
        await ctx.report_progress(progress=i, total=total)
        await ctx.info(f"Generating report {i}/{total}: {report_id}")

        try:
            report_path = await generate_report(report_id)
            generated.append(report_path)
            await ctx.debug(f"Report saved: {report_path}")

        except Exception as e:
            await ctx.error(f"Failed to generate report {report_id}: {e}")
            # Continue with next report

    await ctx.info(f"Generated {len(generated)}/{total} reports")

    return generated
```

### Pattern 3: LLM-Assisted Processing

```python
@mcp.tool()
async def smart_extract(
    documents: list[str],
    fields: list[str],
    ctx: Context
) -> list[dict]:
    """
    Extract structured data from documents using LLM.

    Args:
        documents: Document texts
        fields: Fields to extract
        ctx: Request context

    Returns:
        Extracted data
    """
    results = []
    total = len(documents)

    await ctx.info(f"Extracting {len(fields)} fields from {total} documents")

    for i, doc in enumerate(documents, start=1):
        await ctx.report_progress(progress=i, total=total)

        # Use LLM to extract fields
        response = await ctx.sample(
            messages=[
                {
                    "role": "system",
                    "content": f"Extract the following fields from documents: {', '.join(fields)}"
                },
                {
                    "role": "user",
                    "content": f"Document:\n{doc}\n\nReturn JSON with extracted fields."
                }
            ],
            max_tokens=300
        )

        try:
            extracted = json.loads(response.content)
            results.append(extracted)
            await ctx.debug(f"Extracted: {extracted}")
        except json.JSONDecodeError as e:
            await ctx.warn(f"Failed to parse LLM response for document {i}: {e}")
            results.append({})

    await ctx.info(f"Extraction complete: {len(results)} results")

    return results
```

### Pattern 4: Error Recovery with Logging

```python
@mcp.tool()
async def resilient_fetch(
    urls: list[str],
    max_retries: int = 3,
    ctx: Context
) -> list[dict]:
    """
    Fetch URLs with retry logic and comprehensive logging.

    Args:
        urls: URLs to fetch
        max_retries: Maximum retry attempts
        ctx: Request context

    Returns:
        Fetched data
    """
    results = []

    for url in urls:
        await ctx.info(f"Fetching: {url}")

        for attempt in range(1, max_retries + 1):
            try:
                data = await fetch_url(url)
                results.append(data)
                await ctx.debug(f"Success on attempt {attempt}")
                break

            except Exception as e:
                if attempt < max_retries:
                    await ctx.warn(f"Attempt {attempt} failed: {e}. Retrying...")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    await ctx.error(f"Failed after {max_retries} attempts: {e}")
                    results.append({"error": str(e)})

    return results
```

---

## Best Practices

### 1. Log at Appropriate Levels

```python
# ✓ Good - Appropriate logging levels
@mcp.tool()
async def good_logging(data: str, ctx: Context) -> str:
    await ctx.info("Starting processing")  # Normal operation
    await ctx.debug(f"Input data: {data}")  # Verbose details
    await ctx.warn("Using default config")  # Potential issue
    # await ctx.error() only for actual errors
    return "Done"

# ✗ Bad - Everything is info
@mcp.tool()
async def bad_logging(data: str, ctx: Context) -> str:
    await ctx.info("Starting processing")
    await ctx.info(f"Input data: {data}")  # Should be debug
    await ctx.info("Using default config")  # Should be warn
    return "Done"
```

### 2. Report Progress for Long Operations

```python
# ✓ Good - Progress reporting
@mcp.tool()
async def good_progress(items: list, ctx: Context) -> int:
    for i, item in enumerate(items, 1):
        await ctx.report_progress(progress=i, total=len(items))
        process(item)
    return len(items)

# ✗ Bad - No progress feedback
@mcp.tool()
async def bad_progress(items: list, ctx: Context) -> int:
    for item in items:
        process(item)  # User has no idea what's happening
    return len(items)
```

### 3. Use Sampling Wisely

```python
# ✓ Good - Sampling for complex decisions
@mcp.tool()
async def good_sampling(text: str, ctx: Context) -> str:
    # Use LLM for sentiment analysis (complex)
    response = await ctx.sample(
        messages=[{"role": "user", "content": f"Sentiment: {text}"}],
        max_tokens=50
    )
    return response.content

# ✗ Bad - Sampling for simple operations
@mcp.tool()
async def bad_sampling(a: int, b: int, ctx: Context) -> int:
    # Don't use LLM for math!
    response = await ctx.sample(
        messages=[{"role": "user", "content": f"What is {a} + {b}?"}],
        max_tokens=10
    )
    return int(response.content)  # Just do: return a + b
```

### 4. Always Await Context Methods

```python
# ✓ Good - Awaiting async methods
@mcp.tool()
async def good_async(ctx: Context) -> str:
    await ctx.info("Message")  # Properly awaited
    return "Done"

# ✗ Bad - Forgetting to await
@mcp.tool()
async def bad_async(ctx: Context) -> str:
    ctx.info("Message")  # Returns coroutine, doesn't log!
    return "Done"
```

### 5. Handle Sampling Errors

```python
# ✓ Good - Error handling for sampling
@mcp.tool()
async def good_sampling_errors(text: str, ctx: Context) -> str:
    try:
        response = await ctx.sample(
            messages=[{"role": "user", "content": text}],
            max_tokens=100
        )
        return response.content
    except Exception as e:
        await ctx.error(f"Sampling failed: {e}")
        return "Analysis unavailable"

# ✗ Bad - No error handling
@mcp.tool()
async def bad_sampling_errors(text: str, ctx: Context) -> str:
    response = await ctx.sample(...)  # What if this fails?
    return response.content
```

---

## Troubleshooting

### Issue 1: Context is None

**Problem:** Context parameter is always None.

**Solutions:**
```python
# ✗ Wrong - Missing type hint
@mcp.tool()
async def wrong(query: str, ctx) -> str:  # No type hint
    await ctx.info("test")  # AttributeError

# ✓ Correct - Proper type hint
from fastmcp import Context

@mcp.tool()
async def correct(query: str, ctx: Context) -> str:
    await ctx.info("test")  # Works
    return "Done"
```

### Issue 2: Can't Await Context Methods

**Problem:** SyntaxError when trying to await context methods.

**Solutions:**
```python
# ✗ Wrong - Sync function
@mcp.tool()
def wrong(ctx: Context) -> str:
    await ctx.info("test")  # SyntaxError
    return "Done"

# ✓ Correct - Async function
@mcp.tool()
async def correct(ctx: Context) -> str:
    await ctx.info("test")  # Works
    return "Done"
```

### Issue 3: Progress Not Showing

**Problem:** Progress reports don't appear.

**Solutions:**
```python
# ✗ Wrong - Not awaiting report_progress
@mcp.tool()
async def wrong(items: list, ctx: Context) -> int:
    for i, item in enumerate(items, 1):
        ctx.report_progress(progress=i, total=len(items))  # Missing await
        process(item)
    return len(items)

# ✓ Correct - Await progress reports
@mcp.tool()
async def correct(items: list, ctx: Context) -> int:
    for i, item in enumerate(items, 1):
        await ctx.report_progress(progress=i, total=len(items))
        process(item)
    return len(items)
```

### Issue 4: Sampling Returns Unexpected Results

**Problem:** Sampling doesn't return expected format.

**Solutions:**
```python
# ✗ Wrong - Assuming response format
@mcp.tool()
async def wrong(text: str, ctx: Context) -> dict:
    response = await ctx.sample(
        messages=[{"role": "user", "content": f"Analyze: {text}"}],
        max_tokens=100
    )
    return response.content  # Might be string, not dict

# ✓ Correct - Parse and validate response
@mcp.tool()
async def correct(text: str, ctx: Context) -> dict:
    response = await ctx.sample(
        messages=[{
            "role": "user",
            "content": f"Analyze this and return JSON: {text}"
        }],
        max_tokens=100
    )

    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        await ctx.warn("LLM didn't return valid JSON")
        return {"error": "Invalid response format"}
```

---

## Summary

Context injection in FastMCP enables powerful observability, progress reporting, and LLM integration. Key takeaways:

1. **Use type hint `Context`** for automatic injection
2. **Always use async functions** when injecting context
3. **Await all context methods** (info, warn, error, debug, report_progress, sample)
4. **Log at appropriate levels** - info for normal, debug for verbose, warn for issues, error for failures
5. **Report progress** for long-running operations
6. **Use sampling wisely** for complex decisions, not simple operations
7. **Handle sampling errors** gracefully
8. **Provide detailed logging** to aid debugging and monitoring

Context injection makes your MCP tools more observable, user-friendly, and capable of leveraging LLM intelligence when needed.
