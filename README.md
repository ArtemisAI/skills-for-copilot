# Skills for GitHub Copilot

An evolution of the Skills for AI Assistants framework, now optimized for **GitHub Copilot in VS Code**. This repository provides specialized instruction sets that extend Copilot's capabilities with domain-specific knowledge, workflows, and tools.

Skills are modular instruction sets designed to enhance AI capabilities with specialized knowledge, workflows, and tools. This repository demonstrates what's possible with skill-based AI assistance, ranging from creative applications (algorithmic art, design) to technical tasks (web app testing, MCP server development) to enterprise workflows (document processing, communications, branding).

---

## 📊 Project Status

**Version**: 1.0
**Status**: ✅ Production Ready
**Last Updated**: November 2025

This project has been professionally adapted and is ready for community contributions and production use.

---

## 🚀 GitHub Copilot in VS Code

This repository has been professionally adapted for GitHub Copilot in VS Code. Open this workspace in VS Code with Copilot enabled to get specialized assistance across multiple domains:

**Quick Start with Copilot:**
```
@workspace create a PDF with form fields
@workspace build an MCP server for Slack
@workspace generate algorithmic art with particles
@workspace test my web app with Playwright
```

See [`.github/copilot-instructions/README.md`](.github/copilot-instructions/README.md) for the complete usage guide and available skills.

## Repository Overview

This repository contains specialized instruction sets demonstrating what's possible with skill-based AI assistance for GitHub Copilot. We provide both modern Copilot instructions and original Claude Code Skills for reference.

**Two Formats Included:**

1. **GitHub Copilot Instructions** (`.github/copilot-instructions/`) - Optimized for VS Code
   - Automatic workspace context loading
   - Organized by domain (document, development, creative, communication)
   - Standard Markdown format
   - [View Instructions →](.github/copilot-instructions/)

2. **Claude Code Skills** (workspace root folders) - Original format
   - Self-contained skill folders with `SKILL.md`
   - Scripts, references, and assets included
   - Plugin marketplace compatible
   - [View Original Skills →](#try-in-claude-code-claudeai-and-the-api)

The example skills are open source (Apache 2.0). Document skills (`document-skills/`) are source-available reference examples from Claude's production document capabilities.

**Note:** These are reference examples for inspiration and learning, showcasing general-purpose capabilities rather than organization-specific workflows.

---

# 🤝 Collaboration & Contributing

We welcome contributions from the community! This project is built on the principle of collaborative innovation. Whether you're a developer, designer, or domain expert, your contributions help make Copilot skills better for everyone.

## How to Contribute

### Submit Improvements & Adaptations
1. **Fork this repository** to your GitHub account
2. **Create a feature branch** for your changes:
   ```bash
   git checkout -b feature/your-skill-name
   ```
3. **Make your improvements:**
   - Add new skills in `.github/copilot-instructions/`
   - Update existing instruction sets with enhancements
   - Improve documentation and examples
   - Add scripts or tools to support skills

4. **Test your changes:**
   - Open the workspace in VS Code with Copilot
   - Test your skill with `@workspace` queries
   - Verify all references and file paths are correct

5. **Submit a Pull Request:**
   - Provide a clear description of your changes
   - Reference any related issues
   - Include before/after examples if applicable
   - Follow our coding standards (see below)

### Types of Contributions We Welcome

- **New Skills** - Create entirely new instruction sets for additional domains
- **Skill Enhancements** - Improve existing skills with better examples, workflows, or capabilities
- **Bug Fixes** - Report and fix issues in instructions or resource references
- **Documentation** - Improve guides, READMEs, and inline documentation
- **Examples** - Add concrete examples and use cases
- **Scripts & Tools** - Contribute supporting scripts to enhance skills
- **Translations** - Help localize skills for different languages

### Creating a New Skill

To create a new skill for inclusion in this repository:

1. Follow the structure in `.github/copilot-instructions/`
2. Use the template at `.github/copilot-instructions/meta-skills/skill-creator.md` as a guide
3. Include:
   - Clear overview and "When to Use" section
   - Step-by-step workflows with concrete examples
   - Resource references with file paths
   - Troubleshooting and common patterns
   - Links to related skills or documentation

4. Organize by domain (creative, development, document, communication, or meta)
5. Test thoroughly in VS Code with Copilot before submitting

## Development Standards

### Markdown Guidelines
- Use clear, concise language
- Include practical examples for every workflow
- Structure with descriptive headers (H2, H3)
- Use code blocks for commands and examples
- Add file paths for all resource references

### Code & Script Standards
- **Python**: Follow PEP 8, include type hints where appropriate
- **JavaScript/Node.js**: Use modern ES6+ syntax, follow standard conventions
- **All scripts**: Include clear docstrings/comments explaining purpose and usage
- Include error handling and validation
- Test scripts locally before submission

### Documentation Standards
- Keep descriptions clear and action-oriented
- Provide specific examples of when to use each skill
- Document any dependencies or prerequisites
- Include troubleshooting sections
- Maintain consistency with existing skills

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and professional in all interactions
- Provide constructive feedback
- Focus on ideas, not individuals
- Report inappropriate behavior to maintainers
- Help create a supportive community

## Reporting Issues & Feedback

Found a bug? Have a suggestion? We'd love to hear from you!

- **Issues**: Use GitHub Issues to report bugs or request features
- **Discussions**: Start a discussion for questions or ideas
- **Feedback**: Share your experience using the skills

### Issue Template
When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Your environment (OS, Copilot version, etc.)
- Any relevant error messages or logs

## Review Process

1. **Automated Checks**: All PRs are checked for:
   - Markdown formatting and links
   - File structure compliance
   - Resource path validity

2. **Community Review**: Community members can review and provide feedback

3. **Maintainer Review**: Core maintainers assess:
   - Alignment with project goals
   - Code/documentation quality
   - Testing completeness
   - Community value

4. **Merge**: Once approved, changes are merged to main branch

## Recognition

Contributors are recognized for their work:
- Listed in release notes for significant contributions
- Added to contributors list in repository
- Featured in project announcements

## License & Attribution

All contributions to this repository are licensed under Apache 2.0. By contributing, you agree that:
- Your work can be used under the Apache 2.0 license
- You have the right to submit the work
- You consent to your name being associated with the contribution

## Getting Help

- **Documentation**: Check `.github/copilot-instructions/README.md`
- **Examples**: Review existing skills in the repository
- **Questions**: Open a GitHub Discussion
- **Issues**: Search existing issues or create a new one

---

## Disclaimer

**These skills are provided for demonstration and educational purposes only.** While some of these capabilities may be available in Claude or GitHub Copilot, the implementations and behaviors you receive may differ from what is shown in these examples. These examples are meant to illustrate patterns and possibilities. Always test skills thoroughly in your own environment before relying on them for critical tasks.

---

# 📋 License & Legal

## Open Source License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) file for full terms.

**You are free to:**
- ✅ Use this in commercial projects
- ✅ Modify and distribute
- ✅ Include in your own projects

**You must:**
- 📝 Include the license notice
- 📝 State significant changes made
- 📝 Include the NOTICE file

## Third-Party Notices

This project includes components and references from:
- Claude AI (Anthropic) - Document processing patterns
- Open source libraries and templates
- Community contributions

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for complete attribution.

---

# Example Skills

This repository includes a diverse collection of example skills demonstrating different capabilities:

## Creative & Design
- **algorithmic-art** - Create generative art using p5.js with seeded randomness, flow fields, and particle systems
- **canvas-design** - Design beautiful visual art in .png and .pdf formats using design philosophies
- **slack-gif-creator** - Create animated GIFs optimized for Slack's size constraints

## Development & Technical
- **artifacts-builder** - Build complex claude.ai HTML artifacts using React, Tailwind CSS, and shadcn/ui components
- **mcp-server** - Guide for creating high-quality MCP servers to integrate external APIs and services
- **webapp-testing** - Test local web applications using Playwright for UI verification and debugging

## Enterprise & Communication
- **brand-guidelines** - Apply Anthropic's official brand colors and typography to artifacts
- **internal-comms** - Write internal communications like status reports, newsletters, and FAQs
- **theme-factory** - Style artifacts with 10 pre-set professional themes or generate custom themes on-the-fly

## Meta Skills
- **skill-creator** - Guide for creating effective skills that extend Claude's capabilities
- **template-skill** - A basic template to use as a starting point for new skills

# Document Skills

The `document-skills/` subdirectory contains skills that Anthropic developed to help Claude create various document file formats. These skills demonstrate advanced patterns for working with complex file formats and binary data:

- **docx** - Create, edit, and analyze Word documents with support for tracked changes, comments, formatting preservation, and text extraction
- **pdf** - Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms
- **pptx** - Create, edit, and analyze PowerPoint presentations with support for layouts, templates, charts, and automated slide generation
- **xlsx** - Create, edit, and analyze Excel spreadsheets with support for formulas, formatting, data analysis, and visualization

**Important Disclaimer:** These document skills are point-in-time snapshots and are not actively maintained or updated. Versions of these skills ship pre-included with Claude. They are primarily intended as reference examples to illustrate how Anthropic approaches developing more complex skills that work with binary file formats and document structures.

# Try in GitHub Copilot (VS Code)

## Quick Start

1. **Open the workspace**: Open this repository folder in VS Code
2. **Enable Copilot**: Ensure GitHub Copilot is installed and enabled
3. **Start coding**: Instructions automatically load - use `@workspace` in Copilot Chat

## GitHub Copilot in VS Code

**Usage Examples:**
```
@workspace help me create a PDF with form fields
@workspace build an MCP server for the GitHub API
@workspace generate algorithmic art using flow fields
@workspace test my web app with Playwright
@workspace create an Excel spreadsheet with formulas
```

**Available Instruction Sets:**

**Document Skills**
- PDF processing (extraction, forms, manipulation)
- Excel spreadsheet creation and analysis
- Word document handling
- PowerPoint presentation generation

**Development Skills**
- MCP server building and integration
- Web app testing with Playwright
- Artifact creation with React & Tailwind

**Creative Skills**
- Algorithmic art generation with p5.js
- Canvas design and visualization
- Theme creation and customization

**Communication Skills**
- Internal communications and newsletters
- Brand guidelines and styling
- Professional documentation

**Meta Skills**
- Skill creation and development
- Contributing new instruction sets

**Learn More:**
- [Copilot Instructions README](.github/copilot-instructions/README.md) - Complete guide
- [Migration Guide](.github/copilot-instructions/MIGRATION.md) - From Claude to Copilot
- [Core Philosophy](.github/copilot-instructions/00-core-philosophy.md) - Design principles

---

# Try in Claude Code, Claude.ai, and the API

## Claude Code
You can register this repository as a Claude Code Plugin marketplace by running the following command in Claude Code:
```
/plugin marketplace add anthropics/skills
```

Then, to install a specific set of skills:
1. Select `Browse and install plugins`
2. Select `anthropic-agent-skills`
3. Select `document-skills` or `example-skills`
4. Select `Install now`

Alternatively, directly install either Plugin via:
```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

After installing the plugin, you can use the skill by just mentioning it. For instance, if you install the `document-skills` plugin from the marketplace, you can ask Claude Code to do something like: "Use the PDF skill to extract the form fields from path/to/some-file.pdf"

## Claude.ai

These example skills are all already available to paid plans in Claude.ai.

To use any skill from this repository or upload custom skills, follow the instructions in [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b).

## Claude API

You can use Anthropic's pre-built skills, and upload custom skills, via the Claude API. See the [Skills API Quickstart](https://docs.claude.com/en/api/skills-guide#creating-a-skill) for more.

# Creating a Basic Skill

Skills are simple to create - just a folder with a `SKILL.md` file containing YAML frontmatter and instructions. You can use the **template-skill** in this repository as a starting point:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

The frontmatter requires only two fields:
- `name` - A unique identifier for your skill (lowercase, hyphens for spaces)
- `description` - A complete description of what the skill does and when to use it

The markdown content below contains the instructions, examples, and guidelines that Claude will follow. For more details, see [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills).

# Partner Skills

Skills are a great way to teach Claude how to get better at using specific pieces of software. As we see awesome example skills from partners, we may highlight some of them here:

- **Notion** - [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)
