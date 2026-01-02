# Codebase Analyzer

Description: Comprehensive codebase analysis with parallel scanning

You are a Codebase Analyst. Task: Analyze "$ARGUMENTS" (or entire codebase if not specified).

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| File enumeration | `haiku` | Fast directory traversal |
| Pattern detection | `haiku` | Rule matching |
| Dependency analysis | `haiku` | Package scanning |
| Architecture understanding | `sonnet` | Design comprehension |
| Complexity assessment | `sonnet` | Semantic analysis |

## Parallel Analysis

Spawn parallel agents for comprehensive analysis:

```
# Launch parallel scans
Task(subagent_type=Explore, model=haiku, prompt="Analyze project structure and file organization...")
Task(subagent_type=Explore, model=haiku, prompt="Map all dependencies and their usage...")
Task(subagent_type=Explore, model=haiku, prompt="Identify code patterns and conventions...")
Task(subagent_type=Explore, model=haiku, prompt="Calculate complexity metrics...")
# Consolidate with sonnet for insights
```

## Analysis Categories

1. **Structure** - File organization, module boundaries
2. **Dependencies** - External packages, internal imports
3. **Patterns** - Design patterns, coding conventions
4. **Complexity** - Cyclomatic complexity, coupling metrics
5. **Tech Debt** - TODO/FIXME, outdated patterns
6. **Entry Points** - APIs, exports, main files

## Process

1. Enumerate all source files (haiku)
2. Launch parallel category scans
3. Build dependency graph
4. Calculate metrics
5. Identify patterns and anti-patterns
6. Synthesize findings (sonnet)
7. Update `active_context.md`

## Output

```markdown
## Codebase Analysis

### Overview
| Metric | Value |
|--------|-------|
| Files | X |
| Lines of Code | X |
| Languages | TypeScript, Python, ... |
| Framework | Next.js, ... |

### Structure
```
src/
├── components/  (X files)
├── services/    (X files)
├── utils/       (X files)
└── types/       (X files)
```

### Dependencies
| Package | Version | Usage |
|---------|---------|-------|
| react | ^18.0 | Core framework |
| ... | ... | ... |

### Patterns Detected
- ✅ Repository pattern in `services/`
- ✅ Dependency injection
- ⚠️ Mixed naming conventions
- ❌ God objects in `utils/helpers.ts`

### Complexity Hotspots
| File | Complexity | Issue |
|------|------------|-------|
| `auth/login.ts` | High | 15 conditions |
| `utils/parser.ts` | High | 200+ lines |

### Tech Debt
- [ ] 12 TODO comments
- [ ] 3 deprecated API usages
- [ ] Outdated test patterns

### Recommendations
1. Extract `utils/helpers.ts` into focused modules
2. Add TypeScript strict mode
3. Update deprecated APIs
```

## Self-Assessment

After analysis completes:

```markdown
### Self-Assessment
| Check | Status |
|-------|--------|
| All source files scanned | ✅/❌ |
| Dependencies mapped | ✅/❌ |
| Patterns identified | ✅/❌ |
| Complexity calculated | ✅/❌ |
| Tech debt catalogued | ✅/❌ |

**Coverage**: [Comprehensive/Partial/Surface]
**Confidence**: [High/Medium/Low]
```

## Autonomy

- Scan entire codebase without confirmation
- Do not ask before analyzing files
- Auto-update memory files with findings
- Output self-assessment after analysis completes

---

---

## Integration with User Journey

`/analyze` is the **intelligence layer** bridging discovery and planning:

```
Discovery Layer         Intelligence Layer        Planning Layer
─────────────────       ──────────────────       ────────────────
/initialize   ────┐
                  ├──→  /analyze  ────→  Suggests targets for /deep
/index        ────┘         │                          │
                            │                          ↓
                            └──→  Informs /architect with:
                                  • Complexity hotspots
                                  • Pattern violations
                                  • Integration points
                                  • Tech debt locations
```

### Structured Output for Downstream Commands

When analysis completes, output this section to `active_context.md`:

```markdown
## Latest Analysis Results (from /analyze)
**Analyzed**: <timestamp>
**Target**: <path or "entire codebase">

### Complexity Hotspots
| File | Complexity | Recommendation |
|------|------------|----------------|
| src/services/auth.ts | High | /deep for L2 analysis |
| src/api/routes.ts | Medium | Monitor for growth |

### Recommended /deep Targets
| File | Reason | Suggested Depth |
|------|--------|-----------------|
| src/services/auth.ts | High cyclomatic complexity | L2 |
| src/utils/parser.ts | Many integration points | L2 |

### Architecture Notes for /architect
- **Integration points**: <files that connect systems>
- **Pattern violations**: <deviations from established patterns>
- **Tech debt locations**: <files needing refactoring>
- **Risk areas**: <fragile or complex sections>

### Pre-Review Findings for /code-review
- **Security concerns**: <potential vulnerabilities>
- **Performance issues**: <bottlenecks identified>
- **Test coverage gaps**: <untested critical paths>
```

### Command Handoffs

| When | Then | Output |
|------|------|--------|
| Complexity hotspots found | Suggest `/deep` for specific files | "Recommended /deep Targets" section |
| Planning a feature | Provide context for `/architect` | "Architecture Notes" section |
| Pre-review check | Prepare findings for `/code-review` | "Pre-Review Findings" section |
| Files need deeper analysis | Promote to L1 in registry | Update `_registry.md` |

---

## Skills Used

- **codebase-navigator** - Efficient project exploration
- **performance-analysis** - Complexity and bottleneck detection
- **database-patterns** - Data layer analysis
- **feature-integration** - Understanding system connections

## Agents Used

- **explorer** (haiku) - Fast parallel file enumeration
- **analyzer** (sonnet) - Deep pattern analysis

## Memory Updates

- Updates `active_context.md` with structured analysis results
- May update `patterns/architecture.md` with discovered patterns
- Updates `_registry.md` if running L0 indexing
- May promote high-complexity files to L1 in `_registry.md`
- References `system_patterns.md` to compare with existing patterns

## Update Protocol

| Source | Action | Automatic |
|--------|--------|-----------|
| /analyze run | Outputs structured findings to active_context.md | Yes |
| /analyze run | May update patterns/architecture.md | Yes |
| /analyze run | May promote files in _registry.md | Yes |
| Manual | Reviewing and acting on recommendations | No |
