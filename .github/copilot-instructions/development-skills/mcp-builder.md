# MCP Server Builder

## Overview

Guide for creating high-quality MCP (Model Context Protocol) servers that enable AI agents to interact with external services through well-designed tools. Use these instructions when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

## When to Use

- Building MCP servers to integrate external APIs
- Creating tools for AI agents to access services
- Developing custom integrations for Copilot Extensions
- Designing agent-friendly API wrappers
- Implementing workflow-based tool systems

## Core Philosophy

An MCP server's quality is measured by how well it enables AI agents to accomplish real-world tasks. Focus on:

- **Workflow-oriented tools** - Not just API endpoint wrappers
- **Context efficiency** - High-signal information only
- **Actionable errors** - Guide agents toward correct usage
- **Natural task subdivisions** - Tools that match mental models
- **Evaluation-driven development** - Test with realistic scenarios

## Workflows

### High-Level Development Process

#### Phase 1: Deep Research and Planning

**1. Study Agent-Centric Design Principles**

**Build for Workflows, Not Just API Endpoints:**
- Consolidate related operations (e.g., `schedule_event` that checks availability AND creates event)
- Focus on tools that enable complete tasks
- Consider what workflows agents actually need

**Optimize for Limited Context:**
- Return high-signal information, not data dumps
- Provide "concise" vs "detailed" options
- Default to human-readable identifiers (names over IDs)
- Respect character limits (~25,000 tokens)

**Design Actionable Error Messages:**
- Suggest specific next steps: "Try using filter='active_only'"
- Make errors educational, not just diagnostic
- Guide agents toward correct usage patterns

**2. Study MCP Protocol Documentation**

Using @workspace or browser:
- Fetch: `https://modelcontextprotocol.io/llms-full.txt`
- Read comprehensive MCP specification
- Understand protocol requirements

**3. Study Framework Documentation**

Load reference files from workspace:
- **Best Practices**: `mcp-builder/reference/mcp_best_practices.md`
- **Python Guide**: `mcp-builder/reference/python_mcp_server.md` (for Python)
- **TypeScript Guide**: `mcp-builder/reference/node_mcp_server.md` (for Node/TypeScript)
- **Python SDK**: Fetch `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- **TypeScript SDK**: Fetch `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

**4. Exhaustively Study API Documentation**

Research target service:
- Official API reference
- Authentication requirements
- Rate limiting and pagination
- Error responses
- Data models and schemas

Use web search and fetch tools as needed.

**5. Create Implementation Plan**

Document:

**Tool Selection:**
- Most valuable endpoints/operations
- Prioritized by common use cases
- Tools that enable complete workflows

**Shared Utilities:**
- API request patterns
- Pagination helpers
- Filtering and formatting
- Error handling strategies

**Input/Output Design:**
- Input validation (Pydantic/Zod)
- Response formats (JSON and Markdown)
- Configurable detail levels
- Character limits and truncation

**Error Handling:**
- Graceful failure modes
- Clear, actionable error messages
- Rate limiting scenarios
- Auth/authorization errors

#### Phase 2: Implementation

**1. Set Up Project Structure**

**For Python:**
```bash
# Create main server file
touch mcp_server_name.py

# Or for complex servers
mkdir mcp_server_name
touch mcp_server_name/__init__.py
touch mcp_server_name/server.py
```

**For Node/TypeScript:**
```bash
# Initialize project
npm init -y
npm install @modelcontextprotocol/sdk zod

# Create structure
mkdir src
touch src/index.ts
touch tsconfig.json
```

**2. Implement Core Infrastructure First**

Create shared utilities before tools:
- API request helpers
- Error handling utilities
- Response formatting (JSON and Markdown)
- Pagination helpers
- Authentication/token management

**3. Implement Tools Systematically**

For each tool:

**Define Input Schema:**
```python
# Python with Pydantic
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query string")
    limit: int = Field(10, ge=1, le=100, description="Max results (1-100)")
```

```typescript
// TypeScript with Zod
import { z } from 'zod';

const SearchInputSchema = z.object({
  query: z.string().describe("Search query string"),
  limit: z.number().min(1).max(100).default(10).describe("Max results (1-100)")
}).strict();
```

**Write Comprehensive Docstrings:**
```python
@mcp.tool()
async def search_items(query: str, limit: int = 10) -> str:
    """
    Search for items in the system.
    
    This tool searches across all items using full-text search.
    Returns results in markdown format with key details.
    
    Args:
        query: Search terms (supports AND, OR, NOT operators)
        limit: Maximum results to return (1-100, default 10)
    
    Returns:
        Markdown-formatted list of matching items with:
        - Item name and ID
        - Brief description
        - Last modified date
        
    Examples:
        - "project AND status:active" - Find active projects
        - "bug priority:high" - Find high-priority bugs
        
    Errors:
        - Returns error message if query syntax is invalid
        - Suggests corrected query format when possible
    """
```

**Implement Tool Logic:**
- Use shared utilities
- Follow async/await patterns
- Proper error handling
- Support multiple formats
- Respect pagination
- Check character limits

**Add Tool Annotations:**
```python
@mcp.tool(
    readOnlyHint=True,        # For read operations
    destructiveHint=False,    # For non-destructive operations
    idempotentHint=True,      # If repeated calls have same effect
    openWorldHint=True        # If interacting with external systems
)
```

**4. Follow Language-Specific Best Practices**

**Python:**
- Use MCP Python SDK properly
- Pydantic v2 models
- Type hints throughout
- Async/await for all I/O
- Module-level constants

**TypeScript:**
- Use `server.registerTool` properly
- Zod schemas with `.strict()`
- TypeScript strict mode
- No `any` types
- Explicit Promise<T> returns
- Build process configured

#### Phase 3: Review and Refine

**1. Code Quality Review**

Check for:
- **DRY Principle**: No duplicated code
- **Composability**: Shared logic extracted
- **Consistency**: Similar operations return similar formats
- **Error Handling**: All external calls covered
- **Type Safety**: Full type coverage
- **Documentation**: Comprehensive docstrings

**2. Test and Build**

**Important**: MCP servers are long-running processes. Running them directly will hang.

**Safe testing approaches:**
- Use evaluation harness (recommended)
- Run in tmux/screen
- Use timeout: `timeout 5s python server.py`

**For Python:**
```bash
# Verify syntax
python -m py_compile mcp_server_name.py

# Check imports (review file)
```

**For Node/TypeScript:**
```bash
# Build
npm run build

# Verify dist/index.js created
ls dist/index.js
```

**3. Quality Checklist**

Load appropriate checklist from references:
- Python: `mcp-builder/reference/python_mcp_server.md`
- TypeScript: `mcp-builder/reference/node_mcp_server.md`

#### Phase 4: Create Evaluations

**1. Understand Evaluation Purpose**

Test whether AI agents can effectively use your server to answer realistic questions.

**2. Create 10 Evaluation Questions**

Load: `mcp-builder/reference/evaluation.md`

Follow process:
1. **Tool Inspection**: List available tools
2. **Content Exploration**: Use READ-ONLY operations
3. **Question Generation**: Create 10 complex questions
4. **Answer Verification**: Solve each yourself

**3. Evaluation Requirements**

Each question must be:
- **Independent**: Not dependent on others
- **Read-only**: Non-destructive operations only
- **Complex**: Multiple tool calls required
- **Realistic**: Real use cases
- **Verifiable**: Single clear answer
- **Stable**: Answer won't change over time

**4. Output Format**

Create XML evaluation file:
```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
  <!-- More qa_pairs... -->
</evaluation>
```

## Examples

### Example: GitHub MCP Server

**Workflow Tools:**
- `create_issue_with_labels` - Creates issue AND applies labels (not separate operations)
- `search_code_and_explain` - Searches code AND provides context (consolidated workflow)

**Context Efficiency:**
- Returns issue summary, not full body (configurable with `detail` parameter)
- Lists changed files, not full diffs
- Provides recent activity, not entire history

**Actionable Errors:**
```
Error: Repository not found
Suggestion: Check repository name format. Use 'owner/repo' (e.g., 'octocat/hello-world')
Available repos: [list of user's repos]
```

### Example: Calendar MCP Server

**Workflow Tools:**
- `schedule_meeting` - Checks availability, finds time, creates event
- `reschedule_event` - Finds conflicted events, suggests alternatives, updates

**Natural Subdivisions:**
- `find_free_time` - Natural planning task
- `get_daily_agenda` - Natural information request
- `create_event` - Natural action

## Resources

### Workspace References

**Core Documentation:**
- `mcp-builder/SKILL.md` - Complete original skill documentation
- `mcp-builder/reference/mcp_best_practices.md` - Universal MCP guidelines
- `mcp-builder/reference/evaluation.md` - Evaluation creation guide

**Language-Specific Guides:**
- `mcp-builder/reference/python_mcp_server.md` - Complete Python/FastMCP guide
- `mcp-builder/reference/node_mcp_server.md` - Complete TypeScript guide

**Scripts:**
- `mcp-builder/scripts/` - Evaluation and validation tools (if available)

### External Documentation

**Official MCP Resources:**
- Protocol spec: `https://modelcontextprotocol.io/llms-full.txt`
- Python SDK: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- TypeScript SDK: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

## Guidelines

### Design Principles

1. **Agent-Centric Design**
   - Build for workflows, not API endpoints
   - Optimize for context efficiency
   - Design actionable errors
   - Follow natural task subdivisions

2. **Research-Driven Development**
   - Exhaustively study API documentation
   - Understand agent needs
   - Plan before implementing
   - Validate with evaluations

3. **Quality Standards**
   - No duplicated code
   - Full type coverage
   - Comprehensive documentation
   - Proper error handling

4. **Evaluation-Driven**
   - Test with realistic scenarios
   - Create complex questions
   - Verify answers manually
   - Iterate based on results

### Common Patterns

**Pagination Helper:**
```python
async def paginate_results(api_call, **kwargs):
    """Generic pagination for API calls"""
    all_results = []
    page = 1
    while True:
        results = await api_call(page=page, **kwargs)
        if not results:
            break
        all_results.extend(results)
        if len(results) < PAGE_SIZE:
            break
        page += 1
    return all_results
```

**Response Formatting:**
```python
def format_response(data, format="concise"):
    """Format response based on detail level"""
    if format == "concise":
        return format_concise(data)
    elif format == "detailed":
        return format_detailed(data)
    else:
        return format_json(data)
```

**Error Handling:**
```python
try:
    result = await api_call()
except AuthError:
    return "Authentication failed. Please check API token."
except RateLimitError as e:
    return f"Rate limit exceeded. Retry after {e.retry_after} seconds."
except NotFoundError:
    return "Resource not found. Check the ID and try again."
```

## Troubleshooting

### Server Won't Start

**Problem**: Process hangs when running server
**Solution**: MCP servers are long-running. Use tmux or evaluation harness instead of direct execution.

### Tools Not Working

**Problem**: Agent can't use tools effectively
**Solution**: Check docstrings - they should explain WHAT the tool does, WHEN to use it, and HOW to use it correctly.

### Context Overload

**Problem**: Responses too large, context fills up
**Solution**: Implement character limits, provide concise/detailed modes, return summaries not full content.

### Poor Evaluation Results

**Problem**: Agent fails evaluation questions
**Solution**: Review tool design - likely missing workflow-oriented tools or unclear documentation.

## Next Steps

After creating an MCP server:

1. **Test with Real Scenarios** - Use in actual workflows
2. **Gather Feedback** - Note where agents struggle
3. **Iterate and Improve** - Update based on usage
4. **Expand Evaluations** - Add more test cases
5. **Share Patterns** - Document successful approaches

## Additional Context

This instruction set is adapted from the comprehensive MCP Builder skill. For complete details, examples, and advanced patterns, refer to:
- `mcp-builder/SKILL.md` - Full skill documentation
- `mcp-builder/reference/` - Detailed guides and examples

Use @workspace to query these resources for specific details.
