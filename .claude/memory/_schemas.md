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

### Automatic (via commands)
| Trigger | Promotion |
|---------|-----------|
| `/index` | Everything → L0 |
| `/analyze` | Frequently-touched files → L1 |
| `/deep <path>` | Specified files → L2 or L3 |

### Manual
- Explicitly request deeper analysis
- Files involved in current task
- Files with high complexity scores

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
