# Code Review Command Example

Automated code review command that analyzes code quality, security, and best practices.

## File: `.claude/commands/review.md`

```markdown
---
allowed-tools: Read, Grep, Glob, Bash(git diff:*)
argument-hint: [file-path-or-pattern]
description: Perform comprehensive code review with security and quality analysis
model: claude-3-5-sonnet-20241022
---

## Code Review Analysis

**Target**: $ARGUMENTS (default: all staged files)

## Current Context

- Branch: !`git branch --show-current`
- Staged files: !`git diff --cached --name-only`
- Changed files: !`git diff --name-only`
- File stats: !`git diff --stat`

## Review Checklist

### 1. Code Quality
- [ ] Code follows team standards: @.eslintrc.json @.prettierrc
- [ ] No code smells or anti-patterns
- [ ] Proper error handling
- [ ] Appropriate comments and documentation
- [ ] No dead code or unused imports
- [ ] DRY principle followed

### 2. Security Analysis
- [ ] No hardcoded secrets or credentials
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection where needed
- [ ] Dependency vulnerabilities: !`npm audit` or !`pip-audit`

### 3. Performance Considerations
- [ ] No obvious performance bottlenecks
- [ ] Efficient algorithms and data structures
- [ ] Proper async/await usage
- [ ] Memory leak prevention
- [ ] Database query optimization

### 4. Testing
- [ ] Unit tests present and passing
- [ ] Test coverage adequate
- [ ] Edge cases covered
- [ ] Mock usage appropriate

### 5. Architecture & Design
- [ ] Follows SOLID principles
- [ ] Proper separation of concerns
- [ ] Appropriate design patterns
- [ ] Module dependencies reasonable
- [ ] API design consistent

### 6. Documentation
- [ ] JSDoc/docstrings present
- [ ] README updated if needed
- [ ] API documentation current
- [ ] Changelog updated

## Analysis Format

For each file reviewed, provide:

1. **Summary**: Brief overview of changes
2. **Strengths**: What's done well
3. **Issues**: Problems found (categorized by severity)
   - 🔴 Critical: Must fix before merge
   - 🟡 Warning: Should fix before merge
   - 🔵 Suggestion: Consider for improvement
4. **Recommendations**: Specific actionable improvements
5. **Risk Assessment**: Low/Medium/High risk rating

## Example Output Format

```markdown
### File: src/auth/login.ts

**Summary**: Implements JWT authentication with refresh tokens

**Strengths**:
- Well-structured token validation
- Proper error handling for expired tokens
- Clean separation of concerns

**Issues**:
🔴 Critical:
- Line 45: Hardcoded secret key should use environment variable
- Line 78: SQL query vulnerable to injection

🟡 Warning:
- Line 23: Missing input validation for email format
- Line 56: Consider rate limiting for login attempts

🔵 Suggestion:
- Line 34: Could extract token refresh logic to separate function
- Line 67: Add more descriptive error messages

**Recommendations**:
1. Move secret to environment variable immediately
2. Use parameterized queries or ORM for database access
3. Add input validation using validation library (joi, zod)
4. Implement rate limiting middleware

**Risk Assessment**: High (due to security vulnerabilities)
```

## Additional Analysis

After reviewing all files, provide:
- Overall quality score (1-10)
- Summary of critical issues
- Priority order for fixes
- Estimated time to address issues
- Long-term technical debt considerations
```

## Usage Examples

```bash
# Review all staged files
/review

# Review specific file
/review src/auth/login.ts

# Review all files in directory
/review src/components/

# Review files matching pattern
/review "*.test.ts"
```

## Key Features

1. **Comprehensive Analysis**: Covers quality, security, performance, and architecture
2. **Actionable Feedback**: Specific line numbers and recommendations
3. **Risk Assessment**: Prioritizes issues by severity
4. **Context-Aware**: Uses git status and project configuration
5. **Security Focus**: Includes vulnerability scanning

## Customization Options

Add to the command:
- Specific framework best practices (React, Vue, Angular)
- Language-specific linting rules
- Team-specific coding standards
- Integration with external tools (SonarQube, CodeClimate)
- Automated fix suggestions

## Integration Ideas

Combine with:
- Git hooks for pre-commit reviews
- CI/CD pipeline integration
- Pull request templates
- Issue tracking systems
- Code quality dashboards

## Best Practices

- Run before committing code
- Address critical issues immediately
- Create tickets for non-urgent issues
- Review the review (validate suggestions)
- Use in combination with automated linting
- Share review results with team
