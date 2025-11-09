# Command Review Checklist

This reference document provides comprehensive guidelines for reviewing Claude Code slash commands to ensure quality, consistency, and effectiveness.

## Quick Quality Checklist

Use this checklist when reviewing any command file:

- [ ] **Frontmatter is present and valid**
- [ ] **Description is clear and concise**
- [ ] **Argument hint is helpful (if arguments are used)**
- [ ] **Tools are appropriately restricted**
- [ ] **Model uses correct 4.5/4.1 version (NOT 3.5 or aliases)**
- [ ] **Model selection is appropriate for task complexity**
- [ ] **Command prompt is clear and well-structured**
- [ ] **$ARGUMENTS placeholder is used correctly (if needed)**
- [ ] **Bash commands use valid bash syntax (not Node.js)**
- [ ] **File references use @ syntax correctly**
- [ ] **No TypeScript/JavaScript code in markdown body**
- [ ] **Language is consistent (not mixed)**
- [ ] **Filename has no typos**
- [ ] **Command has a single, clear purpose**

## Frontmatter Validation

### Required Fields

While all frontmatter fields are technically optional, best practices recommend:

#### `description` (Highly Recommended)
```yaml
---
description: Create a git commit with proper formatting
---
```

**Quality Criteria:**
- ✅ Clear, concise (under 60 characters)
- ✅ Action-oriented (starts with verb)
- ✅ Describes the outcome, not the process
- ❌ Too vague ("Do stuff")
- ❌ Too long (multiple sentences)

**Examples:**
```yaml
# Good
description: Analyze code performance and suggest optimizations
description: Generate React component with tests
description: Create database migration with rollback

# Bad
description: Does things
description: This command will help you analyze your code and find performance issues and then suggest optimizations that you can apply
```

### Optional But Important Fields

#### `argument-hint`
```yaml
---
argument-hint: [component-name] [directory]
---
```

**Quality Criteria:**
- ✅ Uses square brackets for required args
- ✅ Uses pipes for alternatives: `add [id] | remove [id] | list`
- ✅ Clear parameter names
- ❌ Vague: `[options]`
- ❌ No description when arguments are needed

**Examples:**
```yaml
# Good
argument-hint: [issue-number]
argument-hint: [component-name] [directory]
argument-hint: add [tagId] | remove [tagId] | list

# Bad
argument-hint: [stuff]
argument-hint: [args]
# Missing when $ARGUMENTS is used in prompt
```

#### `allowed-tools`
```yaml
---
allowed-tools: Read, Edit, Bash(git:*)
---
```

**Quality Criteria:**
- ✅ Minimal necessary tools (principle of least privilege)
- ✅ Specific bash commands when possible: `Bash(git add:*)`
- ✅ Appropriate for task complexity
- ❌ Too permissive: All tools when only Read needed
- ❌ Too restrictive: Missing essential tools

**Common Combinations:**
```yaml
# Code analysis only
allowed-tools: Read, Grep, Glob

# File editing
allowed-tools: Read, Edit

# File creation
allowed-tools: Read, Write

# Git operations
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)

# Web research
allowed-tools: Read, WebSearch, WebFetch

# Full workflow
allowed-tools: Read, Edit, Write, Bash
```

#### `model`
```yaml
---
model: claude-sonnet-4-5-20250929
---
```

**Quality Criteria:**
- ✅ Haiku for simple, fast tasks
- ✅ Sonnet for balanced tasks (default)
- ✅ Opus for complex reasoning/analysis
- ❌ Opus for simple tasks (unnecessary cost)
- ❌ Haiku for complex tasks (insufficient capability)

**Selection Guide:**
```yaml
# Simple tasks: file operations, formatting, quick analysis
model: claude-haiku-4-5-20251001

# Balanced tasks: code generation, reviews, refactoring (default)
model: claude-sonnet-4-5-20250929

# Complex tasks: architecture decisions, complex debugging
model: claude-opus-4-1-20250805
```

**CRITICAL ANTI-PATTERN:**

❌ **WRONG - Using Old/Deprecated Models:**
```yaml
# These are OUTDATED and INCORRECT
model: claude-3-5-sonnet-20241022    # ❌ OLD - DO NOT USE
model: claude-3-5-haiku-20241022     # ❌ OLD - DO NOT USE
model: claude-3-opus-20240229        # ❌ OLD - DO NOT USE
model: sonnet                        # ❌ WRONG FORMAT for commands
model: haiku                         # ❌ WRONG FORMAT for commands
model: opus                          # ❌ WRONG FORMAT for commands
```

✅ **CORRECT - Use Full Dated Versions (4.5/4.1):**
```yaml
# Current models with full version strings
model: claude-sonnet-4-5-20250929    # ✅ CORRECT
model: claude-haiku-4-5-20251001     # ✅ CORRECT
model: claude-opus-4-1-20250805      # ✅ CORRECT
```

**Important Notes:**
- **Commands**: MUST use full dated versions (e.g., `claude-sonnet-4-5-20250929`)
- **Agents**: Use simple aliases (e.g., `sonnet`, `haiku`, `opus`) in `.claude/agents/*.md` files
- **Version format matters**: Commands fail with wrong model format
- **Always use 4.5/4.1 series**: Never use 3.5 or older models

## Command Prompt Quality

### Structure Template

Well-structured commands follow this pattern:

```markdown
---
description: Brief command description
argument-hint: [args if needed]
allowed-tools: Tool1, Tool2
---

## Context Section
[Gather current state, file contents, bash output]

- Current state: !`bash command`
- Relevant files: @path/to/file
- Configuration: @config/file

## Requirements Section
[Clear, numbered requirements]

1. Specific requirement one
2. Specific requirement two
3. Specific requirement three

## Deliverables Section
[Expected outputs]

- Output format
- Quality criteria
- Success criteria
```

### Common Issues

#### ❌ Issue: No structure
```markdown
Fix the code and make it better. Use $ARGUMENTS.
```

#### ✅ Solution: Clear structure
```markdown
---
description: Refactor code following SOLID principles
argument-hint: [file-path]
allowed-tools: Read, Edit
---

## Target File
@$ARGUMENTS

## Requirements
1. Apply Single Responsibility Principle
2. Improve naming conventions
3. Add JSDoc comments
4. Ensure type safety

## Quality Criteria
- Code is more readable
- Functions have single purpose
- No code duplication
```

## Bash Command Validation

### Valid Bash Syntax

Commands can execute bash before running the prompt:

```markdown
Current branch: !`git branch --show-current`
File count: !`find . -name "*.js" | wc -l`
Status: !`git status --porcelain`
```

### Common Errors

#### ❌ Issue: Node.js/JavaScript syntax
```markdown
# WRONG - This won't work in Claude Code
Files: !`${fs.readFileSync('file.txt')}`
Config: !`const x = require('./config')`
Data: !`${process.env.NODE_ENV}`
```

#### ✅ Solution: Use bash commands
```markdown
# CORRECT - Use bash
Files: !`cat file.txt`
Config: !`cat config.js`
Data: !`echo $NODE_ENV`
```

#### ❌ Issue: Complex multi-line commands
```markdown
# Hard to read and maintain
Result: !`for f in $(find . -name "*.js"); do echo $f; cat $f; done`
```

#### ✅ Solution: Break into separate commands or simplify
```markdown
# Clearer intent
JavaScript files: !`find . -name "*.js"`
Line count: !`find . -name "*.js" -exec wc -l {} +`
```

## $ARGUMENTS Usage

### Correct Usage

```markdown
---
argument-hint: [component-name]
---

Generate React component: $ARGUMENTS

Component specifications:
- Name: $ARGUMENTS
- Location: src/components/$ARGUMENTS
```

### Common Issues

#### ❌ Issue: Missing argument-hint
```markdown
---
description: Create component
# Missing: argument-hint
---

Create component named $ARGUMENTS
```

#### ✅ Solution: Add argument-hint
```markdown
---
description: Create React component
argument-hint: [component-name]
---

Create component named $ARGUMENTS
```

#### ❌ Issue: Arguments not in frontmatter
```markdown
# Frontmatter missing completely
Please fix issue #$ARGUMENTS
```

#### ✅ Solution: Add proper frontmatter
```markdown
---
description: Fix GitHub issue
argument-hint: [issue-number]
allowed-tools: Read, Edit, Bash(gh:*)
---

Please fix issue #$ARGUMENTS
```

## File Reference Validation

### Correct Syntax

```markdown
Main component: @src/components/Button.tsx
Tests: @src/components/Button.test.tsx
Styles: @src/components/Button.module.css
```

### Common Issues

#### ❌ Issue: Incorrect syntax
```markdown
# Wrong - missing @
File: src/components/Button.tsx

# Wrong - using quotes
File: "@src/components/Button.tsx"
```

#### ✅ Solution: Use @ prefix without quotes
```markdown
File: @src/components/Button.tsx
```

## Language Consistency

### Issue: Mixed Languages

Commands should be in ONE language consistently.

#### ❌ Issue: Mixed Portuguese and English
```markdown
---
description: Criar o PRD completo
---

Create a complete PRD following best practices...

## Contexto e Visão
Explain the product context...
```

#### ✅ Solution: One language
```markdown
---
description: Create complete PRD document
---

Create a complete PRD following best practices...

## Context and Vision
Explain the product context...
```

## TypeScript/Code in Markdown

### Issue: Literal Code Structures

Commands should contain prompts, not executable code.

#### ❌ Issue: TypeScript interfaces as if they'll execute
```markdown
interface EvaluationReport {
  metadata: {
    timestamp: string;
    version: string;
  }
}
```

#### ✅ Solution: Use as examples in code blocks
```markdown
The evaluation report should follow this structure:

\`\`\`typescript
interface EvaluationReport {
  metadata: {
    timestamp: string;
    version: string;
  }
}
\`\`\`

Generate an evaluation report following the above structure.
```

## Command Naming

### Best Practices

#### ✅ Good Names
- `review-command.md` → `/review-command`
- `create-component.md` → `/create-component`
- `analyze-performance.md` → `/analyze-performance`

#### ❌ Bad Names
- `propose-sulution.md` → typo
- `ReviewCommand.md` → avoid CamelCase
- `review_command.md` → prefer kebab-case
- `rev-cmd.md` → too abbreviated

## Single Responsibility

Each command should have ONE clear purpose.

### ❌ Issue: Multiple purposes
```markdown
---
description: Create component, tests, and deploy
---

Create a React component, write tests, update documentation,
and deploy to staging...
```

### ✅ Solution: Split into focused commands
```markdown
# create-component.md
---
description: Create React component with basic structure
---

# test-component.md
---
description: Generate tests for React component
---

# deploy-staging.md
---
description: Deploy application to staging environment
---
```

## Testing Recommendations

Before promoting a command from review to active:

1. **Test with real arguments**: Invoke with typical use cases
2. **Test edge cases**: Empty args, invalid args, missing files
3. **Verify bash commands**: Ensure they execute successfully
4. **Check file references**: Confirm paths resolve correctly
5. **Validate output**: Ensure Claude responds appropriately
6. **Test tool restrictions**: Verify only allowed tools are used

## Review Process

### Individual Command Review

1. **Read the command file completely**
2. **Check frontmatter against checklist**
3. **Analyze prompt structure and clarity**
4. **Validate bash commands (if any)**
5. **Check $ARGUMENTS usage (if any)**
6. **Verify file references (if any)**
7. **Test the command with sample inputs**
8. **Document issues found**
9. **Propose fixes or improvements**

### Bulk Review Process

1. **Identify all commands needing review**
2. **Categorize by issue severity:**
   - Critical: Won't work at all
   - High: Works but has major issues
   - Medium: Works but needs improvements
   - Low: Minor polish needed
3. **Prioritize fixes**: Critical → High → Medium → Low
4. **Create fix plan for each command**
5. **Track progress on fixes**

## Common Improvement Patterns

### From Basic to Best Practice

#### Before: Minimal command
```markdown
Create a React component for $ARGUMENTS
```

#### After: Well-structured command
```markdown
---
description: Generate React component with TypeScript and tests
argument-hint: [component-name] [directory]
allowed-tools: Read, Write, Edit, Bash
model: claude-sonnet-4-5-20250929
---

## Component Generation

**Component Name**: $ARGUMENTS (first argument)
**Target Directory**: $ARGUMENTS (second argument, default: src/components)

## Project Context

Existing patterns: @src/components/
TypeScript config: @tsconfig.json
Test setup: @jest.config.js

## Requirements

1. **Component Structure**
   - TypeScript functional component
   - Props interface with JSDoc
   - Default export

2. **Testing**
   - Jest + React Testing Library
   - Test rendering and props
   - Accessibility tests

3. **Documentation**
   - JSDoc comments
   - Usage examples

## File Structure to Create

\`\`\`
[directory]/
├── ComponentName.tsx
├── ComponentName.test.tsx
└── index.ts
\`\`\`
```

## Summary

A high-quality Claude Code command has:

1. ✅ **Clear frontmatter** with description, argument hints, and tool restrictions
2. ✅ **Correct model version** (claude-sonnet-4-5-20250929, NOT 3.5 or aliases)
3. ✅ **Well-structured prompt** with context, requirements, and deliverables
4. ✅ **Valid bash syntax** for any command execution
5. ✅ **Correct $ARGUMENTS usage** with proper hints
6. ✅ **Proper file references** using @ syntax
7. ✅ **Single, focused purpose** that solves one problem well
8. ✅ **Language consistency** throughout
9. ✅ **No executable code** in markdown (only prompts and examples)
10. ✅ **Appropriate tool restrictions** for security and clarity
11. ✅ **Tested and validated** with real use cases

Use this checklist when creating new commands or reviewing existing ones to ensure consistent, high-quality command automation in Claude Code.
