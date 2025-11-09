# GitHub Copilot Instructions for Code Skills

This directory contains specialized instructions for GitHub Copilot in VS Code, adapted from the original Claude Code Skills architecture. These instructions extend Copilot's capabilities with domain-specific knowledge, workflows, and best practices.

## Philosophy

These instructions follow a modular, progressive disclosure approach:
- **Core Philosophy**: Foundational principles for AI-assisted development
- **Domain-Specific Instructions**: Specialized knowledge organized by skill area
- **Resource References**: Links to scripts, templates, and documentation in the workspace

## Structure

```
.github/copilot-instructions/
├── README.md                          # This file
├── 00-core-philosophy.md              # Core principles and philosophy
├── document-skills/                   # Document processing capabilities
│   ├── pdf-processing.md
│   ├── docx-editing.md
│   ├── xlsx-spreadsheets.md
│   └── pptx-presentations.md
├── development-skills/                # Development and technical skills
│   ├── mcp-builder.md
│   ├── webapp-testing.md
│   └── artifacts-builder.md
├── creative-skills/                   # Creative and design capabilities
│   ├── algorithmic-art.md
│   ├── canvas-design.md
│   └── theme-factory.md
├── communication-skills/              # Communication and branding
│   ├── internal-comms.md
│   └── brand-guidelines.md
└── meta-skills/                       # Skills about creating skills
    └── skill-creator.md
```

## How to Use

### In VS Code with GitHub Copilot

1. **Automatic Loading**: When you open this workspace in VS Code with GitHub Copilot enabled, these instructions are automatically available as context.

2. **Chat Interface**: Use Copilot Chat to leverage these instructions:
   ```
   @workspace help me create a PDF with forms
   @workspace build an MCP server for Slack
   @workspace generate algorithmic art using p5.js
   ```

3. **Context Awareness**: Copilot will use relevant instructions based on:
   - Your current file and task
   - Workspace structure and resources
   - Semantic similarity to instruction content

4. **Resource Access**: Instructions reference workspace resources:
   - Scripts in skill folders (e.g., `document-skills/pdf/scripts/`)
   - Reference documentation in `references/` directories
   - Assets and templates in `assets/` directories

### Slash Commands

Use Copilot's slash commands with skill-specific context:
- `/explain` - Explain code using skill-specific knowledge
- `/fix` - Fix issues following skill guidelines
- `/tests` - Generate tests consistent with skill patterns
- `/new` - Create new files following skill templates

### Participants

Leverage Copilot's participants for better context:
- `@workspace` - Query workspace-wide instructions
- `@terminal` - Execute scripts referenced in instructions
- `@vscode` - VS Code-specific operations

## Key Differences from Claude Code Skills

| Aspect | Claude Code Skills | GitHub Copilot Instructions |
|--------|-------------------|----------------------------|
| **Activation** | Manual mention/trigger | Automatic workspace context |
| **Format** | SKILL.md with YAML frontmatter | Standard Markdown |
| **Structure** | One folder per skill | Organized by domain |
| **Discovery** | Plugin marketplace | Git repository |
| **Resources** | Bundled in skill folder | Referenced in workspace |
| **Tools** | Claude-specific | VS Code API + @terminal |

## Skill Categories

### Document Skills
Professional document creation, editing, and analysis for PDF, Word, PowerPoint, and Excel formats. These skills provide comprehensive workflows for working with binary document formats while preserving formatting, supporting tracked changes, and handling complex structures.

**When to use**: Creating, editing, or analyzing .pdf, .docx, .pptx, or .xlsx files.

### Development Skills
Technical development capabilities including MCP server creation, web application testing, and artifact building. These skills guide systematic implementation with proper architecture, testing, and best practices.

**When to use**: Building MCP servers, testing web applications, or creating complex HTML artifacts.

### Creative Skills
Generative art, visual design, and creative content creation. These skills enable algorithmic art generation, canvas-based design, and theme creation with professional aesthetics.

**When to use**: Creating generative art, designing visual content, or applying custom themes.

### Communication Skills
Professional communication and branding guidelines. These skills help create internal communications, apply brand guidelines, and maintain consistent messaging.

**When to use**: Writing status reports, newsletters, or applying brand standards.

### Meta Skills
Skills about creating and managing skills themselves. These provide frameworks for developing new capabilities and extending the instruction set.

**When to use**: Creating new instruction sets or extending Copilot's capabilities.

## Migration from Claude Skills

If you're familiar with Claude Code Skills, here's how to adapt:

1. **SKILL.md → Instruction File**: Content from SKILL.md becomes a Copilot instruction file
2. **YAML Frontmatter → Headers**: Metadata becomes section headers and descriptions
3. **Bundled Resources**: Scripts, references, and assets remain in workspace, referenced by path
4. **Tool Calls**: Claude tool calls → VS Code API calls or @terminal commands
5. **Marketplace**: Distribution via Git rather than plugin marketplace

## Contributing

To add new instructions:

1. Choose the appropriate category directory
2. Create a new `.md` file following the template pattern
3. Use clear section headers and actionable instructions
4. Reference workspace resources with relative paths
5. Test with Copilot Chat to ensure effectiveness

## Resources

- **Original Skills Repository**: All original skill folders remain in the workspace root
- **Scripts**: Executable scripts in each skill's `scripts/` directory
- **References**: Detailed documentation in each skill's `references/` directory
- **Assets**: Templates and resources in each skill's `assets/` directory
- **VS Code Copilot Docs**: https://code.visualstudio.com/docs/copilot/overview
- **GitHub Copilot Extensions**: https://github.com/features/copilot/extensions

## License

These instructions are adapted from the Anthropic Agent Skills repository. See the workspace root for original licenses:
- Example skills: Apache 2.0 (see LICENSE in workspace root)
- Document skills: Proprietary (see document-skills/*/LICENSE.txt)
