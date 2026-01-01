# Indexing State

> Tracks progress for large codebase indexing operations.

## Operation: Codebase Indexing

### Status
| Field | Value |
|-------|-------|
| Status | not_started |
| Phase | - |
| Progress | 0/0 (0%) |
| Started | - |
| Last Updated | - |

### Configuration
| Field | Value |
|-------|-------|
| Target Path | <!-- root path being indexed --> |
| Depth Target | L0 |
| Include Patterns | `**/*.{ts,tsx,js,jsx,py,go,rs,java}` |
| Exclude Patterns | `node_modules/`, `dist/`, `.git/` |
| Batch Size | 50 |

---

## Progress by Directory

| Directory | Files | L0 | L1 | L2+ | Status |
|-----------|-------|----|----|-----|--------|
| src/ | 0 | 0 | 0 | 0 | pending |
| tests/ | 0 | 0 | 0 | 0 | pending |
| lib/ | 0 | 0 | 0 | 0 | pending |

---

## Checkpoint

| Field | Value |
|-------|-------|
| Last Directory | - |
| Last File | - |
| Batch | 0 of 0 |
| Files Indexed | 0 |

---

## Statistics

| Metric | Value |
|--------|-------|
| Total Files Discovered | 0 |
| Files Indexed | 0 |
| Concepts Extracted | 0 |
| Cross-References Created | 0 |
| Errors Encountered | 0 |

---

## Depth Distribution

| Depth | Count | Percentage |
|-------|-------|------------|
| L0 (Discovery) | 0 | 0% |
| L1 (Triage) | 0 | 0% |
| L2 (Summary) | 0 | 0% |
| L3 (Deep) | 0 | 0% |

---

## Errors

| File | Error | Resolution |
|------|-------|------------|
| | | |

---

## Pending Batches

| Batch | Files | Status |
|-------|-------|--------|
| | | |

---

## Completed Batches

| Batch | Files | Duration | Result |
|-------|-------|----------|--------|
| | | | |

---

## History

| Date | Action | Result |
|------|--------|--------|
| | | |

---

## Resume Info

To resume interrupted indexing:
```
/index --resume
```

To restart from scratch:
```
/index --force-new
```

---

## Cross-References

- **Created by**: `/index`, `/initialize`
- **Skills used**: codebase-navigator
- **Agents used**: explorer
- **Updates**: `_registry.md`, `_concepts.md`, `_index.md`
