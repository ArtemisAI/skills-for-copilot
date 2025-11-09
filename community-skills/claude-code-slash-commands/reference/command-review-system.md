# Claude Code Command Review System

A comprehensive system for reviewing, validating, and improving Claude Code slash commands.

## Overview

This review system helps you maintain high-quality slash commands by providing:

1. **Review Reference Document**: Comprehensive quality checklist and best practices
2. **Bulk Analyzer** (`/review-commands`): Analyze all commands in a directory
3. **Individual Reviewer** (`/review-command`): Deep review of a single command

## System Components

### 1. Review Reference Document

**Location**: `.claude/skills/claude-code-slash-commands/reference/command-review-checklist.md`

**Purpose**: Defines quality standards for all commands including:
- Frontmatter validation criteria
- Prompt structure best practices
- Bash syntax validation
- Common issues and fixes
- Testing recommendations

**When to use**:
- Before creating new commands
- When manually reviewing commands
- As reference during command development

### 2. Bulk Command Analyzer

**Command**: `/review-commands [directory-path]`

**Purpose**: Analyze multiple commands at once and generate a comprehensive quality report.

**Default behavior**: Analyzes `.claude/commands/review/` if no path specified.

**Output**: Comprehensive report including:
- Executive summary with quality distribution
- Commands categorized by severity (Critical/High/Medium/Low/Ready)
- Common patterns across commands
- Prioritized action plan
- Quality metrics and statistics

### 3. Individual Command Reviewer

**Command**: `/review-command [command-file-path]`

**Purpose**: Perform detailed review of a single command with specific fixes.

**Output**: Detailed analysis including:
- Frontmatter validation
- Prompt structure analysis
- Syntax validation (bash, file references, $ARGUMENTS)
- Content quality assessment
- Specific recommended fixes
- Testing recommendations
- Deployment decision

## Workflow Guide

### Initial Setup (First Time)

1. **Familiarize yourself with quality standards**:
   ```bash
   # Read the review checklist
   open .claude/skills/claude-code-slash-commands/reference/command-review-checklist.md
   ```

2. **Identify commands needing review**:
   ```bash
   # List all commands in review directory
   find .claude/commands/review -name "*.md"
   ```

### Workflow 1: Bulk Review Process

**Use when**: You have many commands to review and need an overview.

#### Step 1: Run Bulk Analysis

```bash
# In Claude Code session
/review-commands .claude/commands/review
```

Or for a specific subdirectory:

```bash
/review-commands .claude/commands/review/code_quality
```

#### Step 2: Review the Report

The report will categorize all commands by severity:

- **🔴 Critical**: Won't work at all (fix immediately)
- **🟠 High Priority**: Works but has major problems
- **🟡 Medium Priority**: Works but needs improvements
- **🟢 Low Priority**: Minor polish needed
- **✅ Ready**: Can be deployed

#### Step 3: Create Action Plan

Based on the report, prioritize fixes:

1. Fix all **Critical** issues first
2. Address **High Priority** issues next
3. Batch **Medium Priority** improvements
4. Polish **Low Priority** items later

#### Step 4: Deploy Ready Commands

Move commands marked as "Ready" to active directory:

```bash
# Move ready command from review to active
mv .claude/commands/review/good-command.md .claude/commands/
```

### Workflow 2: Individual Command Review

**Use when**: You need detailed analysis and specific fixes for a command.

#### Step 1: Run Individual Review

```bash
# In Claude Code session
/review-command .claude/commands/review/problematic-command.md
```

#### Step 2: Analyze the Detailed Report

The report provides:
- Specific issue locations
- Exact fixes needed
- Testing recommendations
- Deployment decision

#### Step 3: Apply Fixes

The report may include exact file edits. If the command suggests using the Edit tool, you can:

1. Review the suggested changes
2. Ask Claude to apply the fixes directly
3. Verify the corrected version

#### Step 4: Re-Review (if needed)

For commands with major changes, run the review again:

```bash
/review-command .claude/commands/review/now-fixed-command.md
```

#### Step 5: Deploy or Iterate

- **If Ready**: Move to `.claude/commands/`
- **If Still Has Issues**: Apply more fixes and re-review

### Workflow 3: New Command Validation

**Use when**: You've just created a new command and want to validate it.

#### Step 1: Create Your Command

Place it in the review directory:

```bash
.claude/commands/review/new-feature.md
```

#### Step 2: Run Individual Review

```bash
/review-command .claude/commands/review/new-feature.md
```

#### Step 3: Fix Any Issues

Apply recommended fixes immediately.

#### Step 4: Test the Command

Use the testing recommendations from the review report:

```bash
# Example test
/new-feature test-argument
```

#### Step 5: Deploy

If review passes and tests work:

```bash
mv .claude/commands/review/new-feature.md .claude/commands/
```

## Example Workflows

### Example 1: Clean Up Review Backlog

**Scenario**: You have 40+ commands in review and need to prioritize.

```bash
# Step 1: Get overview
/review-commands .claude/commands/review

# Step 2: Note the report shows:
# - 5 Critical issues
# - 12 High priority
# - 18 Medium priority
# - 5 Low priority
# - 4 Ready to deploy

# Step 3: Deploy ready commands immediately
mv .claude/commands/review/ready-cmd-1.md .claude/commands/
mv .claude/commands/review/ready-cmd-2.md .claude/commands/
# ... etc

# Step 4: Fix critical issues one by one
/review-command .claude/commands/review/critical-cmd-1.md
# Apply fixes
/review-command .claude/commands/review/critical-cmd-2.md
# Apply fixes

# Step 5: Batch fix high priority issues
# Review similar issues together for efficiency
```

### Example 2: Fix a Specific Problematic Command

**Scenario**: You know one command isn't working correctly.

```bash
# Step 1: Deep review
/review-command .claude/commands/review/broken-command.md

# Step 2: Review shows critical issue:
# "Uses Node.js syntax instead of bash: ${fs.readFileSync('file.txt')}"

# Step 3: Ask Claude to fix it
# "Please fix the bash syntax issues identified in the review"

# Step 4: Verify the fix
/review-command .claude/commands/review/broken-command.md

# Step 5: If now ready, deploy
mv .claude/commands/review/broken-command.md .claude/commands/
```

### Example 3: Maintain Command Quality

**Scenario**: Periodic quality check of all active commands.

```bash
# Step 1: Review all active commands
/review-commands .claude/commands

# Step 2: Check quality metrics
# - Commands with frontmatter: 35/44 (80%)
# - Commands with descriptions: 38/44 (86%)
# - Commands ready to deploy: 40/44 (91%)

# Step 3: Identify and fix the 4 commands with issues
# Step 4: Re-run to confirm 100% quality
```

## Common Issues and Quick Fixes

### Issue: Command Missing Frontmatter

**Symptom**: `/review-command` shows "No frontmatter found"

**Quick Fix**:
```markdown
# Add at the top of the file:
---
description: Brief description of command
argument-hint: [args if needed]
allowed-tools: Read, Edit
---
```

### Issue: Invalid Bash Syntax

**Symptom**: Review shows "Uses Node.js/JavaScript instead of bash"

**Quick Fix**:
```markdown
# Wrong:
Files: !`${fs.readFileSync('file.txt')}`

# Right:
Files: !`cat file.txt`
```

### Issue: Missing Argument Hint

**Symptom**: "Uses $ARGUMENTS but no argument-hint provided"

**Quick Fix**:
```yaml
---
description: Your description
argument-hint: [component-name]  # Add this
---
```

### Issue: Mixed Languages

**Symptom**: "Language inconsistency detected (English/Portuguese)"

**Quick Fix**: Choose one language and be consistent throughout:
```markdown
# Pick one:
# Option 1: All English
description: Create complete PRD document

# Option 2: All Portuguese
description: Criar documento PRD completo
```

## Quality Standards Summary

A command is **ready for deployment** when it has:

1. ✅ Valid frontmatter with clear description
2. ✅ Argument hints (if using $ARGUMENTS)
3. ✅ Appropriate tool restrictions
4. ✅ Well-structured prompt (Context/Requirements/Deliverables)
5. ✅ Valid bash syntax (no Node.js code)
6. ✅ Correct file reference syntax
7. ✅ Single, focused purpose
8. ✅ Consistent language
9. ✅ No typos in filename
10. ✅ Tested with real scenarios

## Maintenance Schedule

### Daily
- Review any newly created commands individually
- Fix critical issues immediately

### Weekly
- Run bulk review on review directory
- Deploy ready commands
- Fix high priority issues

### Monthly
- Run bulk review on ALL commands (active + review)
- Update commands to match new best practices
- Archive or deprecate unused commands

## Integration with Development Workflow

### When Creating New Commands

```bash
# 1. Create command in review directory
# Write to: .claude/commands/review/new-command.md

# 2. Immediate validation
/review-command .claude/commands/review/new-command.md

# 3. Fix any issues

# 4. Test with real arguments
/new-command test-input

# 5. Deploy if successful
mv .claude/commands/review/new-command.md .claude/commands/
```

### When Updating Existing Commands

```bash
# 1. Make changes to active command

# 2. Quick validation
/review-command .claude/commands/updated-command.md

# 3. Fix any issues introduced

# 4. Test to ensure still works
/updated-command test-input
```

## Tips for Efficient Reviews

### 1. Batch Similar Issues

If bulk review shows 10 commands missing descriptions, fix them all at once:
```bash
# Group fix approach: Add descriptions to all commands without them
```

### 2. Use the Reference Document

Keep the checklist open while reviewing:
```bash
open .claude/skills/claude-code-slash-commands/reference/command-review-checklist.md
```

### 3. Test as You Fix

Don't wait until all fixes are done. Test each command as you fix it:
```bash
/review-command path/to/fixed.md
/fixed test-args
```

### 4. Prioritize by Impact

Focus on commands you use most frequently first:
- Daily use commands: Fix immediately
- Weekly use: Fix soon
- Rarely used: Fix when you have time

### 5. Learn from Patterns

If the bulk review shows the same issue in many commands, create a standard fix:
```bash
# Example: If many commands lack argument-hints
# Create a template for adding them consistently
```

## Troubleshooting

### Review Command Not Found

**Problem**: `/review-command` or `/review-commands` not recognized

**Solution**:
1. Verify files exist:
   ```bash
   ls -la .claude/commands/review-command*.md
   ```
2. Restart Claude Code session
3. Check filename matches exactly (with .md extension)

### Review Doesn't Reference Checklist

**Problem**: Review doesn't use quality standards

**Solution**:
1. Verify checklist exists:
   ```bash
   ls -la .claude/skills/claude-code-slash-commands/reference/command-review-checklist.md
   ```
2. Reference is automatic but re-read SKILL.md to refresh context

### False Positives in Review

**Problem**: Review flags valid code as issues

**Solution**:
- Review judgments are guidelines, not rules
- If a pattern works for your use case, document why in a comment
- Adjust the checklist reference document if needed

## Next Steps

1. **Start with bulk review**: Get the big picture
   ```bash
   /review-commands .claude/commands/review
   ```

2. **Fix critical issues first**: These prevent commands from working

3. **Deploy ready commands**: Move them out of review

4. **Schedule regular reviews**: Keep quality high over time

5. **Iterate on quality**: Use learnings to improve future commands

## Additional Resources

- **Command Creation Guide**: `docs/claude-code/command-guide.md`
- **Review Checklist**: `.claude/skills/claude-code-slash-commands/reference/command-review-checklist.md`
- **Skill Documentation**: `.claude/skills/claude-code-slash-commands/SKILL.md`
- **Command Examples**: `.claude/skills/claude-code-slash-commands/examples/`

## Support

For issues with the review system:
1. Check this documentation
2. Review the checklist reference
3. Test with a simple, known-good command first
4. Ask Claude Code for help: "Help me understand the command review system"

---

**Remember**: The goal is quality, not perfection. Start with critical issues and iterate toward excellence.
