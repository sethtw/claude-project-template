# /initialize - Comprehensive Codebase Initialization

> Scan an existing codebase and populate ALL memory files, CLAUDE.md, and context for optimal use.

## Purpose

One-time comprehensive initialization that:
1. Discovers project structure, tech stack, and patterns
2. Populates all memory files with project-specific content
3. Creates L0/L1 registry entries for all files
4. Configures rules based on detected languages
5. Sets up CLAUDE.md with project context
6. Prepares the knowledge base for immediate productive use

## Usage

```
/initialize                     # Full initialization
/initialize --quick             # Fast mode (L0 only, skip deep analysis)
/initialize --update            # Update existing (preserve manual edits)
/initialize --force             # Overwrite everything
```

## Process Overview

```
Phase 1: Discovery (haiku - parallel)
    ↓
Phase 2: Tech Stack Analysis (haiku)
    ↓
Phase 3: Structure Analysis (sonnet)
    ↓
Phase 4: Pattern Detection (sonnet)
    ↓
Phase 5: Memory Population (sonnet)
    ↓
Phase 6: Registry Creation (haiku - parallel)
    ↓
Phase 7: Key File Analysis (sonnet)
    ↓
Phase 8: Finalization (haiku)
```

---

## Phase 1: Discovery (haiku - parallel)

**Goal**: Enumerate all files and gather basic statistics.

### Parallel Agents

```
Task(subagent_type=explorer, model=haiku, prompt="
  Scan entire codebase. Return:
  - Total file count by extension
  - Directory structure (2 levels deep)
  - Largest directories by file count
")

Task(subagent_type=explorer, model=haiku, prompt="
  Find all configuration files:
  - package.json, pyproject.toml, Cargo.toml, go.mod
  - tsconfig.json, webpack.config.js, vite.config.ts
  - .env.example, docker-compose.yml
  - CI/CD configs (.github/workflows, .gitlab-ci.yml)
")

Task(subagent_type=explorer, model=haiku, prompt="
  Find all documentation:
  - README.md, CONTRIBUTING.md, CHANGELOG.md
  - docs/ directory contents
  - API documentation files
")

Task(subagent_type=explorer, model=haiku, prompt="
  Find test files:
  - *.test.ts, *.spec.ts, *_test.go, test_*.py
  - __tests__/ directories
  - Test configuration files
")
```

### Output
```markdown
## Discovery Results
| Metric | Value |
|--------|-------|
| Total Files | X |
| Source Files | Y |
| Test Files | Z |
| Config Files | N |
| Documentation | M |
```

---

## Phase 2: Tech Stack Analysis (haiku)

**Goal**: Identify languages, frameworks, and dependencies.

### Detection Logic

```typescript
// Language detection by file extension
const languages = detectLanguages(files);
// Primary: most files, Secondary: supporting

// Framework detection by config/imports
const frameworks = detectFrameworks(configFiles);
// React, Vue, Express, FastAPI, etc.

// Dependency analysis
const deps = analyzeDependencies(packageFiles);
// Runtime vs dev dependencies
```

### Config File Analysis

| File | Extracts |
|------|----------|
| `package.json` | name, scripts, dependencies, engines |
| `tsconfig.json` | strict mode, paths, target |
| `pyproject.toml` | python version, dependencies |
| `docker-compose.yml` | services, databases |
| `.env.example` | required environment variables |

### Output → `project_brief.md`

```markdown
## Tech Stack
| Layer | Technology | Version |
|-------|------------|---------|
| Language | TypeScript | 5.x |
| Runtime | Node.js | 20.x |
| Framework | Express | 4.x |
| Database | PostgreSQL | 15 |
| Testing | Jest | 29.x |
| Build | Vite | 5.x |
```

---

## Phase 3: Structure Analysis (sonnet)

**Goal**: Understand architectural patterns from directory structure.

### Structure Detection

```
# Detect common patterns
src/
├── api/          → API Layer detected
├── services/     → Service Layer detected
├── models/       → Data Layer detected
├── utils/        → Utilities detected
└── types/        → Type definitions detected

# Or monorepo patterns
packages/
├── api/          → Monorepo: API package
├── web/          → Monorepo: Web package
└── shared/       → Monorepo: Shared package
```

### Entry Point Detection

1. Find main entry: `src/index.ts`, `main.py`, `cmd/main.go`
2. Find route definitions
3. Find configuration loading
4. Find database connections

### Output → `patterns/architecture.md`

```markdown
## Project Structure
### Detected Pattern: Layered Architecture

\`\`\`
src/
├── api/          # HTTP handlers
├── services/     # Business logic
├── repositories/ # Data access
├── models/       # Domain models
└── config/       # Configuration
\`\`\`

### Layer Dependencies
API → Services → Repositories → Database
```

---

## Phase 4: Pattern Detection (sonnet)

**Goal**: Identify coding patterns, conventions, and standards.

### Pattern Categories

**Error Handling**
- Custom error classes?
- Error middleware?
- Result types?

**Logging**
- Logger library?
- Log levels used?
- Structured logging?

**Testing**
- Test framework?
- Mocking approach?
- Coverage configuration?

**Authentication**
- JWT? Sessions? OAuth?
- Middleware patterns?

**Database**
- ORM? Query builder? Raw SQL?
- Migration tool?
- Connection pooling?

### Code Sampling

Read 3-5 representative files from each layer:
- Most imported files (central modules)
- Largest files (complex logic)
- Entry points (patterns established)

### Output → Multiple Files

**`patterns/architecture.md`** - Error handling, config patterns
**`patterns/testing.md`** - Test conventions detected
**`patterns/development.md`** - Workflow patterns observed

---

## Phase 5: Memory Population (sonnet)

**Goal**: Fill all memory files with discovered information.

### Files Updated

| File | Content Source |
|------|----------------|
| `project_brief.md` | Tech stack, structure, commands |
| `product_context.md` | README, docs analysis |
| `active_context.md` | Initial session state |
| `progress.md` | Roadmap from TODO/issues |
| `patterns/architecture.md` | Detected patterns |
| `patterns/testing.md` | Test patterns |
| `patterns/known_issues.md` | TODO comments, FIXME |
| `system_patterns.md` | Skills/agents relevant to stack |

### CLAUDE.md Updates

```markdown
# CLAUDE.md

## Quick Reference
| Resource | Purpose |
|----------|---------|
| @.claude/memory/_index.md | Knowledge base navigation |
| @.claude/memory/project_brief.md | [AUTO-POPULATED] |

## Project: [Detected Name]

[Auto-generated project description from README]

## Development Commands
\`\`\`bash
# [Extracted from package.json scripts]
npm run dev      # Start development server
npm test         # Run tests
npm run build    # Production build
\`\`\`

## Key Directories
- `src/api/` - API endpoints
- `src/services/` - Business logic
[... auto-detected ...]
```

---

## Phase 6: Registry Creation (haiku - parallel)

**Goal**: Create L0 entries for all source files.

### Parallel Indexing

```
Task(subagent_type=explorer, model=haiku, prompt="Index src/ - create L0 entries")
Task(subagent_type=explorer, model=haiku, prompt="Index tests/ - create L0 entries")
Task(subagent_type=explorer, model=haiku, prompt="Index config files - create L0 entries")
Task(subagent_type=explorer, model=haiku, prompt="Index docs/ - create L0 entries")
```

### Output → `_registry.md`

Populated with all files at L0 depth.

---

## Phase 7: Key File Analysis (sonnet)

**Goal**: Promote critical files to L1/L2 for immediate usefulness.

### Auto-Promote to L1

- Entry points (`src/index.ts`, `main.py`)
- Main configuration files
- Core service files (most imported)
- Base model/entity files
- Test setup files

### Auto-Promote to L2

- README.md (full analysis)
- Main API routes file
- Primary database models
- Authentication module

### Concept Extraction

From L2 files, extract key concepts:
- Domain entities
- Core services
- Integration points

### Output → `_registry.md`, `_concepts.md`

Updated with L1/L2 entries and initial concepts.

---

## Phase 8: Finalization (haiku)

**Goal**: Validate, report, and prepare for use.

### Validation Checks

- [ ] All memory files have content
- [ ] Registry has entries
- [ ] CLAUDE.md updated
- [ ] No broken cross-references
- [ ] Rules match detected languages

### Dynamic Rule Creation

Based on detected languages, ensure rules exist:

| Language | Rule File |
|----------|-----------|
| TypeScript | `rules/typescript.md` |
| Python | `rules/python.md` (create if needed) |
| Go | `rules/go.md` (create if needed) |
| Rust | `rules/rust.md` (create if needed) |

### Session Initialization

Update `active_context.md`:
```markdown
## Current Focus
| Field | Value |
|-------|-------|
| Status | Initialized |
| Date | [today] |
| Working On | Ready for first task |
| Branch | [detected branch] |

## Initialization Summary
- Indexed X files
- Analyzed Y key files
- Extracted Z concepts
- Detected: [tech stack summary]
```

---

## Output Format

```markdown
# Initialization Complete

## Project Summary
| Field | Value |
|-------|-------|
| Name | my-project |
| Type | Web API |
| Language | TypeScript |
| Framework | Express + React |
| Database | PostgreSQL |

## Knowledge Base Status
| Metric | Count |
|--------|-------|
| Files Indexed (L0) | 150 |
| Files Analyzed (L1) | 25 |
| Files Deep (L2) | 8 |
| Concepts Extracted | 15 |

## Memory Files Updated
- [x] project_brief.md - Tech stack, structure
- [x] product_context.md - From README
- [x] active_context.md - Session initialized
- [x] patterns/architecture.md - Detected patterns
- [x] patterns/testing.md - Test conventions
- [x] _registry.md - 150 entries
- [x] _concepts.md - 15 concepts
- [x] CLAUDE.md - Project-specific

## Detected Patterns
- Layered architecture (API → Service → Repository)
- JWT authentication
- Jest testing with mocks
- PostgreSQL with Prisma ORM

## Recommended Next Steps
1. Review `project_brief.md` for accuracy
2. Add business context to `product_context.md`
3. Run `/deep src/services/` for service layer analysis
4. Start working with full context available

## Self-Assessment
| Check | Status |
|-------|--------|
| All files populated | YES |
| Tech stack detected | YES |
| Patterns identified | YES |
| Registry created | YES |
| Ready for use | YES |

Confidence: High
```

---

## Model Selection

| Phase | Model | Rationale |
|-------|-------|-----------|
| 1. Discovery | haiku | Fast file enumeration |
| 2. Tech Stack | haiku | Config file parsing |
| 3. Structure | sonnet | Architectural understanding |
| 4. Patterns | sonnet | Code pattern recognition |
| 5. Population | sonnet | Content generation |
| 6. Registry | haiku | Bulk L0 creation |
| 7. Key Files | sonnet | Deep analysis |
| 8. Finalization | haiku | Validation, cleanup |

**Escalate to opus** if:
- Monorepo with 5+ packages
- Multiple languages detected
- Complex architecture patterns

---

## Autonomy Settings

- Scan all files without confirmation
- Create/update memory files automatically
- Generate registry entries automatically
- Create missing rule files for detected languages
- Only pause for:
  - Conflicts with existing manual edits (--update mode)
  - Ambiguous tech stack detection
  - Missing critical files (no entry point found)

---

## Skills Used

- `codebase-navigator` - File discovery
- `feature-integration` - Understanding connections
- `api-design` - API pattern detection
- `database-patterns` - Data layer analysis

## Agents Used

- `explorer` (haiku) - Parallel file scanning
- `analyzer` (sonnet) - Deep pattern analysis

---

## State Tracking

For large codebases (>500 files), creates `state/initialize_state.md`:

```markdown
## Operation: Initialize

### Status
| Field | Value |
|-------|-------|
| Status | in_progress |
| Phase | 4 of 8 |
| Progress | 50% |

### Completed Phases
- [x] Phase 1: Discovery
- [x] Phase 2: Tech Stack
- [x] Phase 3: Structure
- [ ] Phase 4: Patterns (current)
- [ ] Phase 5: Population
- [ ] Phase 6: Registry
- [ ] Phase 7: Key Files
- [ ] Phase 8: Finalization
```

Resume with: `/initialize --resume`

---

## Comparison to Built-in /init

| Feature | Built-in /init | /initialize |
|---------|----------------|-------------|
| Creates CLAUDE.md | Yes | Yes + populates |
| Scans structure | Basic | Comprehensive |
| Detects patterns | No | Yes |
| Creates registry | No | Yes (L0-L2) |
| Extracts concepts | No | Yes |
| Populates memory | No | All files |
| Multi-phase | No | 8 phases |
| Resumable | No | Yes |
| Model tiering | No | haiku/sonnet/opus |

---

## Error Handling

### No Entry Point Found
```markdown
Warning: Could not detect main entry point.
Please specify: /initialize --entry src/main.ts
```

### Multiple Frameworks
```markdown
Detected multiple frameworks:
- Express (backend)
- React (frontend)

Treating as: Full-stack monorepo
```

### Existing Memory Files
```markdown
Found existing memory files with content.
Options:
- /initialize --update (preserve manual edits)
- /initialize --force (overwrite all)
```

---

## Cross-References

- **Runs**: `/index` internally for registry creation
- **Runs**: `/deep` internally for key file analysis
- **Updates**: All memory files
- **Creates**: Language-specific rules if missing
- **Prepares**: System for immediate productive use
