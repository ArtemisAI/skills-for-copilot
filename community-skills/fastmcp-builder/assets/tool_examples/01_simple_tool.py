"""
Example 1: Simple Tools

This example demonstrates basic tool patterns:
- Simple synchronous tool
- Tool with validation
- Tool with default parameters
- Tool with type constraints (Literal)
"""

from typing import Literal
from fastmcp import FastMCP

mcp = FastMCP("simple-tools-example")


@mcp.tool()
def greet(name: str) -> str:
    """
    Greet a person by name.

    Args:
        name: The person's name to greet

    Returns:
        A personalized greeting message
    """
    return f"Hello, {name}! Welcome to FastMCP."


@mcp.tool()
def calculate(
    operation: Literal["add", "subtract", "multiply", "divide"],
    a: float,
    b: float
) -> float:
    """
    Perform basic arithmetic operations.

    Args:
        operation: The operation to perform (add, subtract, multiply, or divide)
        a: First number
        b: Second number

    Returns:
        Result of the calculation

    Raises:
        ValueError: If dividing by zero
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


@mcp.tool()
def format_text(
    text: str,
    style: Literal["uppercase", "lowercase", "title", "capitalize"] = "lowercase"
) -> str:
    """
    Format text in different styles.

    Args:
        text: The text to format
        style: The formatting style to apply (default: lowercase)

    Returns:
        Formatted text
    """
    if style == "uppercase":
        return text.upper()
    elif style == "lowercase":
        return text.lower()
    elif style == "title":
        return text.title()
    elif style == "capitalize":
        return text.capitalize()


@mcp.tool()
def count_words(text: str, min_length: int = 1) -> dict:
    """
    Count words in text with minimum length filter.

    Args:
        text: The text to analyze
        min_length: Minimum word length to count (default: 1)

    Returns:
        Dictionary with total words, filtered words, and word list
    """
    words = text.split()
    filtered_words = [w for w in words if len(w) >= min_length]

    return {
        "total_words": len(words),
        "filtered_words": len(filtered_words),
        "words": filtered_words
    }


if __name__ == "__main__":
    mcp.run()
