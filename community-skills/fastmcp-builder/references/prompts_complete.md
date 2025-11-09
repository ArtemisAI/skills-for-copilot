# Prompts Complete Reference

This guide provides comprehensive documentation for the `@mcp.prompt()` decorator in FastMCP, which enables you to create reusable prompt templates that LLM agents can use.

---

## Table of Contents

1. [Overview](#overview)
2. [The @prompt Decorator](#the-prompt-decorator)
3. [Decorator Parameters Reference](#decorator-parameters-reference)
4. [Static vs Dynamic Prompts](#static-vs-dynamic-prompts)
5. [Arguments and Variables](#arguments-and-variables)
6. [Return Types](#return-types)
7. [Prompt Metadata](#prompt-metadata)
8. [Context Injection](#context-injection)
9. [Common Patterns](#common-patterns)
10. [Troubleshooting](#troubleshooting)

---

## Overview

**Prompts** are reusable prompt templates that help agents accomplish specific tasks. They provide structured guidance, context, and instructions that improve agent performance on common workflows.

**Key Characteristics:**
- **Reusable**: Templates can be used multiple times with different arguments
- **Parameterized**: Accept arguments to customize behavior
- **Structured**: Provide consistent format and instructions
- **Discoverable**: Agents can list and select appropriate prompts

**Common Use Cases:**
- Code review templates
- Documentation generation
- Analysis frameworks
- Testing strategies
- Refactoring guides
- Debugging workflows
- Report generation

**Why Use Prompts:**
- **Consistency**: Ensure agents follow best practices
- **Efficiency**: Save tokens by reusing well-crafted instructions
- **Guidance**: Help agents tackle complex, multi-step tasks
- **Standardization**: Establish common patterns across workflows

---

## The @prompt Decorator

The `@mcp.prompt()` decorator converts a Python function into an MCP prompt template.

### Basic Syntax

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.prompt()
def code_review() -> str:
    """
    Guide for reviewing code changes.

    Returns:
        Code review prompt template
    """
    return """Please review the following code changes:

1. Check for correctness and logic errors
2. Verify error handling is comprehensive
3. Ensure code follows best practices
4. Look for security vulnerabilities
5. Suggest improvements for readability

Provide detailed feedback with specific line references."""
```

### Full Decorator Signature

```python
@mcp.prompt(
    name: str | None = None,               # Prompt name (optional)
    description: str | None = None,        # Description (optional)
    enabled: bool = True,                  # Enable/disable prompt
    _meta: dict | None = None              # Internal metadata
)
```

---

## Decorator Parameters Reference

### 1. `name` (Optional)

Human-readable prompt name. If not provided, FastMCP derives it from the function name.

```python
@mcp.prompt(name="Code Review Guide")
def code_review_prompt() -> str:
    return "Review the code for..."
```

### 2. `description` (Optional)

Detailed description of what the prompt does and when to use it. If not provided, uses the function's docstring.

```python
@mcp.prompt(
    name="API Documentation Generator",
    description="Generates comprehensive API documentation from code with examples, parameter descriptions, and usage notes"
)
def api_docs() -> str:
    return "Generate API documentation for..."
```

### 3. `enabled` (Optional, Default: True)

Whether the prompt is currently enabled. Useful for feature flags or conditional availability.

```python
EXPERIMENTAL_FEATURES = os.getenv("EXPERIMENTAL") == "true"

@mcp.prompt(
    name="Advanced Refactoring",
    enabled=EXPERIMENTAL_FEATURES
)
def advanced_refactoring() -> str:
    return "Perform advanced refactoring..."
```

### 4. `_meta` (Optional, Internal)

Internal metadata for FastMCP framework use. Generally not used in application code.

---

## Static vs Dynamic Prompts

### Static Prompts

Prompts that return the same template every time (no parameters).

```python
@mcp.prompt()
def security_audit() -> str:
    """
    Security audit checklist for code review.

    Returns:
        Security audit prompt
    """
    return """Perform a comprehensive security audit:

## Authentication & Authorization
- [ ] Verify authentication is properly implemented
- [ ] Check authorization controls are in place
- [ ] Ensure principle of least privilege

## Input Validation
- [ ] All user inputs are validated
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Command injection prevention

## Sensitive Data
- [ ] No hardcoded credentials
- [ ] Secrets are properly managed
- [ ] Sensitive data is encrypted

## Dependencies
- [ ] No known vulnerable dependencies
- [ ] Dependencies are up to date

Provide detailed findings for any issues discovered."""
```

### Dynamic Prompts

Prompts that generate customized templates based on parameters.

```python
@mcp.prompt()
def code_review(language: str, focus: str = "general") -> str:
    """
    Generate language-specific code review prompt.

    Args:
        language: Programming language (python, javascript, etc.)
        focus: Review focus area (general, security, performance)

    Returns:
        Customized code review prompt
    """
    base_prompt = f"Review the following {language} code:\n\n"

    if focus == "security":
        base_prompt += """Focus on security aspects:
- Input validation
- Authentication/authorization
- Secure data handling
- Known vulnerabilities
"""
    elif focus == "performance":
        base_prompt += """Focus on performance:
- Algorithm efficiency
- Resource usage
- Bottlenecks
- Optimization opportunities
"""
    else:
        base_prompt += """Provide comprehensive review:
- Correctness
- Best practices
- Readability
- Maintainability
"""

    return base_prompt
```

---

## Arguments and Variables

### Simple Arguments

```python
@mcp.prompt()
def test_plan(feature: str) -> str:
    """
    Generate test plan for a specific feature.

    Args:
        feature: Feature name to create test plan for

    Returns:
        Test plan prompt
    """
    return f"""Create a comprehensive test plan for: {feature}

## Test Coverage
1. Unit Tests
   - Test individual functions/methods
   - Edge cases and error conditions

2. Integration Tests
   - Test feature interactions
   - API endpoints (if applicable)

3. E2E Tests
   - User workflows
   - Critical paths

## Test Cases
For each test:
- Description
- Prerequisites
- Steps
- Expected result

Organize by priority (P0/P1/P2)."""
```

### Multiple Arguments

```python
@mcp.prompt()
def documentation(
    component: str,
    audience: str = "developers",
    include_examples: bool = True
) -> str:
    """
    Generate documentation template.

    Args:
        component: Component name to document
        audience: Target audience (developers, users, admins)
        include_examples: Whether to include code examples

    Returns:
        Documentation prompt
    """
    prompt = f"Create {audience}-focused documentation for: {component}\n\n"

    if audience == "developers":
        prompt += """## Developer Documentation
- API reference
- Architecture overview
- Integration guide
"""
    elif audience == "users":
        prompt += """## User Guide
- Getting started
- Common tasks
- Troubleshooting
"""
    else:
        prompt += """## Administrator Guide
- Installation
- Configuration
- Maintenance
"""

    if include_examples:
        prompt += "\nInclude practical examples for each section."

    return prompt
```

### Type-Constrained Arguments

```python
from typing import Literal

@mcp.prompt()
def refactoring_guide(
    pattern: Literal["extract_function", "extract_class", "rename", "move"],
    language: Literal["python", "javascript", "typescript", "go"]
) -> str:
    """
    Generate refactoring guide for specific pattern and language.

    Args:
        pattern: Refactoring pattern to apply
        language: Programming language

    Returns:
        Refactoring guide prompt
    """
    patterns = {
        "extract_function": "Extract Function refactoring",
        "extract_class": "Extract Class refactoring",
        "rename": "Rename refactoring",
        "move": "Move refactoring"
    }

    return f"""Guide for {patterns[pattern]} in {language}:

1. Identify refactoring opportunity
2. Plan the changes
3. Apply refactoring incrementally
4. Run tests after each step
5. Update documentation

Provide step-by-step instructions with code examples."""
```

---

## Return Types

### String (Standard)

Most common return type - return prompt as string.

```python
@mcp.prompt()
def bug_report() -> str:
    """Bug report template."""
    return """Please provide detailed bug report:

**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS:
- Version:
- Browser (if applicable):

**Additional Context**
Screenshots, logs, etc."""
```

### Multiline Strings

Use triple quotes for formatted, multiline prompts.

```python
@mcp.prompt()
def design_review() -> str:
    """Design review template."""
    return """# Design Review: [Component Name]

## Overview
Brief description of the design

## Goals
- Goal 1
- Goal 2

## Architecture
Describe the architecture and key components

## Data Model
Describe data structures and relationships

## API Design
List and describe API endpoints/interfaces

## Security Considerations
- Authentication
- Authorization
- Data protection

## Performance Considerations
- Expected load
- Scalability approach
- Caching strategy

## Testing Strategy
How will this be tested?

## Rollout Plan
How will this be deployed?

## Open Questions
List any unresolved questions

## Decision Log
Key decisions made and rationale"""
```

### Dynamic Content

Generate content based on context or external data.

```python
from datetime import datetime

@mcp.prompt()
def daily_standup(team: str) -> str:
    """
    Generate daily standup template for a team.

    Args:
        team: Team name

    Returns:
        Standup template
    """
    today = datetime.now().strftime("%Y-%m-%d")

    return f"""# Daily Standup - {team} Team
Date: {today}

For each team member:

## [Name]
### Yesterday
- What I completed

### Today
- What I plan to work on

### Blockers
- Any blockers or dependencies

---

## Action Items
List any action items from standup"""
```

---

## Prompt Metadata

### Using PromptMessage for Rich Prompts

For advanced use cases, return `PromptMessage` objects with role-based content.

```python
from fastmcp.prompts import PromptMessage

@mcp.prompt()
def code_explanation(code: str) -> list[PromptMessage]:
    """
    Generate structured prompt for code explanation.

    Args:
        code: Code snippet to explain

    Returns:
        Structured prompt messages
    """
    return [
        PromptMessage(
            role="system",
            content="You are an expert code educator. Explain code clearly and thoroughly."
        ),
        PromptMessage(
            role="user",
            content=f"""Explain the following code:

```
{code}
```

Include:
1. What the code does (high-level)
2. How it works (step-by-step)
3. Key concepts or patterns used
4. Potential improvements or issues"""
        )
    ]
```

### Multi-Turn Conversation Setup

```python
@mcp.prompt()
def pair_programming(task: str) -> list[PromptMessage]:
    """
    Set up pair programming conversation.

    Args:
        task: Programming task to work on

    Returns:
        Conversation setup messages
    """
    return [
        PromptMessage(
            role="system",
            content="""You are a pair programming partner. Work collaboratively:
- Ask clarifying questions
- Suggest approaches
- Catch potential issues
- Explain your reasoning"""
        ),
        PromptMessage(
            role="user",
            content=f"Let's work together on: {task}"
        ),
        PromptMessage(
            role="assistant",
            content="I'd be happy to help! Let me ask a few questions to understand the requirements better..."
        )
    ]
```

---

## Context Injection

Prompts can access context for logging and enhanced functionality.

```python
from fastmcp import Context

@mcp.prompt()
async def analysis_prompt(topic: str, ctx: Context) -> str:
    """
    Generate analysis prompt with context logging.

    Args:
        topic: Topic to analyze
        ctx: Request context (injected)

    Returns:
        Analysis prompt
    """
    await ctx.info(f"Generating analysis prompt for: {topic}")

    prompt = f"""Analyze the following topic: {topic}

## Analysis Framework

1. **Overview**
   Provide high-level summary

2. **Key Components**
   Break down into main parts

3. **Strengths**
   What works well?

4. **Weaknesses**
   What could be improved?

5. **Recommendations**
   Specific actionable suggestions

6. **Conclusion**
   Summary and key takeaways"""

    await ctx.info("Analysis prompt generated successfully")

    return prompt
```

---

## Common Patterns

### Pattern 1: Code Review

```python
@mcp.prompt()
def code_review(
    change_type: Literal["feature", "bugfix", "refactor"] = "feature",
    severity: Literal["critical", "important", "minor"] = "important"
) -> str:
    """
    Generate code review prompt based on change type and severity.

    Args:
        change_type: Type of code change
        severity: Review severity level

    Returns:
        Code review prompt
    """
    base = "Review the code changes:\n\n"

    if severity == "critical":
        base += "⚠️ CRITICAL REVIEW - Extra scrutiny required\n\n"

    base += "## Checklist\n"

    # Common checks
    base += """- [ ] Code is correct and works as intended
- [ ] Error handling is comprehensive
- [ ] Tests are included and passing
- [ ] Code follows style guide
"""

    # Change-type specific checks
    if change_type == "feature":
        base += """- [ ] Feature is fully implemented
- [ ] Documentation is updated
- [ ] Backward compatibility maintained
"""
    elif change_type == "bugfix":
        base += """- [ ] Root cause is addressed
- [ ] Similar issues are checked
- [ ] Regression test is added
"""
    else:  # refactor
        base += """- [ ] Behavior is unchanged
- [ ] Code is simpler/clearer
- [ ] Performance is not degraded
"""

    if severity == "critical":
        base += """
## Security Review
- [ ] No security vulnerabilities introduced
- [ ] Authentication/authorization correct
- [ ] Input validation in place
- [ ] Sensitive data handled properly"""

    return base
```

### Pattern 2: Documentation Generation

```python
@mcp.prompt()
def api_documentation(
    endpoint: str,
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
) -> str:
    """
    Generate API endpoint documentation template.

    Args:
        endpoint: API endpoint path
        method: HTTP method

    Returns:
        Documentation prompt
    """
    return f"""Generate comprehensive documentation for:

**Endpoint:** `{method} {endpoint}`

## Documentation Structure

### Overview
Brief description of what this endpoint does

### Authentication
Required authentication method and permissions

### Request

**HTTP Method:** {method}

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| | | | |

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| | | | | |

{"**Request Body:**" if method in ["POST", "PUT", "PATCH"] else ""}
{"```json" if method in ["POST", "PUT", "PATCH"] else ""}
{"{" if method in ["POST", "PUT", "PATCH"] else ""}
{"  // Example request body" if method in ["POST", "PUT", "PATCH"] else ""}
{"}" if method in ["POST", "PUT", "PATCH"] else ""}
{"```" if method in ["POST", "PUT", "PATCH"] else ""}

### Response

**Success Response (200 OK):**
```json
{{
  // Example success response
}}
```

**Error Responses:**
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid authentication
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Examples

**Example Request:**
```bash
curl -X {method} https://api.example.com{endpoint}
```

**Example Response:**
```json
{{}}
```

### Notes
Any additional notes or edge cases"""
```

### Pattern 3: Testing Strategy

```python
@mcp.prompt()
def testing_strategy(
    component: str,
    test_levels: list[str] = ["unit", "integration", "e2e"]
) -> str:
    """
    Generate comprehensive testing strategy.

    Args:
        component: Component to create testing strategy for
        test_levels: Testing levels to include

    Returns:
        Testing strategy prompt
    """
    prompt = f"Create comprehensive testing strategy for: {component}\n\n"

    if "unit" in test_levels:
        prompt += """## Unit Tests

Test individual functions/methods in isolation:
- Happy path cases
- Edge cases (empty, null, boundary values)
- Error conditions
- Mock external dependencies

"""

    if "integration" in test_levels:
        prompt += """## Integration Tests

Test component interactions:
- Database operations
- API integrations
- Service dependencies
- State management

"""

    if "e2e" in test_levels:
        prompt += """## End-to-End Tests

Test complete user workflows:
- Critical user paths
- Cross-component scenarios
- Real browser/environment
- Data persistence

"""

    prompt += """## Test Data
- Setup/teardown strategies
- Fixture management
- Test data generation

## Assertions
- What to verify
- Expected behaviors
- Error messages

## Coverage Goals
- Code coverage targets
- Critical path coverage
- Edge case coverage"""

    return prompt
```

### Pattern 4: Debugging Guide

```python
@mcp.prompt()
def debugging_guide(
    issue_type: Literal["error", "performance", "unexpected_behavior"]
) -> str:
    """
    Generate debugging guide for specific issue type.

    Args:
        issue_type: Type of issue being debugged

    Returns:
        Debugging guide prompt
    """
    guides = {
        "error": """Debug the error systematically:

## 1. Reproduce the Error
- Get exact steps to reproduce
- Note when it started happening
- Check if it's consistent

## 2. Gather Information
- Full error message and stack trace
- Environment (OS, version, etc.)
- Recent changes that might be related

## 3. Isolate the Cause
- Binary search: disable code sections
- Check inputs and data
- Verify assumptions

## 4. Form Hypothesis
- What do you think is causing it?
- How can you test this hypothesis?

## 5. Fix and Verify
- Implement fix
- Test thoroughly
- Add test to prevent regression""",

        "performance": """Analyze and improve performance:

## 1. Measure Current Performance
- Baseline metrics
- Identify slow operations
- Profile the code

## 2. Find Bottlenecks
- CPU usage
- Memory usage
- I/O operations
- Network calls
- Database queries

## 3. Analyze Root Cause
- Inefficient algorithms (O(n²) vs O(n log n))
- Unnecessary operations
- Missing caching
- N+1 queries

## 4. Optimize
- Improve algorithms
- Add caching
- Optimize queries
- Parallelize operations

## 5. Measure Again
- Compare before/after
- Verify no regression
- Document improvements""",

        "unexpected_behavior": """Investigate unexpected behavior:

## 1. Define Expected vs Actual
- What should happen?
- What actually happens?
- What's the difference?

## 2. Review Assumptions
- Are your assumptions correct?
- Check documentation
- Verify dependencies

## 3. Trace Execution
- Add logging
- Use debugger
- Check state at each step

## 4. Check Edge Cases
- Null/empty values
- Boundary conditions
- Timing issues

## 5. Verify Fix
- Test expected behavior
- Test edge cases
- Update tests"""
    }

    return guides[issue_type]
```

### Pattern 5: Architecture Review

```python
@mcp.prompt()
def architecture_review(scale: Literal["small", "medium", "large"] = "medium") -> str:
    """
    Generate architecture review template based on system scale.

    Args:
        scale: System scale (affects depth of review)

    Returns:
        Architecture review prompt
    """
    base = """# Architecture Review

## System Overview
Describe the system and its purpose

## Components
List and describe major components

"""

    base += """## Data Flow
How does data move through the system?

## API Design
- Endpoints
- Data contracts
- Versioning strategy

## Data Storage
- Database choice and why
- Schema design
- Caching strategy

"""

    if scale in ["medium", "large"]:
        base += """## Scalability
- Current capacity
- Scaling strategy (horizontal/vertical)
- Bottlenecks
- Load balancing

## Reliability
- Error handling
- Retry logic
- Circuit breakers
- Graceful degradation

"""

    if scale == "large":
        base += """## Observability
- Logging strategy
- Metrics collection
- Distributed tracing
- Alerting

## Disaster Recovery
- Backup strategy
- Recovery procedures
- RTO/RPO targets

## Cost Optimization
- Resource utilization
- Cost-effective alternatives
- Waste reduction

"""

    base += """## Security
- Authentication/authorization
- Data encryption
- Security best practices

## Recommendations
Key improvements and priorities"""

    return base
```

### Pattern 6: Migration Plan

```python
@mcp.prompt()
def migration_plan(
    from_tech: str,
    to_tech: str,
    has_users: bool = True
) -> str:
    """
    Generate migration plan from one technology to another.

    Args:
        from_tech: Current technology
        to_tech: Target technology
        has_users: Whether there are active users

    Returns:
        Migration plan prompt
    """
    prompt = f"""Create migration plan: {from_tech} → {to_tech}

## 1. Assessment
- Current system analysis
- Migration complexity
- Risks and challenges
- Resource requirements

## 2. Strategy
- Big bang vs incremental
- Parallel run period
- Rollback plan

## 3. Preparation
- Code/data compatibility analysis
- Dependency mapping
- Test environment setup

## 4. Migration Steps
1. Preparation phase
2. Initial migration
3. Validation
4. Cutover
5. Cleanup

"""

    if has_users:
        prompt += """## 5. User Communication
- Migration timeline
- Expected downtime
- User actions required
- Support plan

## 6. Rollout
- Pilot users
- Gradual rollout
- Monitoring
- Feedback collection

"""

    prompt += """## 7. Post-Migration
- Verify functionality
- Monitor performance
- Collect metrics
- Document lessons learned

## 8. Rollback Plan
When and how to rollback if needed

## Timeline
Estimated timeline for each phase

## Success Criteria
How to measure migration success"""

    return prompt
```

---

## Troubleshooting

### Issue 1: Prompt Not Found

**Problem:** Prompt doesn't appear in available prompts list.

**Solutions:**
```python
# ✗ Wrong - Forgot decorator
def my_prompt() -> str:  # Not decorated
    return "Prompt text"

# ✓ Correct - Use decorator
@mcp.prompt()
def my_prompt() -> str:
    return "Prompt text"
```

### Issue 2: Arguments Not Working

**Problem:** Prompt function has parameters but they're not being passed correctly.

**Solutions:**
```python
# ✗ Wrong - Missing type hints
@mcp.prompt()
def review(language, focus):  # No type hints
    return f"Review {language} code focusing on {focus}"

# ✓ Correct - Add type hints for proper schema generation
@mcp.prompt()
def review(language: str, focus: str = "general") -> str:
    return f"Review {language} code focusing on {focus}"
```

### Issue 3: Multiline Formatting Issues

**Problem:** Prompt formatting is broken or has extra whitespace.

**Solutions:**
```python
# ✗ Wrong - Inconsistent indentation
@mcp.prompt()
def bad_format() -> str:
    return """This is a prompt
    with bad indentation
        that looks messy"""

# ✓ Correct - Use consistent formatting
@mcp.prompt()
def good_format() -> str:
    return """This is a prompt
with proper formatting
that looks clean"""

# ✓ Better - Use textwrap.dedent for complex prompts
from textwrap import dedent

@mcp.prompt()
def best_format() -> str:
    return dedent("""
        This is a prompt
        with consistent indentation
        using dedent
    """).strip()
```

### Issue 4: Dynamic Content Not Updating

**Problem:** Prompt content doesn't change when it should.

**Solutions:**
```python
# ✗ Wrong - Static content evaluated at decoration time
TIMESTAMP = datetime.now().isoformat()

@mcp.prompt()
def timestamped() -> str:
    return f"Generated at: {TIMESTAMP}"  # Always same timestamp

# ✓ Correct - Generate dynamically on each call
@mcp.prompt()
def timestamped() -> str:
    timestamp = datetime.now().isoformat()
    return f"Generated at: {timestamp}"  # Fresh timestamp each call
```

### Issue 5: Type Constraints Not Enforced

**Problem:** Invalid argument values are accepted.

**Solutions:**
```python
# ✗ Wrong - String type accepts any value
@mcp.prompt()
def review(severity: str) -> str:  # Any string accepted
    if severity == "high":
        return "High severity review"
    return "Normal review"

# ✓ Correct - Use Literal to constrain values
from typing import Literal

@mcp.prompt()
def review(severity: Literal["low", "medium", "high"]) -> str:
    if severity == "high":
        return "High severity review"
    return "Normal review"
```

### Issue 6: Context Injection Not Working

**Problem:** Context parameter is None or missing.

**Solutions:**
```python
from fastmcp import Context

# ✗ Wrong - Missing type hint
@mcp.prompt()
async def my_prompt(context) -> str:  # Won't be injected
    await context.info("test")  # AttributeError
    return "Prompt"

# ✓ Correct - Proper type hint
@mcp.prompt()
async def my_prompt(ctx: Context) -> str:
    await ctx.info("Generating prompt")
    return "Prompt"
```

---

## Summary

Prompts in FastMCP enable you to create reusable, parameterized templates that guide agents through complex tasks. Key takeaways:

1. **Use descriptive names** that clearly indicate the prompt's purpose
2. **Parameterize prompts** for flexibility and reuse
3. **Use type hints** for proper schema generation and validation
4. **Use Literal types** to constrain argument values
5. **Format carefully** with consistent indentation
6. **Document thoroughly** with clear descriptions
7. **Generate dynamically** when content should change
8. **Use context injection** for logging and progress
9. **Provide structured guidance** that helps agents succeed
10. **Test prompts** with actual agent workflows

Prompts are powerful tools for encoding best practices and workflows into your MCP server, helping agents consistently deliver high-quality results.
