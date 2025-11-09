# Skills Testing Guide for GitHub Copilot Environment

This guide provides practical instructions for testing and using each skill in the GitHub Copilot coding environment.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Node.js 16+ (optional, only for MCP Builder Node.js path)
- Git
- VS Code with GitHub Copilot (for optimal experience)

### Installation Commands

**For Document Skills:**
```bash
# PDF Processing
pip install pypdf pdfplumber pdf2image

# Word Documents
pip install python-docx

# PowerPoint Presentations  
pip install python-pptx

# Excel Spreadsheets
pip install openpyxl
```

**For Web App Testing:**
```bash
pip install playwright
playwright install chromium
```

**For MCP Builder (Python path):**
```bash
pip install fastmcp
# OR use the official SDK
pip install mcp
```

**For MCP Builder (Node.js path):**
```bash
npm install -g @modelcontextprotocol/sdk
```

---

## Testing Each Skill

### 1. Meta Skills

#### Skill Creator
**Purpose**: Create new skills for Claude or GitHub Copilot

**Test Commands:**
```bash
# Test init_skill.py
cd skill-creator/scripts
python3 init_skill.py test-skill --path /tmp

# Test validation
python3 quick_validate.py /tmp/test-skill

# Test packaging
python3 package_skill.py /tmp/test-skill /tmp
```

**Expected Results:**
- Creates skill directory with proper structure
- Validation passes for well-formed skills
- Packaging creates .zip file

**Status**: ✅ Fully tested and working

#### Template Skill
**Purpose**: Skeleton template for new skills

**Test Commands:**
```bash
# View the template
cat template-skill/SKILL.md
```

**Expected Results:**
- Shows minimal SKILL.md with YAML frontmatter

**Status**: ✅ Template confirmed

---

### 2. Creative Skills

#### Algorithmic Art
**Purpose**: Create generative art using p5.js

**Test Commands:**
```bash
# View the template
cat algorithmic-art/templates/viewer.html | head -100

# Create a test HTML file based on the template
cp algorithmic-art/templates/viewer.html /tmp/test-art.html
# Open in browser to view
```

**Usage in Copilot:**
```
@workspace using algorithmic-art skill, create a flow field visualization
```

**Expected Results:**
- HTML file with p5.js generative art
- Interactive controls for parameters
- Seed-based reproducibility

**Status**: ✅ Template ready, requires manual HTML creation

#### Canvas Design
**Purpose**: Design philosophy and guidelines

**Test Commands:**
```bash
# Read the skill documentation
cat canvas-design/SKILL.md
```

**Usage in Copilot:**
```
@workspace using canvas-design principles, create a visual design
```

**Expected Results:**
- Design guidance and principles
- No executable code

**Status**: ✅ Documentation ready

#### Slack GIF Creator
**Purpose**: Create GIFs optimized for Slack

**Test Commands:**
```bash
# Read the specifications
cat slack-gif-creator/SKILL.md
```

**Usage in Copilot:**
```
@workspace create an animated GIF for Slack following slack-gif-creator guidelines
```

**Expected Results:**
- Specifications and constraints for Slack GIFs
- No executable code

**Status**: ✅ Specifications ready

---

### 3. Development Skills

#### MCP Builder
**Purpose**: Build MCP servers for external API integration

**Test Commands:**
```bash
# Read the references
ls -la mcp-builder/reference/
cat mcp-builder/reference/mcp_best_practices.md
```

**Usage in Copilot:**
```
@workspace using mcp-builder, create an MCP server for the GitHub API
```

**Expected Results:**
- Step-by-step guide for creating MCP servers
- Best practices documentation
- Example implementations

**Status**: ✅ Documentation ready, requires MCP SDK installation for actual testing

#### Artifacts Builder
**Purpose**: Build complex HTML artifacts with React/Tailwind

**Test Commands:**
```bash
# Read the skill
cat artifacts-builder/SKILL.md
```

**Usage in Copilot:**
```
@workspace using artifacts-builder, create a todo app with React and Tailwind
```

**Expected Results:**
- Templates and patterns for HTML artifacts
- Component examples
- No installation required (uses CDN)

**Status**: ✅ Templates ready

#### Web App Testing
**Purpose**: Test web applications with Playwright

**Test Commands:**
```bash
# Install Playwright first
pip install playwright
playwright install chromium

# Test the helper script
cd webapp-testing/scripts
python3 with_server.py --help

# View examples
ls -la ../examples/
```

**Usage in Copilot:**
```
@workspace using webapp-testing, create a Playwright test for localhost:3000
```

**Expected Results:**
- Playwright test scripts
- Server management helpers
- Screenshot and debugging capabilities

**Status**: ⚠️ Requires Playwright installation

---

### 4. Document Skills

#### PDF Processing
**Purpose**: Extract, create, merge, split PDFs

**Test Commands:**
```bash
# Install dependencies
pip install pypdf pdfplumber

# Test a simple extraction script
cd /tmp
python3 << 'EOF'
from pypdf import PdfReader, PdfWriter
# Create a simple PDF test would go here
print("PyPDF installed successfully")
EOF
```

**Usage in Copilot:**
```
@workspace using pdf skill, extract text from document.pdf
@workspace using pdf skill, merge multiple PDFs
@workspace using pdf skill, fill form fields in form.pdf
```

**Expected Results:**
- PDF text extraction
- PDF manipulation (merge, split, rotate)
- Form field filling

**Status**: ⚠️ Requires pypdf and pdfplumber installation

#### Word Documents (DOCX)
**Purpose**: Create and edit Word documents

**Test Commands:**
```bash
# Install dependencies
pip install python-docx

# Test installation
python3 -c "import docx; print('python-docx installed')"
```

**Usage in Copilot:**
```
@workspace using docx skill, create a Word document with headers and tables
```

**Expected Results:**
- Word document creation
- Formatting and styles
- Tracked changes support

**Status**: ⚠️ Requires python-docx installation

#### PowerPoint Presentations (PPTX)
**Purpose**: Create and edit PowerPoint presentations

**Test Commands:**
```bash
# Install dependencies
pip install python-pptx

# Test installation
python3 -c "import pptx; print('python-pptx installed')"

# View helper scripts
ls -la document-skills/pptx/scripts/
```

**Usage in Copilot:**
```
@workspace using pptx skill, create a presentation with charts
```

**Expected Results:**
- PowerPoint creation and editing
- Layout and template support
- Chart and table support

**Status**: ⚠️ Requires python-pptx installation

#### Excel Spreadsheets (XLSX)
**Purpose**: Create and edit Excel spreadsheets

**Test Commands:**
```bash
# Install dependencies
pip install openpyxl

# Test installation
python3 -c "import openpyxl; print('openpyxl installed')"
```

**Usage in Copilot:**
```
@workspace using xlsx skill, create a spreadsheet with formulas
```

**Expected Results:**
- Excel creation and editing
- Formula support
- Data analysis capabilities

**Status**: ⚠️ Requires openpyxl installation

---

### 5. Communication Skills

#### Brand Guidelines
**Purpose**: Apply Anthropic brand standards

**Test Commands:**
```bash
# Read the guidelines
cat brand-guidelines/SKILL.md
```

**Usage in Copilot:**
```
@workspace apply brand-guidelines to this artifact
```

**Expected Results:**
- Brand color palettes
- Typography guidelines
- No executable code

**Status**: ✅ Documentation ready

#### Internal Communications
**Purpose**: Write internal communications

**Test Commands:**
```bash
# Read the templates
cat internal-comms/SKILL.md
```

**Usage in Copilot:**
```
@workspace using internal-comms, write a status update
```

**Expected Results:**
- Communication templates
- Writing guidelines
- No executable code

**Status**: ✅ Templates ready

---

### 6. Theme Skills

#### Theme Factory
**Purpose**: Apply professional themes to artifacts

**Test Commands:**
```bash
# View available themes
ls -la theme-factory/themes/
cat theme-factory/themes/modern-minimalist.md
```

**Usage in Copilot:**
```
@workspace apply ocean-depths theme from theme-factory
```

**Expected Results:**
- 10+ pre-defined themes
- Color palettes and design specs
- No executable code

**Status**: ✅ Themes ready

---

## Quick Start Testing Priority

### Tier 1: Zero Dependencies (Test First)
1. ✅ skill-creator - Works perfectly
2. ✅ template-skill - Simple template
3. ✅ algorithmic-art - HTML/JS only
4. ✅ brand-guidelines - Documentation
5. ✅ internal-comms - Templates
6. ✅ theme-factory - Themes
7. ✅ canvas-design - Documentation
8. ✅ slack-gif-creator - Specifications
9. ✅ artifacts-builder - Templates

### Tier 2: Simple Dependencies (Test Second)
1. ⚠️ webapp-testing - Requires Playwright
2. ⚠️ mcp-builder - Requires MCP SDK

### Tier 3: Document Processing (Test Third)
1. ⚠️ pdf - Requires pypdf, pdfplumber
2. ⚠️ docx - Requires python-docx
3. ⚠️ pptx - Requires python-pptx
4. ⚠️ xlsx - Requires openpyxl

---

## Environment Setup Script

Create this script to set up all dependencies at once:

```bash
#!/bin/bash
# setup_skills_environment.sh

echo "Setting up Skills for Copilot environment..."

# Python dependencies for document skills
echo "Installing Python document processing libraries..."
pip install pypdf pdfplumber pdf2image python-docx python-pptx openpyxl

# Playwright for web testing
echo "Installing Playwright..."
pip install playwright
playwright install chromium

# MCP SDK (Python)
echo "Installing MCP SDK..."
pip install fastmcp

echo "Setup complete! All skills are ready to use."
```

**Usage:**
```bash
chmod +x setup_skills_environment.sh
./setup_skills_environment.sh
```

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'pypdf'`
**Solution**: `pip install pypdf`

**Issue**: `playwright executable not found`
**Solution**: `playwright install chromium`

**Issue**: `Permission denied` when running scripts
**Solution**: `chmod +x script_name.py`

**Issue**: Python version too old
**Solution**: Install Python 3.8+

### Getting Help

1. Check the skill's SKILL.md for specific instructions
2. Review reference documentation in skill's reference/ directory
3. Check LICENSE.txt for usage terms
4. Review examples/ directory if present

---

## Next Steps

After testing:
1. Identify which skills are most useful for your workflow
2. Install only the dependencies you need
3. Create custom adaptations for your specific use cases
4. Contribute improvements back to the repository

---

## License Notes

- **Example Skills**: Apache 2.0 (open source)
- **Document Skills**: Proprietary (see individual LICENSE.txt files)
- **Meta Skills**: Apache 2.0 (open source)

See individual skill directories for specific license information.
