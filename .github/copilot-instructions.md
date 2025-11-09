# GitHub Copilot Instructions for code-skills Repository

## Repository Overview

This repository contains specialized instruction sets and skills that extend AI capabilities with domain-specific knowledge. Originally designed for Claude Code, this repository has been adapted for GitHub Copilot in VS Code while preserving the original Claude skills for reference.

**Two Systems Included:**
1. **GitHub Copilot Instructions** - Adapted for VS Code (`.github/copilot-instructions/`)
2. **Claude Code Skills** - Original format for Claude (workspace root folders)

## GitHub Copilot Instructions

The `.github/copilot-instructions/` directory contains instruction sets optimized for GitHub Copilot in VS Code:

- **Core Philosophy** (`00-core-philosophy.md`) - Foundational principles for skill-based AI assistance
- **Document Skills** - PDF, Word, Excel, PowerPoint processing
- **Development Skills** - MCP server building, web app testing, artifact creation
- **Creative Skills** - Algorithmic art, canvas design, theme creation
- **Communication Skills** - Internal comms, brand guidelines
- **Meta Skills** - Creating new instruction sets

**See** `.github/copilot-instructions/README.md` for complete usage guide.

## Original Claude Code Skills

The workspace root contains original Claude skills for reference:

- **Example Skills**: Creative (algorithmic-art, canvas-design, slack-gif-creator), Development (artifacts-builder, mcp-builder, webapp-testing), Enterprise (brand-guidelines, internal-comms, theme-factory), and Meta skills (skill-creator, template-skill)
- **Document Skills** (`document-skills/`): Advanced skills for binary file formats (docx, pdf, pptx, xlsx) - source-available reference examples
- **Agent Skills Spec** (`agent_skills_spec.md`): Original specification for Claude skills
- **Template Skill** (`template-skill/`): Basic starting point for new skills

## How to Use in VS Code with GitHub Copilot

### Quick Start

1. **Open this workspace in VS Code** with GitHub Copilot enabled
2. **Instructions load automatically** from `.github/copilot-instructions/`
3. **Use @workspace** in Copilot Chat to leverage instructions:

```
@workspace create a PDF with form fields using pdf-processing instructions
@workspace build an MCP server for Slack API following mcp-builder guide
@workspace generate algorithmic art with particle systems
```

### Accessing Instruction Sets

**Via Copilot Chat:**
```
@workspace list available skills and their purposes
@workspace help me with PDF processing
@workspace show mcp-builder workflow
```

**Via Inline Chat (Ctrl+I / Cmd+I):**
```
create PDF rotation function using pdf skill
implement following mcp-builder patterns
apply algorithmic art principles
```

### Workspace Resources

Instructions reference workspace resources that remain in original skill folders:
- **Scripts**: `skill-name/scripts/` - Executable tools
- **References**: `skill-name/references/` - Detailed documentation
- **Assets**: `skill-name/assets/` - Templates and resources

**Example:** Run a PDF script via @terminal:
```
@terminal python document-skills/pdf/scripts/rotate_pdf.py input.pdf 90
```

## Key Differences: Copilot vs Claude

| Aspect | GitHub Copilot | Claude Code |
|--------|----------------|-------------|
| **Instructions** | `.github/copilot-instructions/*.md` | `SKILL.md` with YAML |
| **Activation** | Automatic workspace context | Manual skill mention |
| **Structure** | Organized by category | One folder per skill |
| **Tools** | VS Code API + @terminal | Claude-specific tools |
| **Distribution** | Git repository | Plugin marketplace ZIP |

## Original Claude Skill Structure

For reference, Claude skills follow this structure:

Every skill MUST follow this structure:

1. **Folder naming**: Use hyphen-case (lowercase, hyphens for spaces)
2. **SKILL.md file**: Required entrypoint file with:
   - YAML frontmatter with required fields:
     - `name`: Must match directory name (hyphen-case, lowercase Unicode alphanumeric + hyphen only)
     - `description`: Complete description of what the skill does and when to use it
   - Optional YAML fields:
     - `license`: License applied to the skill
     - `allowed-tools`: List of pre-approved tools (Claude Code only)
     - `metadata`: Additional properties as key-value pairs
   - Markdown body with instructions, examples, and guidelines

## Coding Standards

### For Skills with Scripts

- **Python scripts**: Follow PEP 8 conventions, use type hints where appropriate
- **JavaScript/Node.js scripts**: Use modern ES6+ syntax, follow standard JavaScript conventions
- **All scripts**: Include clear docstrings/comments explaining purpose and usage

### File Structure

- Keep skills self-contained in their directories
- Additional resources (templates, scripts, reference docs) should be organized in subdirectories
- Use descriptive file names

## Creating New Skills

When creating a new skill:

1. Start with the `template-skill` as a base
2. Create a new directory with a hyphen-case name
3. Create `SKILL.md` with proper YAML frontmatter
4. Ensure the `name` field matches the directory name exactly
5. Write clear, actionable instructions in the markdown body
6. Include examples demonstrating the skill's usage
7. Add supporting scripts/resources only if necessary

## Documentation Standards

- Use clear, concise language in skill descriptions
- Provide specific examples of when to use each skill
- Document any dependencies or prerequisites
- Include usage examples in the markdown body

## Important Notes

- **Document skills** are point-in-time snapshots, not actively maintained
- These are reference examples for inspiration, not production-ready implementations
- Skills showcased are general-purpose capabilities, not organization-specific workflows
- Test skills thoroughly before relying on them for critical tasks

## Contributing

When modifying or adding skills:

- Maintain consistency with existing skill patterns
- Follow the Agent Skills Spec (v1.0) requirements
- Keep skills focused and single-purpose
- Ensure backward compatibility when updating existing skills
- Update README.md if adding new example skills to the collection
