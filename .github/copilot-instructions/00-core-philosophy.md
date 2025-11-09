# Core Philosophy: Agent Skills for GitHub Copilot

## Overview

This workspace implements a modular, skill-based approach to AI-assisted development. Each instruction set extends GitHub Copilot's capabilities with specialized knowledge, workflows, and tools - transforming it from a general-purpose coding assistant into a domain expert.

## What Are Skills?

Skills are self-contained packages of specialized knowledge that guide AI agents through specific domains or tasks. Think of them as "onboarding guides" that provide:

1. **Specialized Workflows** - Multi-step procedures for specific domains
2. **Tool Integrations** - Instructions for working with specific file formats or APIs
3. **Domain Expertise** - Specialized knowledge, schemas, and business logic
4. **Bundled Resources** - Scripts, references, and assets for complex tasks

## Progressive Disclosure Principle

Skills are designed with a three-level approach to manage context efficiently:

### Level 1: Metadata (Always Active)
- Skill name and category
- Brief description of when to use
- ~100 words of context

### Level 2: Core Instructions (Loaded When Relevant)
- Primary workflow guidance
- Key procedures and decision trees
- Essential best practices
- ~5,000 words maximum

### Level 3: Bundled Resources (Loaded As Needed)
- Detailed reference documentation
- Executable scripts for deterministic tasks
- Templates and assets
- Unlimited depth

**Adaptation Note**: GitHub Copilot loads all workspace instructions as context, so maintain concise core instructions and reference detailed files when needed.

## Skill Anatomy

### Instruction Structure

Each skill instruction file contains:

```markdown
# Skill Name

## Overview
[What this skill does and when to use it]

## When to Use This Skill
[Specific triggers and use cases]

## Workflows
[Step-by-step procedures]

## Examples
[Concrete usage examples]

## Resources
[References to workspace files, scripts, assets]

## Guidelines
[Best practices and principles]
```

### Workspace Resources

Resources complement instructions:

- **`scripts/`** - Executable code for deterministic tasks
  - When: Code is repeatedly rewritten or needs 100% reliability
  - Examples: PDF rotation, file conversion, data processing
  - Access: Run via `@terminal` or reference in code

- **`references/`** - Documentation loaded as needed
  - When: Detailed reference material that doesn't fit in core instructions
  - Examples: API docs, schemas, specifications, detailed guides
  - Access: Reference by path, Copilot reads when needed

- **`assets/`** - Files used in outputs
  - When: Templates, images, or resources needed in final output
  - Examples: Brand assets, templates, boilerplate code
  - Access: Copy, modify, or reference in generated code

## Design Principles

### 1. Build for Workflows, Not Just APIs

Don't simply wrap existing APIs - design thoughtful, high-impact workflows that enable complete tasks.

**Example**: Instead of separate "check availability" and "create event" tools, provide a `schedule_event` workflow that handles both.

### 2. Optimize for Context Efficiency

AI agents have limited context windows - make every token count.

- Return high-signal information, not exhaustive dumps
- Provide "concise" vs "detailed" options
- Default to human-readable identifiers (names over IDs)
- Consider context budget as a scarce resource

### 3. Design Actionable Instructions

Instructions should guide toward correct usage patterns.

- Provide specific next steps when possible
- Include concrete examples of good vs bad approaches
- Make instructions educational, not just informative
- Help users learn patterns through clear guidance

### 4. Follow Natural Task Subdivisions

Organize skills around how humans think about tasks.

- Use intuitive names that reflect user mental models
- Group related instructions with consistent structure
- Design around natural workflows, not technical architecture

### 5. Enable Iteration and Improvement

Skills should evolve based on actual usage.

- Test with realistic scenarios
- Gather feedback from actual use
- Iterate based on what works and what doesn't
- Maintain clear, actionable instructions

## Instruction Writing Guidelines

### Voice and Style

- **Use imperative/infinitive form**: "To accomplish X, do Y" (not "You should do X")
- **Be objective and instructional**: Focus on procedures, not preferences
- **Provide concrete examples**: Show, don't just tell
- **Reference workspace resources**: Point to scripts, docs, and assets

### Organization

- **Start with overview**: What and when
- **Provide clear workflows**: Step-by-step procedures
- **Include decision trees**: Guide through choices
- **Reference resources**: Link to detailed documentation

### Context Management

- **Keep core instructions lean**: <5,000 words ideal
- **Extract details to references**: Move lengthy content to reference files
- **Use clear section headers**: Enable semantic search
- **Avoid duplication**: Information should live in one place

## Using Skills in GitHub Copilot

### Chat Interface

Engage with skills through Copilot Chat:

```
@workspace create a PDF with form fields for a survey
@workspace help me build an MCP server for GitHub API
@workspace generate algorithmic art using particle systems
```

### Inline Chat

Quick access while coding (Ctrl+I / Cmd+I):

```
create a function to rotate PDFs using the pdf skill
write tests following the testing skill guidelines
apply brand guidelines to this component
```

### Context Awareness

Copilot automatically considers:
- Current file and task context
- Workspace structure and available resources
- Semantic similarity to instruction content
- Referenced files and dependencies

### Resource Access

Access workspace resources through:
- **File references**: Direct paths to scripts, docs, assets
- **@terminal**: Execute scripts from skill folders
- **@workspace**: Query across all instruction files
- **File system**: Standard VS Code file operations

## Skill Categories

### Document Skills
Binary document format expertise (PDF, Word, PowerPoint, Excel).
- Comprehensive format manipulation
- Preserving formatting and structure
- Advanced features (forms, tracked changes, formulas)

### Development Skills
Technical development and tooling (MCP servers, testing, artifacts).
- Systematic implementation workflows
- Best practices and architecture patterns
- Testing and quality assurance

### Creative Skills
Generative and visual content creation (art, design, themes).
- Algorithmic generation principles
- Design philosophies and aesthetics
- Professional presentation

### Communication Skills
Professional communication and branding (internal comms, guidelines).
- Company-specific messaging
- Brand consistency
- Effective documentation

### Meta Skills
Creating and managing skills themselves.
- Skill development frameworks
- Extension patterns
- Quality guidelines

## Quality Standards

### Effective Instructions Should:

1. **Be specific and actionable** - Clear steps, not vague suggestions
2. **Provide concrete examples** - Show real usage patterns
3. **Reference workspace resources** - Use available scripts and docs
4. **Follow consistent structure** - Predictable organization
5. **Optimize for context** - Concise core with detailed references
6. **Enable workflows** - Complete tasks, not just individual operations
7. **Iterate based on feedback** - Improve through actual use

### Avoid:

1. **Excessive detail in core instructions** - Move to reference files
2. **Duplicated information** - Keep single source of truth
3. **Vague or ambiguous guidance** - Be specific and concrete
4. **Copying API docs verbatim** - Provide workflow context
5. **Ignoring workspace resources** - Leverage existing scripts and assets

## Integration with GitHub Copilot Features

### Slash Commands

Use with skill context:
- `/explain` - Explain using skill-specific knowledge
- `/fix` - Fix following skill guidelines
- `/tests` - Generate tests matching skill patterns
- `/new` - Create files using skill templates

### Participants

Enhance with context providers:
- `@workspace` - Access all skill instructions
- `@terminal` - Run skill scripts
- `@vscode` - VS Code operations

### Extensions

For complex skills, consider building Copilot Extensions:
- Custom chat participants
- Language Model API integration
- VS Code Extension API
- Published to marketplace

## Adaptation from Claude Code

### Key Changes

1. **Format**: SKILL.md with YAML → standard Markdown
2. **Activation**: Manual mention → automatic context
3. **Distribution**: Plugin marketplace → Git repository
4. **Resources**: Bundled in skill ZIP → workspace directories
5. **Tools**: Claude-specific → VS Code API + @terminal

### Migration Pattern

```
Claude Skill Structure:
skill-name/
  SKILL.md (with YAML frontmatter)
  scripts/
  references/
  assets/

GitHub Copilot Structure:
.github/copilot-instructions/category/skill-name.md
skill-name/ (in workspace root)
  scripts/
  references/
  assets/
```

### Preserved Principles

- Progressive disclosure philosophy
- Modular, self-contained knowledge
- Workflow-oriented design
- Resource bundling patterns
- Quality and iteration focus

## Examples of Excellence

### Document Skills: PDF Processing

**Philosophy**: Comprehensive toolkit for deterministic PDF manipulation.

**Approach**:
- Core instructions: Overview and workflow decision tree
- Scripts: Reliable, tested Python tools for common operations
- References: Detailed API documentation and edge cases
- Assets: Sample PDFs and templates

### Development Skills: MCP Builder

**Philosophy**: Systematic approach to building high-quality MCP servers.

**Approach**:
- Core instructions: 4-phase development process
- References: Language-specific implementation guides
- Scripts: Evaluation harness and validation tools
- Examples: Real MCP server patterns

### Creative Skills: Algorithmic Art

**Philosophy**: Code as creative expression through generative algorithms.

**Approach**:
- Core instructions: Philosophy creation → code expression
- References: p5.js patterns and techniques
- Assets: Example sketches and templates
- Guidelines: Principles of computational aesthetics

## Continuous Improvement

Skills evolve through:

1. **Usage Feedback** - Real-world testing reveals gaps
2. **Iteration** - Update based on what works
3. **Documentation** - Keep instructions current
4. **Community** - Share patterns and improvements
5. **Measurement** - Track effectiveness and impact

## Conclusion

This skill-based approach transforms GitHub Copilot from a general coding assistant into a specialized domain expert. By providing structured, workflow-oriented instructions with supporting resources, we enable AI to deliver professional-quality results in specialized areas.

The key is maintaining the balance:
- **Specific enough** to be genuinely helpful
- **General enough** to handle variety
- **Concise enough** to fit in context
- **Detailed enough** through references
- **Actionable enough** to drive results

Follow these principles, and you'll create instructions that genuinely extend Copilot's capabilities.
