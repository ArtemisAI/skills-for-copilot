---
name: technical-docs
description: Create technical documentation in markdown including READMEs, API docs, changelogs, and technical specifications. Uses proper syntax, code blocks with language tags, and standard conventions. Claude should use this skill when creating or maintaining technical documentation in markdown format.
---

## When to use this skill

Use this skill for README files, API documentation, technical specifications, changelogs (Keep a Changelog format), architecture documentation, and configuration guides.

## How to use this skill

1. **Identify the document type** from the request
2. **Load the appropriate template** from `references/templates.md`
3. **Apply markdown conventions** - Language tags, proper hierarchy, tables
4. **Validate structure** against quality checklist

## Key markdown conventions

**Code blocks with language tags**:
````markdown
```python
def example():
    return "code"
```
````

**Header hierarchy**: H1 (one per doc), H2 (major sections), H3 (subsections)

**Tables**: Use proper alignment for structured data

## Document templates

See [references/templates.md](references/templates.md) for detailed templates:
- README structure
- Changelog format (Keep a Changelog)
- API documentation
- Technical specifications

## Quality checklist

- Valid markdown syntax
- Language tags on all code blocks
- Logical header hierarchy (no skipped levels)
- Working, runnable code examples
- Consistent formatting throughout
- One H1 per document

## Best practices

1. One H1 as document title only
2. Use tables for structured data
3. Relative links for internal docs
4. Blank lines around code blocks
5. Descriptive link text (not "click here")

## Keywords

technical documentation, markdown docs, README, API documentation, changelog, technical spec, code documentation, developer docs
