# Community Skills

This directory contains skills discovered from community forks of the original anthropics/skills repository.

## Source

These skills were collected from the top forks of https://github.com/anthropics/skills

## Fork Analysis Summary

**Total Forks Analyzed**: 19 (10 round 1 + 9 round 2)
**Total New Skills Found**: ~75 unique skills  
**Skills Imported**: 28 (21 round 1 + 7 round 2)

### Source Repositories

#### Round 1 - High Activity Forks
1. **Bantarus/skills** - 17 new skills (ML/Desktop focused)
2. **aabrius/skills** - 13 new skills (Development guidelines)
3. **btli/skills** - 32 new skills (Cloud/Dev tools)
4. **SimWerx/claude_skills** - 5 new skills (Research/Documentation)

#### Round 2 - Star-Rated Forks
1. **PixelML/skills** (2 stars) - 1 new skill (NotebookLM)
2. **chyax98/skills** - 3 new skills (Code analysis, mindmaps, slides)
3. **rm2thaddeus/skills** - 2 new skills (Document handling)
4. **amicoda1/ClaudeSkills** - 1 new skill (MarkItDown)
5. **mateusztylec/awesome-llm-skills** (1 star) - 1 new skill (Notion)

## Skills Included

### Round 1 - High Priority (10 skills)

#### Development Tools
- **debugging** (btli) - Debugging strategies and techniques
- **docker** (btli) - Docker containerization workflows
- **agent-builder** (btli) - Build AI agents and automation
- **chrome-devtools** (btli) - Chrome DevTools integration

#### Meta Skills
- **claude-code-slash-commands** (aabrius) - Slash commands for Claude Code
- **brainstorming** (aabrius) - Structured brainstorming techniques
- **writing-plans** (aabrius) - Plan writing and documentation
- **fastmcp-builder** (aabrius) - FastMCP server development
- **using-git-worktrees** (aabrius) - Git worktrees workflow
- **problem-solving** (btli) - Systematic problem-solving approach

#### Research & Documentation
- **research-synthesis** (SimWerx) - Research synthesis and analysis
- **data-interrogation** (SimWerx) - Data analysis and questioning
- **executive-memo** (SimWerx) - Executive memo writing
- **technical-docs** (SimWerx) - Technical documentation

### Medium Priority - Domain Specific (11)

#### Web Development
- **fastapi-dev-guidelines** (aabrius) - FastAPI development best practices
- **react-shadcn-guidelines** (aabrius) - React + shadcn/ui patterns
- **nextjs** (btli) - Next.js development guide
- **tailwindcss** (btli) - Tailwind CSS utilities and patterns
- **shadcn-ui** (btli) - shadcn/ui component library

#### Cloud & Infrastructure
- **gcloud** (btli) - Google Cloud Platform tools
- **mongodb** (btli) - MongoDB database operations

### Round 2 - High Priority (7 skills)

#### Knowledge & Research Tools
- **notebooklm** (PixelML) - Google NotebookLM integration for document analysis
- **notion-knowledge-capture** (mateusztylec) - Notion knowledge management

#### Content Generation
- **mindmap-generator** (chyax98) - Convert text/files into structured Markdown mindmaps
- **slides-generator** (chyax98) - Automated presentation generation

#### Development Tools
- **code-analyzer** (chyax98) - Code analysis and review (Chinese language)

#### Document Processing
- **markitdown** (amicoda1) - Microsoft MarkItDown integration
- **document_handling** (rm2thaddeus) - Document handling workflows

## Skills Not Yet Imported

### Lower Priority - Specialized (see FORK_ANALYSIS.md for full list)

#### Machine Learning / AI (13 skills from Bantarus and btli)
- ComfyUI, Flux, GGUF quantization, HuggingFace, PyTorch, Gemini APIs

#### Desktop Development (6 skills from Bantarus)
- Tauri, PyO3, PyInstaller, Unity UI Toolkit, Python desktop backends

#### Additional Cloud Tools (4 skills from btli)
- Cloudflare Workers/R2/Browser Rendering, PostgreSQL

#### Additional Web Dev (5 skills from aabrius and btli)
- Hono.js, NestJS, Shopify, Better Auth, Turborepo

#### Additional Dev Tools (7 skills from btli)
- FFmpeg, ImageMagick, Repomix, OpenAPI, Image Downloader, Docs Seeker

## Usage

These community skills work the same way as the core skills:

### In GitHub Copilot
```
@workspace using debugging skill, help me debug this issue
@workspace using docker skill, create a Dockerfile
@workspace using brainstorming skill, help me brainstorm ideas
```

### In Claude Code
```
Use the problem-solving skill to work through this challenge
Use the research-synthesis skill to analyze these papers
```

## Testing Status

- [ ] debugging
- [ ] docker  
- [ ] problem-solving
- [ ] agent-builder
- [ ] claude-code-slash-commands
- [ ] brainstorming
- [ ] writing-plans
- [ ] fastmcp-builder
- [ ] using-git-worktrees
- [ ] research-synthesis
- [ ] data-interrogation
- [ ] executive-memo
- [ ] technical-docs
- [ ] fastapi-dev-guidelines
- [ ] react-shadcn-guidelines
- [ ] nextjs
- [ ] tailwindcss
- [ ] shadcn-ui
- [ ] gcloud
- [ ] mongodb
- [ ] chrome-devtools

**Round 2 Skills (7)**
- [ ] notebooklm
- [ ] notion-knowledge-capture
- [ ] mindmap-generator
- [ ] slides-generator
- [ ] code-analyzer
- [ ] markitdown
- [ ] document_handling

## License

These skills come from various authors in the community. Please check individual skill directories for license information. Most are likely Apache 2.0 or MIT, following the original repository's license.

## Attribution

Skills are attributed to their source repositories:
- **btli**: https://github.com/btli/skills
- **aabrius**: https://github.com/aabrius/skills
- **SimWerx**: https://github.com/SimWerx/claude_skills
- **Bantarus**: https://github.com/Bantarus/skills

Thank you to these community members for their contributions!

## Next Steps

1. Test each imported skill
2. Document dependencies
3. Create GitHub Copilot instructions for high-priority skills
4. Consider importing additional specialized skills based on needs
5. Contribute improvements back to source repositories

## Full Analysis

See `FORK_ANALYSIS.md` in the root directory for complete analysis of all 67 discovered skills.
