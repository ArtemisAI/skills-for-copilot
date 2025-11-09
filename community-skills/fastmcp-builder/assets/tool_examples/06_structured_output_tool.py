"""
Example 6: Structured Output and ToolResult

This example demonstrates:
- Using ToolResult for full control over responses
- Structured output (v2.10.0+)
- Multiple content blocks
- Media handling (images, files)
- Metadata inclusion
"""

from typing import Literal
from pathlib import Path
from fastmcp import FastMCP, Context
from fastmcp.utilities.types import ToolResult, Image

mcp = FastMCP("structured-output-example")


@mcp.tool()
async def analyze_data(
    data: list[float],
    output_format: Literal["summary", "detailed"] = "summary",
    ctx: Context | None = None
) -> ToolResult:
    """
    Analyze numerical data with structured output.

    Args:
        data: List of numbers to analyze
        output_format: Level of detail in output
        ctx: Request context for logging

    Returns:
        ToolResult with analysis in both human and structured formats
    """
    if ctx:
        await ctx.info(f"Analyzing {len(data)} data points")

    # Perform analysis
    mean = sum(data) / len(data)
    minimum = min(data)
    maximum = max(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5

    # Human-readable summary
    if output_format == "summary":
        human_text = f"""Data Analysis Summary:
- Count: {len(data)}
- Mean: {mean:.2f}
- Range: {minimum:.2f} to {maximum:.2f}
- Std Dev: {std_dev:.2f}"""
    else:
        human_text = f"""Detailed Data Analysis:
- Data points: {len(data)}
- Mean (average): {mean:.2f}
- Median: {sorted(data)[len(data)//2]:.2f}
- Minimum: {minimum:.2f}
- Maximum: {maximum:.2f}
- Range: {maximum - minimum:.2f}
- Variance: {variance:.2f}
- Standard Deviation: {std_dev:.2f}"""

    # Structured data for programmatic use
    structured_data = {
        "count": len(data),
        "mean": mean,
        "median": sorted(data)[len(data)//2],
        "min": minimum,
        "max": maximum,
        "std_dev": std_dev,
        "variance": variance
    }

    return ToolResult(
        content=[human_text],
        structured_content=structured_data,
        meta={"analysis_type": output_format}
    )


@mcp.tool()
async def generate_report(
    title: str,
    sections: list[str],
    include_chart: bool = False,
    ctx: Context | None = None
) -> ToolResult:
    """
    Generate a report with multiple content blocks.

    Args:
        title: Report title
        sections: Section names to include
        include_chart: Whether to include a chart (mock)
        ctx: Request context for logging

    Returns:
        ToolResult with report text and optional chart
    """
    if ctx:
        await ctx.info(f"Generating report: {title}")

    content_blocks = []

    # Title and summary
    content_blocks.append(f"# {title}\n\nGenerated Report\n")

    # Sections
    for i, section in enumerate(sections, 1):
        content_blocks.append(f"## {i}. {section}\n\nContent for {section} section...\n")

    # Structured metadata
    structured_data = {
        "title": title,
        "sections": sections,
        "section_count": len(sections),
        "has_chart": include_chart
    }

    # Add mock chart if requested
    # In production, this would be a real generated image
    if include_chart:
        # Note: This is a placeholder - in production, generate real chart
        content_blocks.append("[Chart would be included here]")
        structured_data["chart_type"] = "bar"

    if ctx:
        await ctx.info("Report generated successfully")

    return ToolResult(
        content=content_blocks,
        structured_content=structured_data,
        meta={
            "format": "markdown",
            "version": "1.0"
        }
    )


@mcp.tool()
async def process_with_status(
    items: list[str],
    ctx: Context | None = None
) -> ToolResult:
    """
    Process items and return detailed status.

    Args:
        items: Items to process
        ctx: Request context for logging

    Returns:
        ToolResult with processing results and detailed metadata
    """
    if ctx:
        await ctx.info(f"Processing {len(items)} items")

    successful = []
    failed = []

    for item in items:
        # Simulate processing
        if len(item) > 0:  # Simple validation
            successful.append(item)
        else:
            failed.append(item)

    # Human-readable summary
    summary = f"""Processing Results:
✓ Successful: {len(successful)}
✗ Failed: {len(failed)}

Success rate: {len(successful)/len(items)*100:.1f}%"""

    # Structured results
    structured = {
        "total": len(items),
        "successful": len(successful),
        "failed": len(failed),
        "success_rate": len(successful) / len(items),
        "successful_items": successful,
        "failed_items": failed
    }

    # Metadata about processing
    metadata = {
        "processor_version": "1.0",
        "validation_rules": ["non_empty"],
        "timestamp": "2025-01-15T10:30:00Z"
    }

    return ToolResult(
        content=[summary],
        structured_content=structured,
        meta=metadata
    )


@mcp.tool()
async def multi_format_output(
    query: str,
    include_json: bool = True,
    include_markdown: bool = True,
    ctx: Context | None = None
) -> ToolResult:
    """
    Return data in multiple formats.

    Args:
        query: Query to process
        include_json: Include JSON format in output
        include_markdown: Include Markdown format in output
        ctx: Request context for logging

    Returns:
        ToolResult with multiple content formats
    """
    if ctx:
        await ctx.info(f"Processing query: {query}")

    # Generate data
    data = {
        "query": query,
        "results": [
            {"id": 1, "title": "Result 1", "score": 0.95},
            {"id": 2, "title": "Result 2", "score": 0.87},
            {"id": 3, "title": "Result 3", "score": 0.76}
        ],
        "total": 3
    }

    content_blocks = []

    # Markdown format
    if include_markdown:
        markdown = f"""# Results for: {query}

Found {data['total']} results:

1. **{data['results'][0]['title']}** (Score: {data['results'][0]['score']})
2. **{data['results'][1]['title']}** (Score: {data['results'][1]['score']})
3. **{data['results'][2]['title']}** (Score: {data['results'][2]['score']})
"""
        content_blocks.append(markdown)

    # JSON format
    if include_json:
        import json
        json_output = json.dumps(data, indent=2)
        content_blocks.append(f"```json\n{json_output}\n```")

    return ToolResult(
        content=content_blocks,
        structured_content=data,
        meta={
            "formats": {
                "markdown": include_markdown,
                "json": include_json
            }
        }
    )


@mcp.tool()
async def validation_result(
    input_data: dict,
    ctx: Context | None = None
) -> ToolResult:
    """
    Validate input and return detailed validation result.

    Args:
        input_data: Data to validate
        ctx: Request context for logging

    Returns:
        ToolResult with validation status and details
    """
    if ctx:
        await ctx.info("Validating input data")

    errors = []
    warnings = []

    # Validation rules
    required_fields = ["name", "email", "age"]

    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")

    if "email" in input_data and "@" not in input_data["email"]:
        errors.append("Invalid email format")

    if "age" in input_data:
        if not isinstance(input_data["age"], int):
            errors.append("Age must be an integer")
        elif input_data["age"] < 0:
            errors.append("Age cannot be negative")
        elif input_data["age"] < 18:
            warnings.append("Age is below 18")

    # Generate result
    is_valid = len(errors) == 0
    status = "✓ Valid" if is_valid else "✗ Invalid"

    human_text = f"""Validation Result: {status}

Errors: {len(errors)}
Warnings: {len(warnings)}
"""

    if errors:
        human_text += "\nErrors:\n" + "\n".join(f"- {e}" for e in errors)

    if warnings:
        human_text += "\nWarnings:\n" + "\n".join(f"- {w}" for w in warnings)

    structured = {
        "valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings)
    }

    return ToolResult(
        content=[human_text],
        structured_content=structured,
        meta={
            "validator_version": "1.0",
            "rules_applied": required_fields
        }
    )


if __name__ == "__main__":
    mcp.run()
