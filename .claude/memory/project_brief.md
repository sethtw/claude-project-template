# Project Brief

> High-level project overview. Read this first when new to the project.

## Overview

(Project description not yet configured. Run `/initialize` to set up.)

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Language | (not set) | - |
| Framework | (not set) | - |
| Database | (not set) | - |
| Testing | (not set) | - |
| Build | (not set) | - |

## Architecture Highlights

### Structure
```
src/
├── api/          # API endpoints
├── services/     # Business logic
├── models/       # Data models
├── utils/        # Shared utilities
└── types/        # TypeScript types
```

### Key Patterns
- (none documented yet)

## Key Features

| Feature | Status | Description |
|---------|--------|-------------|
| (none) | - | - |

## Development Setup

### Prerequisites
- Node.js >= 18

### Quick Start
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test
```

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Database connection string |

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch |
| `feature/*` | New features |
| `fix/*` | Bug fixes |

## MCP Servers

See `.mcp.json` for configured servers:
- `filesystem` - Local file access
- `github` - GitHub integration (requires `GITHUB_TOKEN`)

---

## Update Protocol

| Source | Action | Automatic |
|--------|--------|-----------|
| /initialize | Creates initial content, detects tech stack | Yes |
| /analyze | Updates architecture highlights, key patterns | Yes |
| /implement | May update key features on completion | Yes |
| Manual | User updates for project-specific details | No |

---

## Related Documentation

- [Active Context](active_context.md) - Current session work
- [Progress](progress.md) - Roadmap and milestones
- [System Patterns](system_patterns.md) - Development patterns index
- [Knowledge Base Index](_index.md) - Full navigation
