---
name: claude-code-slash-commands
description: Create and structure custom slash commands for Claude Code. Use when users want to build reusable prompt shortcuts, workflow automations, or standardized development commands stored as Markdown files.
version: 1.0.0
tags: [claude-code, automation, commands, workflow, productivity]
---

# Claude Code Slash Commands Creator

## Overview

This skill helps you create custom slash commands for Claude Code - reusable prompts that can be invoked with simple slash syntax. Commands transform repetitive workflows into single-command executions, complete with dynamic arguments, bash integration, and file references.

## Using Bundled Resources

This skill includes comprehensive resources for command creation and maintenance:

### 🎯 Quick Start Guide
Load `reference/command-guide.md` for the **complete command creation guide** (900+ lines) covering:
- Command structure and syntax
- Frontmatter configuration
- Dynamic arguments and bash integration
- File references
- 6 complete production examples
- Best practices and common patterns
- Troubleshooting guide

### 📋 Review System
Load `reference/command-review-system.md` for **command quality workflows**:
- Bulk review process (`/review-commands`)
- Individual command review (`/review-command`)
- Quality standards and checklists
- Common issues and quick fixes
- Maintenance schedules
- Integration with development workflow

### 🗺️ System Overview
Load `reference/COMMAND_SYSTEM_OVERVIEW.md` for **complete ecosystem understanding**:
- End-to-end command lifecycle
- Review and deployment workflows
- Quality standards and metrics
- Integration with command-specialist agent
- Action plans and best practices

### ✅ Quality Checklist
Load `reference/command-review-checklist.md` for **quality validation standards**:
- Frontmatter validation criteria
- Prompt structure requirements
- Bash syntax validation
- Testing recommendations
- Deployment criteria

### 📚 Additional References
- `reference/frontmatter.md` - Complete frontmatter field reference
- `reference/tools.md` - Tool selection guide and patterns

### 💡 Examples & Templates
- `examples/` - 3 production-ready command examples
- `templates/` - 2 command templates for common patterns

### Workflow for Creating Commands
1. **Learn basics**: Load `reference/command-guide.md`
2. **Browse examples**: Check `examples/` directory
3. **Start with template**: Copy from `templates/`
4. **Create command**: Write to `.claude/commands/review/`
5. **Validate quality**: Load `reference/command-review-checklist.md`
6. **Review**: Use `/review-command` to validate
7. **Test**: Try command with real arguments
8. **Deploy**: Move to `.claude/commands/`

## When to Use This Skill

Use this skill when the user wants to:
- Create custom `/command` shortcuts for Claude Code
- Automate repetitive development workflows
- Build team-shared project commands
- Standardize coding practices across teams
- Integrate bash commands with AI prompts
- Create context-aware development automation

## Core Concepts

### What are Claude Code Commands?

Commands are Markdown files (`.md`) that define reusable prompts. Each command:
- Has a specific purpose and can accept arguments
- Can execute bash commands before running the prompt
- Supports file references using `@` syntax
- Can be project-scoped or personal
- Includes optional YAML frontmatter for configuration

### Command Locations

| Type | Location | Scope | Visibility | Priority |
|------|----------|-------|------------|----------|
| **Project Commands** | `.claude/commands/` | Current project only | Shared with team | Higher |
| **Personal Commands** | `~/.claude/commands/` | All projects | Private to user | Lower |

*When there are name conflicts, project commands take precedence over personal commands.*

### Key Benefits

**🚀 Rapid Execution**: Execute complex prompts with `/command` syntax

**🔧 Dynamic Arguments**: Pass variables using `$ARGUMENTS` placeholder

**📁 Smart Organization**: Organize commands in subdirectories with automatic namespacing

**🔄 Context Enrichment**: Include bash output and file contents automatically

**♻️ Team Collaboration**: Share project commands while keeping personal ones private

## Command Structure

### Basic Format

```markdown
---
allowed-tools: Read, Edit, Bash
argument-hint: [optional-arg]
description: Brief description of the command
model: sonnet
---

Your command prompt goes here. This can include:

- Dynamic arguments using $ARGUMENTS
- File references using @filename.js
- Bash command output using !`command`
- Multiple paragraphs with detailed instructions

Include specific instructions and context that Claude should follow.
```

### Filename to Command Mapping

- **File**: `optimize.md` → **Command**: `/optimize`
- **File**: `fix-issue.md` → **Command**: `/fix-issue`
- **File**: `security-review.md` → **Command**: `/security-review`

### Directory Organization

Commands can be organized in subdirectories:

```
.claude/commands/
├── frontend/
│   ├── component.md      # /component (project:frontend)
│   └── styling.md        # /styling (project:frontend)
├── backend/
│   ├── api-test.md       # /api-test (project:backend)
│   └── database.md       # /database (project:backend)
└── git/
    ├── commit.md         # /commit (project:git)
    └── review.md         # /review (project:git)
```

## Frontmatter Configuration

### `allowed-tools` (Optional)

Restricts which tools the command can use:

```yaml
allowed-tools: Read, Edit, Bash(git add:*), Bash(git status:*)
```

**Common tool combinations:**

- **Code Analysis**: `Read, Grep, Glob`
- **File Operations**: `Read, Edit, Write`
- **Git Operations**: `Bash(git add:*), Bash(git status:*), Bash(git commit:*)`
- **Web Research**: `Read, WebSearch, WebFetch`
- **Full Access**: Leave empty to inherit all tools

### `argument-hint` (Optional)

Provides autocomplete guidance for command arguments:

```yaml
argument-hint: add [tagId] | remove [tagId] | list
argument-hint: [issue-number]
argument-hint: [component-name] [directory]
```

### `description` (Optional)

Brief description shown in `/help`:

```yaml
description: Create a git commit with proper formatting
description: Analyze code performance and suggest optimizations
description: Generate React component with tests
```

### `model` (Optional)

Specify which Claude model to use:

```yaml
model: claude-3-5-sonnet-20241022    # Default, balanced performance
model: claude-3-5-haiku-20241022     # Faster, simpler tasks
model: claude-3-opus-20240229        # Most capable, complex tasks
```

## Advanced Features

### Dynamic Arguments

Use `$ARGUMENTS` to pass values to commands:

```markdown
---
argument-hint: [issue-number]
description: Fix GitHub issue following coding standards
---

Fix issue #$ARGUMENTS following our team's coding standards:

1. Review the issue requirements
2. Implement the solution
3. Add appropriate tests
4. Update documentation if needed
```

**Usage**: `/fix-issue 123`

### Bash Command Integration

Execute commands before the prompt runs using `!` prefix:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a comprehensive git commit
---

## Current Repository State

- Git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Recent commits: !`git log --oneline -5`

## Task

Based on the above repository state, create a well-formatted commit message.
```

### File References

Include file contents using `@` syntax:

```markdown
---
description: Review code implementation
---

Please review the following implementation:

Main component: @src/components/UserProfile.js
Test file: @tests/components/UserProfile.test.js
Types: @types/user.ts

Analyze for:
- Code quality and best practices
- Test coverage completeness
- Type safety implementation
- Performance considerations
```

### Extended Thinking Mode

Trigger extended thinking by including specific keywords:

```markdown
---
description: Complex architectural decision analysis
---

<thinking>
I need to carefully analyze this architectural decision considering multiple factors.
</thinking>

Analyze the architectural implications of @src/config/architecture.md and provide:

1. Detailed analysis of current approach
2. Alternative solutions with trade-offs
3. Recommended implementation strategy
4. Migration path if changes are needed
```

## Best Practices

### 1. Command Design Principles

- **Single Responsibility**: One clear purpose per command
- **Descriptive Names**: Use clear, action-oriented names
- **Consistent Patterns**: Follow established naming conventions
- **Atomic Operations**: Complete tasks that don't require follow-up

### 2. Effective Prompt Structure

```markdown
## Structure Template

### Context Section
- Current state analysis
- Relevant file contents
- System information

### Requirements Section  
- Clear, numbered requirements
- Acceptance criteria
- Quality standards

### Deliverables Section
- Specific outputs expected
- Format requirements
- Documentation needs
```

### 3. Tool Selection Strategy

```yaml
# ✅ Focused tool selection
allowed-tools: Read, Edit, Bash(git add:*), Bash(git status:*)

# ❌ Too permissive
allowed-tools: Read, Write, Edit, Bash, WebFetch, WebSearch, Grep, Glob
```

### 4. Argument Design

```yaml
# ✅ Clear argument guidance
argument-hint: [component-name] [directory] [--typescript]

# ❌ Vague guidance  
argument-hint: [options]
```

### 5. Command Testing

- Test with real scenarios from your projects
- Verify argument handling works correctly
- Check bash command execution produces expected output
- Validate file references resolve properly
- Test error conditions and edge cases

## Command Examples

See the `examples/` directory for complete, production-ready command examples including:
- Git workflow commands
- React component generators
- Code review automation
- Testing helpers
- Documentation generators

## Common Use Cases

### Development Workflow
```bash
/init                    # Setup project configuration
/component Button        # Generate React component
/test Button            # Generate component tests
/commit                 # Create formatted git commit
/review                 # Request code review
```

### Debugging & Analysis
```bash
/performance            # Analyze performance issues
/security               # Security audit
/dependencies           # Analyze and update dependencies
/logs                   # Analyze log files
/errors                 # Debug error patterns
```

### Database Operations
```bash
/migrate create_users   # Create database migration
/seed                   # Generate test data
/backup                 # Backup database
/optimize               # Optimize database performance
```

### DevOps & Deployment
```bash
/deploy staging         # Deploy to staging environment  
/rollback               # Rollback deployment
/monitor                # Check system health
/scale                  # Scale application resources
```

## Command Organization Strategies

### By Project Phase
```
.claude/commands/
├── setup/              # Project initialization
├── development/        # Daily development tasks  
├── testing/           # Testing and QA
├── deployment/        # Deployment and DevOps
└── maintenance/       # Ongoing maintenance
```

### By Technology Stack
```
.claude/commands/
├── frontend/          # React, Vue, Angular commands
├── backend/           # Node.js, Python, API commands
├── database/          # SQL, migrations, seeding
├── infrastructure/    # Docker, K8s, cloud commands
└── tools/            # Build tools, linting, formatting
```

### By Team Role
```
~/.claude/commands/
├── developer/         # General development commands
├── devops/           # Infrastructure and deployment
├── qa/               # Testing and quality assurance
└── lead/             # Architecture and code review
```

## Troubleshooting

### Command Not Found
**Symptoms**: `/command` shows "Command not found"

**Solutions**:
- Verify file exists in `.claude/commands/` or `~/.claude/commands/`
- Check filename matches command name (without `.md`)
- Ensure markdown file has proper content
- Restart Claude Code session

### Arguments Not Working
**Symptoms**: `$ARGUMENTS` appears literally in output

**Solutions**:
- Ensure arguments are provided when calling command
- Check `argument-hint` frontmatter is correctly formatted
- Verify `$ARGUMENTS` placement in command content

### Bash Commands Failing
**Symptoms**: `!command` output shows errors

**Solutions**:
- Verify `allowed-tools` includes `Bash` or specific commands
- Test bash commands work in terminal first
- Check file paths and permissions
- Ensure commands are available in system PATH

### File References Not Working
**Symptoms**: `@filename` shows "File not found"

**Solutions**:
- Verify file paths are correct relative to working directory
- Check file permissions are readable
- Use `/add-dir` to add additional working directories
- Test file references with absolute paths

### Permission Issues
**Symptoms**: Commands fail with permission errors

**Solutions**:
- Use `/permissions` to check current access levels
- Ensure `allowed-tools` includes necessary tools
- Check file system permissions
- Verify MCP server authentication if using MCP commands

## MCP Integration

Commands can leverage MCP (Model Context Protocol) servers for extended functionality:

```bash
# Slack integration  
/mcp__slack__send_message "#general" "Deployment complete"
/mcp__slack__list_channels

# GitHub integration
/mcp__github__create_pr "main" "feature/new-api"
/mcp__github__list_issues

# Jira integration  
/mcp__jira__create_issue "Bug title" high
/mcp__jira__list_issues

# Database operations
/mcp__postgres__query "SELECT * FROM users LIMIT 10"
/mcp__postgres__migrate
```

### MCP Management

Use `/mcp` to:
- View configured MCP servers
- Check connection status
- Authenticate with OAuth-enabled servers
- Clear authentication tokens
- View available tools and prompts

## Advanced Patterns

### Conditional Logic

```markdown
---
description: Smart deployment based on environment
---

Analyze the current environment and deploy accordingly:

**Current branch**: !`git branch --show-current`
**Environment config**: @.env
**Package.json**: @package.json

If production branch:
1. Run full test suite
2. Build production assets  
3. Deploy with zero downtime
4. Run smoke tests

If staging branch:
1. Run quick tests
2. Deploy to staging
3. Send notification to team

If development branch:
1. Deploy to development environment
2. Skip extensive testing
```

### Multi-Step Workflows

```markdown
---
allowed-tools: Read, Write, Edit, Bash
description: Complete feature implementation workflow
---

Implement feature: $ARGUMENTS

## Step 1: Planning
1. Analyze requirements
2. Check existing code: @src/
3. Plan implementation approach

## Step 2: Implementation  
1. Create necessary files
2. Implement core functionality
3. Add error handling

## Step 3: Testing
1. Create unit tests
2. Create integration tests  
3. Run test suite: !`npm test`

## Step 4: Documentation
1. Update README if needed
2. Add JSDoc comments
3. Update API documentation

## Step 5: Quality Assurance
1. Run linting: !`npm run lint`
2. Format code: !`npm run format`
3. Check build: !`npm run build`

Complete each step before proceeding to the next.
```

### Environment-Aware Commands

```markdown
---
description: Environment-specific database operations
---

**Current environment**: !`echo $NODE_ENV`
**Database config**: @config/database.js

## Environment-Specific Actions

### Production Environment
- Use read-only operations only
- Require explicit confirmation for changes
- Enable audit logging
- Use connection pooling

### Staging Environment  
- Allow controlled data modifications
- Enable detailed logging
- Use production-like configuration
- Reset data daily

### Development Environment
- Allow all operations
- Use local database
- Enable debug logging
- Seed with test data

Execute database operation: $ARGUMENTS
```

## Implementation Guide

When helping users create commands:

1. **Understand the Use Case**: Ask about the workflow they want to automate
2. **Define Scope**: Determine if it's project-specific or personal
3. **Choose Location**: `.claude/commands/` for project, `~/.claude/commands/` for personal
4. **Design the Prompt**: Structure with clear context, requirements, and deliverables
5. **Add Frontmatter**: Configure tools, arguments, and description
6. **Test Thoroughly**: Run the command with various inputs
7. **Document**: Add clear description and argument hints
8. **Iterate**: Refine based on actual usage

## Reference Files

- `reference/frontmatter.md` - Complete frontmatter field reference
- `reference/tools.md` - Available tools and their usage
- `reference/bash-integration.md` - Bash command patterns
- `reference/file-references.md` - File reference syntax
- `templates/` - Ready-to-use command templates

## Conclusion

Claude Code commands significantly improve development workflow by:
- Automating repetitive tasks with simple slash syntax
- Standardizing team workflows through shared project commands  
- Integrating with external tools via bash commands and MCP
- Providing context-aware assistance through file references and dynamic arguments

Start with simple, focused commands and gradually build more sophisticated workflows as you become comfortable with the system.
