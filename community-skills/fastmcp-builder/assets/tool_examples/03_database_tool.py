"""
Example 3: Database Tools

This example demonstrates tools that interact with databases:
- SQLite database operations
- CRUD operations
- Parameterized queries
- Transaction handling
"""

import sqlite3
from typing import Literal
from pathlib import Path
from fastmcp import FastMCP, Context

mcp = FastMCP("database-example")

# Database file path (for demo - use in-memory or temp file in production)
DB_PATH = Path("demo.db")


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize demo database with users table."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Initialize database on server start
init_database()


@mcp.tool()
async def create_user(
    name: str,
    email: str,
    role: Literal["admin", "user", "guest"] = "user",
    ctx: Context | None = None
) -> dict:
    """
    Create a new user in the database.

    Args:
        name: User's full name
        email: User's email address (must be unique)
        role: User's role (admin, user, or guest)
        ctx: Request context for logging

    Returns:
        Created user data with ID

    Raises:
        ValueError: If email already exists
    """
    if ctx:
        await ctx.info(f"Creating user: {email}")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            (name, email, role)
        )
        conn.commit()

        user_id = cursor.lastrowid

        if ctx:
            await ctx.info(f"User created with ID: {user_id}")

        return {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role
        }

    except sqlite3.IntegrityError:
        raise ValueError(f"User with email {email} already exists")

    finally:
        conn.close()


@mcp.tool()
async def get_user(
    user_id: int | None = None,
    email: str | None = None,
    ctx: Context | None = None
) -> dict | None:
    """
    Get user by ID or email.

    Args:
        user_id: User ID to look up (optional)
        email: User email to look up (optional)
        ctx: Request context for logging

    Returns:
        User data if found, None otherwise

    Raises:
        ValueError: If neither user_id nor email provided
    """
    if user_id is None and email is None:
        raise ValueError("Either user_id or email must be provided")

    if ctx:
        await ctx.info(f"Looking up user: {user_id or email}")

    conn = get_connection()
    cursor = conn.cursor()

    if user_id is not None:
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    else:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


@mcp.tool()
async def list_users(
    role: Literal["admin", "user", "guest", "all"] = "all",
    limit: int = 100,
    ctx: Context | None = None
) -> list[dict]:
    """
    List users with optional role filter.

    Args:
        role: Filter by role (admin, user, guest, or all)
        limit: Maximum number of users to return
        ctx: Request context for logging

    Returns:
        List of user data
    """
    if ctx:
        await ctx.info(f"Listing users with role: {role}")

    conn = get_connection()
    cursor = conn.cursor()

    if role == "all":
        cursor.execute("SELECT * FROM users LIMIT ?", (limit,))
    else:
        cursor.execute(
            "SELECT * FROM users WHERE role = ? LIMIT ?",
            (role, limit)
        )

    rows = cursor.fetchall()
    conn.close()

    users = [dict(row) for row in rows]

    if ctx:
        await ctx.info(f"Found {len(users)} users")

    return users


@mcp.tool()
async def update_user(
    user_id: int,
    name: str | None = None,
    email: str | None = None,
    role: Literal["admin", "user", "guest"] | None = None,
    ctx: Context | None = None
) -> dict:
    """
    Update user information.

    Args:
        user_id: User ID to update
        name: New name (optional)
        email: New email (optional)
        role: New role (optional)
        ctx: Request context for logging

    Returns:
        Updated user data

    Raises:
        ValueError: If user not found or email already exists
    """
    if ctx:
        await ctx.info(f"Updating user ID: {user_id}")

    # Build dynamic UPDATE query based on provided fields
    updates = []
    params = []

    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if email is not None:
        updates.append("email = ?")
        params.append(email)
    if role is not None:
        updates.append("role = ?")
        params.append(role)

    if not updates:
        raise ValueError("No fields to update")

    params.append(user_id)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()

        if cursor.rowcount == 0:
            raise ValueError(f"User with ID {user_id} not found")

        # Fetch updated user
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()

        if ctx:
            await ctx.info(f"User {user_id} updated successfully")

        return dict(row)

    except sqlite3.IntegrityError:
        raise ValueError(f"Email {email} already exists")

    finally:
        conn.close()


@mcp.tool()
async def delete_user(user_id: int, ctx: Context | None = None) -> dict:
    """
    Delete a user from the database.

    Args:
        user_id: User ID to delete
        ctx: Request context for logging

    Returns:
        Deletion confirmation message

    Raises:
        ValueError: If user not found
    """
    if ctx:
        await ctx.info(f"Deleting user ID: {user_id}")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError(f"User with ID {user_id} not found")

    conn.close()

    if ctx:
        await ctx.info(f"User {user_id} deleted successfully")

    return {"message": f"User {user_id} deleted successfully"}


if __name__ == "__main__":
    mcp.run()
