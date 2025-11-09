# Community Skills

This directory contains skills discovered from community forks of the original anthropics/skills repository.

## Source

These skills were collected from the top 10 most active forks of https://github.com/anthropics/skills

## Fork Analysis Summary

**Forks Analyzed**: 10  
**New Skills Found**: ~67 unique skills  
**Skills Imported**: 21 (high and medium priority)

### Source Repositories

1. **Bantarus/skills** - 17 new skills (ML/Desktop focused)
2. **aabrius/skills** - 13 new skills (Development guidelines)
3. **btli/skills** - 32 new skills (Cloud/Dev tools)
4. **SimWerx/claude_skills** - 5 new skills (Research/Documentation)

## Skills Included

### High Priority - General Purpose (10)

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
