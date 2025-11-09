"""
Example 5: Async and Parallel Operations

This example demonstrates:
- Async/await patterns
- Parallel execution with asyncio.gather
- Progress reporting for concurrent operations
- Error handling in parallel tasks
"""

import asyncio
from typing import Literal
from fastmcp import FastMCP, Context

mcp = FastMCP("async-parallel-example")


async def simulate_task(task_id: int, duration: float) -> dict:
    """
    Simulate an async task that takes time to complete.

    Args:
        task_id: Task identifier
        duration: Time to sleep (simulating work)

    Returns:
        Task result
    """
    await asyncio.sleep(duration)
    return {
        "task_id": task_id,
        "duration": duration,
        "result": f"Task {task_id} completed"
    }


@mcp.tool()
async def run_parallel_tasks(
    num_tasks: int,
    duration: float = 1.0,
    ctx: Context | None = None
) -> list[dict]:
    """
    Run multiple tasks in parallel.

    Args:
        num_tasks: Number of tasks to run (1-20)
        duration: Duration for each task in seconds
        ctx: Request context for logging and progress

    Returns:
        List of task results
    """
    if num_tasks < 1 or num_tasks > 20:
        raise ValueError("Number of tasks must be between 1 and 20")

    if ctx:
        await ctx.info(f"Starting {num_tasks} tasks in parallel")

    # Create all tasks
    tasks = [
        simulate_task(i, duration)
        for i in range(1, num_tasks + 1)
    ]

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)

    if ctx:
        await ctx.info(f"All {num_tasks} tasks completed")

    return results


@mcp.tool()
async def run_sequential_tasks(
    num_tasks: int,
    duration: float = 1.0,
    ctx: Context | None = None
) -> list[dict]:
    """
    Run multiple tasks sequentially with progress reporting.

    Args:
        num_tasks: Number of tasks to run (1-20)
        duration: Duration for each task in seconds
        ctx: Request context for logging and progress

    Returns:
        List of task results
    """
    if num_tasks < 1 or num_tasks > 20:
        raise ValueError("Number of tasks must be between 1 and 20")

    if ctx:
        await ctx.info(f"Starting {num_tasks} tasks sequentially")

    results = []

    for i in range(1, num_tasks + 1):
        if ctx:
            await ctx.report_progress(progress=i, total=num_tasks)

        result = await simulate_task(i, duration)
        results.append(result)

        if ctx:
            await ctx.info(f"Completed task {i}/{num_tasks}")

    if ctx:
        await ctx.info("All tasks completed")

    return results


@mcp.tool()
async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    ctx: Context | None = None
) -> dict:
    """
    Fetch URL with exponential backoff retry logic.

    Args:
        url: URL to fetch
        max_retries: Maximum retry attempts
        ctx: Request context for logging

    Returns:
        Fetch result
    """
    if ctx:
        await ctx.info(f"Fetching: {url}")

    for attempt in range(1, max_retries + 1):
        try:
            # Simulate fetch (replace with actual HTTP request in production)
            await asyncio.sleep(0.5)

            # Simulate occasional failures
            if attempt < max_retries and url.endswith("flaky"):
                raise Exception("Simulated network error")

            if ctx:
                await ctx.info(f"Success on attempt {attempt}")

            return {
                "url": url,
                "status": 200,
                "attempt": attempt,
                "content": f"Content from {url}"
            }

        except Exception as e:
            if attempt < max_retries:
                backoff = 2 ** (attempt - 1)
                if ctx:
                    await ctx.warn(f"Attempt {attempt} failed: {e}. Retrying in {backoff}s...")
                await asyncio.sleep(backoff)
            else:
                if ctx:
                    await ctx.error(f"Failed after {max_retries} attempts: {e}")
                raise


@mcp.tool()
async def process_batch(
    items: list[str],
    batch_size: int = 5,
    ctx: Context | None = None
) -> dict:
    """
    Process items in batches with parallel execution within each batch.

    Args:
        items: Items to process
        batch_size: Number of items to process in parallel per batch
        ctx: Request context for logging and progress

    Returns:
        Processing results
    """
    total = len(items)
    processed = []
    errors = []

    if ctx:
        await ctx.info(f"Processing {total} items in batches of {batch_size}")

    for i in range(0, total, batch_size):
        batch = items[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        if ctx:
            await ctx.info(f"Processing batch {batch_num}")

        # Process batch in parallel
        async def process_item(item: str) -> dict:
            try:
                await asyncio.sleep(0.3)  # Simulate processing
                return {"item": item, "status": "success"}
            except Exception as e:
                return {"item": item, "status": "error", "error": str(e)}

        batch_results = await asyncio.gather(
            *[process_item(item) for item in batch],
            return_exceptions=True
        )

        for result in batch_results:
            if isinstance(result, Exception):
                errors.append(str(result))
            elif result.get("status") == "success":
                processed.append(result["item"])
            else:
                errors.append(result.get("error"))

        if ctx:
            await ctx.report_progress(
                progress=min(i + batch_size, total),
                total=total
            )

    if ctx:
        await ctx.info(f"Completed: {len(processed)} successful, {len(errors)} errors")

    return {
        "total": total,
        "successful": len(processed),
        "errors": len(errors),
        "processed_items": processed
    }


@mcp.tool()
async def rate_limited_requests(
    urls: list[str],
    requests_per_second: int = 2,
    ctx: Context | None = None
) -> list[dict]:
    """
    Make requests with rate limiting.

    Args:
        urls: URLs to fetch
        requests_per_second: Maximum requests per second
        ctx: Request context for logging

    Returns:
        List of fetch results
    """
    delay = 1.0 / requests_per_second
    results = []

    if ctx:
        await ctx.info(f"Fetching {len(urls)} URLs at {requests_per_second} req/s")

    for i, url in enumerate(urls, 1):
        # Simulate fetch
        await asyncio.sleep(0.2)

        results.append({
            "url": url,
            "status": 200,
            "content": f"Content from {url}"
        })

        if ctx:
            await ctx.report_progress(progress=i, total=len(urls))

        # Rate limiting delay
        if i < len(urls):
            await asyncio.sleep(delay)

    if ctx:
        await ctx.info(f"All {len(urls)} requests completed")

    return results


@mcp.tool()
async def concurrent_aggregation(
    sources: list[str],
    ctx: Context | None = None
) -> dict:
    """
    Fetch data from multiple sources concurrently and aggregate.

    Args:
        sources: Data source identifiers
        ctx: Request context for logging

    Returns:
        Aggregated results from all sources
    """
    if ctx:
        await ctx.info(f"Fetching from {len(sources)} sources concurrently")

    async def fetch_source(source: str) -> dict:
        """Fetch data from a single source."""
        await asyncio.sleep(0.5)  # Simulate fetch
        return {
            "source": source,
            "data": [f"item-{i}" for i in range(5)]
        }

    # Fetch all sources concurrently
    results = await asyncio.gather(
        *[fetch_source(source) for source in sources],
        return_exceptions=True
    )

    # Aggregate results
    aggregated = {
        "sources": len(sources),
        "total_items": 0,
        "data_by_source": {}
    }

    for result in results:
        if isinstance(result, Exception):
            if ctx:
                await ctx.warn(f"Source failed: {result}")
        else:
            source = result["source"]
            data = result["data"]
            aggregated["data_by_source"][source] = data
            aggregated["total_items"] += len(data)

    if ctx:
        await ctx.info(f"Aggregated {aggregated['total_items']} items from {len(sources)} sources")

    return aggregated


if __name__ == "__main__":
    mcp.run()
