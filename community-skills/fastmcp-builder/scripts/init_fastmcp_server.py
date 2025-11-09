#!/usr/bin/env python3
"""
FastMCP Server Initialization Script

This script creates a new FastMCP server project with proper structure and configuration.

Usage:
    python init_fastmcp_server.py [server_name] [--dir directory] [--description "desc"]

Examples:
    python init_fastmcp_server.py weather-server
    python init_fastmcp_server.py github-mcp --dir ~/projects --description "GitHub API integration"
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def get_template_path() -> Path:
    """Get the path to the server template file."""
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / "assets" / "server_template.py"

    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        sys.exit(1)

    return template_path


def create_server(name: str, description: str, target_dir: Path, init_git: bool = False):
    """
    Create a new FastMCP server project.

    Args:
        name: Server name (e.g., "weather-server")
        description: Server description
        target_dir: Directory to create the server in
        init_git: Whether to initialize git repository
    """
    # Validate server name
    if not name.replace("-", "").replace("_", "").isalnum():
        print(f"❌ Error: Server name must contain only letters, numbers, hyphens, and underscores")
        sys.exit(1)

    # Create target directory
    server_dir = target_dir / name
    if server_dir.exists():
        print(f"❌ Error: Directory {server_dir} already exists")
        sys.exit(1)

    print(f"📦 Creating FastMCP server: {name}")
    server_dir.mkdir(parents=True)

    # Copy and customize server template
    template_path = get_template_path()
    server_file = server_dir / "server.py"

    with open(template_path, "r") as f:
        template_content = f.read()

    # Customize template
    customized_content = template_content.replace(
        'mcp = FastMCP("my-server")',
        f'mcp = FastMCP("{name}")'
    )
    customized_content = customized_content.replace(
        'Minimal FastMCP Server Template',
        f'{name.replace("-", " ").replace("_", " ").title()}'
    )

    with open(server_file, "w") as f:
        f.write(customized_content)

    print(f"✅ Created server.py")

    # Create pyproject.toml
    pyproject_content = f'''[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=2.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
{name} = "{name}.server:mcp.run"
'''

    pyproject_file = server_dir / "pyproject.toml"
    with open(pyproject_file, "w") as f:
        f.write(pyproject_content)

    print(f"✅ Created pyproject.toml")

    # Create .env.example
    env_example = '''# Environment Variables Template
# Copy this file to .env and fill in your actual values

# Example API key (uncomment and set if needed)
# MY_API_KEY=your_api_key_here
'''

    env_file = server_dir / ".env.example"
    with open(env_file, "w") as f:
        f.write(env_example)

    print(f"✅ Created .env.example")

    # Create .gitignore
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
'''

    gitignore_file = server_dir / ".gitignore"
    with open(gitignore_file, "w") as f:
        f.write(gitignore_content)

    print(f"✅ Created .gitignore")

    # Initialize git if requested
    if init_git:
        import subprocess
        try:
            subprocess.run(["git", "init"], cwd=server_dir, check=True, capture_output=True)
            print(f"✅ Initialized git repository")
        except subprocess.CalledProcessError:
            print(f"⚠️  Warning: Failed to initialize git repository")

    # Print next steps
    print(f"\n🎉 FastMCP server '{name}' created successfully!\n")
    print("📋 Next steps:")
    print(f"   1. cd {server_dir.relative_to(Path.cwd()) if server_dir.is_relative_to(Path.cwd()) else server_dir}")
    print(f"   2. uv venv && source .venv/bin/activate  # or python -m venv .venv")
    print(f"   3. uv pip install -e .  # or pip install -e .")
    print(f"   4. Edit server.py to add your tools, resources, and prompts")
    print(f"   5. Test: python server.py  # or fastmcp dev server.py")
    print(f"\n📚 Documentation: Load the fastmcp-builder skill for comprehensive guides")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new FastMCP server project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s weather-server
  %(prog)s github-mcp --dir ~/projects --description "GitHub API integration"
  %(prog)s my-server --git
        """
    )

    parser.add_argument(
        "name",
        help="Server name (e.g., 'weather-server')"
    )

    parser.add_argument(
        "--dir",
        type=Path,
        default=Path.cwd(),
        help="Directory to create the server in (default: current directory)"
    )

    parser.add_argument(
        "--description",
        default="A FastMCP server",
        help="Server description"
    )

    parser.add_argument(
        "--git",
        action="store_true",
        help="Initialize git repository"
    )

    args = parser.parse_args()

    create_server(
        name=args.name,
        description=args.description,
        target_dir=args.dir,
        init_git=args.git
    )


if __name__ == "__main__":
    main()
