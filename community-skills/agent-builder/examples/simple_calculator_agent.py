"""
Simple Calculator Agent Example

This example demonstrates:
- Basic query() usage
- Simple system prompt
- Minimal tool setup

Purpose: Show the simplest possible agent implementation
"""

import asyncio
from claude_agent_sdk import query


async def main():
    """
    Simple calculator agent that can perform mathematical operations
    """

    # Define the task
    prompt = """
    Calculate the following:
    1. What is 25% of 450?
    2. If I invest $1000 at 5% annual interest, how much will I have after 3 years?
    3. What is the square root of 144?

    Show your work for each calculation.
    """

    # Configure system prompt
    system_prompt = """
    You are a helpful calculator assistant. When performing calculations:
    - Show your work step by step
    - Double-check your arithmetic
    - Provide clear, formatted answers
    - Use Python code execution when helpful
    """

    print("Starting calculator agent...\n")

    # Run agent
    async for message in query(
        prompt=prompt,
        system_prompt=system_prompt,
        turn_limit=10  # Limit iterations to prevent infinite loops
    ):
        print(message)

    print("\nAgent completed!")


if __name__ == "__main__":
    asyncio.run(main())
