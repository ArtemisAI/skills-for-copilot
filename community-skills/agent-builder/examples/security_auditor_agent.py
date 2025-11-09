"""
Security Auditor Agent Example

This example demonstrates:
- ClaudeSDKClient usage
- Custom tools with @tool decorator
- Tool parameters and validation
- Error handling and reporting
- Verification loops

Purpose: Show a practical agent with custom tools and verification
"""

import asyncio
import os
import re
import json
from typing import Literal
from claude_agent_sdk import ClaudeSDKClient, tool


# Security patterns to check
SECURITY_PATTERNS = {
    "sql_injection": {
        "pattern": r'execute\(["\'].*\+.*["\']\)|cursor\.execute\(.*%.*\)',
        "severity": "critical",
        "message": "Potential SQL injection: Use parameterized queries",
        "example": "Use cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
    },
    "hardcoded_secret": {
        "pattern": r'(api_key|password|secret|token|credential)\s*=\s*["\'][^"\']{8,}["\']',
        "severity": "critical",
        "message": "Hardcoded secret detected: Use environment variables",
        "example": "Use os.environ.get('API_KEY') instead"
    },
    "command_injection": {
        "pattern": r'os\.system\(.*\+.*\)|subprocess\.(call|run)\(.*shell=True.*\)',
        "severity": "high",
        "message": "Potential command injection: Avoid shell=True with user input",
        "example": "Use subprocess.run(['command', arg1, arg2]) without shell=True"
    },
    "insecure_random": {
        "pattern": r'import random\n.*random\.(randint|choice)',
        "severity": "medium",
        "message": "Insecure randomness: Use secrets module for cryptographic purposes",
        "example": "Use secrets.token_bytes() or secrets.token_hex()"
    }
}


@tool(
    "scan_file_for_vulnerabilities",
    "Scan a single file for security vulnerabilities using pattern matching",
    {
        "file_path": str,
        "severity_threshold": Literal["critical", "high", "medium", "low"]
    }
)
async def scan_file_for_vulnerabilities(args):
    """
    Scan a file for common security vulnerabilities.

    Returns:
    - JSON object with findings
    - Each finding includes: type, severity, line number, code snippet, message, fix example
    """
    file_path = args["file_path"]
    severity_threshold = args.get("severity_threshold", "low")

    # Check if file exists
    if not os.path.exists(file_path):
        return {
            "content": [{
                "type": "text",
                "text": f"Error: File not found: {file_path}"
            }]
        }

    # Read file
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error reading file {file_path}: {str(e)}"
            }]
        }

    # Scan for vulnerabilities
    findings = []
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    threshold_level = severity_order[severity_threshold]

    for vuln_type, config in SECURITY_PATTERNS.items():
        matches = re.finditer(config["pattern"], content, re.MULTILINE | re.DOTALL)
        for match in matches:
            # Only include if severity meets threshold
            if severity_order[config["severity"]] <= threshold_level:
                line_num = content[:match.start()].count('\n') + 1
                findings.append({
                    "type": vuln_type,
                    "severity": config["severity"],
                    "line": line_num,
                    "code": match.group(0)[:100],  # Truncate long matches
                    "message": config["message"],
                    "fix_example": config["example"]
                })

    # Sort by severity
    findings.sort(key=lambda x: severity_order[x["severity"]])

    # Format response
    if findings:
        summary = {
            "file": file_path,
            "total_findings": len(findings),
            "by_severity": {
                "critical": sum(1 for f in findings if f["severity"] == "critical"),
                "high": sum(1 for f in findings if f["severity"] == "high"),
                "medium": sum(1 for f in findings if f["severity"] == "medium"),
                "low": sum(1 for f in findings if f["severity"] == "low")
            },
            "findings": findings
        }

        return {
            "content": [{
                "type": "text",
                "text": f"⚠️ Security scan found {len(findings)} issues:\n\n" +
                        json.dumps(summary, indent=2)
            }]
        }
    else:
        return {
            "content": [{
                "type": "text",
                "text": f"✓ No security issues found in {file_path}"
            }]
        }


@tool(
    "generate_security_report",
    "Generate a comprehensive security report from scan findings",
    {
        "findings": dict,
        "format": Literal["json", "markdown"]
    }
)
async def generate_security_report(args):
    """
    Generate a formatted security report.

    Returns:
    - Security report in requested format (JSON or Markdown)
    """
    findings = args["findings"]
    output_format = args.get("format", "markdown")

    if output_format == "json":
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(findings, indent=2)
            }]
        }
    else:  # markdown
        report = f"""# Security Audit Report

## Executive Summary

- **Files Scanned**: {findings.get('files_scanned', 0)}
- **Total Issues**: {findings.get('total_issues', 0)}
- **Critical Issues**: {findings.get('critical', 0)}
- **High Severity Issues**: {findings.get('high', 0)}
- **Medium Severity Issues**: {findings.get('medium', 0)}
- **Low Severity Issues**: {findings.get('low', 0)}

## Findings

"""
        for file, file_findings in findings.get('files', {}).items():
            report += f"\n### {file}\n\n"
            for finding in file_findings:
                report += f"**{finding['type'].replace('_', ' ').title()}** (Line {finding['line']}) - {finding['severity'].upper()}\n"
                report += f"- **Issue**: {finding['message']}\n"
                report += f"- **Fix**: {finding['fix_example']}\n\n"

        report += "\n## Recommendations\n\n"
        report += "1. Address all critical and high severity issues immediately\n"
        report += "2. Review medium severity issues and prioritize based on risk\n"
        report += "3. Implement automated security scanning in CI/CD pipeline\n"
        report += "4. Conduct regular security audits\n"

        return {
            "content": [{
                "type": "text",
                "text": report
            }]
        }


async def main():
    """
    Security auditor agent that scans files for vulnerabilities
    """

    # Create agent with custom tools
    client = ClaudeSDKClient(
        system_prompt="""
You are a senior security engineer specializing in code security audits.

Your role:
1. Scan codebases for security vulnerabilities
2. Identify and prioritize issues by severity
3. Provide actionable remediation recommendations
4. Generate comprehensive security reports

Tools available:
- scan_file_for_vulnerabilities: Scan individual files
- generate_security_report: Create formatted reports

Guidelines:
- Focus on critical and high severity issues first
- Provide clear, actionable feedback
- Include fix examples for each issue
- Generate reports in the format requested by the user

Do not:
- Proceed without file access
- Skip verification of findings
- Overlook context-specific security considerations
""",
        tools=[scan_file_for_vulnerabilities, generate_security_report],
        turn_limit=20
    )

    # Example task
    task = """
    Scan this directory for security vulnerabilities:
    - Focus on Python files (*.py)
    - Look for: SQL injection, hardcoded secrets, command injection, insecure randomness
    - Prioritize critical and high severity issues
    - Generate a markdown security report

    Start by finding all Python files, then scan each one.
    """

    print("Starting security auditor agent...\n")
    print(f"Task: {task}\n")
    print("=" * 80 + "\n")

    try:
        # Send task to agent
        response = await client.send_message(task)
        print(response)

    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 80)
    print("Agent completed!")


if __name__ == "__main__":
    asyncio.run(main())
