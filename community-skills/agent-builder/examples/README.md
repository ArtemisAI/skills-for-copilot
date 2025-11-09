# Agent Builder Examples

This directory contains working examples demonstrating how to build agents with the Claude Agent SDK.

## Prerequisites

```bash
# Install Claude Agent SDK
pip install claude-agent-sdk

# Install Claude Code CLI (required)
npm install -g @anthropic-ai/claude-code

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Examples

### 1. Simple Calculator Agent (`simple_calculator_agent.py`)

**Demonstrates:**
- Basic `query()` function usage
- Simple system prompt configuration
- Task-oriented agent design
- Turn limits for safety

**Run:**
```bash
python simple_calculator_agent.py
```

**What it does:**
- Performs mathematical calculations
- Shows step-by-step work
- Uses Python code execution for complex math

**Key learnings:**
- How to use the simplest agent pattern
- Configuring system prompts
- Setting turn limits

---

### 2. Security Auditor Agent (`security_auditor_agent.py`)

**Demonstrates:**
- `ClaudeSDKClient` for interactive agents
- Custom tools with `@tool` decorator
- Tool parameter validation
- Structured error handling
- Multi-step workflows

**Run:**
```bash
python security_auditor_agent.py
```

**What it does:**
- Scans files for security vulnerabilities
- Detects SQL injection, hardcoded secrets, command injection
- Generates formatted security reports
- Prioritizes findings by severity

**Key learnings:**
- How to create custom tools
- Input validation and error handling
- Structured output formatting
- Multi-step agent workflows

---

## Usage Patterns

### Pattern 1: Simple One-Shot Queries

Use `query()` for straightforward, single-interaction tasks:

```python
async for message in query(
    prompt="Your task here",
    system_prompt="Agent instructions",
    turn_limit=10
):
    print(message)
```

**When to use:**
- Simple, self-contained tasks
- No custom tools needed
- One-way communication (no follow-up)

### Pattern 2: Interactive Agents with Custom Tools

Use `ClaudeSDKClient` with custom tools for complex, interactive tasks:

```python
client = ClaudeSDKClient(
    system_prompt="Agent role and instructions",
    tools=[tool1, tool2],
    turn_limit=20
)

response = await client.send_message("Your task")
```

**When to use:**
- Multi-step workflows
- Custom domain-specific tools
- Bidirectional interaction
- Complex verification loops

---

## Extending the Examples

### Adding New Tools

```python
from claude_agent_sdk import tool

@tool(
    "your_tool_name",
    "Brief description of what the tool does",
    {
        "param1": str,
        "param2": int,
        "param3": Literal["option1", "option2"]
    }
)
async def your_tool_name(args):
    """
    Detailed docstring explaining:
    - What the tool does
    - Parameter details
    - Return format
    - Error handling
    """
    # Implementation
    result = do_something(args["param1"], args["param2"])

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(result, indent=2)
        }]
    }
```

### Adding Verification Loops

```python
# In system prompt:
"""
After completing each task:
1. Verify the result using appropriate tools
2. If issues found, iterate to fix
3. Only proceed when verification passes
"""

# Example verification tool:
@tool("verify_output", "Verify output meets requirements")
async def verify_output(args):
    # Verification logic
    if meets_requirements(args["output"]):
        return {"content": [{"type": "text", "text": "✓ Verification passed"}]}
    else:
        return {"content": [{"type": "text", "text": "✗ Issues found: ..."}]}
```

---

## Common Issues

### Issue: "Claude Code CLI not found"

**Solution:**
```bash
npm install -g @anthropic-ai/claude-code
```

### Issue: "Authentication failed"

**Solution:**
Check your API key is set correctly:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
# Verify it's set:
echo $ANTHROPIC_API_KEY
```

### Issue: "Agent hangs indefinitely"

**Cause:** Agent execution is async and long-running

**Solution:** Always use `asyncio.run()` and set appropriate `turn_limit`:
```python
async for message in query(prompt="...", turn_limit=10):
    print(message)
```

---

## Next Steps

1. **Modify existing examples:** Change prompts, add new tools, adjust verification
2. **Create your own agent:** Start with a template and customize
3. **Read the guides:** Check `../references/` for detailed guides on:
   - Tool design best practices
   - Context management strategies
   - Verification techniques
4. **Explore the SDK:** Read official documentation at https://docs.claude.com/en/api/agent-sdk/overview

---

## Resources

- [Claude Agent SDK Documentation](https://docs.claude.com/en/api/agent-sdk/overview)
- [Python SDK GitHub](https://github.com/anthropics/claude-agent-sdk-python)
- [Agent Building Guide](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Tool Design Guide](../references/tool_design.md)
- [Context Management Guide](../references/context_management.md)
- [Verification Strategies](../references/verification.md)
