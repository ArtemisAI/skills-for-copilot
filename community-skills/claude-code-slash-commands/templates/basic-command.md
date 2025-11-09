# Basic Command Template

Simple template for creating a new Claude Code command.

## File: `.claude/commands/[your-command-name].md`

```markdown
---
allowed-tools: Read, Write, Edit
argument-hint: [your-arguments]
description: Brief description of what this command does
model: claude-3-5-sonnet-20241022
---

## Context

Provide context about what you want Claude to do.

Current files: @path/to/relevant/files
Current state: !`relevant-bash-command`

## Task

Describe the specific task clearly:

1. First step
2. Second step
3. Third step

## Requirements

- Requirement 1
- Requirement 2
- Requirement 3

## Expected Output

Describe what Claude should produce or accomplish.
```

## Customization Guide

### 1. Choose Your Filename
The filename (without `.md`) becomes the command name:
- `analyze.md` → `/analyze`
- `fix-bug.md` → `/fix-bug`
- `deploy-prod.md` → `/deploy-prod`

### 2. Configure Tools
Select only the tools you need:

```yaml
# Read-only analysis
allowed-tools: Read, Grep, Glob

# File modifications
allowed-tools: Read, Edit, Write

# Git workflow
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)

# Full development
allowed-tools: Read, Write, Edit, Bash(npm:*), Bash(git:*)
```

### 3. Define Arguments
Specify what arguments your command accepts:

```yaml
# No arguments
argument-hint: 

# Single argument
argument-hint: [filename]

# Multiple arguments
argument-hint: [name] [directory]

# Optional argument
argument-hint: [optional-message]

# Multiple options
argument-hint: start | stop | restart
```

### 4. Write Clear Description
Keep it under 80 characters, use active verbs:

```yaml
# Good
description: Generate React component with TypeScript and tests
description: Create formatted git commit with conventional commits
description: Analyze code for security vulnerabilities

# Avoid
description: Does component stuff
description: Git helper
description: Code checker
```

### 5. Choose Model
Match model to task complexity:

```yaml
# Fast, simple tasks (formatting, basic generation)
model: claude-3-5-haiku-20241022

# Most tasks (default, balanced)
model: claude-3-5-sonnet-20241022

# Complex tasks (architecture, advanced refactoring)
model: claude-3-opus-20240229
```

### 6. Structure Your Prompt

**Good Structure**:
```markdown
## Context
[What Claude needs to know]

## Task
[What Claude should do]

## Requirements
[Specific constraints and standards]

## Expected Output
[What the result should look like]
```

**Include Dynamic Elements**:
- `$ARGUMENTS` - User-provided arguments
- `@file/path` - File contents
- `!backtick-command-backtick` - Bash command output

## Usage Example

After creating your command file:

```bash
# If you created: .claude/commands/analyze.md
/analyze src/components/Button.tsx

# If you created: ~/.claude/commands/deploy.md
/deploy staging --force
```

## Quick Start Checklist

- [ ] Choose clear, descriptive filename
- [ ] Add frontmatter with minimal required tools
- [ ] Write clear description
- [ ] Define argument-hint if command takes arguments
- [ ] Structure prompt with Context, Task, Requirements, Output
- [ ] Use $ARGUMENTS for dynamic values
- [ ] Include @file references for context
- [ ] Add !`bash` commands for system state
- [ ] Test command with real inputs
- [ ] Refine based on results

## Next Steps

1. Copy this template
2. Customize for your use case
3. Save as `.claude/commands/your-command.md`
4. Test with `/your-command`
5. Iterate and improve

## Related Templates

- `git-workflow.md` - Template for git operations
- `code-generation.md` - Template for generating code
- `analysis.md` - Template for code analysis
- `deployment.md` - Template for deployment tasks
