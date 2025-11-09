"""
Example 2: API Wrapper Tools

This example demonstrates tools that wrap external APIs:
- Async HTTP requests
- Error handling for API calls
- Response formatting
- Context injection for logging
"""

from typing import Literal
import asyncio
import aiohttp
from fastmcp import FastMCP, Context

mcp = FastMCP("api-wrapper-example")


@mcp.tool()
async def fetch_weather(city: str, ctx: Context) -> dict:
    """
    Fetch current weather data for a city.

    This is a mock example - replace with real API in production.

    Args:
        city: City name to get weather for
        ctx: Request context for logging

    Returns:
        Weather data including temperature and conditions
    """
    await ctx.info(f"Fetching weather for {city}")

    # Mock API call (replace with real API)
    await asyncio.sleep(0.5)  # Simulate network delay

    # Mock weather data
    mock_data = {
        "city": city,
        "temperature": 22,
        "conditions": "Partly Cloudy",
        "humidity": 65,
        "wind_speed": 12
    }

    await ctx.info(f"Weather data retrieved for {city}")

    return mock_data


@mcp.tool()
async def search_github_repos(
    query: str,
    language: str | None = None,
    sort: Literal["stars", "forks", "updated"] = "stars",
    limit: int = 10,
    ctx: Context | None = None
) -> list[dict]:
    """
    Search GitHub repositories.

    This is a mock example - replace with real GitHub API in production.

    Args:
        query: Search query
        language: Filter by programming language (optional)
        sort: Sort results by (stars, forks, or updated)
        limit: Maximum number of results (1-100)
        ctx: Request context for logging (optional)

    Returns:
        List of repository data
    """
    if ctx:
        await ctx.info(f"Searching GitHub for: {query}")

    # Validate limit
    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")

    # Mock search results
    mock_repos = [
        {
            "name": f"repo-{i}",
            "description": f"Mock repository for {query}",
            "stars": 1000 - i * 100,
            "language": language or "Python",
            "url": f"https://github.com/user/repo-{i}"
        }
        for i in range(min(limit, 5))
    ]

    if ctx:
        await ctx.info(f"Found {len(mock_repos)} repositories")

    return mock_repos


@mcp.tool()
async def fetch_multiple_urls(urls: list[str], ctx: Context) -> list[dict]:
    """
    Fetch multiple URLs concurrently.

    Args:
        urls: List of URLs to fetch
        ctx: Request context for logging and progress

    Returns:
        List of results with URL, status, and content/error
    """
    total = len(urls)
    await ctx.info(f"Fetching {total} URLs concurrently")

    results = []

    async def fetch_one(url: str, index: int) -> dict:
        """Fetch a single URL with error handling."""
        try:
            # Mock HTTP request (replace with aiohttp in production)
            await asyncio.sleep(0.3)  # Simulate network delay

            # Mock successful response
            result = {
                "url": url,
                "status": 200,
                "content": f"Mock content from {url}"
            }

            await ctx.report_progress(progress=index + 1, total=total)

            return result

        except Exception as e:
            await ctx.warn(f"Failed to fetch {url}: {e}")
            return {
                "url": url,
                "status": 0,
                "error": str(e)
            }

    # Fetch all URLs concurrently
    results = await asyncio.gather(*[
        fetch_one(url, i) for i, url in enumerate(urls)
    ])

    successful = sum(1 for r in results if r.get("status") == 200)
    await ctx.info(f"Completed: {successful}/{total} successful")

    return results


if __name__ == "__main__":
    mcp.run()
