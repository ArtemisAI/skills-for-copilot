# Git Commit Command Example

This is a complete, production-ready command for creating well-formatted git commits.

## File: `.claude/commands/commit.md`

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git log:*)
argument-hint: [optional-commit-message]
description: Create a well-formatted git commit
model: claude-3-5-sonnet-20241022
---

## Repository Context

- Current status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Staged files: !`git diff --cached --name-only`
- Unstaged changes: !`git diff --name-only`
- Last 3 commits: !`git log --oneline -3`

## Task

Create a git commit with proper formatting:

1. **If no message provided**: Generate a descriptive commit message based on the staged changes
2. **If message provided**: Use "$ARGUMENTS" as the commit message
3. **Follow conventional commits format**: `type(scope): description`
4. **Add co-authored-by**: Include Claude attribution

Commit message should be:
- Clear and descriptive
- Under 50 characters for the title
- Include detailed body if necessary
- Follow our team's commit standards

Example format:
```
feat(auth): add JWT token validation

- Implemented token expiration check
- Added refresh token mechanism
- Updated authentication middleware

Co-authored-by: Claude <claude@anthropic.com>
```
```

## Usage Examples

```bash
# Generate commit message automatically
/commit

# Use custom commit message
/commit "Fix authentication bug"

# Will analyze staged files and create appropriate message
/commit
```

## Key Features

1. **Automatic Message Generation**: Analyzes staged changes to create descriptive messages
2. **Conventional Commits**: Follows industry-standard commit format
3. **Context Awareness**: Uses git status and recent commits for context
4. **Flexible Usage**: Works with or without custom messages
5. **Attribution**: Includes co-authored-by for Claude contributions

## Best Practices

- Stage your changes before running the command
- Review the generated commit message before confirming
- Use custom messages for quick fixes or specific requirements
- Ensure your changes are cohesive for a single commit
