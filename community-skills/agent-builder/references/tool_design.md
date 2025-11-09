# Tool Design Guide

## Overview

Tools are the primary building blocks for agent execution. Well-designed tools enable agents to accomplish complex tasks efficiently, while poorly designed tools lead to confusion, errors, and wasted context.

## Core Principles

### 1. Build for Workflows, Not Just API Endpoints

**Don't:** Simply wrap existing API endpoints one-to-one

```python
@tool("get_calendar", "Get calendar")
async def get_calendar(args): ...

@tool("check_availability", "Check availability")
async def check_availability(args): ...

@tool("create_event", "Create event")
async def create_event(args): ...
```

**Do:** Consolidate related operations into workflow tools

```python
@tool(
    "schedule_meeting",
    "Check availability and schedule a meeting in one operation",
    {
        "attendees": list[str],
        "duration_minutes": int,
        "preferred_times": list[str],
        "title": str
    }
)
async def schedule_meeting(args):
    """
    This tool:
    1. Checks availability for all attendees
    2. Finds the best time slot
    3. Creates the calendar event
    4. Sends invitations

    Returns the scheduled time and event ID.
    """
    # Implementation that handles the full workflow
    ...
```

**Why:** Agents can accomplish complete tasks in fewer steps, reducing context usage and API calls.

### 2. Optimize for Limited Context

Agents operate under strict context limits. Every token matters.

**Don't:** Return exhaustive data dumps

```python
@tool("list_issues", "List GitHub issues")
async def list_issues(args):
    # Returns ALL issues with FULL details
    issues = fetch_all_issues()
    return {"content": [{"type": "text", "text": json.dumps(issues)}]}
```

**Do:** Provide concise summaries by default, detailed on demand

```python
@tool(
    "list_issues",
    "List GitHub issues with configurable detail level",
    {
        "state": Literal["open", "closed", "all"],
        "limit": int,
        "detail": Literal["concise", "detailed"],
        "filter": str  # e.g., "label:bug", "assignee:@me"
    }
)
async def list_issues(args):
    """
    Returns issues in the requested format:
    - concise: ID, title, state (default)
    - detailed: Above plus description, labels, assignee, timestamps
    """
    issues = fetch_issues(args["state"], args.get("limit", 20), args.get("filter"))

    if args.get("detail", "concise") == "concise":
        summary = [f"#{i.number}: {i.title} ({i.state})" for i in issues]
        return {"content": [{"type": "text", "text": "\n".join(summary)}]}
    else:
        # Return detailed information
        ...
```

**Why:** Concise responses conserve context. Agents can request details when needed.

### 3. Design Actionable Error Messages

Error messages should guide agents toward correct usage.

**Don't:** Provide cryptic or generic errors

```python
return {"error": "Invalid request"}
return {"error": "Error 400"}
return {"error": "Something went wrong"}
```

**Do:** Provide specific, actionable guidance

```python
if not args.get("attendees"):
    return {
        "content": [{
            "type": "text",
            "text": "Error: 'attendees' parameter is required. Provide a list of email addresses, e.g., ['alice@example.com', 'bob@example.com']"
        }]
    }

if len(results) > 1000:
    return {
        "content": [{
            "type": "text",
            "text": f"Error: Query returned {len(results)} results, exceeding the 1000 limit. Try using filters to narrow the search:\n- filter='state:open' for open items only\n- filter='label:bug' for bugs only\n- Set a lower limit parameter (currently {args.get('limit', 'unlimited')})"
        }]
    }
```

**Why:** Clear errors help agents self-correct without human intervention.

### 4. Use Human-Readable Identifiers

**Don't:** Force agents to work with opaque technical IDs

```python
# Agent must remember: issue_id="ISS-2847392", project_id="PROJ-8392847"
@tool("update_issue", "Update issue", {"issue_id": str, "project_id": str})
```

**Do:** Accept human-readable identifiers and resolve them internally

```python
@tool(
    "update_issue",
    "Update an issue by title or ID",
    {
        "identifier": str,  # Can be "Fix login bug" or "ISS-123"
        "project": str,  # Can be "Frontend" or "PROJ-456"
        "updates": dict
    }
)
async def update_issue(args):
    """
    Accepts natural identifiers:
    - identifier: Issue title (e.g., "Fix login bug") or ID (e.g., "ISS-123")
    - project: Project name (e.g., "Frontend") or ID (e.g., "PROJ-456")

    Automatically resolves to technical IDs internally.
    """
    issue = resolve_issue(args["identifier"], args["project"])
    ...
```

**Why:** Natural identifiers are easier for agents to work with and remember.

### 5. Follow Natural Task Subdivisions

Group tools by how humans think about tasks.

**Don't:** Organize by technical implementation

```bash
api_get_user()
api_post_user()
api_delete_user()
database_query_user()
cache_get_user()
```

**Do:** Organize by user-facing tasks

```bash
# User management
create_user()
update_user()
deactivate_user()
find_users()

# User authentication
authenticate_user()
reset_password()
verify_email()
```

**Why:** Intuitive organization makes tools discoverable and easier to use correctly.

## Input Schema Design

### Use Strong Typing

**Python with Type Hints:**

```python
from typing import Literal, Optional
from enum import Enum

@tool(
    "analyze_sentiment",
    "Analyze sentiment of text",
    {
        "text": str,
        "language": Literal["en", "es", "fr", "de"],
        "detail_level": Literal["basic", "advanced"],
        "include_emotions": bool
    }
)
```

### Provide Comprehensive Descriptions

**Don't:** Minimal descriptions

```python
{
    "text": str,  # No description
    "threshold": float  # What threshold?
}
```

**Do:** Detailed descriptions with examples

```python
{
    "text": {
        "type": "string",
        "description": "The text to analyze. Can be a sentence, paragraph, or full document. Example: 'The customer service was excellent and the product exceeded expectations.'"
    },
    "confidence_threshold": {
        "type": "number",
        "description": "Minimum confidence score (0.0 to 1.0) for sentiment classification. Results below this threshold will be marked as 'uncertain'. Default: 0.7. Example: 0.85 for high-confidence results only."
    }
}
```

### Include Validation and Constraints

```python
{
    "email": {
        "type": "string",
        "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "description": "Valid email address"
    },
    "age": {
        "type": "integer",
        "minimum": 0,
        "maximum": 150,
        "description": "Person's age in years"
    },
    "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "critical"],
        "description": "Task priority level"
    }
}
```

## Output Format Design

### Return Structured Data

**Don't:** Return unstructured text

```python
return {
    "content": [{
        "type": "text",
        "text": "Found 3 issues. Issue 1 is critical. Issue 2 is medium severity..."
    }]
}
```

**Do:** Return parseable structured data

```python
result = {
    "summary": {
        "total": 3,
        "critical": 1,
        "high": 0,
        "medium": 2,
        "low": 0
    },
    "issues": [
        {
            "id": "ISS-123",
            "title": "SQL injection vulnerability",
            "severity": "critical",
            "location": "auth.py:45"
        },
        # ... more issues
    ]
}

return {
    "content": [{
        "type": "text",
        "text": json.dumps(result, indent=2)
    }]
}
```

### Provide Multiple Format Options

```python
@tool(
    "generate_report",
    "Generate analysis report",
    {
        "data": dict,
        "format": Literal["json", "markdown", "html"]
    }
)
async def generate_report(args):
    data = args["data"]
    output_format = args.get("format", "json")

    if output_format == "json":
        return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}

    elif output_format == "markdown":
        markdown = convert_to_markdown(data)
        return {"content": [{"type": "text", "text": markdown}]}

    elif output_format == "html":
        html = convert_to_html(data)
        return {"content": [{"type": "text", "text": html}]}
```

## Tool Documentation

### Write Comprehensive Docstrings

```python
@tool(
    "search_codebase",
    "Search codebase using semantic or regex search",
    {
        "query": str,
        "search_type": Literal["semantic", "regex"],
        "file_pattern": str,
        "max_results": int
    }
)
async def search_codebase(args):
    """
    Search the codebase using semantic understanding or regex patterns.

    This tool provides two search modes:
    1. Semantic: Uses embeddings to find conceptually similar code
    2. Regex: Uses pattern matching for precise text search

    Parameters:
    - query: Search query or regex pattern
        Example (semantic): "functions that handle authentication"
        Example (regex): "def.*authenticate.*\\(.*\\):"
    - search_type: "semantic" for concept search, "regex" for pattern matching
    - file_pattern: Glob pattern to filter files (e.g., "**/*.py")
    - max_results: Maximum number of results (default: 20, max: 100)

    Returns:
    JSON object with:
    - results: List of matches with file path, line number, and context
    - total_matches: Total number of matches found
    - truncated: Boolean indicating if results were limited

    Error handling:
    - If query is too broad (>1000 matches), returns error with suggestion to narrow search
    - If no matches found, suggests similar queries
    - If regex is invalid, returns error with syntax help

    Performance notes:
    - Semantic search: ~2-5 seconds for medium codebases
    - Regex search: ~0.5-2 seconds for medium codebases
    - Use file_pattern to improve performance on large codebases

    Examples:
    1. Find authentication code:
       search_codebase("authentication functions", "semantic", "**/*.py", 10)

    2. Find all TODO comments:
       search_codebase("# TODO:", "regex", "**/*", 50)

    3. Find specific function definition:
       search_codebase("def calculate_total\\(", "regex", "**/*.py", 20)
    """
    # Implementation
    ...
```

## Common Tool Patterns

### Pagination Pattern

```python
@tool(
    "list_items",
    "List items with pagination support",
    {
        "page": int,
        "page_size": int,
        "cursor": str  # Optional: for cursor-based pagination
    }
)
async def list_items(args):
    page = args.get("page", 1)
    page_size = min(args.get("page_size", 20), 100)  # Cap at 100

    items, next_cursor = fetch_items(page, page_size)

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "items": items,
                "page": page,
                "page_size": page_size,
                "has_more": next_cursor is not None,
                "next_cursor": next_cursor,
                "hint": "Use next_cursor parameter to fetch the next page"
            })
        }]
    }
```

### Filtering Pattern

```python
@tool(
    "search_items",
    "Search items with advanced filtering",
    {
        "filters": dict,  # {"status": "active", "priority": ["high", "critical"]}
        "sort_by": str,
        "sort_order": Literal["asc", "desc"]
    }
)
async def search_items(args):
    filters = args.get("filters", {})
    sort_by = args.get("sort_by", "created_at")
    sort_order = args.get("sort_order", "desc")

    # Parse filters
    query = build_query(filters)
    items = execute_query(query, sort_by, sort_order)

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "items": items,
                "total": len(items),
                "filters_applied": filters,
                "available_filters": ["status", "priority", "assignee", "label"]
            })
        }]
    }
```

### Batch Operations Pattern

```python
@tool(
    "process_items",
    "Process multiple items in batch",
    {
        "item_ids": list[str],
        "operation": Literal["update", "delete", "archive"],
        "parameters": dict
    }
)
async def process_items(args):
    item_ids = args["item_ids"]
    operation = args["operation"]
    params = args.get("parameters", {})

    results = []
    errors = []

    for item_id in item_ids:
        try:
            result = perform_operation(item_id, operation, params)
            results.append({"id": item_id, "status": "success", "result": result})
        except Exception as e:
            errors.append({"id": item_id, "status": "error", "error": str(e)})

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "processed": len(results),
                "failed": len(errors),
                "results": results,
                "errors": errors
            })
        }]
    }
```

## Testing Tools

### Unit Test Tools Independently

```python
# test_tools.py
import pytest
from your_agent import analyze_sentiment

@pytest.mark.asyncio
async def test_sentiment_analysis_positive():
    result = await analyze_sentiment({
        "text": "This product is amazing!",
        "language": "en",
        "detail_level": "basic",
        "include_emotions": False
    })

    data = json.loads(result["content"][0]["text"])
    assert data["sentiment"] == "positive"
    assert 0.7 <= data["confidence"] <= 1.0

@pytest.mark.asyncio
async def test_sentiment_analysis_error_handling():
    result = await analyze_sentiment({
        "text": "",  # Empty text should trigger error
        "language": "en"
    })

    text = result["content"][0]["text"]
    assert "Error" in text
    assert "text" in text.lower()
```

### Integration Test with Agent

```python
@pytest.mark.asyncio
async def test_agent_uses_tool_correctly():
    client = ClaudeSDKClient(
        system_prompt="You are a sentiment analyzer.",
        tools=[analyze_sentiment]
    )

    response = await client.send_message(
        "Analyze the sentiment of: 'The service was terrible and I'm very disappointed'"
    )

    # Verify agent called tool and interpreted results
    assert "negative" in response.lower()
```

## Performance Optimization

### Cache Expensive Operations

```python
from functools import lru_cache
import asyncio

# Cache results for 5 minutes
_cache = {}
_cache_ttl = 300

@tool("fetch_data", "Fetch data with caching")
async def fetch_data(args):
    cache_key = f"{args['query']}-{args.get('filter', 'none')}"

    # Check cache
    if cache_key in _cache:
        cached_result, timestamp = _cache[cache_key]
        if time.time() - timestamp < _cache_ttl:
            return cached_result

    # Fetch fresh data
    result = await expensive_api_call(args)

    # Update cache
    _cache[cache_key] = (result, time.time())

    return result
```

### Implement Timeouts

```python
import asyncio

@tool("long_running_operation", "Operation with timeout")
async def long_running_operation(args):
    timeout = args.get("timeout", 30)  # Default 30 seconds

    try:
        result = await asyncio.wait_for(
            perform_operation(args),
            timeout=timeout
        )
        return result

    except asyncio.TimeoutError:
        return {
            "content": [{
                "type": "text",
                "text": f"Error: Operation timed out after {timeout} seconds. Try increasing the timeout parameter or simplifying the request."
            }]
        }
```

## Security Considerations

### Validate All Inputs

```python
@tool("execute_query", "Execute database query with validation")
async def execute_query(args):
    query = args["query"]

    # Validate query for SQL injection
    dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "GRANT"]
    if any(keyword in query.upper() for keyword in dangerous_keywords):
        return {
            "content": [{
                "type": "text",
                "text": "Error: Query contains potentially dangerous keywords. This tool only supports SELECT queries for safety."
            }]
        }

    # Parameterized query execution
    result = execute_safe_query(query, args.get("parameters", {}))
    return result
```

### Implement Rate Limiting

```python
from collections import defaultdict
import time

_rate_limits = defaultdict(list)
_max_calls_per_minute = 60

@tool("api_call", "Rate-limited API call")
async def api_call(args):
    user_id = args.get("user_id", "default")

    # Check rate limit
    now = time.time()
    _rate_limits[user_id] = [t for t in _rate_limits[user_id] if now - t < 60]

    if len(_rate_limits[user_id]) >= _max_calls_per_minute:
        return {
            "content": [{
                "type": "text",
                "text": f"Error: Rate limit exceeded. Maximum {_max_calls_per_minute} calls per minute. Try again in {60 - (now - _rate_limits[user_id][0]):.0f} seconds."
            }]
        }

    # Record this call
    _rate_limits[user_id].append(now)

    # Proceed with API call
    result = await make_api_call(args)
    return result
```
