# Context Management Guide

## Overview

Effective context management is critical for building agents that can handle complex, long-running tasks without exhausting context limits. The Claude Agent SDK provides several strategies for managing context efficiently: agentic search, semantic search, subagents, and automatic compaction.

## Understanding Context Limits

### Token Budgets

Different Claude models have different context windows:
- Claude Sonnet 4.5: 200K tokens
- Claude Sonnet 3.5: 200K tokens
- Claude Opus: 200K tokens

**Important considerations:**
- Input + output combined count toward limit
- Tool responses consume context
- System prompt and conversation history accumulate
- Context exhaustion leads to compaction or failure

### Context Allocation Strategy

Typical context allocation for a production agent:

```
System Prompt:         ~2K tokens   (1%)
Tool Descriptions:     ~5K tokens   (2.5%)
Conversation History:  ~50K tokens  (25%)
Tool Results:          ~100K tokens (50%)
Working Space:         ~43K tokens  (21.5%)
```

**Recommendation:** Design agents to stay within 150K tokens for safety, leaving 50K tokens as buffer for compaction and unexpected expansions.

## Agentic Search

### What is Agentic Search?

Agentic search means the agent uses bash commands (grep, tail, find, cat, etc.) to selectively load information from the file system. The agent actively searches for what it needs rather than having everything loaded upfront.

### How It Works

```python
# Agent receives this task
"Analyze the authentication system for security issues"

# Agent's internal process:
# 1. Search for authentication-related files
$ find . -name "*auth*" -type f

# 2. Search for specific patterns
$ grep -r "password" --include="*.py" .

# 3. Read specific files
$ cat ./src/auth/login.py

# 4. Search within files
$ grep -n "authenticate" ./src/auth/login.py
```

### Advantages

**Accuracy**: Agent finds exactly what it needs based on current task
**Transparency**: All search operations are visible in the transcript
**Adaptability**: Search strategy adjusts based on what's discovered
**No maintenance**: No indexing or embeddings to maintain

### Disadvantages

**Speed**: Multiple tool calls required to find information
**Token cost**: Each tool call consumes input/output tokens
**Learning curve**: Agent must learn effective search strategies

### When to Use

**Use agentic search when:**
- Accuracy is more important than speed
- File structure is well-organized and predictable
- Agent tasks are exploratory or investigative
- You want full transparency into information gathering

**Example use cases:**
- Code review and security auditing
- Bug investigation and root cause analysis
- Documentation generation
- Compliance checking

### Optimization Techniques

**1. Folder Structure as Documentation**

Organize files to make searching intuitive:

```
project/
├── src/
│   ├── auth/           # Authentication related code
│   ├── api/            # API endpoints
│   ├── db/             # Database models and queries
│   └── utils/          # Utility functions
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
└── docs/
    ├── api/            # API documentation
    └── architecture/   # Architecture docs
```

**2. Naming Conventions**

Use consistent, descriptive names:

```python
# Good: Clear, searchable names
user_authentication_service.py
password_reset_handler.py
jwt_token_validator.py

# Bad: Ambiguous names
service.py
handler.py
utils.py
```

**3. Strategic File Comments**

Add searchable markers in code:

```python
# SECURITY: Password hashing implementation
def hash_password(password: str) -> str:
    ...

# API: User registration endpoint
@router.post("/register")
def register_user():
    ...

# DATABASE: User model definition
class User(BaseModel):
    ...
```

## Semantic Search

### What is Semantic Search?

Semantic search uses vector embeddings to find conceptually similar content, even if exact keywords don't match. Content is indexed upfront, enabling fast similarity-based retrieval.

### How It Works

```python
# Upfront indexing (done once)
1. Chunk all documents into segments
2. Generate embeddings for each chunk
3. Store in vector database (Pinecone, Weaviate, ChromaDB)

# Query time (fast)
1. Generate embedding for search query
2. Find similar embeddings in vector DB
3. Return matching content
```

### Advantages

**Speed**: Single query returns relevant results instantly
**Conceptual matching**: Finds related content without exact keywords
**Scalability**: Handles large codebases efficiently

### Disadvantages

**Maintenance overhead**: Must re-index when content changes
**Less transparency**: Why specific results were returned is opaque
**Accuracy trade-offs**: May return false positives or miss exact matches
**Infrastructure**: Requires vector database setup

### When to Use

**Use semantic search when:**
- Speed is critical (customer-facing applications)
- Codebase is very large (100K+ files)
- Search queries are conceptual rather than specific
- Resources available for index maintenance

**Example use cases:**
- Customer support chatbots (fast response needed)
- Code suggestions as-you-type
- Large-scale documentation search
- Conceptual code exploration

### Implementation Example

```python
from claude_agent_sdk import ClaudeSDKClient, tool
import chromadb

# Initialize vector database
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("codebase")

# Index codebase (run once or on updates)
def index_codebase(directory):
    for file in find_all_files(directory):
        content = read_file(file)
        chunks = chunk_content(content)
        for chunk in chunks:
            collection.add(
                documents=[chunk],
                metadatas=[{"file": file, "line": chunk.start_line}],
                ids=[f"{file}:{chunk.start_line}"]
            )

# Create semantic search tool
@tool(
    "semantic_search",
    "Search codebase using semantic similarity",
    {"query": str, "limit": int}
)
async def semantic_search(args):
    results = collection.query(
        query_texts=[args["query"]],
        n_results=args.get("limit", 10)
    )

    formatted_results = []
    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
        formatted_results.append({
            "file": metadata["file"],
            "line": metadata["line"],
            "content": doc
        })

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(formatted_results, indent=2)
        }]
    }

# Use in agent
client = ClaudeSDKClient(
    system_prompt="You are a code explorer. Use semantic_search to find relevant code.",
    tools=[semantic_search]
)
```

### Hybrid Approach

Combine both strategies for optimal results:

```python
@tool(
    "search_codebase",
    "Search codebase with multiple strategies",
    {
        "query": str,
        "strategy": Literal["semantic", "keyword", "hybrid"]
    }
)
async def search_codebase(args):
    query = args["query"]
    strategy = args.get("strategy", "hybrid")

    if strategy == "semantic":
        return semantic_search_only(query)

    elif strategy == "keyword":
        return keyword_search_only(query)

    else:  # hybrid
        # Get results from both methods
        semantic_results = semantic_search_only(query)
        keyword_results = keyword_search_only(query)

        # Merge and rank results
        merged = merge_results(semantic_results, keyword_results)

        return {
            "content": [{
                "type": "text",
                "text": json.dumps(merged, indent=2)
            }]
        }
```

## Subagents

### What are Subagents?

Subagents are separate agent instances that handle specific sub-tasks independently. They run in isolated contexts and return only relevant results to the parent agent.

### Why Use Subagents?

**Context Isolation**: Each subagent has its own context window
**Parallelization**: Multiple subagents can work simultaneously
**Specialization**: Each subagent focuses on a specific domain
**Result Filtering**: Only essential information returned to parent

### Architecture

```
┌─────────────────────────────────────┐
│   Parent Agent (Orchestrator)      │
│   Context: 50K tokens               │
└──────────┬──────────────────────────┘
           │
     ┌─────┴────────────────┐
     │                      │
┌────▼─────┐          ┌────▼─────┐
│ Subagent │          │ Subagent │
│    A     │          │    B     │
│ Context: │          │ Context: │
│ 200K     │          │ 200K     │
└──────────┘          └──────────┘
```

### Implementation

**1. Define Subagent as Markdown File**

Create `.claude/subagents/security_checker.md`:

```markdown
You are a security auditor specializing in code review.

Task: Analyze the given file for security vulnerabilities.

Focus on:
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization issues
- Hardcoded secrets
- Unsafe deserialization

Return ONLY:
1. File path
2. Number of issues found (integer)
3. Severity: "critical", "high", "medium", or "low"
4. Top 3 issues (brief descriptions)

Do NOT include:
- Full code listings
- Detailed explanations
- Line-by-line analysis
- Remediation steps

Format response as JSON.
```

**2. Invoke Subagent from Parent Agent**

```python
# Parent agent system prompt includes:
"""
You have access to specialized subagents for different tasks:
- security_checker: Analyzes files for security issues
- performance_analyzer: Identifies performance bottlenecks
- test_generator: Creates unit tests for code

To use a subagent, use the Bash tool to invoke it:
$ claude subagent security_checker --file path/to/file.py
"""
```

**3. Parent Agent Workflow**

```
1. Parent receives task: "Audit the codebase for security issues"

2. Parent identifies files to audit:
   $ find . -name "*.py" | grep -E "(auth|login|session)"

3. Parent invokes subagents in parallel:
   $ claude subagent security_checker --file src/auth/login.py &
   $ claude subagent security_checker --file src/auth/session.py &
   $ claude subagent security_checker --file src/api/auth.py &

4. Collect results (each ~1K tokens vs 50K+ if done directly)

5. Synthesize final report
```

### Best Practices

**1. Keep Subagent Responses Concise**

```markdown
<!-- Bad: Verbose subagent -->
Return a detailed analysis including:
- Full vulnerability description
- Affected code snippets
- OWASP category
- CVE references
- Detailed remediation steps
- Testing recommendations
```

```markdown
<!-- Good: Concise subagent -->
Return ONLY:
1. Vulnerability count (number)
2. Highest severity found
3. Top 3 issues (title only)

Format: JSON, max 500 tokens
```

**2. Design for Parallel Execution**

```python
# Bad: Sequential subagent calls
for file in files:
    result = invoke_subagent(file)
    results.append(result)

# Good: Parallel subagent calls
tasks = [invoke_subagent(file) for file in files]
results = await asyncio.gather(*tasks)
```

**3. Filter Information Early**

Subagents should filter and summarize before returning results:

```python
# In subagent prompt:
"""
After analysis, filter results:
- Only include issues with severity >= MEDIUM
- Limit to top 10 most critical issues
- Exclude false positives based on context
- Return summary statistics, not full details
"""
```

## Automatic Compaction

### What is Compaction?

Compaction is the automatic summarization of conversation history when context approaches limits. The Claude Agent SDK handles this automatically.

### How It Works

```
1. Agent context reaches ~80% of limit (e.g., 160K/200K tokens)

2. SDK triggers compaction:
   - Identifies messages eligible for summarization
   - Sends to Claude with summarization prompt
   - Replaces original messages with summaries

3. Context reduced to ~50% (e.g., 100K tokens)

4. Agent continues with more headroom
```

### What Gets Compacted

**Compacted:**
- Tool results from earlier in conversation
- Agent reasoning and intermediate steps
- Verbose outputs and data dumps

**Not compacted:**
- System prompt
- Recent messages (last N turns)
- Current task context
- Explicitly pinned information

### Designing for Compaction

**1. Write Summari

zable Content**

```python
# Bad: Context-dependent references
"As mentioned above, the issue is..."
"Looking at the previous results, we can see..."
"Based on what we found earlier..."

# Good: Self-contained information
"The authentication module has 3 SQL injection vulnerabilities..."
"Performance analysis of api.py shows 200ms average latency..."
"Security scan identified: hardcoded API key in config.py:42"
```

**2. Structure Information Hierarchically**

```python
# Summary-friendly format
{
    "summary": "Found 5 critical issues in authentication module",
    "details": {
        "sql_injection": 2,
        "xss": 1,
        "hardcoded_secrets": 2
    },
    "files_affected": ["auth/login.py", "auth/session.py"],
    "next_steps": ["Fix critical issues", "Run security scan again"]
}
```

**3. Use Persistent Storage for Long-Term Memory**

Don't rely on conversation context for important information:

```python
# Store important findings externally
@tool("save_finding", "Save important finding to persistent storage")
async def save_finding(args):
    finding = args["finding"]
    severity = args["severity"]

    # Save to file or database
    with open("findings.json", "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "finding": finding
        }) + "\n")

    return {"content": [{"type": "text", "text": "Finding saved"}]}

# Later, reload findings
@tool("load_findings", "Load saved findings")
async def load_findings(args):
    with open("findings.json", "r") as f:
        findings = [json.loads(line) for line in f]

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(findings, indent=2)
        }]
    }
```

## Practical Context Management Strategies

### Strategy 1: Incremental Information Loading

Load information progressively based on agent's needs:

```python
# System prompt guidance:
"""
When exploring a codebase:
1. Start with high-level overview (directory structure)
2. Identify relevant modules
3. Read specific files only when needed
4. Search within files for specific patterns

Do NOT:
- Read all files upfront
- Load full file contents when grep suffices
- Keep verbose outputs in context
"""
```

### Strategy 2: Stateful Checkpoints

Save progress at key checkpoints:

```python
@tool("save_checkpoint", "Save current progress")
async def save_checkpoint(args):
    state = args["state"]

    with open(".agent_state.json", "w") as f:
        json.dump(state, f)

    return {"content": [{"type": "text", "text": "Checkpoint saved"}]}

@tool("load_checkpoint", "Load previous progress")
async def load_checkpoint(args):
    with open(".agent_state.json", "r") as f:
        state = json.load(f)

    return {
        "content": [{
            "type": "text",
            "text": f"Loaded checkpoint: {json.dumps(state, indent=2)}"
        }]
    }

# Agent can resume from checkpoint after compaction
```

### Strategy 3: Streaming Summaries

Continuously summarize progress:

```python
# System prompt:
"""
After analyzing each file, append a one-line summary to summary.txt:
- filename: key finding (severity)

This creates a persistent, concise record that survives compaction.
"""

# Agent actions:
$ echo "auth/login.py: SQL injection in line 45 (CRITICAL)" >> summary.txt
$ echo "auth/session.py: No issues found (OK)" >> summary.txt
$ echo "api/auth.py: Missing rate limiting (MEDIUM)" >> summary.txt

# Later, review summary:
$ cat summary.txt
```

### Strategy 4: Two-Pass Processing

First pass: Gather information concisely
Second pass: Deep analysis of high-priority items

```python
# Pass 1: Quick scan
"""
Scan all files and list:
- Filename
- Primary purpose
- Priority (high/medium/low) for detailed analysis

Do NOT perform detailed analysis in this pass.
"""

# Pass 2: Detailed analysis
"""
From the prioritized list, analyze HIGH priority files in detail.
For each file:
1. Perform deep analysis
2. Document findings
3. Save to findings.json
4. Move to next file

This approach prevents context exhaustion from detailed analysis of low-priority items.
"""
```

## Monitoring Context Usage

### Built-in Monitoring

The SDK provides context usage information:

```python
from claude_agent_sdk import ClaudeSDKClient

client = ClaudeSDKClient()

# Context information available in response
response = await client.send_message("Analyze this codebase")

# Check context usage
if hasattr(response, 'usage'):
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    print(f"Total: {response.usage.input_tokens + response.usage.output_tokens}")
```

### Custom Context Tracking

```python
# Track context usage over time
context_log = []

@tool("track_context", "Log current context usage")
async def track_context(args):
    usage = args["current_usage"]  # From SDK

    context_log.append({
        "timestamp": datetime.now().isoformat(),
        "input_tokens": usage["input"],
        "output_tokens": usage["output"],
        "total": usage["input"] + usage["output"],
        "percentage": (usage["input"] + usage["output"]) / 200000 * 100
    })

    # Alert if approaching limit
    if context_log[-1]["percentage"] > 75:
        return {
            "content": [{
                "type": "text",
                "text": "⚠️ Warning: Context usage at 75%. Consider saving progress and compacting."
            }]
        }

    return {"content": [{"type": "text", "text": "Context tracked"}]}
```

## Performance Optimization Tips

1. **Use grep instead of reading full files**: `grep "pattern" file.py` vs `cat file.py`
2. **Limit output length**: `head -n 20` instead of full file
3. **Filter results early**: Return summaries, not raw data
4. **Cache expensive operations**: Avoid re-fetching same data
5. **Parallel subagents**: Process multiple items simultaneously
6. **Incremental loading**: Load details only when needed
7. **Persistent storage**: Save findings outside conversation context
8. **Regular checkpoints**: Save progress at milestones
9. **Concise tool responses**: Default to summaries, detailed on request
10. **Strategic compaction**: Design content to be summarization-friendly
