#!/usr/bin/env python3
"""
FastMCP Server Validation Script

This script validates FastMCP server files for common issues and best practices.

Usage:
    python validate_fastmcp.py <server_file.py>
    python validate_fastmcp.py server.py --strict

Checks:
- Python syntax validity
- FastMCP imports and initialization
- Decorator usage (@mcp.tool, @mcp.resource, @mcp.prompt)
- Type hints on parameters
- Async/await patterns
- Common anti-patterns
"""

import argparse
import ast
import sys
from pathlib import Path
from typing import NamedTuple


class ValidationIssue(NamedTuple):
    """Represents a validation issue."""
    severity: str  # "error", "warning", "info"
    line: int | None
    message: str
    suggestion: str | None = None


class FastMCPValidator:
    """Validator for FastMCP server files."""

    def __init__(self, filepath: Path, strict: bool = False):
        self.filepath = filepath
        self.strict = strict
        self.issues: list[ValidationIssue] = []
        self.tree: ast.Module | None = None

    def validate(self) -> bool:
        """
        Run all validations.

        Returns:
            True if validation passed (no errors), False otherwise
        """
        print(f"🔍 Validating FastMCP server: {self.filepath}\n")

        # Check file exists
        if not self.filepath.exists():
            self.add_error(None, f"File not found: {self.filepath}")
            return False

        # Read file
        try:
            with open(self.filepath) as f:
                content = f.read()
        except Exception as e:
            self.add_error(None, f"Failed to read file: {e}")
            return False

        # Parse Python
        try:
            self.tree = ast.parse(content, filename=str(self.filepath))
        except SyntaxError as e:
            self.add_error(e.lineno, f"Python syntax error: {e.msg}")
            return False

        # Run all checks
        self.check_imports()
        self.check_server_init()
        self.check_decorators()
        self.check_type_hints()
        self.check_async_patterns()
        self.check_context_usage()
        self.check_best_practices()

        # Print results
        self.print_results()

        # Determine pass/fail
        has_errors = any(issue.severity == "error" for issue in self.issues)
        return not has_errors

    def add_error(self, line: int | None, message: str, suggestion: str | None = None):
        """Add an error."""
        self.issues.append(ValidationIssue("error", line, message, suggestion))

    def add_warning(self, line: int | None, message: str, suggestion: str | None = None):
        """Add a warning."""
        self.issues.append(ValidationIssue("warning", line, message, suggestion))

    def add_info(self, line: int | None, message: str, suggestion: str | None = None):
        """Add an info message."""
        if self.strict:  # Only show info in strict mode
            self.issues.append(ValidationIssue("info", line, message, suggestion))

    def check_imports(self):
        """Check for required FastMCP imports."""
        has_fastmcp_import = False

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == "fastmcp":
                    has_fastmcp_import = True
                    # Check what's imported
                    imported_names = [alias.name for alias in node.names]
                    if "FastMCP" not in imported_names:
                        self.add_warning(
                            node.lineno,
                            "FastMCP class not imported from fastmcp",
                            "Add: from fastmcp import FastMCP"
                        )

        if not has_fastmcp_import:
            self.add_error(
                None,
                "Missing FastMCP import",
                "Add: from fastmcp import FastMCP"
            )

    def check_server_init(self):
        """Check for FastMCP server initialization."""
        has_server_init = False

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                # Check for: mcp = FastMCP("server-name")
                if (isinstance(node.value, ast.Call) and
                    isinstance(node.value.func, ast.Name) and
                    node.value.func.id == "FastMCP"):
                    has_server_init = True

                    # Check server name argument
                    if not node.value.args:
                        self.add_error(
                            node.lineno,
                            "FastMCP initialized without server name",
                            'Use: mcp = FastMCP("server-name")'
                        )

        if not has_server_init:
            self.add_error(
                None,
                "No FastMCP server initialization found",
                'Add: mcp = FastMCP("server-name")'
            )

    def check_decorators(self):
        """Check decorator usage on functions."""
        tool_count = 0
        resource_count = 0
        prompt_count = 0

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                decorators = [self.get_decorator_name(d) for d in node.decorator_list]

                if "mcp.tool" in decorators:
                    tool_count += 1
                    self.check_tool_function(node)

                if "mcp.resource" in decorators:
                    resource_count += 1
                    self.check_resource_function(node)

                if "mcp.prompt" in decorators:
                    prompt_count += 1
                    self.check_prompt_function(node)

        # Summary
        if tool_count == 0 and resource_count == 0 and prompt_count == 0:
            self.add_warning(
                None,
                "No tools, resources, or prompts defined",
                "Add @mcp.tool(), @mcp.resource(), or @mcp.prompt() decorators"
            )
        else:
            self.add_info(
                None,
                f"Found: {tool_count} tools, {resource_count} resources, {prompt_count} prompts"
            )

    def check_tool_function(self, node: ast.FunctionDef):
        """Check a tool function for best practices."""
        # Check for docstring
        if not ast.get_docstring(node):
            self.add_warning(
                node.lineno,
                f"Tool '{node.name}' missing docstring",
                "Add comprehensive docstring with Args and Returns sections"
            )

    def check_resource_function(self, node: ast.FunctionDef):
        """Check a resource function for best practices."""
        # Resource should have URI parameter in decorator
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                if (isinstance(decorator.func, ast.Attribute) and
                    decorator.func.attr == "resource"):
                    if not decorator.args:
                        self.add_error(
                            node.lineno,
                            f"Resource '{node.name}' missing URI",
                            'Use: @mcp.resource("resource://path")'
                        )

    def check_prompt_function(self, node: ast.FunctionDef):
        """Check a prompt function for best practices."""
        # Check return type
        if node.returns:
            return_type = ast.unparse(node.returns)
            if return_type not in ["str", "list[PromptMessage]"]:
                self.add_warning(
                    node.lineno,
                    f"Prompt '{node.name}' has unusual return type: {return_type}",
                    "Prompts typically return str or list[PromptMessage]"
                )

    def check_type_hints(self):
        """Check for type hints on function parameters."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # Skip if not a decorated function
                if not node.decorator_list:
                    continue

                decorators = [self.get_decorator_name(d) for d in node.decorator_list]
                if not any(d.startswith("mcp.") for d in decorators):
                    continue

                # Check each parameter has type hint
                for arg in node.args.args:
                    if arg.arg == "self":
                        continue

                    if arg.annotation is None:
                        self.add_warning(
                            node.lineno,
                            f"Parameter '{arg.arg}' in '{node.name}' missing type hint",
                            f"Add type hint: {arg.arg}: str"
                        )

                # Check return type hint
                if node.returns is None:
                    self.add_warning(
                        node.lineno,
                        f"Function '{node.name}' missing return type hint",
                        "Add return type hint: -> str"
                    )

    def check_async_patterns(self):
        """Check for async/await patterns."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                decorators = [self.get_decorator_name(d) for d in node.decorator_list]
                if not any(d.startswith("mcp.") for d in decorators):
                    continue

                # Check if function uses await but isn't async
                has_await = self.has_await(node)
                is_async = isinstance(node, ast.AsyncFunctionDef)

                if has_await and not is_async:
                    self.add_error(
                        node.lineno,
                        f"Function '{node.name}' uses await but is not async",
                        f"Change to: async def {node.name}(...)"
                    )

    def check_context_usage(self):
        """Check for Context injection usage."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                decorators = [self.get_decorator_name(d) for d in node.decorator_list]
                if not any(d.startswith("mcp.") for d in decorators):
                    continue

                # Check if function has Context parameter
                has_context_param = False
                context_has_type_hint = False

                for arg in node.args.args:
                    if arg.arg in ["ctx", "context"]:
                        has_context_param = True
                        if arg.annotation:
                            type_hint = ast.unparse(arg.annotation)
                            if "Context" in type_hint:
                                context_has_type_hint = True

                # If has context param, ensure it has type hint
                if has_context_param and not context_has_type_hint:
                    self.add_error(
                        node.lineno,
                        f"Context parameter in '{node.name}' missing type hint",
                        "Add type hint: ctx: Context"
                    )

                # Check if function uses ctx but not async
                if has_context_param and not isinstance(node, ast.AsyncFunctionDef):
                    self.add_warning(
                        node.lineno,
                        f"Function '{node.name}' has Context parameter but is not async",
                        "Context methods are async - make function async"
                    )

    def check_best_practices(self):
        """Check for FastMCP best practices."""
        # Check for main block
        has_main_block = False

        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                if (isinstance(node.test, ast.Compare) and
                    isinstance(node.test.left, ast.Name) and
                    node.test.left.id == "__name__"):
                    has_main_block = True

        if not has_main_block:
            self.add_info(
                None,
                "Missing if __name__ == '__main__' block",
                "Add: if __name__ == '__main__': mcp.run()"
            )

    def get_decorator_name(self, decorator: ast.expr) -> str:
        """Get decorator name as string."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{ast.unparse(decorator.value)}.{decorator.attr}"
        elif isinstance(decorator, ast.Call):
            return self.get_decorator_name(decorator.func)
        return ""

    def has_await(self, node: ast.AST) -> bool:
        """Check if AST node contains await expressions."""
        for child in ast.walk(node):
            if isinstance(child, ast.Await):
                return True
        return False

    def print_results(self):
        """Print validation results."""
        if not self.issues:
            print("✅ No issues found!\n")
            return

        # Group by severity
        errors = [i for i in self.issues if i.severity == "error"]
        warnings = [i for i in self.issues if i.severity == "warning"]
        infos = [i for i in self.issues if i.severity == "info"]

        # Print errors
        if errors:
            print(f"❌ Errors ({len(errors)}):")
            for issue in errors:
                self.print_issue(issue)
            print()

        # Print warnings
        if warnings:
            print(f"⚠️  Warnings ({len(warnings)}):")
            for issue in warnings:
                self.print_issue(issue)
            print()

        # Print info
        if infos:
            print(f"ℹ️  Info ({len(infos)}):")
            for issue in infos:
                self.print_issue(issue)
            print()

        # Summary
        print(f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")

    def print_issue(self, issue: ValidationIssue):
        """Print a single issue."""
        location = f"Line {issue.line}" if issue.line else "General"
        print(f"  [{location}] {issue.message}")
        if issue.suggestion:
            print(f"    💡 {issue.suggestion}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate FastMCP server files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s server.py
  %(prog)s server.py --strict
  %(prog)s path/to/my_server.py
        """
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Path to FastMCP server file to validate"
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode (show all info messages)"
    )

    args = parser.parse_args()

    # Validate
    validator = FastMCPValidator(args.file, strict=args.strict)
    success = validator.validate()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
