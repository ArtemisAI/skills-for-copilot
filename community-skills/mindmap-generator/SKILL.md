---
name: mindmap-generator
description: This skill should be used when converting text, files, URLs, or code repositories into structured Markdown mindmaps. It provides format validation, structure review, and scenario-specific templates for concept analysis, technical architecture, process flows, and knowledge systems.
license: Apache-2.0
---

# Mindmap Generator

Transform any input into structured Markdown mindmaps with automated validation and quality review.

## When to Use This Skill

Use this skill when:
- Converting text descriptions into mindmaps
- Transforming documentation or articles into structured outlines
- Analyzing code repositories and creating architecture mindmaps
- Building knowledge maps from learning materials
- Organizing complex information hierarchically

## Workflow

### Step 1: Analyze Input

Extract and analyze content based on input type:

**Input Types**:
- Text description: Parse content directly
- File path: Read file content using Read tool
- URL: Fetch webpage content using SearXNG MCP
- Code repository: Analyze directory structure and code organization

For detailed analysis strategies, reference @references/guides/content-analysis.md

### Step 2: Identify Scenario

Determine the appropriate mindmap structure based on content characteristics:

| Scenario | Triggers | Template |
|----------|----------|----------|
| Concept Analysis | Concepts, theories, principles | @assets/templates/concept-analysis.md |
| Technical Architecture | Systems, frameworks, architecture | @assets/templates/technical-architecture.md |
| Process Flow | Workflows, procedures, steps | @assets/templates/process-flow.md |
| Knowledge System | Learning paths, knowledge domains | @assets/templates/knowledge-system.md |

### Step 3: Structure Content

Organize content following mindmap conventions:

1. Extract core theme (H1 - root node)
2. Identify main branches (H2 - 3-7 recommended)
3. Expand details progressively (H3-H6)
4. Ensure logical coherence between levels

For detailed structuring strategies, reference @references/guides/content-structuring.md

Apply formatting rules from @references/specs/mindmap-format-rules.md

### Step 4: Validate Format

Run format validation to ensure compliance:

```bash
./scripts/validate-mindmap.sh <file-path>
```

**Validation Checks**:
- Heading hierarchy (# to ######)
- Level logic (no skipped levels)
- Content brevity (nodes not too long)
- Markdown syntax correctness
- UTF-8 encoding

**Results**:
- ❌ Errors: Must fix before proceeding
- ⚠️ Warnings: Recommended improvements
- ✅ Pass: Proceed to structure review

Reference @references/specs/validation-checklist.md for detailed error codes.

### Step 5: Review Structure

Run structure review to identify potential issues:

```bash
./scripts/review-mindmap.sh <file-path>
```

**Review Aspects**:
- Content scale (node count, depth)
- Structural balance (leaf ratio, branch distribution)
- Single-child nodes (recommend merging)
- Sibling count (avoid overcrowding)
- Empty nodes (ensure completeness)

**Output Types**:
- 🔴 Issues: Structural problems requiring fixes
- 🟡 Suggestions: Improvement opportunities
- 🟢 Strengths: Well-structured aspects

### Step 6: Save Output

Save generated mindmap to current working directory:

**Output Location**: `./mindmap/`
- Auto-create directory if not exists
- Example: `/Users/Apple/projects/foo/mindmap/`

**File Naming**: `topic-type-date.md`
- Example: `react-hooks-concept-20251107.md`
- Auto-sanitize special characters

**Output Format**: Standard Markdown compatible with any Markdown viewer

## Mindmap Format Conventions

### Heading Levels

```markdown
# Level 1 - Core Theme (root node, unique)
## Level 2 - Main Branches (3-7 recommended)
### Level 3 - Sub-branches
#### Level 4 - Details
##### Level 5 - Fine details
###### Level 6 - Maximum depth (avoid excessive use)
```

### Content Standards

1. **Brevity**: Keep each node to 1-2 lines
2. **Logic**: Siblings are parallel, parent-child are progressive
3. **Completeness**: Cover core dimensions of the topic
4. **Clarity**: Use clear expressions, avoid ambiguity

### Common Structure Patterns

**Concept Analysis**:
```
# Concept Name
## Executive Summary
### Core Findings
### Key Value
## Core Concept Explanation
### Definition
### Key Characteristics
## Detailed Exploration
### Use Cases
### Implementation
```

**Technical Architecture**:
```
# System Name
## Architecture Overview
### Overall Design
### Core Components
## Technology Stack
### Frontend Technologies
### Backend Technologies
## Implementation Details
### Key Modules
### Data Flow
```

For complete formatting rules, reference @references/specs/mindmap-format-rules.md

## Template Library

- Concept Analysis: @assets/templates/concept-analysis.md
- Technical Architecture: @assets/templates/technical-architecture.md
- Process Flow: @assets/templates/process-flow.md
- Knowledge System: @assets/templates/knowledge-system.md

## Quality Standards

Generated mindmaps must meet:

1. **Format Compliance**: Follow @references/specs/mindmap-format-rules.md
2. **Content Completeness**: Cover core aspects of the topic
3. **Logical Clarity**: Reasonable structure, clear hierarchy
4. **Concise Expression**: Brief and clear node content

## Tool Scripts

### Format Validation

```bash
./scripts/validate-mindmap.sh <file-path>
```

Check mindmap format compliance. Options: `-v` (verbose), `-s` (strict), `--no-color`.

### Structure Review

```bash
./scripts/review-mindmap.sh <file-path>
```

Review mindmap structure and logic. Options: `-v` (verbose), `-s` (summary), `-j` (JSON output).

## Best Practices

### Content Organization

1. **Top-down**: From whole to details
2. **Clear Layers**: Each level max 7 nodes (cognitive limit)
3. **Parallel Clarity**: Sibling relationships explicit
4. **Progressive Logic**: Parent-child logical progression

### Expression Standards

1. **Use Noun Phrases**: Prefer nouns for node titles
2. **Avoid Redundancy**: Don't repeat parent information
3. **Consistency**: Uniform style among siblings
4. **Specificity**: Avoid overly abstract expressions

### Common Issues

**Issue 1: Excessive Depth**
- Cause: Over-segmentation
- Solution: Merge similar nodes, limit to 4-5 levels

**Issue 2: Overly Long Nodes**
- Cause: Too much detail
- Solution: Extract keywords, move details to documentation

**Issue 3: Logical Confusion**
- Cause: Inconsistent classification criteria
- Solution: Re-examine dimensions, unify standards

## Resource References

### Format Specifications

- Core Rules: @references/specs/mindmap-format-rules.md
- Validation Checklist: @references/specs/validation-checklist.md

### Usage Guides

- Content Analysis: @references/guides/content-analysis.md
- Structuring Strategy: @references/guides/content-structuring.md

### Template Library

- Concept Analysis: @assets/templates/concept-analysis.md
- Technical Architecture: @assets/templates/technical-architecture.md
- Process Flow: @assets/templates/process-flow.md
- Knowledge System: @assets/templates/knowledge-system.md

## Technical Implementation

### Scripts

All scripts written in Bash, compatible with macOS and Linux.

**Dependencies**: Standard Unix tools only (grep, awk, sed)

**No external dependencies required**

### Extension Development

To add new validation rules or templates:

1. Reference existing scripts and templates
2. Follow project coding conventions
3. Add corresponding test cases
4. Update documentation

## Version History

- 1.0 (2025-11-07) Initial release
  - Core mindmap generation
  - Format validation script
  - Structure review script
  - 4 scenario templates
