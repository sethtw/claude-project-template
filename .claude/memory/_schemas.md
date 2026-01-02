# Progressive Depth Schemas

> Defines the L0-L3 extraction depth system for managing context across large codebases.

## Core Principle

**Index shallow, deepen on demand.** Not everything needs full analysis upfront.

---

## Extraction Depths

| Depth | Name | Description | Token Cost | When to Use |
|-------|------|-------------|------------|-------------|
| L0 | Discovery | File exists, type identified | ~10 | Initial scan, everything |
| L1 | Triage | 1-2 sentence summary | ~50 | Quick reference, navigation |
| L2 | Summary | Key concepts, relationships | ~200 | Working context |
| L3 | Deep | Full detail, excerpts | ~500+ | Active development |

---

## Document Templates

### L0 Entry (Discovery)

```markdown
## DOC_XXX: <filename>

| Field | Value |
|-------|-------|
| Path | <relative path> |
| Type | code / doc / config / test / asset |
| Language | typescript / python / markdown / json / ... |
| Lines | <count> |
| Last Modified | <date> |
| Depth | L0 |
```

### L1 Entry (Triage)

```markdown
## DOC_XXX: <filename>

| Field | Value |
|-------|-------|
| Path | <relative path> |
| Type | <type> |
| Language | <language> |
| Lines | <count> |
| Last Modified | <date> |
| Depth | L1 |

### Summary
<1-2 sentences describing purpose>

### Exports
- <public function/class 1>
- <public function/class 2>

### Dependencies
- <import 1>
- <import 2>
```

### L2 Entry (Summary)

```markdown
## DOC_XXX: <filename>

| Field | Value |
|-------|-------|
| Path | <relative path> |
| Type | <type> |
| Depth | L2 |
| Complexity | low / medium / high |
| Last Analyzed | <date> |

### Summary
<1-2 sentences>

### Key Concepts
- [[Concept1]] - brief explanation
- [[Concept2]] - brief explanation

### Related Documents
- DOC_XXX (<filename>) - relationship
- DOC_YYY (<filename>) - relationship

### Patterns Used
- <pattern name> - where/why

### Public Interface
<key exports with signatures>
```

### L3 Entry (Deep)

```markdown
## DOC_XXX: <filename>

| Field | Value |
|-------|-------|
| Path | <relative path> |
| Type | <type> |
| Depth | L3 |
| Complexity | <level> |
| Last Deep Analysis | <date> |

### Summary
<1-2 sentences>

### Full Outline
1. <section 1>
   - <subsection>
2. <section 2>

### Key Code Excerpts
\`\`\`typescript
// Critical logic at line XX
<code excerpt>
\`\`\`

### Integration Points
- Calls: <what this calls>
- Called by: <what calls this>
- Events: <emits/listens>

### Known Issues / TODOs
- [ ] <issue or todo found in code>

### Edge Cases
- <edge case 1>
- <edge case 2>
```

---

## Source Code Depth Applications

| Depth | What's Captured | Model | Time |
|-------|-----------------|-------|------|
| L0 | File exists, language, line count | haiku | <1s |
| L1 | Exports, imports, public interface | haiku | ~2s |
| L2 | Patterns, complexity, relationships | sonnet | ~10s |
| L3 | Full analysis, logic flow, edge cases | sonnet/opus | ~30s |

---

## Depth Promotion Triggers

### Automatic Promotion Rules

| From | To | Trigger | Command |
|------|----|---------|---------|
| - | L0 | New file discovered | `/index` |
| L0 | L1 | File referenced in 3+ sessions | Automatic |
| L0 | L1 | High-complexity file identified | `/analyze` |
| L0 | L1 | File modified this session | Hooks |
| L1 | L2 | User requests deep analysis | `/deep <path>` |
| L1 | L2 | File critical to current feature | `/architect` |
| L2 | L3 | User requests exhaustive analysis | `/deep --l3 <path>` |
| L2 | L3 | File has integration issues | `/implement` (Stage 5) |

### Command-Triggered Promotions

| Command | Promotion Behavior |
|---------|-------------------|
| `/index` | All new files → L0 |
| `/analyze` | Suggests files for promotion, outputs to active_context.md |
| `/deep <path>` | Specified files → L2 (default) or L3 (--l3 flag) |
| `/architect` | May promote integration point files → L2 |
| `/implement` | May promote files with issues → L2/L3 during Fix stage |

### /analyze Recommendations

When `/analyze` identifies complexity hotspots, it outputs to `active_context.md`:

```markdown
## Latest Analysis Results (from /analyze)
**Analyzed**: <timestamp>

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
- Integration points: <list>
- Pattern violations: <list>
- Tech debt locations: <list>
```

### Manual Promotion
- Explicitly request deeper analysis with `/deep`
- Files involved in current task are auto-promoted by hooks
- Files with high complexity scores identified by `/analyze`

---

## Depth Demotion (Archival)

To manage registry size, old entries can be demoted:
- L3 → L2 after 30 days without access
- L2 → L1 after 60 days without access
- L1 entries retained indefinitely
- L0 entries never deleted (discovery record)

---

## ID Allocation

Documents use sequential IDs: DOC_001, DOC_002, etc.

### Reserved Ranges
| Scan Type | Range | Purpose |
|-----------|-------|---------|
| Memory files | DOC_001-DOC_099 | .claude/memory/ |
| Source code | DOC_100-DOC_4999 | src/, lib/ |
| Tests | DOC_5000-DOC_6999 | tests/, __tests__/ |
| Config | DOC_7000-DOC_7999 | Config files |
| Docs | DOC_8000-DOC_8999 | Documentation |
| Other | DOC_9000+ | Everything else |

### Next Available ID
DOC_001

---

## Cross-References

- **Skills use this**: codebase-navigator, feature-integration
- **Commands reference this**: /initialize, /index, /deep, /analyze
- **Updated by**: /initialize, /index, /deep commands
