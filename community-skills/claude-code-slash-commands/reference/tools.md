# Tools Reference

Complete guide to all tools available in Claude Code commands.

## Overview

Tools are Claude Code's capabilities for interacting with files, executing commands, and accessing external systems. Control tool access via the `allowed-tools` frontmatter field.

## Core File Tools

### Read

Read file contents into the command context.

**Syntax**: `allowed-tools: Read`

**Capabilities**:
- Read any text file
- Parse structured data (JSON, YAML, TOML)
- View configuration files
- Access source code

**Usage in Commands**:
```markdown
---
allowed-tools: Read
---

Analyze the configuration: @config/app.json
Review the implementation: @src/main.ts
```

**Best For**:
- Code analysis
- Configuration review
- Documentation reading
- Data file inspection

**Limitations**:
- Binary files may not display correctly
- Very large files (>1MB) may be truncated
- Requires file path relative to working directory

---

### Write

Create new files in the project.

**Syntax**: `allowed-tools: Write`

**Capabilities**:
- Create new files with content
- Create files in new directories (creates parents)
- Write multiple files in one operation
- Generate boilerplate code

**Usage in Commands**:
```markdown
---
allowed-tools: Read, Write
---

Generate new React component in src/components/:
- Create ComponentName.tsx
- Create ComponentName.test.tsx
- Create ComponentName.module.css
- Create index.ts barrel export
```

**Best For**:
- Scaffolding new code
- Generating test files
- Creating configuration files
- Setting up project structure

**Limitations**:
- Cannot overwrite existing files (use Edit instead)
- File permissions depend on system settings
- Large binary files should be generated externally

---

### Edit

Modify existing files.

**Syntax**: `allowed-tools: Edit`

**Capabilities**:
- Update file contents
- Insert, replace, or delete lines
- Refactor code across multiple files
- Apply formatting changes

**Usage in Commands**:
```markdown
---
allowed-tools: Read, Edit
---

Refactor @src/utils/helpers.ts:
1. Extract duplicated logic into separate functions
2. Update import statements
3. Add TypeScript types
4. Improve error handling
```

**Best For**:
- Refactoring code
- Fixing bugs
- Updating configurations
- Applying code reviews

**Limitations**:
- Requires file to exist (use Write for new files)
- Large changes may need multiple operations
- Cannot rename files (delete + write instead)

---

### Grep

Search file contents for patterns.

**Syntax**: `allowed-tools: Grep`

**Capabilities**:
- Search files with regex patterns
- Find text across multiple files
- Case-sensitive or insensitive search
- Include context lines around matches

**Usage in Commands**:
```markdown
---
allowed-tools: Read, Grep
---

Find all TODO comments:
- Search for: TODO:|FIXME:|HACK:
- Include 2 lines of context
- Exclude test files and node_modules

Generate report of technical debt items.
```

**Best For**:
- Finding TODOs and FIXMEs
- Locating specific code patterns
- Dependency analysis
- Security audits (finding secrets)

**Limitations**:
- Not designed for binary files
- Performance depends on project size
- Complex regex may be slow

---

### Glob

Find files matching patterns.

**Syntax**: `allowed-tools: Glob`

**Capabilities**:
- Find files by name patterns
- Recursive directory searching
- Exclude patterns (gitignore-style)
- List files for processing

**Usage in Commands**:
```markdown
---
allowed-tools: Read, Glob
---

Find all test files:
- Pattern: **/*.test.ts, **/*.spec.ts
- Exclude: node_modules/**, dist/**

Analyze test coverage across project.
```

**Best For**:
- Finding files by extension
- Bulk operations on similar files
- Project structure analysis
- Inventory of code files

**Limitations**:
- Pattern syntax may differ from shell
- Very large projects may be slow
- Hidden files (.) may need special handling

---

## Bash Tool

Execute shell commands in the project directory.

**Syntax**: 
```yaml
# Full access (use carefully)
allowed-tools: Bash

# Restricted to specific commands
allowed-tools: Bash(command:*), Bash(another:*)
```

**Capabilities**:
- Run any shell command
- Execute npm/yarn/pnpm scripts
- Git operations
- Build and test commands
- System utilities

**Usage in Commands**:

**Full Access**:
```markdown
---
allowed-tools: Bash
---

Run project tests: !`npm test`
Check git status: !`git status`
List files: !`ls -la src/`
```

**Restricted Access**:
```yaml
---
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(npm test:*)
---

Git status: !`git status`        ✅ Allowed
Add files: !`git add .`           ✅ Allowed
Run tests: !`npm test`            ✅ Allowed
Remove files: !`rm -rf dist/`     ❌ Blocked (not in allowed list)
```

**Common Bash Command Patterns**:

**Git Operations**:
```yaml
allowed-tools: |
  Bash(git status:*),
  Bash(git add:*),
  Bash(git diff:*),
  Bash(git log:*),
  Bash(git branch:*)
```

**NPM Scripts**:
```yaml
allowed-tools: |
  Bash(npm test:*),
  Bash(npm run build:*),
  Bash(npm run lint:*),
  Bash(npm install:*)
```

**Python/Pip**:
```yaml
allowed-tools: |
  Bash(python -m:*),
  Bash(pip install:*),
  Bash(pytest:*)
```

**Docker**:
```yaml
allowed-tools: |
  Bash(docker ps:*),
  Bash(docker logs:*),
  Bash(docker-compose:*)
```

**Best For**:
- Git workflow automation
- Running tests and builds
- Checking system state
- Package management
- Deployment tasks

**Limitations**:
- Security risk if unrestricted
- Platform-specific (Unix/Linux vs Windows)
- Long-running commands may timeout
- Interactive prompts won't work

**Security Best Practices**:
1. Always restrict to specific commands when possible
2. Never allow destructive commands globally
3. Validate inputs before bash execution
4. Use `Bash(command:*)` pattern, not full `Bash`
5. Document why bash access is needed

---

## Web Tools

### WebSearch

Search the web for information.

**Syntax**: `allowed-tools: WebSearch`

**Capabilities**:
- Search for current information
- Find documentation
- Research solutions
- Gather examples

**Usage in Commands**:
```markdown
---
allowed-tools: Read, WebSearch, WebFetch
---

Research best practices for $ARGUMENTS:
1. Search for official documentation
2. Find community solutions
3. Look for common pitfalls
4. Summarize findings with links
```

**Best For**:
- Finding current documentation
- Researching unfamiliar technologies
- Checking latest version information
- Learning from community examples

**Limitations**:
- Results may vary by query
- Requires internet connection
- May return outdated information
- Rate limits may apply

---

### WebFetch

Fetch and read web pages.

**Syntax**: `allowed-tools: WebFetch`

**Capabilities**:
- Download web page content
- Read API documentation
- Parse HTML content
- Access online resources

**Usage in Commands**:
```markdown
---
allowed-tools: WebSearch, WebFetch
---

Research framework usage:
1. Find official documentation site
2. Fetch and parse relevant pages
3. Extract code examples
4. Summarize implementation approach
```

**Best For**:
- Reading documentation directly
- Parsing API references
- Downloading examples
- Accessing changelogs

**Limitations**:
- Cannot handle JavaScript-heavy sites
- Rate limits apply
- Authentication not supported
- Large pages may be truncated

---

## MCP (Model Context Protocol) Tools

Access tools from MCP servers configured in your Claude Code.

**Syntax**: `allowed-tools: MCP`

**Common MCP Integrations**:

**Slack**:
```bash
/mcp__slack__send_message
/mcp__slack__list_channels
/mcp__slack__search_messages
```

**GitHub**:
```bash
/mcp__github__create_pr
/mcp__github__list_issues
/mcp__github__search_code
/mcp__github__get_file_contents
```

**Jira**:
```bash
/mcp__jira__create_issue
/mcp__jira__update_issue
/mcp__jira__search_issues
```

**Database (PostgreSQL)**:
```bash
/mcp__postgres__query
/mcp__postgres__get_schema
/mcp__postgres__run_migration
```

**Usage in Commands**:
```markdown
---
allowed-tools: Read, MCP
description: Create Jira ticket from code comments
---

Scan @src/ for TODO comments marked with "JIRA"

For each TODO:
1. Extract description and priority
2. Create Jira issue using: /mcp__jira__create_issue
3. Replace TODO with ticket reference
4. Report created tickets
```

**Best For**:
- Team integrations
- External service automation
- Database operations
- CI/CD integration

**Limitations**:
- Requires MCP server setup
- Server must be running and authenticated
- Tools vary by server implementation
- Check `/mcp` for available tools

**Setup**:
1. Configure MCP servers in `~/.claude/claude_desktop_config.json`
2. Start MCP servers
3. Authenticate if required (OAuth)
4. Check available tools with `/mcp`

---

## Tool Combinations

### Code Analysis (Read-Only)
```yaml
allowed-tools: Read, Grep, Glob
```
Safe for analyzing code without modifications.

### File Operations
```yaml
allowed-tools: Read, Write, Edit
```
Complete file manipulation without system access.

### Git Workflow
```yaml
allowed-tools: Read, Edit, Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```
Typical git commit workflow.

### Testing
```yaml
allowed-tools: Read, Bash(npm test:*), Bash(npm run:*)
```
Run tests and check results.

### Full Development
```yaml
allowed-tools: Read, Write, Edit, Bash(npm:*), Bash(git:*)
```
Complete development environment (use carefully).

### Research & Implementation
```yaml
allowed-tools: Read, Write, WebSearch, WebFetch
```
Research solutions and implement them.

### External Integration
```yaml
allowed-tools: Read, Edit, MCP, Bash(git:*)
```
Integrate with external services via MCP.

---

## Troubleshooting

### Tool Access Denied
- Check `allowed-tools` includes the needed tool
- Verify spelling and capitalization
- For Bash, ensure specific command is allowed

### Bash Commands Failing
- Test command works in terminal first
- Check `Bash(command:*)` pattern is correct
- Verify command is in system PATH
- Check for platform compatibility (Mac/Linux/Windows)

### File Not Found Errors
- Verify file path relative to working directory
- Use `/add-dir` to add directories to workspace
- Check file permissions
- Try absolute paths if relative fails

### MCP Tools Not Available
- Confirm MCP server is configured and running
- Check authentication status with `/mcp`
- Verify tool name with `/mcp` list
- Restart Claude Code if server was just added

---

## Best Practices

### Security
1. **Principle of Least Privilege**: Only include tools you need
2. **Restrict Bash**: Use `Bash(command:*)` not full `Bash`
3. **Validate Inputs**: Especially before bash execution
4. **Review Generated Commands**: Before running destructive operations

### Performance
1. **Minimize Tool Count**: Fewer tools = faster execution
2. **Batch Operations**: Group file operations when possible
3. **Cache Results**: Use bash output in multiple places if needed
4. **Avoid Redundancy**: Don't Read + Grep if Grep alone works

### Maintainability
1. **Document Choices**: Comment why specific tools are needed
2. **Consistent Patterns**: Use similar tool sets for similar commands
3. **Test Thoroughly**: Verify tool access works as expected
4. **Update Regularly**: Review and update tool permissions as commands evolve

---

## Tool Selection Decision Tree

```
Do you need to modify files?
├─ No → allowed-tools: Read, Grep, Glob
└─ Yes
   ├─ Only read + edit existing? → allowed-tools: Read, Edit
   ├─ Create new files? → allowed-tools: Read, Write, Edit
   └─ Need system commands?
      ├─ Git only? → add Bash(git add:*), Bash(git commit:*)
      ├─ NPM scripts? → add Bash(npm run:*), Bash(npm test:*)
      └─ General commands? → add Bash (with caution)

Need external services?
├─ Yes → add MCP, WebSearch, WebFetch as needed
└─ No → stick with file and bash tools
```

---

## Related Documentation

- See `frontmatter.md` for configuration syntax
- See `bash-integration.md` for bash command patterns
- See `../examples/` for real-world tool usage patterns
