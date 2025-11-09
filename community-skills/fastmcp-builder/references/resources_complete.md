# Resources Complete Reference

This guide provides comprehensive documentation for the `@mcp.resource()` decorator in FastMCP, which enables you to expose dynamic data sources that provide context to LLM agents.

---

## Table of Contents

1. [Overview](#overview)
2. [The @resource Decorator](#the-resource-decorator)
3. [Decorator Parameters Reference](#decorator-parameters-reference)
4. [URI Patterns](#uri-patterns)
5. [Static vs Dynamic Resources](#static-vs-dynamic-resources)
6. [URI Templates with Parameters](#uri-templates-with-parameters)
7. [Return Types](#return-types)
8. [Resource Metadata](#resource-metadata)
9. [Context Injection](#context-injection)
10. [Async vs Sync](#async-vs-sync)
11. [Resource Management](#resource-management)
12. [Common Patterns](#common-patterns)
13. [Troubleshooting](#troubleshooting)

---

## Overview

**Resources** are dynamic data sources that provide context to LLM agents. Unlike tools (which perform actions), resources provide information that agents can read and use to make decisions.

**Key Characteristics:**
- **Read-only**: Resources provide data but don't modify state
- **URI-based**: Each resource is identified by a unique URI
- **Dynamic**: Can generate content on-demand based on parameters
- **Context providers**: Supply information for decision-making

**Common Use Cases:**
- Configuration data (API schemas, system settings)
- Dynamic content (user profiles, database records)
- Documentation (API docs, help text)
- File content (logs, data files)
- System state (server status, metrics)

---

## The @resource Decorator

The `@mcp.resource()` decorator converts a Python function into an MCP resource.

### Basic Syntax

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.resource("resource://server/info")
def server_info() -> str:
    """
    Provide server information.

    Returns:
        Server info as text
    """
    return "Server Version: 1.0.0\nStatus: Running"
```

### Full Decorator Signature

```python
@mcp.resource(
    uri: str,                              # Resource URI (required)
    name: str | None = None,               # Display name (optional)
    description: str | None = None,        # Description (optional)
    mime_type: str | None = None,          # MIME type (optional)
    enabled: bool = True,                  # Enable/disable resource
    _meta: dict | None = None              # Internal metadata
)
```

---

## Decorator Parameters Reference

### 1. `uri` (Required)

The unique identifier for the resource. Must follow URI conventions.

**Best Practices:**
- Use scheme prefixes: `resource://`, `file://`, `data://`, `config://`
- Use hierarchical structure: `resource://category/subcategory/item`
- Be descriptive and consistent
- Use lowercase with hyphens or underscores

**Examples:**
```python
# Good URIs
@mcp.resource("config://server/settings")
@mcp.resource("data://users/profile")
@mcp.resource("file://logs/application")
@mcp.resource("docs://api/endpoints")

# Poor URIs (too vague or inconsistent)
@mcp.resource("info")  # No scheme
@mcp.resource("SETTINGS")  # Uppercase inconsistent
@mcp.resource("x")  # Not descriptive
```

### 2. `name` (Optional)

Human-readable display name. If not provided, FastMCP derives it from the URI.

```python
@mcp.resource(
    "config://database/connection",
    name="Database Connection Configuration"
)
def db_config() -> str:
    return "host=localhost\nport=5432"
```

### 3. `description` (Optional)

Detailed description of what the resource provides. If not provided, uses the function's docstring.

```python
@mcp.resource(
    "data://users/active",
    description="List of currently active users with their last activity timestamps"
)
def active_users() -> str:
    return "user1: 2025-01-15 10:30\nuser2: 2025-01-15 10:25"
```

### 4. `mime_type` (Optional)

MIME type of the resource content. Common values:
- `text/plain` (default)
- `application/json`
- `text/markdown`
- `application/xml`
- `image/png`, `image/jpeg`
- `application/pdf`

```python
@mcp.resource(
    "docs://api/schema",
    mime_type="application/json"
)
def api_schema() -> str:
    import json
    schema = {"version": "1.0", "endpoints": [...]}
    return json.dumps(schema, indent=2)
```

### 5. `enabled` (Optional, Default: True)

Whether the resource is currently enabled. Useful for feature flags or conditional availability.

```python
FEATURE_ENABLED = os.getenv("ADVANCED_FEATURES") == "true"

@mcp.resource(
    "data://advanced/metrics",
    enabled=FEATURE_ENABLED
)
def advanced_metrics() -> str:
    return "Advanced metrics data..."
```

### 6. `_meta` (Optional, Internal)

Internal metadata for FastMCP framework use. Generally not used in application code.

---

## URI Patterns

### Static URIs

Resources with fixed URIs that don't change.

```python
@mcp.resource("config://app/settings")
def app_settings() -> str:
    """Application settings resource."""
    return "theme=dark\nlanguage=en\ntimezone=UTC"

@mcp.resource("docs://readme")
def readme() -> str:
    """Project README documentation."""
    with open("README.md") as f:
        return f.read()
```

### URI Hierarchies

Organize related resources using hierarchical URIs.

```python
# Server configuration hierarchy
@mcp.resource("config://server/database")
def db_config() -> str:
    return "Connection: postgresql://localhost/mydb"

@mcp.resource("config://server/cache")
def cache_config() -> str:
    return "Provider: Redis\nHost: localhost:6379"

@mcp.resource("config://server/logging")
def log_config() -> str:
    return "Level: INFO\nFormat: JSON"
```

### Scheme Conventions

Use appropriate URI schemes to categorize resources:

```python
# Configuration data
@mcp.resource("config://database/credentials")

# Static documents
@mcp.resource("docs://api/authentication")

# Dynamic data
@mcp.resource("data://users/list")

# File access
@mcp.resource("file://logs/application.log")

# System information
@mcp.resource("system://status")
```

---

## Static vs Dynamic Resources

### Static Resources

Resources that return the same content each time (or change infrequently).

```python
@mcp.resource("docs://api/overview")
def api_docs() -> str:
    """Static API documentation."""
    return """
# API Documentation

Version: 1.0.0

## Endpoints
- GET /users - List all users
- POST /users - Create user
"""
```

### Dynamic Resources

Resources that generate fresh content on each access.

```python
from datetime import datetime

@mcp.resource("data://system/status")
async def system_status() -> str:
    """Dynamic system status - updates in real-time."""
    import psutil

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    timestamp = datetime.now().isoformat()

    return f"""System Status (as of {timestamp}):
CPU Usage: {cpu}%
Memory Usage: {memory}%
Status: Operational
"""
```

---

## URI Templates with Parameters

Resources can use URI templates with parameters to provide dynamic content based on the requested URI.

### Basic URI Template

```python
@mcp.resource("data://users/{user_id}")
def user_profile(user_id: str) -> str:
    """
    Get user profile by ID.

    Args:
        user_id: The user's unique identifier

    Returns:
        User profile information
    """
    # In production, fetch from database
    users = {
        "123": "Name: Alice\nEmail: alice@example.com\nRole: Admin",
        "456": "Name: Bob\nEmail: bob@example.com\nRole: User"
    }

    return users.get(user_id, f"User {user_id} not found")
```

### Multiple Parameters

```python
@mcp.resource("data://projects/{project_id}/files/{file_path}")
def project_file(project_id: str, file_path: str) -> str:
    """
    Get file content from a project.

    Args:
        project_id: Project identifier
        file_path: Path to file within project

    Returns:
        File content
    """
    # In production, fetch from project storage
    full_path = f"/projects/{project_id}/{file_path}"

    if os.path.exists(full_path):
        with open(full_path) as f:
            return f.read()

    return f"File {file_path} not found in project {project_id}"
```

### Parameter Validation

```python
from typing import Literal

@mcp.resource("config://{environment}/settings")
def environment_config(environment: Literal["dev", "staging", "prod"]) -> str:
    """
    Get configuration for specific environment.

    Args:
        environment: Target environment (dev, staging, or prod)

    Returns:
        Environment-specific configuration
    """
    configs = {
        "dev": "DEBUG=true\nDB=dev_db",
        "staging": "DEBUG=false\nDB=staging_db",
        "prod": "DEBUG=false\nDB=prod_db"
    }

    return configs[environment]
```

---

## Return Types

### Text Content (Default)

Most common return type - plain text or formatted text.

```python
@mcp.resource("data://logs/latest")
def latest_logs() -> str:
    """Return latest log entries as text."""
    return """
2025-01-15 10:30:00 INFO Server started
2025-01-15 10:30:01 INFO Database connected
2025-01-15 10:30:05 WARN High memory usage detected
"""
```

### JSON Content

Return JSON data (as string) with appropriate MIME type.

```python
import json

@mcp.resource("data://users/list", mime_type="application/json")
def users_json() -> str:
    """Return users as JSON."""
    users = [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"}
    ]
    return json.dumps(users, indent=2)
```

### Markdown Content

Return formatted markdown documentation.

```python
@mcp.resource("docs://api/guide", mime_type="text/markdown")
def api_guide() -> str:
    """Return API guide as markdown."""
    return """
# API Usage Guide

## Authentication

All requests require an API key:

```bash
curl -H "X-API-Key: YOUR_KEY" https://api.example.com/endpoint
```

## Rate Limits

- 1000 requests per hour
- 10000 requests per day
"""
```

### Binary Content

Return binary data (images, files) as bytes.

```python
@mcp.resource("image://logo", mime_type="image/png")
def company_logo() -> bytes:
    """Return company logo image."""
    with open("assets/logo.png", "rb") as f:
        return f.read()
```

### List of Resources

Return multiple related resources.

```python
from fastmcp.resources import Resource

@mcp.resource("collection://project-files")
def project_files() -> list[Resource]:
    """Return list of all project files as resources."""
    files = []

    for filename in os.listdir("./project"):
        if filename.endswith(".py"):
            uri = f"file://project/{filename}"
            with open(f"./project/{filename}") as f:
                content = f.read()

            files.append(Resource(
                uri=uri,
                name=filename,
                mimeType="text/x-python",
                text=content
            ))

    return files
```

---

## Resource Metadata

### Resource Objects

For advanced use cases, return `Resource` objects with full metadata control.

```python
from fastmcp.resources import Resource

@mcp.resource("data://user/{user_id}/profile")
def user_profile_advanced(user_id: str) -> Resource:
    """Return user profile with metadata."""
    # Fetch user data
    user_data = fetch_user(user_id)

    return Resource(
        uri=f"data://user/{user_id}/profile",
        name=f"Profile for {user_data['name']}",
        description=f"User profile for {user_id}",
        mimeType="application/json",
        text=json.dumps(user_data, indent=2)
    )
```

### Embedded Resources

Resources can contain references to other resources.

```python
@mcp.resource("docs://project/index")
def project_index() -> str:
    """Main project documentation with links to other resources."""
    return """
# Project Documentation

## Configuration
See: resource://config://server/settings

## API Reference
See: resource://docs://api/endpoints

## User Guide
See: resource://docs://guide/getting-started
"""
```

---

## Context Injection

Resources can access request context through injected parameters.

### Available Context

```python
from fastmcp import Context

@mcp.resource("data://request/info")
async def request_info(ctx: Context) -> str:
    """
    Display information about the current request context.

    Args:
        ctx: Request context (automatically injected)

    Returns:
        Context information
    """
    # Access context properties
    await ctx.info("Generating request info")

    return f"""Request Context:
Client Info: {ctx.request_id if hasattr(ctx, 'request_id') else 'N/A'}
Timestamp: {datetime.now().isoformat()}
"""
```

### Logging in Resources

```python
@mcp.resource("data://system/diagnostics")
async def system_diagnostics(ctx: Context) -> str:
    """Generate system diagnostics with logging."""
    await ctx.info("Starting diagnostics check")

    # Perform checks
    cpu_ok = check_cpu()
    memory_ok = check_memory()

    await ctx.info(f"CPU: {'OK' if cpu_ok else 'WARNING'}")
    await ctx.info(f"Memory: {'OK' if memory_ok else 'WARNING'}")

    return f"CPU: {cpu_ok}\nMemory: {memory_ok}"
```

---

## Async vs Sync

### Synchronous Resources

Use synchronous functions for lightweight, non-blocking operations.

```python
@mcp.resource("config://app/version")
def app_version() -> str:
    """Return application version (sync)."""
    return "1.0.0"
```

### Asynchronous Resources

Use async functions for I/O operations, API calls, or database queries.

```python
import aiohttp

@mcp.resource("data://weather/{city}")
async def weather_data(city: str) -> str:
    """
    Fetch current weather data for a city.

    Args:
        city: City name

    Returns:
        Weather information
    """
    async with aiohttp.ClientSession() as session:
        url = f"https://api.weather.com/v1/current?city={city}"
        async with session.get(url) as response:
            data = await response.json()
            return f"Temperature: {data['temp']}°C\nConditions: {data['conditions']}"
```

### Async Best Practices

```python
import asyncio

@mcp.resource("data://multi-source/aggregate")
async def aggregate_data() -> str:
    """Fetch data from multiple sources concurrently."""

    # Run multiple async operations in parallel
    results = await asyncio.gather(
        fetch_source_a(),
        fetch_source_b(),
        fetch_source_c(),
        return_exceptions=True  # Don't fail if one source fails
    )

    # Combine results
    output = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            output.append(f"Source {i+1}: Error - {result}")
        else:
            output.append(f"Source {i+1}: {result}")

    return "\n".join(output)
```

---

## Resource Management

### Enabling/Disabling Resources

Control resource availability at runtime.

```python
# Disable resource based on configuration
DEBUG_MODE = os.getenv("DEBUG") == "true"

@mcp.resource(
    "data://internal/debug-info",
    enabled=DEBUG_MODE
)
def debug_info() -> str:
    """Internal debug information (only in debug mode)."""
    return "Debug data: ..."
```

### Dynamic Resource Registration

Resources can be registered programmatically.

```python
def register_project_resources(mcp: FastMCP, project_path: str):
    """Dynamically register resources for all files in a project."""

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, project_path)
            uri = f"file://project/{rel_path}"

            @mcp.resource(uri)
            def file_content(path=filepath) -> str:
                with open(path) as f:
                    return f.read()
```

---

## Common Patterns

### Pattern 1: Configuration Provider

Provide application configuration through resources.

```python
import json
import os

@mcp.resource("config://app/settings", mime_type="application/json")
def app_settings() -> str:
    """Application configuration."""
    config = {
        "environment": os.getenv("ENV", "development"),
        "debug": os.getenv("DEBUG", "false") == "true",
        "api_url": os.getenv("API_URL", "http://localhost:8000"),
        "features": {
            "auth": True,
            "analytics": os.getenv("ANALYTICS_ENABLED", "true") == "true"
        }
    }
    return json.dumps(config, indent=2)
```

### Pattern 2: File System Access

Expose file system content as resources.

```python
from pathlib import Path

@mcp.resource("file://docs/{path}")
def documentation_file(path: str) -> str:
    """
    Access documentation files.

    Args:
        path: Relative path to documentation file

    Returns:
        File content
    """
    docs_dir = Path("./docs")
    file_path = docs_dir / path

    # Security: Ensure path is within docs directory
    if not file_path.resolve().is_relative_to(docs_dir.resolve()):
        return "Error: Access denied - path outside docs directory"

    if not file_path.exists():
        return f"Error: File {path} not found"

    with open(file_path) as f:
        return f.read()
```

### Pattern 3: Database Query Results

Expose database queries as resources.

```python
import sqlite3

@mcp.resource("data://database/users/recent")
async def recent_users() -> str:
    """Recently registered users."""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, created_at
        FROM users
        ORDER BY created_at DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()

    # Format as text
    output = ["Recent Users:", ""]
    for user_id, username, created_at in rows:
        output.append(f"- {username} (ID: {user_id}) - {created_at}")

    return "\n".join(output)
```

### Pattern 4: API Schema/Documentation

Provide API schemas for agents to understand available endpoints.

```python
@mcp.resource("docs://api/schema", mime_type="application/json")
def api_schema() -> str:
    """OpenAPI schema for the API."""
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "My API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "get": {
                    "summary": "List users",
                    "responses": {
                        "200": {
                            "description": "List of users"
                        }
                    }
                }
            }
        }
    }
    return json.dumps(schema, indent=2)
```

### Pattern 5: Dynamic Content Generation

Generate content on-demand based on current state.

```python
from datetime import datetime, timedelta

@mcp.resource("data://reports/daily")
async def daily_report() -> str:
    """Generate daily activity report."""
    today = datetime.now().date()

    # Gather stats
    total_users = await count_users()
    new_signups = await count_signups_since(today)
    active_sessions = await count_active_sessions()

    return f"""Daily Report - {today}

Users:
- Total: {total_users}
- New Today: {new_signups}
- Currently Active: {active_sessions}

Generated at: {datetime.now().isoformat()}
"""
```

### Pattern 6: Multi-Environment Configuration

Provide environment-specific configuration.

```python
@mcp.resource("config://{env}/database")
def database_config(env: Literal["dev", "staging", "prod"]) -> str:
    """
    Database configuration for specific environment.

    Args:
        env: Environment name

    Returns:
        Database connection string
    """
    configs = {
        "dev": "postgresql://localhost:5432/myapp_dev",
        "staging": "postgresql://staging.example.com:5432/myapp_staging",
        "prod": "postgresql://prod.example.com:5432/myapp_prod"
    }

    return f"Database URL: {configs[env]}"
```

---

## Troubleshooting

### Issue 1: Resource Not Found

**Problem:** Resource URI returns "not found" error.

**Solutions:**
```python
# ✗ Wrong - URI doesn't match decorator
@mcp.resource("config://app/settings")
def get_settings() -> str:
    return "..."

# Access with: "config://app/setting" (typo) -> Not found

# ✓ Correct - Ensure URI exactly matches
@mcp.resource("config://app/settings")
def get_settings() -> str:
    return "..."

# Access with: "config://app/settings" -> Works
```

### Issue 2: Parameter Type Mismatch

**Problem:** URI template parameters aren't being extracted correctly.

**Solutions:**
```python
# ✗ Wrong - Parameter name must match URI template variable
@mcp.resource("data://users/{user_id}")
def get_user(id: str) -> str:  # Parameter name doesn't match
    return f"User {id}"

# ✓ Correct - Parameter name matches template variable
@mcp.resource("data://users/{user_id}")
def get_user(user_id: str) -> str:
    return f"User {user_id}"
```

### Issue 3: Binary Content Not Displaying

**Problem:** Binary resources (images, PDFs) not rendering correctly.

**Solutions:**
```python
# ✗ Wrong - Missing MIME type for binary content
@mcp.resource("image://logo")
def logo() -> bytes:
    with open("logo.png", "rb") as f:
        return f.read()

# ✓ Correct - Specify MIME type for binary content
@mcp.resource("image://logo", mime_type="image/png")
def logo() -> bytes:
    with open("logo.png", "rb") as f:
        return f.read()
```

### Issue 4: Resource Takes Too Long

**Problem:** Resource generation is blocking or slow.

**Solutions:**
```python
# ✗ Wrong - Synchronous blocking operation
@mcp.resource("data://large-dataset")
def large_dataset() -> str:
    # This blocks the entire server
    data = slow_database_query()  # Takes 10 seconds
    return format_data(data)

# ✓ Correct - Use async for I/O operations
@mcp.resource("data://large-dataset")
async def large_dataset() -> str:
    data = await async_database_query()  # Non-blocking
    return format_data(data)

# ✓ Better - Add caching for expensive operations
from functools import lru_cache
from datetime import datetime, timedelta

_cache = {}
_cache_time = {}

@mcp.resource("data://large-dataset")
async def large_dataset() -> str:
    cache_key = "large_dataset"
    now = datetime.now()

    # Return cached result if less than 5 minutes old
    if cache_key in _cache:
        if now - _cache_time[cache_key] < timedelta(minutes=5):
            return _cache[cache_key]

    # Generate fresh data
    data = await async_database_query()
    result = format_data(data)

    # Update cache
    _cache[cache_key] = result
    _cache_time[cache_key] = now

    return result
```

### Issue 5: Path Traversal Security Issue

**Problem:** URI parameters allow access to files outside intended directory.

**Solutions:**
```python
from pathlib import Path

# ✗ Wrong - Vulnerable to path traversal
@mcp.resource("file://docs/{path}")
def get_doc(path: str) -> str:
    # Attacker could use path="../../../etc/passwd"
    with open(f"./docs/{path}") as f:
        return f.read()

# ✓ Correct - Validate path is within allowed directory
@mcp.resource("file://docs/{path}")
def get_doc(path: str) -> str:
    docs_dir = Path("./docs").resolve()
    requested_file = (docs_dir / path).resolve()

    # Ensure requested file is within docs directory
    if not requested_file.is_relative_to(docs_dir):
        return "Error: Access denied"

    if not requested_file.exists():
        return "Error: File not found"

    with open(requested_file) as f:
        return f.read()
```

### Issue 6: JSON Serialization Errors

**Problem:** Complex objects can't be serialized to JSON.

**Solutions:**
```python
import json
from datetime import datetime
from decimal import Decimal

# ✗ Wrong - datetime and Decimal aren't JSON serializable
@mcp.resource("data://orders/recent", mime_type="application/json")
def recent_orders() -> str:
    orders = [
        {"id": 1, "amount": Decimal("99.99"), "created": datetime.now()}
    ]
    return json.dumps(orders)  # Raises TypeError

# ✓ Correct - Use custom JSON encoder
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

@mcp.resource("data://orders/recent", mime_type="application/json")
def recent_orders() -> str:
    orders = [
        {"id": 1, "amount": Decimal("99.99"), "created": datetime.now()}
    ]
    return json.dumps(orders, cls=CustomEncoder, indent=2)

# ✓ Better - Use Pydantic for automatic serialization
from pydantic import BaseModel

class Order(BaseModel):
    id: int
    amount: Decimal
    created: datetime

@mcp.resource("data://orders/recent", mime_type="application/json")
def recent_orders() -> str:
    orders = [
        Order(id=1, amount=Decimal("99.99"), created=datetime.now())
    ]
    return json.dumps([order.model_dump() for order in orders], default=str, indent=2)
```

### Issue 7: Resource List Not Displaying

**Problem:** Returning a list of `Resource` objects doesn't work as expected.

**Solutions:**
```python
from fastmcp.resources import Resource

# ✗ Wrong - Returning plain dictionaries
@mcp.resource("collection://files")
def all_files() -> list:
    return [
        {"uri": "file://a.txt", "content": "..."},
        {"uri": "file://b.txt", "content": "..."}
    ]

# ✓ Correct - Return list of Resource objects
@mcp.resource("collection://files")
def all_files() -> list[Resource]:
    return [
        Resource(uri="file://a.txt", text="Content of A"),
        Resource(uri="file://b.txt", text="Content of B")
    ]
```

### Issue 8: Context Injection Not Working

**Problem:** Context parameter is None or not being injected.

**Solutions:**
```python
from fastmcp import Context

# ✗ Wrong - Context parameter must be named 'ctx' or have Context type hint
@mcp.resource("data://info")
async def info(context) -> str:  # Won't be injected
    await context.info("test")  # AttributeError
    return "Info"

# ✓ Correct - Use proper type hint
@mcp.resource("data://info")
async def info(ctx: Context) -> str:
    await ctx.info("Generating info")
    return "Info"
```

---

## Summary

Resources in FastMCP enable you to expose dynamic data sources to LLM agents. Key takeaways:

1. **Use descriptive URIs** with proper schemes and hierarchies
2. **Choose appropriate return types** - text, JSON, binary, or Resource objects
3. **Use URI templates** for parameterized resources
4. **Specify MIME types** for non-text content
5. **Use async functions** for I/O operations
6. **Validate inputs** to prevent security issues
7. **Add proper error handling** for missing or invalid resources
8. **Use context injection** for logging and progress reporting
9. **Cache expensive operations** to improve performance
10. **Document thoroughly** with clear descriptions

Resources complement tools by providing the context agents need to make informed decisions when using your MCP server.
