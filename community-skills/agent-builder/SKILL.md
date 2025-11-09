---
name: agent-builder
description: Guide for building AI agents using the Anthropic Claude Agent SDK. Use when building custom autonomous agents that can perform complex, multi-step tasks with tools, context management, and verification loops. Supports both Python and TypeScript implementations.
license: MIT
---

# Agent Builder with Claude Agent SDK

## Overview

To create production-ready AI agents that can autonomously perform complex tasks, use this skill. The Claude Agent SDK (formerly Claude Code SDK) provides the battle-tested infrastructure powering Claude Code, enabling developers to build custom agents with automatic context management, rich tool ecosystems, and robust error handling.

An effective agent operates on a feedback loop: **gather context → take action → verify work → repeat**. This skill guides through the complete process of designing, implementing, and deploying agents that follow this pattern.

---

# Process

## 🚀 High-Level Workflow

Building a production-ready agent involves four main phases:

### Phase 1: Agent Design and Planning

#### 1.1 Define Agent Purpose and Scope

Before implementation, clearly define:
- **Primary task**: What is the agent's main objective?
- **Success criteria**: How to measure if the agent accomplished its goal?
- **Scope boundaries**: What should the agent NOT attempt to do?
- **User interaction model**: Fully autonomous, semi-autonomous, or human-in-the-loop?

**Examples of well-defined agent purposes:**
- "Review pull requests for code quality issues and suggest improvements"
- "Analyze customer support tickets and draft responses for human review"
- "Monitor system logs for anomalies and generate incident reports"
- "Research companies and compile competitive analysis reports"

#### 1.2 Identify Required Capabilities

Based on the agent's purpose, determine what capabilities are needed:

**Context Gathering:**
- File system access (read/write files)
- Web search (research and information gathering)
- API integrations (Slack, GitHub, databases)
- Document parsing (PDF, Excel, Word)

**Action Execution:**
- Code generation (Python, TypeScript, SQL)
- Bash commands (system operations)
- Tool invocations (custom domain-specific tools)
- External API calls (REST, GraphQL)

**Verification:**
- Rules-based validation (linting, schema validation)
- Visual feedback (screenshots for UI work)
- LLM-as-judge evaluation (fuzzy criteria)
- Unit tests (automated testing)

#### 1.3 Study Claude Agent SDK Documentation

**Load the following documentation:**

Use WebFetch to load these resources:
- **Agent SDK Overview**: `https://docs.claude.com/en/api/agent-sdk/overview`
- **Python SDK README**: `https://raw.githubusercontent.com/anthropics/claude-agent-sdk-python/main/README.md`
- **Engineering Blog**: `https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk`

**Also read these reference files:**
- [🔧 Tool Design Guide](./references/tool_design.md) - Best practices for creating effective agent tools
- [📊 Context Management Guide](./references/context_management.md) - Strategies for efficient context usage
- [✅ Verification Strategies](./references/verification.md) - Methods for ensuring agent correctness

#### 1.4 Plan Tool Architecture

Design the tool ecosystem the agent will use:

**Built-in Tools (Available by Default):**
- File operations (Read, Write, Edit, Glob)
- Code execution (Bash, Python)
- Web capabilities (WebFetch, WebSearch)
- Grep (content search)

**Custom Tools (Define for Domain-Specific Needs):**
- Identify operations that will be performed frequently
- Design tools that represent complete workflows, not just API wrappers
- Plan input schemas with proper validation
- Define clear, actionable error messages

**MCP Integrations (For Third-Party Services):**
- Identify external services needed (Slack, GitHub, databases)
- Plan authentication flows
- Consider rate limiting and error handling

#### 1.5 Design Context Management Strategy

Plan how the agent will handle context efficiently:

**Agentic Search vs Semantic Search:**
- **Agentic search**: Claude uses bash commands (grep, tail) to find information - slower but more accurate
- **Semantic search**: Vector-based search - faster but requires maintenance and less transparent
- **Recommendation**: Start with agentic search; add semantic search only if speed becomes critical

**Folder Structure as Context Engineering:**
- Organize files to make information discoverable
- Use clear naming conventions
- Consider how the agent will search for information

**Subagents for Parallelization:**
- Identify tasks that can run in parallel
- Design subagent interfaces to return only essential information
- Plan orchestration logic

**Compaction Strategy:**
- The SDK automatically compacts context when limits approach
- Design system prompts to remain relevant after compaction
- Test agent behavior with long-running sessions

---

### Phase 2: Implementation

Now implement the agent following language-specific best practices.

#### 2.1 Set Up Development Environment

**For Python (Recommended for most use cases):**

```bash
# Install SDK
pip install claude-agent-sdk

# Install Claude Code CLI (required)
npm install -g @anthropic-ai/claude-code

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

**For TypeScript:**

```bash
# Install SDK
npm install @anthropic-ai/claude-agent-sdk

# Install Claude Code CLI (required)
npm install -g @anthropic-ai/claude-code

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

**Requirements:**
- Python 3.10+ (for Python SDK)
- Node.js (for CLI and TypeScript SDK)
- Claude Code 2.0.0+

#### 2.2 Implement Basic Agent Loop

**For Python - Simple Query Pattern:**

```python
from claude_agent_sdk import query

async def run_agent():
    async for message in query(
        prompt="Analyze the codebase and identify potential security issues",
        system_prompt="You are a security auditor. Focus on finding vulnerabilities.",
        working_directory="/path/to/codebase"
    ):
        print(message)
```

**For Python - Interactive Agent with Custom Tools:**

```python
from claude_agent_sdk import ClaudeSDKClient, tool

@tool("check_vulnerability", "Check if a code pattern is vulnerable", {"pattern": str, "file_path": str})
async def check_vulnerability(args):
    # Custom security checking logic
    pattern = args["pattern"]
    file_path = args["file_path"]
    # ... implementation ...
    return {
        "content": [{
            "type": "text",
            "text": f"Analysis results for {file_path}: ..."
        }]
    }

async def run_interactive_agent():
    client = ClaudeSDKClient(
        system_prompt="You are a security auditor with access to custom vulnerability checking tools.",
        tools=[check_vulnerability]
    )

    response = await client.send_message(
        "Audit the authentication module for security issues"
    )
    print(response)
```

#### 2.3 Implement Custom Tools

Custom tools are the primary way to extend agent capabilities. Follow these principles:

**Tool Design Principles (see [Tool Design Guide](./references/tool_design.md) for details):**
- Represent complete workflows, not just API wrappers
- Provide clear, actionable error messages that guide the agent
- Use descriptive parameter names and comprehensive descriptions
- Include examples in parameter descriptions
- Return structured data that's easy for agents to parse

**Python Tool Implementation:**

```python
from claude_agent_sdk import tool
from typing import Literal

@tool(
    "analyze_sentiment",
    "Analyze sentiment of customer feedback and categorize urgency",
    {
        "feedback_text": str,
        "include_suggestions": bool,
        "format": Literal["json", "markdown"]
    }
)
async def analyze_sentiment(args):
    feedback = args["feedback_text"]
    include_suggestions = args.get("include_suggestions", False)
    output_format = args.get("format", "json")

    # Implement sentiment analysis logic
    sentiment_score = analyze_text(feedback)
    urgency = determine_urgency(sentiment_score)

    if output_format == "json":
        result = {
            "sentiment": sentiment_score,
            "urgency": urgency,
            "suggestions": generate_suggestions(feedback) if include_suggestions else None
        }
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    else:
        # Return markdown format
        markdown = format_as_markdown(sentiment_score, urgency)
        return {"content": [{"type": "text", "text": markdown}]}
```

**Key Implementation Details:**
- Use type hints for parameters
- Provide default values for optional parameters
- Handle errors gracefully with clear messages
- Return responses in the format: `{"content": [{"type": "text", "text": "..."}]}`

#### 2.4 Implement Hooks for Control Flow

Hooks provide deterministic checkpoints in the agent loop. Common use cases:

**Pre-Tool-Use Hook (Validation and Safety):**

```python
async def validate_bash_command(input_data, tool_use_id, context):
    """Prevent dangerous bash commands from executing"""
    command = input_data.get("command", "")

    # Check for dangerous patterns
    dangerous_patterns = ["rm -rf /", ":(){ :|:& };:", "mkfs", "dd if="]
    for pattern in dangerous_patterns:
        if pattern in command:
            return {
                "permitToolUse": False,
                "error": f"Dangerous command blocked: {pattern} is not allowed"
            }

    return {"permitToolUse": True}

client = ClaudeSDKClient(
    hooks={"pre_tool_use": validate_bash_command}
)
```

**Post-Tool-Use Hook (Logging and Monitoring):**

```python
async def log_tool_usage(result, tool_use_id, context):
    """Log all tool usage for monitoring"""
    logger.info(f"Tool {tool_use_id} executed with result: {result}")
    return {}

client = ClaudeSDKClient(
    hooks={"post_tool_use": log_tool_usage}
)
```

#### 2.5 Implement Context Management

**Using Subagents for Parallelization:**

```python
# Create subagent as markdown file
subagent_prompt = """
Analyze the given file for security vulnerabilities.

Return only:
1. File path
2. Number of issues found
3. Severity (critical/high/medium/low)

Do not include full code listings or detailed explanations.
"""

# Save to .claude/subagents/security_checker.md
# Agent can invoke: "Use the security_checker subagent to analyze auth.py"
```

**Configuring Working Directory:**

```python
async for message in query(
    prompt="Analyze this codebase",
    working_directory="/path/to/project",  # Agent has access to these files
    turn_limit=50  # Prevent infinite loops
):
    print(message)
```

#### 2.6 Add Verification Logic

Implement verification strategies appropriate for the task:

**Rules-Based Verification (Code Quality):**

```python
@tool("validate_code", "Run linting and type checking on code", {"file_path": str})
async def validate_code(args):
    file_path = args["file_path"]

    # Run multiple validators
    lint_result = run_linter(file_path)
    type_result = run_type_checker(file_path)
    test_result = run_tests(file_path)

    issues = []
    if not lint_result.success:
        issues.extend(lint_result.errors)
    if not type_result.success:
        issues.extend(type_result.errors)
    if not test_result.success:
        issues.extend(test_result.failures)

    if issues:
        return {
            "content": [{
                "type": "text",
                "text": f"Validation failed with {len(issues)} issues:\n" +
                        "\n".join(f"- {issue}" for issue in issues)
            }]
        }
    else:
        return {
            "content": [{
                "type": "text",
                "text": "All validation checks passed!"
            }]
        }
```

**Visual Verification (UI Work):**

```python
@tool("verify_ui", "Take screenshot of rendered UI and verify layout", {"url": str})
async def verify_ui(args):
    url = args["url"]

    # Take screenshot using playwright or similar
    screenshot_path = take_screenshot(url)

    # Return screenshot for agent to analyze
    return {
        "content": [{
            "type": "text",
            "text": f"Screenshot saved to {screenshot_path}. Please review the layout."
        }]
    }
```

---

### Phase 3: Testing and Refinement

After initial implementation, thoroughly test and refine the agent.

#### 3.1 Create Test Scenarios

Design test cases that cover:

**Happy Path Scenarios:**
- Typical use cases with expected inputs
- Multi-step workflows
- Tool combinations

**Edge Cases:**
- Missing or invalid inputs
- Rate limiting and timeouts
- Partially available data
- Ambiguous requests

**Failure Scenarios:**
- Authentication failures
- Network errors
- Resource exhaustion
- Malformed responses

#### 3.2 Monitor Agent Behavior

During testing, observe:

**Context Usage:**
- Is the agent efficiently using context?
- Does it load unnecessary information?
- Does compaction happen at appropriate times?

**Tool Usage Patterns:**
- Does the agent use tools as intended?
- Are there unnecessary tool calls?
- Does it handle errors gracefully?

**Verification Effectiveness:**
- Does the agent catch its own mistakes?
- Are verification loops terminating properly?
- Is feedback leading to improvements?

#### 3.3 Iterate on Tool Design

Based on testing, refine tools:

**Common Issues and Solutions:**
- **Tool returns too much data**: Add pagination or filtering parameters
- **Agent misuses tool**: Improve tool description and parameter docs
- **Tool errors are unclear**: Enhance error messages with actionable guidance
- **Tool too narrow**: Combine related operations into workflow tools

#### 3.4 Optimize System Prompt

Refine the system prompt based on observed behavior:

**System Prompt Best Practices:**
- Be specific about agent's role and expertise
- Include explicit guidelines for tool usage
- Define clear success criteria
- Provide examples of good outputs
- Set boundaries on what not to do

**Example System Prompt:**

```
You are a senior security engineer specializing in code audits. Your role is to:

1. Analyze codebases for security vulnerabilities
2. Prioritize issues by severity (critical, high, medium, low)
3. Provide actionable remediation recommendations
4. Generate detailed audit reports

Guidelines:
- Use the check_vulnerability tool for pattern-based scanning
- Review authentication, authorization, and data validation code carefully
- Flag any hardcoded credentials or API keys
- Consider OWASP Top 10 categories in your analysis

Output format:
- Executive summary with key findings
- Detailed vulnerability list with code references
- Remediation steps for each issue
- Risk assessment and prioritization

Do not:
- Modify code without explicit permission
- Skip verification of potential false positives
- Proceed if authentication tokens are unavailable
```

---

### Phase 4: Deployment and Monitoring

Prepare the agent for production use.

#### 4.1 Error Handling Strategy

Implement comprehensive error handling:

**SDK-Specific Exceptions:**

```python
from claude_agent_sdk import (
    CLINotFoundError,
    CLIConnectionError,
    ProcessError,
    CLIJSONDecodeError
)

async def run_agent_with_error_handling():
    try:
        async for message in query(prompt="..."):
            process_message(message)

    except CLINotFoundError:
        print("Error: Claude Code CLI not installed. Run: npm install -g @anthropic-ai/claude-code")

    except CLIConnectionError as e:
        print(f"Connection error: {e}. Check your API key and network.")

    except ProcessError as e:
        print(f"Process failed with exit code {e.exit_code}: {e.stderr}")

    except CLIJSONDecodeError as e:
        print(f"Failed to parse response: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        # Log for debugging
        logger.exception("Agent execution failed")
```

**Graceful Degradation:**
- Implement fallback behaviors when tools fail
- Cache results to avoid redundant operations
- Set reasonable timeouts for long-running operations

#### 4.2 Logging and Monitoring

Implement comprehensive logging:

**What to Log:**
- All tool invocations and results
- Context compaction events
- Verification loop iterations
- Error occurrences and recoveries
- Performance metrics (latency, token usage)

**Example Logging Setup:**

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('security_agent')

async def run_agent_with_logging():
    logger.info("Starting security audit agent")

    try:
        async for message in query(prompt="Audit the codebase"):
            logger.info(f"Agent response: {message[:100]}...")

    except Exception as e:
        logger.exception("Agent failed")
        raise
```

#### 4.3 Performance Optimization

**Token Usage Optimization:**
- Use concise tool responses by default
- Offer detailed mode only when needed
- Implement aggressive compaction for long sessions
- Cache frequently accessed information

**Latency Optimization:**
- Run independent operations in parallel using subagents
- Batch API calls when possible
- Implement connection pooling for external services
- Use appropriate context window sizes

#### 4.4 Security Considerations

**Authentication and Secrets:**
- Never hardcode API keys or credentials
- Use environment variables or secure vaults
- Implement token rotation for long-running agents
- Audit tool permissions regularly

**Sandboxing and Isolation:**
- Run agents in isolated environments
- Restrict file system access via working_directory
- Use hooks to block dangerous operations
- Implement rate limiting to prevent abuse

**Audit Trail:**
- Log all agent actions for review
- Implement human-in-the-loop for sensitive operations
- Create audit reports for compliance
- Monitor for anomalous behavior

---

# Reference Files

## 📚 Documentation Library

Load these resources as needed during development:

### Core Documentation (Load First)
- **Agent SDK Overview**: Fetch from `https://docs.claude.com/en/api/agent-sdk/overview` - Complete SDK introduction
- **Python SDK**: Fetch from `https://raw.githubusercontent.com/anthropics/claude-agent-sdk-python/main/README.md` - Python SDK reference
- **Engineering Blog**: Fetch from `https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk` - Architectural insights

### Implementation Guides (Load During Development)
- [🔧 Tool Design Guide](./references/tool_design.md) - Comprehensive guide for creating effective agent tools
- [📊 Context Management Guide](./references/context_management.md) - Strategies for efficient context usage
- [✅ Verification Strategies](./references/verification.md) - Methods for ensuring agent correctness

### Example Implementations (Reference As Needed)
- [📝 Examples Directory](./examples/) - Working agent implementations for common use cases

---

# Quick Start Examples

## Simple One-Shot Agent

```python
from claude_agent_sdk import query

async def analyze_codebase():
    """Simple agent that analyzes a codebase once"""
    async for message in query(
        prompt="Review this codebase for potential bugs and code quality issues",
        system_prompt="You are an experienced code reviewer",
        working_directory="/path/to/project"
    ):
        print(message)
```

## Interactive Agent with Custom Tools

```python
from claude_agent_sdk import ClaudeSDKClient, tool

@tool("run_tests", "Execute test suite", {"test_path": str})
async def run_tests(args):
    # Run tests and return results
    result = execute_tests(args["test_path"])
    return {"content": [{"type": "text", "text": f"Tests: {result}"}]}

async def code_review_agent():
    """Interactive agent with custom test runner"""
    client = ClaudeSDKClient(
        system_prompt="You are a code reviewer. Use the run_tests tool to verify code quality.",
        tools=[run_tests]
    )

    response = await client.send_message(
        "Review the authentication module and run all relevant tests"
    )
    print(response)
```

---

# Common Use Cases

## Security Auditor Agent

**Purpose**: Scan codebases for security vulnerabilities

**Key Tools**:
- `check_vulnerability`: Pattern-based vulnerability detection
- `run_security_scan`: Execute security scanning tools
- `generate_report`: Create audit reports

**Verification**: Rules-based (OWASP guidelines, CWE patterns)

## Customer Support Agent

**Purpose**: Analyze support tickets and draft responses

**Key Tools**:
- `search_knowledge_base`: Find relevant documentation
- `check_ticket_history`: Review customer history
- `draft_response`: Generate response drafts

**Verification**: LLM-as-judge (tone, accuracy, completeness)

## Research Agent

**Purpose**: Gather and synthesize information from multiple sources

**Key Tools**:
- `web_search`: Search for information online
- `extract_content`: Parse and extract relevant data
- `synthesize_findings`: Combine information into reports

**Verification**: Citation checking, source credibility assessment

---

# Tips and Best Practices

## Agent Design
- Start simple; add complexity incrementally
- Define clear success criteria before building
- Test with real-world scenarios early
- Build verification loops into every agent

## Tool Development
- Design tools for workflows, not just API endpoints
- Make error messages actionable and specific
- Return concise responses by default
- Test tools independently before integration

## Context Management
- Use folder structure as documentation
- Start with agentic search; optimize later if needed
- Leverage subagents for parallelization
- Monitor context usage during development

## Debugging
- Examine failure cases specifically
- Check if agent has appropriate tools
- Verify system prompt clarity
- Test with turn limits to prevent infinite loops

## Performance
- Minimize unnecessary tool calls
- Cache expensive operations
- Use parallel execution where possible
- Monitor token usage and optimize prompts
