"""
Example 4: File Operations Tools

This example demonstrates tools for file system operations:
- Reading files
- Writing files
- Listing directories
- File metadata
- Path validation for security
"""

import os
from pathlib import Path
from typing import Literal
from fastmcp import FastMCP, Context

mcp = FastMCP("file-operations-example")

# Base directory for file operations (security boundary)
BASE_DIR = Path("./sandbox")
BASE_DIR.mkdir(exist_ok=True)


def validate_path(path: str) -> Path:
    """
    Validate that path is within BASE_DIR (prevent path traversal).

    Args:
        path: Relative path to validate

    Returns:
        Absolute path within BASE_DIR

    Raises:
        ValueError: If path is outside BASE_DIR
    """
    requested_path = (BASE_DIR / path).resolve()

    if not requested_path.is_relative_to(BASE_DIR.resolve()):
        raise ValueError(f"Access denied: path outside sandbox directory")

    return requested_path


@mcp.tool()
async def read_file(filepath: str, ctx: Context) -> str:
    """
    Read content from a file.

    Args:
        filepath: Relative path to file (within sandbox)
        ctx: Request context for logging

    Returns:
        File content as string

    Raises:
        ValueError: If path is invalid or file doesn't exist
    """
    await ctx.info(f"Reading file: {filepath}")

    safe_path = validate_path(filepath)

    if not safe_path.exists():
        raise ValueError(f"File not found: {filepath}")

    if not safe_path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    with open(safe_path, "r") as f:
        content = f.read()

    await ctx.info(f"Read {len(content)} characters from {filepath}")

    return content


@mcp.tool()
async def write_file(
    filepath: str,
    content: str,
    mode: Literal["overwrite", "append"] = "overwrite",
    ctx: Context | None = None
) -> dict:
    """
    Write content to a file.

    Args:
        filepath: Relative path to file (within sandbox)
        content: Content to write
        mode: Write mode - overwrite or append
        ctx: Request context for logging

    Returns:
        Success message with file info
    """
    if ctx:
        await ctx.info(f"Writing to file: {filepath} (mode: {mode})")

    safe_path = validate_path(filepath)

    # Create parent directories if needed
    safe_path.parent.mkdir(parents=True, exist_ok=True)

    # Write file
    write_mode = "w" if mode == "overwrite" else "a"
    with open(safe_path, write_mode) as f:
        f.write(content)

    if ctx:
        await ctx.info(f"Wrote {len(content)} characters to {filepath}")

    return {
        "filepath": filepath,
        "bytes_written": len(content.encode()),
        "mode": mode
    }


@mcp.tool()
async def list_directory(
    dirpath: str = ".",
    include_hidden: bool = False,
    ctx: Context | None = None
) -> dict:
    """
    List contents of a directory.

    Args:
        dirpath: Relative path to directory (within sandbox)
        include_hidden: Include hidden files (starting with .)
        ctx: Request context for logging

    Returns:
        Dictionary with files and directories lists
    """
    if ctx:
        await ctx.info(f"Listing directory: {dirpath}")

    safe_path = validate_path(dirpath)

    if not safe_path.exists():
        raise ValueError(f"Directory not found: {dirpath}")

    if not safe_path.is_dir():
        raise ValueError(f"Path is not a directory: {dirpath}")

    files = []
    directories = []

    for item in safe_path.iterdir():
        # Skip hidden files unless requested
        if not include_hidden and item.name.startswith("."):
            continue

        relative_path = str(item.relative_to(BASE_DIR))

        if item.is_file():
            files.append({
                "name": item.name,
                "path": relative_path,
                "size": item.stat().st_size
            })
        elif item.is_dir():
            directories.append({
                "name": item.name,
                "path": relative_path
            })

    if ctx:
        await ctx.info(f"Found {len(files)} files, {len(directories)} directories")

    return {
        "path": dirpath,
        "files": files,
        "directories": directories
    }


@mcp.tool()
async def get_file_info(filepath: str, ctx: Context | None = None) -> dict:
    """
    Get detailed information about a file.

    Args:
        filepath: Relative path to file (within sandbox)
        ctx: Request context for logging

    Returns:
        File metadata including size, modification time, etc.
    """
    if ctx:
        await ctx.info(f"Getting info for: {filepath}")

    safe_path = validate_path(filepath)

    if not safe_path.exists():
        raise ValueError(f"File not found: {filepath}")

    stat = safe_path.stat()

    return {
        "name": safe_path.name,
        "path": filepath,
        "size_bytes": stat.st_size,
        "is_file": safe_path.is_file(),
        "is_directory": safe_path.is_dir(),
        "created": stat.st_ctime,
        "modified": stat.st_mtime,
        "permissions": oct(stat.st_mode)[-3:]
    }


@mcp.tool()
async def delete_file(filepath: str, ctx: Context) -> dict:
    """
    Delete a file.

    Args:
        filepath: Relative path to file (within sandbox)
        ctx: Request context for logging

    Returns:
        Deletion confirmation message
    """
    await ctx.info(f"Deleting file: {filepath}")

    safe_path = validate_path(filepath)

    if not safe_path.exists():
        raise ValueError(f"File not found: {filepath}")

    if safe_path.is_dir():
        raise ValueError(f"Path is a directory, not a file: {filepath}")

    safe_path.unlink()

    await ctx.info(f"File deleted: {filepath}")

    return {"message": f"File {filepath} deleted successfully"}


@mcp.tool()
async def search_files(
    pattern: str,
    directory: str = ".",
    ctx: Context | None = None
) -> list[dict]:
    """
    Search for files matching a pattern.

    Args:
        pattern: Glob pattern to match (e.g., "*.txt", "**/*.py")
        directory: Directory to search in
        ctx: Request context for logging

    Returns:
        List of matching files with metadata
    """
    if ctx:
        await ctx.info(f"Searching for pattern: {pattern} in {directory}")

    safe_path = validate_path(directory)

    if not safe_path.exists():
        raise ValueError(f"Directory not found: {directory}")

    matches = []

    for match in safe_path.glob(pattern):
        if match.is_file():
            relative_path = str(match.relative_to(BASE_DIR))
            matches.append({
                "name": match.name,
                "path": relative_path,
                "size": match.stat().st_size
            })

    if ctx:
        await ctx.info(f"Found {len(matches)} matching files")

    return matches


if __name__ == "__main__":
    mcp.run()
