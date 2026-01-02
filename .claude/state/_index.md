# State Tracking

> Tracks progress for long-running operations that span multiple sessions.

## Active States



| Operation | State File | Status | Progress | Started |
|------|------|------|------|------|
| Current Plan | .claude\state\current_plan.md | pending | - | - |
| Implement | .claude\state\implement_state.md | not_started | 0/5 (0%) | - |
---

## Session Tracking

### Current Session
| Metric | Value |
|--------|-------|
| Session ID | - |
| Started | - |
| Documents Touched | 0 |
| Commands Run | 0 |

### Session History
| Session | Date | Focus | Outcome |
|---------|------|-------|---------|
| (none yet) | - | - | - |

---

## State Files

| File | Purpose | Created By |
|------|---------|------------|
| `current_plan.md` | **Active implementation plan** | `/architect` |
| `refactor_state.md` | Multi-file refactoring progress | `/refactor` |
| `migration_state.md` | Version/framework migration progress | `/migrate` |
| `review_state.md` | Ongoing code review findings | `/code-review` |
| `index_state.md` | Large codebase indexing progress | `/index` |
| `implement_state.md` | Staged implementation progress | `/implement` |
| `initialize_state.md` | Comprehensive initialization progress | `/initialize` |

---

## Plan Handoff Workflow

```
/architect <feature>     →  Creates current_plan.md
                         →  Suggests /implement --planned

/implement --planned     →  Reads current_plan.md
                         →  Skips Stage 2 (planning)
                         →  Executes with Sonnet
                         →  Saves ~$0.30 per implementation
```

---

## Usage

### Resume an Operation
```
/refactor --resume
/migrate --resume
```

### Check Status
```
/context --operations
```

### Clear State
```
/refactor --clear-state
/migrate --clear-state
```

---

## State File Format

All state files follow this structure:

```markdown
## Operation: <name>

### Status
| Field | Value |
|-------|-------|
| Status | not_started / in_progress / paused / complete / failed |
| Phase | Current phase name |
| Progress | X/Y (X%) |
| Started | <timestamp> |
| Last Updated | <timestamp> |

### Checkpoint
| Field | Value |
|-------|-------|
| Commit | <hash> |
| Branch | <name> |
| Last File | <path> |
| Batch | X of Y |

### Pending Items
| Item | Status |
|------|--------|
| <remaining work> | pending |

### Completed Items
| Item | Result | Timestamp |
|------|--------|-----------|
| <completed work> | success/failed | <time> |

### Rollback Info
| Field | Value |
|-------|-------|
| Backup Branch | <name> |
| Restore Command | <command> |

### History
| Date | Action | Result |
|------|--------|--------|
| | | |
```

---

## Recovery Procedures

### If Operation Failed
1. Read state file for last checkpoint
2. Check backup branch exists
3. Determine which items completed
4. Resume from last successful item

### If State Corrupted
1. Delete state file
2. Start fresh with `--force-new`
3. Operation will re-analyze current state

---

## Cross-References

- **Commands**: `/refactor`, `/migrate`, `/code-review`, `/review`, `/index`, `/initialize`, `/cleanup`
- **Memory**: Updates `active_context.md` with operation status
- **Pattern**: See `development.md` for state management patterns
