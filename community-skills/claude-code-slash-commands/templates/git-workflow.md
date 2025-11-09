# Git Workflow Template

Template for creating git-related commands.

## File: `.claude/commands/[git-command-name].md`

```markdown
---
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*)
argument-hint: [optional-arguments]
description: [Your git workflow description]
model: claude-3-5-haiku-20241022
---

## Repository State

- Current branch: !`git branch --show-current`
- Git status: !`git status --porcelain`
- Staged files: !`git diff --cached --name-only`
- Unstaged changes: !`git diff --name-only`
- Recent commits: !`git log --oneline -5`
- Current changes: !`git diff --stat`

## Task

[Describe what git operation to perform]

## Requirements

- Follow conventional commits format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep title under 50 characters
- Add detailed body if needed
- Include co-authored-by if applicable

## Expected Behavior

[Describe expected git operation outcome]
```

## Common Git Command Patterns

### 1. Smart Commit
```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create intelligent commit message based on changes
---

Analyze staged changes and create a commit:
- If no files staged: inform user to stage files first
- Generate conventional commit message
- Include co-authored-by: Claude
```

### 2. Branch Operations
```markdown
---
allowed-tools: Bash(git branch:*), Bash(git checkout:*), Bash(git status:*)
argument-hint: [branch-name]
description: Create and switch to new feature branch
---

Create feature branch: feature/$ARGUMENTS
- Check for uncommitted changes
- Create branch from current HEAD
- Switch to new branch
- Confirm creation
```

### 3. Code Review Prep
```markdown
---
allowed-tools: Bash(git diff:*), Bash(git log:*), Read
description: Prepare code for review
---

Review changes since main:
- Show diff stats: !`git diff main --stat`
- List modified files
- Analyze changes for review
- Generate PR description
```

### 4. Clean Working Directory
```markdown
---
allowed-tools: Bash(git status:*), Bash(git clean:*), Bash(git reset:*)
description: Clean up working directory
---

Check for:
- Untracked files: !`git status --porcelain | grep "^??"`
- Unstaged changes
- Staged but uncommitted changes

Provide cleanup options (don't execute automatically)
```

### 5. Sync with Remote
```markdown
---
allowed-tools: Bash(git fetch:*), Bash(git status:*), Bash(git log:*)
description: Check sync status with remote
---

Check remote sync:
- Fetch updates: !`git fetch`
- Compare with remote: !`git log HEAD..origin/$(git branch --show-current) --oneline`
- Show divergence status
- Suggest pull/push actions
```

## Tool Configuration Guide

### Safe Git Tools (Read-Only)
```yaml
# Check status without modifications
allowed-tools: Bash(git status:*), Bash(git log:*), Bash(git diff:*)
```

### Standard Commit Workflow
```yaml
# Add, commit, but no push
allowed-tools: |
  Bash(git status:*),
  Bash(git add:*),
  Bash(git diff:*),
  Bash(git commit:*)
```

### Branch Management
```yaml
# Create, switch, delete branches
allowed-tools: |
  Bash(git branch:*),
  Bash(git checkout:*),
  Bash(git switch:*)
```

### Full Git Access (Use Carefully)
```yaml
# All git commands (dangerous!)
allowed-tools: Bash(git:*)
```

## Argument Patterns

### No Arguments
```yaml
# Auto-detect operation from git state
argument-hint:
```

### Optional Message
```yaml
# Use custom message or generate one
argument-hint: [optional-commit-message]
```

### Branch Name
```yaml
# Require branch name
argument-hint: [branch-name]
```

### Multiple Options
```yaml
# Different git operations
argument-hint: status | commit | branch [name] | review
```

## Safety Patterns

### 1. Check Before Destructive Operations
```markdown
Before committing:
1. Show what will be committed: !`git diff --cached`
2. Confirm files are correct
3. Ask user to verify before proceeding
```

### 2. Never Auto-Push
```markdown
After commit:
- Show commit details: !`git show HEAD --stat`
- Suggest push command but don't execute
- Let user decide when to push
```

### 3. Validate State
```markdown
Before operations:
- Check for conflicts: !`git diff --check`
- Verify branch is correct
- Ensure working directory is clean if needed
```

## Example Commands

### Smart Commit Command
```markdown
---
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git commit:*), Bash(git diff:*)
argument-hint: [optional-message]
description: Create well-formatted git commit
model: claude-3-5-haiku-20241022
---

## Repository Analysis

- Current branch: !`git branch --show-current`
- Staged: !`git diff --cached --name-only`
- Status: !`git status --porcelain`

## Commit Task

1. If $ARGUMENTS provided: use as commit message
2. If no arguments: analyze changes and generate message
3. Format: `type(scope): description`
4. Add co-authored-by: Claude

Commit after user confirmation.
```

### Branch Cleanup Command
```markdown
---
allowed-tools: Bash(git branch:*), Bash(git log:*)
description: List branches that can be cleaned up
model: claude-3-5-haiku-20241022
---

## Branch Analysis

- All branches: !`git branch -a`
- Merged branches: !`git branch --merged`
- Remote branches: !`git branch -r`

## Task

Identify branches to clean up:
1. Find merged branches (except main/master/develop)
2. Check last commit date
3. Suggest branches for deletion
4. Provide delete commands (don't execute)
```

## Testing Your Git Commands

1. **Create test repository**:
```bash
mkdir test-git-repo
cd test-git-repo
git init
echo "test" > file.txt
git add file.txt
```

2. **Test command**:
```bash
/your-git-command
```

3. **Verify results**:
```bash
git log
git status
```

4. **Clean up**:
```bash
cd ..
rm -rf test-git-repo
```

## Best Practices

1. **Always show state first**: Let user see what's happening
2. **Use conventional commits**: Standardize message format
3. **Avoid destructive operations**: Never auto-delete or force-push
4. **Confirm before actions**: Show intent, ask permission
5. **Provide undo instructions**: Tell user how to revert if needed
6. **Check for conflicts**: Verify clean state before operations
7. **Test in isolation**: Use test repos before production use

## Common Pitfalls

### ❌ Don't
```markdown
# Auto-pushing without confirmation
!`git push origin HEAD`

# Force operations without checks
!`git reset --hard HEAD`

# Deleting branches automatically
!`git branch -D feature-branch`
```

### ✅ Do
```markdown
# Show status and suggest action
Status: !`git status`
To push: git push origin $(git branch --show-current)

# Warn before destructive operations
⚠️  This will reset uncommitted changes!
Command: git reset --hard HEAD
Execute manually if certain.

# List deletable branches
Merged branches safe to delete:
- feature-old-1
- bugfix-123
Delete with: git branch -d [branch-name]
```

## Related Templates

- `basic-command.md` - General command structure
- `code-generation.md` - For generating git hooks or scripts
- `analysis.md` - For analyzing git history and stats
