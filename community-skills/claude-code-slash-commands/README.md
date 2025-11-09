# Claude Code Slash Commands Creator - Skill

> Create powerful, reusable command shortcuts for Claude Code

## Quick Start

This skill helps you create custom slash commands for Claude Code. Commands are Markdown files stored in `.claude/commands/` (project) or `~/.claude/commands/` (personal) that define reusable AI workflows.

### Installation

1. Copy this entire skill folder to your skills directory
2. Claude Code will automatically recognize and use it

### Basic Usage

When a user wants to create a command:

1. **Read the SKILL.md** - Main reference
2. **Check examples/** - See real commands
3. **Use templates/** - Copy and customize
4. **Reference docs** - Deep dive as needed

## Structure

```
claude-code-slash-commands/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── examples/                   # Real command examples
│   ├── git-commit.md          # Git workflow automation
│   ├── react-component.md     # Component generation
│   └── code-review.md         # Automated code review
├── reference/                  # Detailed references
│   ├── frontmatter.md         # YAML configuration guide
│   └── tools.md               # Available tools reference
└── templates/                  # Ready-to-use templates
    ├── basic-command.md       # Simple command template
    └── git-workflow.md        # Git command template
```

## What This Skill Teaches

### Core Concepts
- Command structure and syntax
- YAML frontmatter configuration
- Dynamic arguments with `$ARGUMENTS`
- File references with `@` syntax
- Bash integration with `!` syntax
- Extended thinking patterns

### Best Practices
- Tool selection and security
- Prompt engineering for commands
- Argument design patterns
- Testing and validation
- Team collaboration strategies

### Advanced Patterns
- Conditional logic
- Multi-step workflows
- Environment-aware commands
- MCP integration
- Complex argument parsing

## When to Use This Skill

Use this skill when the user asks to:
- "Create a slash command for..."
- "Make a command that..."
- "Automate [workflow] with Claude Code"
- "Set up a [task] command"
- "How do I create custom commands?"

## Example Interactions

### User: "Create a command to generate React components"

**Response Pattern**:
1. Read `examples/react-component.md`
2. Customize for their tech stack
3. Explain frontmatter choices
4. Provide complete command file
5. Show usage examples

### User: "Make a git commit helper"

**Response Pattern**:
1. Read `templates/git-workflow.md`
2. Configure for their commit style
3. Add safety checks
4. Explain bash tool restrictions
5. Test command logic

### User: "Help me organize my commands"

**Response Pattern**:
1. Reference organization strategies from SKILL.md
2. Suggest directory structure
3. Explain project vs personal commands
4. Show namespacing examples

## Teaching Approach

### 1. Understand Use Case
Ask clarifying questions:
- What workflow are you automating?
- Who will use this command?
- What inputs does it need?
- What should it output?

### 2. Choose Starting Point
- Simple task → Use `templates/basic-command.md`
- Git workflow → Use `templates/git-workflow.md`
- Complex task → Start from relevant example

### 3. Build Incrementally
- Start with minimal frontmatter
- Add tools as needed
- Test with simple cases
- Add complexity gradually
- Refine based on feedback

### 4. Explain Decisions
- Why these tools?
- Why this model?
- Why these restrictions?
- What are the trade-offs?

## Key Principles

### Security First
- Restrict tools to minimum needed
- Use `Bash(command:*)` not full `Bash`
- Never auto-execute destructive operations
- Validate inputs before bash execution

### User Experience
- Clear, descriptive command names
- Helpful argument hints
- Informative descriptions
- Good error messages
- Predictable behavior

### Maintainability
- Well-documented prompts
- Consistent patterns
- Easy to modify
- Testable logic
- Version control friendly

## Command Creation Workflow

```
1. Understand → Ask about the workflow
2. Design     → Plan command structure
3. Configure  → Set up frontmatter
4. Write      → Craft the prompt
5. Test       → Verify with real inputs
6. Document   → Add usage examples
7. Iterate    → Refine based on usage
```

## Common Patterns

### Analysis Commands
```yaml
allowed-tools: Read, Grep, Glob
model: claude-3-5-sonnet-20241022
```

### Generation Commands
```yaml
allowed-tools: Read, Write, Edit
model: claude-3-5-sonnet-20241022
```

### Git Commands
```yaml
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
model: claude-3-5-haiku-20241022
```

### Research Commands
```yaml
allowed-tools: Read, WebSearch, WebFetch
model: claude-3-5-sonnet-20241022
```

## Troubleshooting

### Command doesn't work
1. Check YAML frontmatter syntax
2. Verify file is in correct location
3. Ensure `---` markers are present
4. Test in isolation

### Tools not available
1. Check `allowed-tools` list
2. Verify tool names match exactly
3. For Bash, check specific command patterns
4. Confirm MCP servers are running

### Arguments not passing
1. Verify `$ARGUMENTS` placement
2. Test with simple inputs
3. Check argument-hint formatting
4. Review prompt logic

## Tips for Success

### For Simple Commands
- Start with basic template
- Use minimal tools
- Clear, focused purpose
- Test immediately

### For Complex Commands
- Break into steps
- Use reference docs
- Study examples first
- Build incrementally

### For Team Commands
- Document thoroughly
- Use consistent naming
- Restrict destructive operations
- Provide clear usage examples

## Learning Resources

### Start Here
1. Read `SKILL.md` overview
2. Study one example that matches your use case
3. Copy and modify a template
4. Test and iterate

### Deep Dive
1. Read all reference documentation
2. Study all examples
3. Experiment with patterns
4. Create custom templates

### Master Level
1. Combine multiple patterns
2. Create command libraries
3. Build team standards
4. Contribute examples back

## Contributing

To extend this skill:
1. Add new examples to `examples/`
2. Create specialized templates in `templates/`
3. Expand reference docs
4. Share patterns that work

## Version

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Compatible With**: Claude Code latest

## Support

For Claude Code itself:
- Documentation: https://docs.claude.com/en/docs/claude-code
- Support: https://support.claude.com

For this skill:
- Check examples for patterns
- Review reference docs
- Test in isolation
- Iterate based on results

---

**Remember**: Start simple, test often, and iterate based on real usage. Commands should make your workflow faster and more consistent, not more complex.
