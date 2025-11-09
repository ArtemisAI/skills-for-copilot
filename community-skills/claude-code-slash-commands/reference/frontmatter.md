# Frontmatter Configuration Reference

Complete guide to all YAML frontmatter fields available for Claude Code commands.

## Overview

Frontmatter is optional YAML metadata at the top of your command file, enclosed in `---` markers:

```markdown
---
field1: value
field2: value
---

Command content here...
```

## All Available Fields

### `allowed-tools`

Controls which tools the command can access.

**Type**: String (comma-separated list)

**Default**: All tools available in Claude Code

**Examples**:
```yaml
# Basic tools
allowed-tools: Read, Write, Edit

# Git operations
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)

# Read-only analysis
allowed-tools: Read, Grep, Glob

# Web research
allowed-tools: Read, WebSearch, WebFetch

# Full bash access
allowed-tools: Bash

# Specific bash commands only
allowed-tools: Bash(npm run:*), Bash(git status:*)
```

**Available Tools**:
- `Read` - Read file contents
- `Write` - Create new files
- `Edit` - Modify existing files
- `Grep` - Search file contents
- `Glob` - Find files by pattern
- `Bash` - Execute bash commands
- `Bash(command:*)` - Specific bash commands
- `WebSearch` - Search the web
- `WebFetch` - Fetch web pages
- `MCP` - Access MCP server tools

**Best Practice**: Restrict tools to minimum needed for security and clarity

---

### `argument-hint`

Provides autocomplete suggestions and documentation for command arguments.

**Type**: String

**Default**: None (command accepts any or no arguments)

**Examples**:
```yaml
# Single argument
argument-hint: [component-name]

# Multiple arguments
argument-hint: [component-name] [directory]

# Optional argument
argument-hint: [optional-message]

# Multiple options
argument-hint: add [tagId] | remove [tagId] | list

# Flag-style arguments
argument-hint: [file-path] [--watch] [--verbose]

# Complex combinations
argument-hint: deploy [env:staging|production] [--force]
```

**Best Practice**: Use clear, descriptive names in brackets; use `|` for alternatives

---

### `description`

Brief description of what the command does, shown in `/help` output.

**Type**: String

**Default**: None (command appears without description)

**Length**: Keep under 80 characters for readability

**Examples**:
```yaml
# Good descriptions (clear and concise)
description: Create a git commit with proper formatting
description: Generate React component with TypeScript and tests
description: Analyze code performance and suggest optimizations
description: Deploy application to specified environment
description: Run comprehensive code security audit

# Avoid (too vague)
description: Do stuff with git
description: Create component
description: Check code
```

**Best Practice**: Use active verbs; describe the outcome, not the process

---

### `model`

Specifies which Claude model to use for the command.

**Type**: String (model identifier)

**Default**: `claude-3-5-sonnet-20241022` (if not specified)

**Available Models**:
```yaml
# Sonnet - Balanced performance and speed (default)
model: claude-3-5-sonnet-20241022

# Haiku - Fastest, for simple tasks
model: claude-3-5-haiku-20241022

# Opus - Most capable, for complex tasks
model: claude-3-opus-20240229
```

**When to Use Each**:

**Haiku** (Fast):
- Simple code formatting
- Basic file operations
- Quick searches
- Template generation
- Style fixes

**Sonnet** (Balanced) - **Default**:
- Most development tasks
- Code generation
- Refactoring
- Test creation
- Documentation

**Opus** (Powerful):
- Complex architecture decisions
- Large-scale refactoring
- Advanced debugging
- System design
- Critical code review

**Best Practice**: Use Haiku for speed, Sonnet for most tasks, Opus only when needed

---

## Complete Example

```markdown
---
allowed-tools: Read, Edit, Bash(npm test:*), Bash(npm run lint:*)
argument-hint: [component-name] [--with-tests]
description: Generate React component with full setup
model: claude-3-5-sonnet-20241022
---

Generate a complete React component: $ARGUMENTS

Current project structure: @src/components/

Requirements:
1. TypeScript component with proper types
2. CSS modules for styling
3. Jest tests if --with-tests flag present
4. ESLint compliant: !`npm run lint`

Create component following our team standards...
```

## Field Interactions

### Tools + Bash Commands

When using `Bash(command:*)` in `allowed-tools`, the command can only execute those specific bash commands:

```yaml
# Only git commands allowed
allowed-tools: Read, Bash(git status:*), Bash(git add:*)

# Then in command content:
- Status: !`git status`  ✅ Works
- Add files: !`git add .` ✅ Works  
- List files: !`ls -la`   ❌ Fails (not allowed)
```

### Arguments + Model Choice

Complex argument parsing benefits from more capable models:

```yaml
# Simple argument - Haiku is fine
argument-hint: [filename]
model: claude-3-5-haiku-20241022

# Complex parsing - use Sonnet or Opus
argument-hint: deploy [env] [--force] [--rollback-on-error]
model: claude-3-5-sonnet-20241022
```

### Description + Discoverability

Good descriptions improve command discoverability in `/help`:

```yaml
# User searches /help for "test"
description: Generate unit tests for React components  ✅ Found
description: Create tests                              ✅ Found
description: Make component                            ❌ Not found
```

## Common Patterns

### Read-Only Analysis Commands

```yaml
---
allowed-tools: Read, Grep, Glob
description: Analyze codebase for patterns
model: claude-3-5-sonnet-20241022
---
```

### Git Workflow Commands

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [commit-message]
description: Create formatted git commit
model: claude-3-5-haiku-20241022
---
```

### File Generation Commands

```yaml
---
allowed-tools: Read, Write, Edit, Bash(npm run:*)
argument-hint: [name] [path]
description: Generate component with tests
model: claude-3-5-sonnet-20241022
---
```

### Research Commands

```yaml
---
allowed-tools: Read, WebSearch, WebFetch
description: Research and document solution
model: claude-3-5-sonnet-20241022
---
```

## Validation Rules

1. **YAML must be valid**: Test with a YAML validator
2. **Field names are case-sensitive**: Use exact names shown here
3. **Unknown fields are ignored**: Typos won't error but won't work
4. **Empty frontmatter is valid**: `---\n---` works (uses all defaults)
5. **Model IDs must match exactly**: Wrong model ID falls back to default

## Troubleshooting

### Command not recognizing frontmatter
- Check `---` markers are on their own lines
- Verify YAML syntax (use a validator)
- Ensure no spaces before `---`

### Tools not working as expected
- Verify tool names exactly match available tools
- Check bash command patterns with `Bash(command:*)`
- Confirm MCP servers are connected for MCP tools

### Arguments not passing correctly
- Test with and without `argument-hint`
- Verify `$ARGUMENTS` placement in command content
- Check for typos in placeholder name

### Model not being used
- Confirm model ID is valid and available
- Check Claude Code version supports the model
- Verify no typos in model identifier

## Advanced Patterns

### Environment-Specific Tools

```yaml
---
allowed-tools: |
  Read, Write, 
  Bash(npm run test:*),
  Bash(npm run build:*),
  Bash(git status:*)
---
```

### Dynamic Model Selection

While you can't dynamically change models, you can create variants:

```
.claude/commands/
├── review-quick.md     # model: haiku
├── review-standard.md  # model: sonnet  
└── review-deep.md      # model: opus
```

### Complex Argument Patterns

```yaml
# Subcommands with multiple options
argument-hint: create [type:component|page|hook] [name] | list | delete [name]

# Flags and values
argument-hint: [file-path] [--format json|yaml|toml] [--output path]

# Required and optional mix
argument-hint: [required-name] [optional-path] [--optional-flag]
```

## Best Practices Summary

1. **Minimal Tools**: Only include tools the command actually needs
2. **Clear Arguments**: Descriptive hints help users understand usage
3. **Descriptive**: Write descriptions that appear helpful in `/help`
4. **Right Model**: Match model to complexity (Haiku → Sonnet → Opus)
5. **Test**: Verify frontmatter works as expected with real usage
6. **Document**: Add comments explaining non-obvious configuration choices
7. **Version**: Keep model identifiers updated with new Claude releases
8. **Consistent**: Use similar patterns across related commands

## Related Documentation

- See `tools.md` for detailed tool capabilities
- See `bash-integration.md` for bash command patterns
- See `../templates/` for ready-to-use frontmatter configurations
