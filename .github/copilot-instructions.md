# GitHub Copilot Instructions for code-skills Repository

## Repository Overview

This repository contains example skills for Claude's skills system. Skills are folders containing instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks.

## Repository Structure

- **Example Skills**: Creative (algorithmic-art, canvas-design, slack-gif-creator), Development (artifacts-builder, mcp-builder, webapp-testing), Enterprise (brand-guidelines, internal-comms, theme-factory), and Meta skills (skill-creator, template-skill)
- **Document Skills** (`document-skills/`): Advanced skills for working with binary file formats (docx, pdf, pptx, xlsx) - these are source-available reference examples, not open source
- **Agent Skills Spec** (`agent_skills_spec.md`): Specification for creating skills
- **Template Skill** (`template-skill/`): Basic starting point for new skills

## Skill Structure Requirements

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
