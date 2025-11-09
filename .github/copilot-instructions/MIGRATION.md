# Migration Guide: Claude Code Skills to GitHub Copilot Instructions

## Overview

This guide explains how to migrate from Claude Code Skills to GitHub Copilot Instructions in VS Code. While both systems share the same core philosophy - extending AI capabilities with specialized knowledge - they differ in format, activation, and usage patterns.

## Key Differences

| Aspect | Claude Code Skills | GitHub Copilot Instructions |
|--------|-------------------|----------------------------|
| **File Format** | SKILL.md with YAML frontmatter | Standard Markdown (.md) |
| **Activation** | Manual skill mention/trigger | Automatic workspace context |
| **Discovery** | Plugin marketplace | Git repository (automatic) |
| **Structure** | One folder per skill | Organized by category |
| **Distribution** | ZIP files via marketplace | Git clone/fork |
| **Resources** | Bundled in skill folder | Referenced in workspace |
| **Tools** | Claude-specific tool calls | VS Code API + @terminal |
| **Loading** | 3-level progressive disclosure | All loaded as workspace context |

## Architecture Comparison

### Claude Code Skills

```
skill-name/
├── SKILL.md                    # Required entrypoint
│   ├── --- (YAML frontmatter)
│   │   ├── name: skill-name
│   │   ├── description: ...
│   │   └── license: ...
│   └── (Markdown body)
├── scripts/                    # Optional executables
├── references/                 # Optional documentation
└── assets/                     # Optional templates

Distribution: ZIP file via marketplace
Activation: User mentions skill or automatic based on description
Loading: Progressive (metadata → SKILL.md → resources)
```

### GitHub Copilot Instructions

```
.github/copilot-instructions/
├── README.md                   # System overview
├── 00-core-philosophy.md       # Core principles
└── [category]/
    └── skill-name.md           # Instruction file

workspace-root/skill-name/      # Supporting resources
├── SKILL.md                    # Original (for reference)
├── scripts/                    # Same scripts
├── references/                 # Same references
└── assets/                     # Same assets

Distribution: Git repository
Activation: Automatic when workspace is open
Loading: All instructions loaded as workspace context
```

## Migration Process

### Step 1: Understand the Mapping

**Claude Skill Component** → **Copilot Equivalent**

- **SKILL.md YAML frontmatter** → Section headers and descriptions in .md file
- **SKILL.md name field** → Markdown heading (# Skill Name)
- **SKILL.md description** → "Overview" and "When to Use" sections
- **SKILL.md body** → Instruction file content (organized into sections)
- **Bundled resources** → Remain in workspace, referenced by path
- **Tool calls** → @terminal commands or code examples
- **Marketplace distribution** → Git repository

### Step 2: Convert SKILL.md to Instruction File

**Original Claude Skill (SKILL.md):**
```markdown
---
name: pdf-processor
description: Process PDF files - extract text, merge, split, rotate pages
license: Apache 2.0
---

# PDF Processor

This skill helps with PDF manipulation tasks.

## Common Operations

To extract text from a PDF:
[instructions]

To merge PDFs:
[instructions]
```

**Converted Copilot Instruction:**
```markdown
# PDF Processing

## Overview

Process PDF files - extract text, merge, split, rotate pages. Use when
working with PDF documents programmatically.

## When to Use

- Extracting text or tables from PDFs
- Merging multiple PDF files
- Splitting PDFs into separate pages
- Rotating PDF pages

## Workflows

### Workflow 1: Extract Text

[instructions]

### Workflow 2: Merge PDFs

[instructions]

## Resources

### Workspace References
- `pdf-processor/SKILL.md` - Original skill documentation
- `pdf-processor/scripts/` - Utility scripts
- `pdf-processor/references/` - Detailed guides

## Examples

[concrete examples]
```

### Step 3: Organize by Category

Choose appropriate category for each skill:

**Document Skills** (`.github/copilot-instructions/document-skills/`)
- PDF processing
- Word documents (docx)
- Excel spreadsheets (xlsx)
- PowerPoint presentations (pptx)

**Development Skills** (`.github/copilot-instructions/development-skills/`)
- MCP server building
- Web app testing
- Artifact building

**Creative Skills** (`.github/copilot-instructions/creative-skills/`)
- Algorithmic art
- Canvas design
- Theme creation

**Communication Skills** (`.github/copilot-instructions/communication-skills/`)
- Internal communications
- Brand guidelines

**Meta Skills** (`.github/copilot-instructions/meta-skills/`)
- Skill creation
- Instruction writing

### Step 4: Structure Instruction Files

Use this template for consistency:

```markdown
# [Skill Name]

## Overview
[Brief description - 2-3 sentences]

## When to Use
[Bullet list of specific use cases]

## Core Concepts (optional)
[Key principles or philosophy]

## Workflows

### Workflow 1: [Primary Task]
[Step-by-step instructions]

### Workflow 2: [Secondary Task]
[Step-by-step instructions]

## Examples

### Example 1: [Scenario]
[Complete code example with explanation]

### Example 2: [Scenario]
[Complete code example with explanation]

## Resources

### Workspace References
- `skill-name/SKILL.md` - Original documentation
- `skill-name/scripts/script.py` - [Description]
- `skill-name/references/guide.md` - [Description]

### External Resources
- [Links to relevant documentation]

## Guidelines
[Best practices and principles]

## Common Patterns
[Reusable code patterns]

## Troubleshooting
[Common issues and solutions]

## Next Steps
[What to explore after mastering basics]

## Additional Context
[Reference to original skill for complete details]
```

### Step 5: Adapt Tool Calls

**Claude Tool Calls** → **Copilot Equivalents**

```markdown
<!-- Claude: Tool call -->
Use the read_file tool to access config.json

<!-- Copilot: File reference -->
Read `config.json` from workspace
or
@workspace read config.json
```

```markdown
<!-- Claude: Execute script -->
Run the processing script using bash tool

<!-- Copilot: Terminal execution -->
Run via @terminal:
`python skill-name/scripts/process.py input.txt`
```

```markdown
<!-- Claude: Web search -->
Use web_search to find API documentation

<!-- Copilot: Instruction to user -->
Use web search or fetch API documentation from:
https://api-docs-url.com
```

### Step 6: Update Resource References

**Original (Claude):**
```markdown
See the reference documentation in this skill's references/ folder.
Run the script located in scripts/process.py.
```

**Converted (Copilot):**
```markdown
## Resources

**Detailed Documentation:**
- `skill-name/references/api-guide.md` - Complete API reference

**Scripts:**
- `skill-name/scripts/process.py` - Data processing utility
  ```bash
  @terminal python skill-name/scripts/process.py input.txt
  ```
```

### Step 7: Preserve Original Skills

Keep original skill folders in workspace root for:
- Reference and complete documentation
- Scripts and executables
- Detailed references
- Assets and templates

```
workspace-root/
├── .github/copilot-instructions/   # New Copilot instructions
├── skill-name/                     # Original skill (preserved)
│   ├── SKILL.md                    # Original documentation
│   ├── scripts/                    # Working scripts
│   ├── references/                 # Detailed docs
│   └── assets/                     # Templates
```

## Usage Pattern Changes

### Claude Code Usage

```
# In Claude Code chat
Use the pdf skill to extract text from document.pdf

# Claude automatically:
1. Loads pdf skill SKILL.md
2. Reads relevant sections
3. May load references if needed
4. Executes with Claude-specific tools
```

### GitHub Copilot Usage

```
# In VS Code Copilot Chat
@workspace extract text from document.pdf using pdf processing

# Copilot automatically:
1. Has all instructions loaded as workspace context
2. Finds relevant pdf-processing.md instruction
3. Generates code based on instructions
4. Can reference scripts via @terminal
```

## Progressive Disclosure Adaptation

### Claude's 3-Level Loading

1. **Level 1: Metadata** (~100 words) - Always loaded
2. **Level 2: SKILL.md body** (<5k words) - Loaded when triggered
3. **Level 3: Resources** (unlimited) - Loaded as needed

### Copilot's Context Model

1. **All instructions loaded** - Entire `.github/copilot-instructions/` directory
2. **Semantic search** - Copilot finds relevant sections based on query
3. **Referenced resources** - Loaded on demand when mentioned

**Implication:** Keep Copilot instruction files concise (<5k words core content), with references to detailed documentation.

## Feature Equivalents

### Claude Features → Copilot Equivalents

**Skill Marketplace:**
- Claude: Plugin marketplace, install via commands
- Copilot: Git clone repository, automatic workspace loading

**Tool Calls:**
- Claude: `use_tool("bash", command="...")`
- Copilot: `@terminal command` or code generation

**Web Access:**
- Claude: `web_search()`, `fetch_url()`
- Copilot: Instructions to user to fetch/search, or use extensions

**File Access:**
- Claude: Built-in file tools
- Copilot: VS Code file system access, `@workspace` participant

**Allowed Tools:**
- Claude: `allowed-tools` in YAML
- Copilot: Handled by VS Code permissions

## Best Practices for Migration

### DO:

1. **Preserve all original skills** - Keep for reference and scripts
2. **Organize by domain** - Use category directories
3. **Keep instructions concise** - <5k words core content
4. **Reference original skills** - Link to complete documentation
5. **Test with Copilot** - Verify instructions work as expected
6. **Use clear sections** - Help semantic search find content
7. **Provide examples** - Concrete code examples are valuable
8. **Update paths** - Use workspace-relative paths

### DON'T:

1. **Delete original skills** - They contain scripts and detailed docs
2. **Copy everything verbatim** - Adapt for Copilot's context model
3. **Use Claude-specific syntax** - Convert tool calls to Copilot patterns
4. **Assume Claude features** - No direct web access, different tools
5. **Make instructions too long** - All are loaded, keep concise
6. **Forget to test** - Always verify with actual Copilot usage

## Example Migrations

### Example 1: Simple Skill

**Original (Claude):**
```markdown
---
name: code-formatter
description: Format code according to style guidelines
---

# Code Formatter

Format code using standard formatters.

Use black for Python:
`black file.py`

Use prettier for JavaScript:
`prettier --write file.js`
```

**Migrated (Copilot):**
```markdown
# Code Formatting

## Overview
Format code according to language-specific style guidelines.

## When to Use
- Formatting Python code with black
- Formatting JavaScript/TypeScript with prettier
- Applying consistent code style

## Workflows

### Workflow 1: Format Python
```bash
@terminal black file.py
# or for entire directory
@terminal black src/
```

### Workflow 2: Format JavaScript
```bash
@terminal prettier --write file.js
# or
@terminal prettier --write "src/**/*.{js,jsx,ts,tsx}"
```

## Resources
- `code-formatter/SKILL.md` - Original skill documentation
```

### Example 2: Complex Skill with Resources

**Original Structure:**
```
mcp-builder/
├── SKILL.md (4000 words + references to resources)
├── references/
│   ├── python_guide.md (3000 words)
│   ├── typescript_guide.md (3000 words)
│   └── best_practices.md (2000 words)
└── scripts/
    └── evaluate.py
```

**Migrated Structure:**
```
.github/copilot-instructions/development-skills/
└── mcp-builder.md (4000 words core + refs)

mcp-builder/ (preserved)
├── SKILL.md (complete original)
├── references/ (detailed guides)
└── scripts/ (working scripts)
```

**Key Adaptation:**
- Core workflow in mcp-builder.md (~4k words)
- References to detailed guides for specifics
- Scripts remain in original location
- Links to external MCP documentation

## Testing Your Migration

### Verification Checklist

- [ ] All instruction files in `.github/copilot-instructions/`
- [ ] Original skills preserved in workspace root
- [ ] Category organization makes sense
- [ ] Instruction files follow template structure
- [ ] Resource paths are correct (workspace-relative)
- [ ] No Claude-specific tool calls
- [ ] Examples use Copilot patterns (@workspace, @terminal)
- [ ] Tested with actual Copilot queries

### Test Queries

Try these with Copilot to verify:

```
@workspace what skills are available?
@workspace help me with PDF processing
@workspace use mcp-builder to create a server
@workspace show algorithmic art examples
@workspace list files in document-skills/pdf/scripts/
```

## Troubleshooting Migration

### Issue: Copilot not finding instructions
**Solution:** Check files are in `.github/copilot-instructions/`, valid markdown

### Issue: Instructions too long
**Solution:** Extract details to reference files, keep core <5k words

### Issue: Scripts not working
**Solution:** Verify paths, ensure scripts are in original skill folders

### Issue: Missing functionality
**Solution:** Reference original SKILL.md, may need VS Code extension

## Conclusion

Migration from Claude Code Skills to GitHub Copilot Instructions preserves the core philosophy while adapting to Copilot's different architecture:

- **Same knowledge** - Domain expertise and workflows maintained
- **Same resources** - Scripts, references, assets preserved
- **Different format** - Standard Markdown vs YAML frontmatter
- **Different activation** - Automatic vs manual triggering
- **Different tools** - VS Code API vs Claude tools

The result is a workspace that provides specialized AI assistance through GitHub Copilot, leveraging the same high-quality instruction sets developed for Claude Code.

## Additional Resources

- **Core Philosophy**: `.github/copilot-instructions/00-core-philosophy.md`
- **Creating Instructions**: `.github/copilot-instructions/meta-skills/skill-creator.md`
- **Example Instructions**: Browse `.github/copilot-instructions/` for patterns
- **Original Skills**: Workspace root folders for complete examples
