# Skill Creator - Creating Copilot Instructions

## Overview

Guide for creating effective instruction sets for GitHub Copilot in VS Code. Use these guidelines when creating new instruction files or extending Copilot's capabilities with specialized knowledge, workflows, or tool integrations.

## When to Use

- Creating new instruction sets for specific domains
- Extending Copilot capabilities with specialized workflows
- Documenting team-specific knowledge for AI assistance
- Building reusable patterns for common tasks
- Integrating external tools or APIs with Copilot

## About Copilot Instructions

Instructions are structured guidance that extend Copilot's capabilities by providing specialized knowledge, workflows, and tools. They transform Copilot from a general-purpose coding assistant into a domain expert equipped with procedural knowledge and context.

### What Instructions Provide

1. **Specialized Workflows** - Multi-step procedures for specific domains
2. **Tool Integrations** - Guidance for working with specific file formats or APIs
3. **Domain Expertise** - Team-specific knowledge, schemas, business logic
4. **Resource References** - Links to scripts, documentation, and assets

### Instruction File Anatomy

Each instruction set includes:

```
.github/copilot-instructions/category/
├── skill-name.md              # Main instruction file
└── ...

workspace-root/skill-name/     # Supporting resources
├── scripts/                   # Executable code
├── references/                # Documentation
└── assets/                    # Templates and resources
```

## Creating Instructions: Step-by-Step

### Step 1: Understand with Concrete Examples

Begin by gathering real examples of how the instructions will be used.

**Questions to answer:**
- What functionality should these instructions support?
- What would trigger using this knowledge?
- What are concrete examples of tasks users will perform?
- What workflows need to be documented?

**Example**: For image editing instructions:
- "Remove red-eye from this image"
- "Rotate image 90 degrees"
- "Resize while maintaining aspect ratio"

Conclude when you have clear examples of functionality to support.

### Step 2: Plan Reusable Resources

Analyze each example to identify helpful resources:

1. Consider how to execute the task from scratch
2. Identify scripts, references, and assets that would help
3. Determine what should be instruction vs. resource

**Examples:**

**PDF Rotation Workflow:**
- Analysis: Rotating PDFs requires same code repeatedly
- Resource: Create `scripts/rotate_pdf.py` script
- Instruction: Document when and how to use the script

**Frontend Webapp Builder:**
- Analysis: Building webapps needs same boilerplate
- Resource: Create `assets/hello-world/` template with boilerplate
- Instruction: Explain how to customize the template

**BigQuery Integration:**
- Analysis: Querying requires rediscovering schemas
- Resource: Create `references/schema.md` with table documentation
- Instruction: Provide query patterns and best practices

### Step 3: Initialize the Instruction File

Create the instruction file in the appropriate category:

```bash
# Choose category: document-skills, development-skills, creative-skills,
#                  communication-skills, or meta-skills
cd .github/copilot-instructions/[category]/
touch skill-name.md
```

**Directory Structure Pattern:**
```
.github/copilot-instructions/
├── document-skills/          # Document processing
├── development-skills/       # Development tools
├── creative-skills/          # Creative content
├── communication-skills/     # Communication & branding
└── meta-skills/             # Meta instructions
```

### Step 4: Write the Instruction File

#### Template Structure

```markdown
# Skill Name

## Overview
[Brief description of what this provides and its purpose]

## When to Use
[Specific scenarios and triggers for using these instructions]

## Workflows
[Step-by-step procedures for common tasks]

### Workflow 1: [Task Name]
[Detailed steps]

### Workflow 2: [Task Name]
[Detailed steps]

## Examples
[Concrete examples with inputs and expected outputs]

## Resources
[References to workspace scripts, documentation, and assets]

### Scripts
- **`workspace-root/skill-name/scripts/tool.py`** - [Description]

### References
- **`workspace-root/skill-name/references/guide.md`** - [Description]

### Assets
- **`workspace-root/skill-name/assets/template/`** - [Description]

## Guidelines
[Best practices and principles]

## Common Patterns
[Reusable patterns and examples]

## Troubleshooting
[Common issues and solutions]
```

#### Writing Style Guidelines

**Voice and Style:**
- Use imperative/infinitive form: "To accomplish X, do Y"
- Be objective and instructional
- Provide concrete examples
- Reference workspace resources with paths

**Example - Good:**
```markdown
To rotate a PDF, use the rotation script:

1. Locate the PDF file in the workspace
2. Run: `python skill-name/scripts/rotate_pdf.py input.pdf 90`
3. The rotated PDF will be saved as `input_rotated.pdf`
```

**Example - Avoid:**
```markdown
You should rotate PDFs when you need them in a different orientation.
Consider using a script for this.
```

#### Content Organization

**Start with Overview:**
- What does this provide?
- When should it be used?
- What makes it valuable?

**Provide Clear Workflows:**
- Step-by-step procedures
- Decision trees for complex choices
- Entry points for different scenarios

**Include Decision Trees:**
When multiple approaches exist, guide the choice:

```markdown
## Workflow Decision Tree

### For Simple Documents
Use basic workflow...

### For Documents with Complex Formatting
Use advanced workflow with preservation...

### For Batch Processing
Use script-based approach...
```

**Reference Resources:**
Always link to detailed documentation:

```markdown
## Resources

For detailed API documentation, see:
- `skill-name/references/api-docs.md`

For implementation examples, see:
- `skill-name/references/examples.md`
```

#### Context Management

**Keep Core Instructions Concise:**
- Aim for <5,000 words in main instruction file
- Extract lengthy details to reference files
- Focus on workflows and decision points

**Extract to References:**
Move to reference files:
- Detailed API documentation
- Extensive examples
- Technical specifications
- Background information

Keep in instructions:
- Core workflows
- Decision points
- When to use what approach
- Links to references

**Use Clear Section Headers:**
Enable semantic search with descriptive headers:
- `## When to Use Image Processing`
- `## Workflow: Creating PDFs with Forms`
- `## Pattern: Async API Requests`

### Step 5: Create Supporting Resources

#### Scripts Directory

Create executable tools for deterministic tasks:

```bash
mkdir -p skill-name/scripts
```

**When to include scripts:**
- Code is repeatedly rewritten
- Deterministic reliability needed
- Complex operations that shouldn't vary

**Script guidelines:**
- Include clear docstrings
- Add usage examples
- Handle errors gracefully
- Accept parameters for flexibility

#### References Directory

Create detailed documentation:

```bash
mkdir -p skill-name/references
```

**When to include references:**
- API documentation
- Schemas and data models
- Detailed examples
- Background knowledge
- Technical specifications

**Reference guidelines:**
- Use clear markdown structure
- Include search-friendly headings
- Provide concrete examples
- Keep updated with sources

#### Assets Directory

Create templates and resources:

```bash
mkdir -p skill-name/assets
```

**When to include assets:**
- Templates for generated output
- Boilerplate code
- Brand resources
- Sample files
- Configuration templates

**Asset guidelines:**
- Keep templates minimal and customizable
- Include documentation for each asset
- Version control appropriately
- Reference in instructions with paths

### Step 6: Test and Iterate

Test instructions with real scenarios:

1. **Use in Copilot Chat:**
   ```
   @workspace [describe task using these instructions]
   ```

2. **Test inline:**
   ```
   Use Ctrl+I / Cmd+I to test inline suggestions
   ```

3. **Verify resource access:**
   ```
   @terminal run scripts from instruction set
   ```

**Iteration workflow:**
- Use instructions on real tasks
- Notice where Copilot struggles or needs clarification
- Identify needed improvements
- Update instructions and resources
- Test again

## Quality Standards

### Effective Instructions Should:

1. **Be Specific and Actionable**
   - Clear steps, not vague suggestions
   - Concrete examples
   - Explicit resource references

2. **Provide Concrete Examples**
   - Real usage patterns
   - Input/output examples
   - Common scenarios

3. **Reference Workspace Resources**
   - Use available scripts with paths
   - Link to documentation
   - Point to assets

4. **Follow Consistent Structure**
   - Predictable organization
   - Clear section headers
   - Logical flow

5. **Optimize for Context**
   - Concise core instructions
   - Detailed references separate
   - No duplication

6. **Enable Complete Workflows**
   - End-to-end procedures
   - Not just individual operations
   - Handle common variations

7. **Iterate Based on Feedback**
   - Test with real tasks
   - Update based on results
   - Improve continuously

### Avoid:

1. **Excessive detail in core file** - Move to references
2. **Duplicated information** - Single source of truth
3. **Vague guidance** - Be specific and concrete
4. **Copying docs verbatim** - Provide workflow context
5. **Ignoring workspace resources** - Leverage existing tools

## Integration with GitHub Copilot

### Chat Interface Usage

```
@workspace create a [task] using [skill name] instructions
@workspace help me [task] following [skill name] guidelines
@workspace what's the best way to [task] in [domain]
```

### Inline Chat Usage

```
create function following [skill name] pattern
implement [feature] using [skill name] approach
refactor to match [skill name] guidelines
```

### Resource Access

**Scripts:**
```
@terminal python skill-name/scripts/tool.py input.txt
```

**References:**
```
@workspace check skill-name/references/api-docs.md for [detail]
```

**Assets:**
```
@workspace copy skill-name/assets/template/ to new project
```

## Examples of Excellence

### Document Processing Instructions

**Structure:**
- Core: Overview and workflow decision tree (<3,000 words)
- Scripts: PDF rotation, text extraction, form filling
- References: Detailed library documentation
- Assets: Sample PDFs and form templates

**Why it works:**
- Clear decision tree for different scenarios
- Reliable scripts for deterministic tasks
- Comprehensive references for edge cases
- Ready-to-use templates

### MCP Server Builder Instructions

**Structure:**
- Core: 4-phase development process (<4,000 words)
- Scripts: Evaluation harness, validation tools
- References: Language-specific guides (Python, TypeScript)
- Assets: Server templates and examples

**Why it works:**
- Systematic, phase-based workflow
- Evaluation-driven development approach
- Language-specific deep-dives in references
- Working examples to learn from

### Algorithmic Art Instructions

**Structure:**
- Core: Philosophy creation → code expression (<3,000 words)
- Scripts: p5.js boilerplate generator
- References: Generative art techniques
- Assets: Example sketches and templates

**Why it works:**
- Two-phase creative process
- Principles of computational aesthetics
- Rich examples and patterns
- Reusable templates

## Continuous Improvement

Instructions evolve through:

1. **Real Usage** - Test with actual tasks
2. **Feedback Collection** - Note what works and what doesn't
3. **Documentation Updates** - Keep instructions current
4. **Resource Expansion** - Add helpful scripts and references
5. **Pattern Recognition** - Identify and document successful patterns

## Workspace Organization

### Recommended Structure

```
workspace-root/
├── .github/
│   └── copilot-instructions/
│       ├── README.md
│       ├── 00-core-philosophy.md
│       └── [category]/
│           └── skill-name.md
├── skill-name/
│   ├── scripts/
│   ├── references/
│   └── assets/
└── [other workspace files]
```

### File Naming Conventions

**Instructions:**
- `skill-name.md` (lowercase, hyphens)
- Match instruction file name to workspace folder

**Scripts:**
- `action_verb_noun.py` (snake_case)
- Descriptive names: `rotate_pdf.py`, `extract_text.py`

**References:**
- `topic-description.md` (kebab-case)
- `api-docs.md`, `best-practices.md`, `examples.md`

**Assets:**
- Descriptive names matching purpose
- `template-name/` for directory structures

## Conclusion

Creating effective Copilot instructions requires:
- Understanding concrete use cases
- Planning reusable resources
- Writing clear, actionable instructions
- Testing with real scenarios
- Iterating based on feedback

Follow these guidelines to create instructions that genuinely extend Copilot's capabilities and deliver professional-quality results in specialized domains.

## Additional Resources

- **Core Philosophy**: See `.github/copilot-instructions/00-core-philosophy.md`
- **Example Instructions**: Browse `.github/copilot-instructions/[category]/`
- **Original Skills**: See workspace root skill folders for complete examples
- **VS Code Copilot Docs**: https://code.visualstudio.com/docs/copilot/overview
