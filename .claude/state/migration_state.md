# Migration State

> Template for version/framework migration operations.

## Operation: (not started)

### Status
| Field | Value |
|-------|-------|
| Status | not_started |
| Phase | 1. Analysis |
| Progress | 0/5 phases (0%) |
| Started | - |
| Last Updated | - |

---

## Migration Details

### From
<!-- Current version/framework -->

### To
<!-- Target version/framework -->

### Breaking Changes
| Change | Impact | Migration Strategy |
|--------|--------|-------------------|
| | | |

---

## Phases

### Phase 1: Analysis
| Task | Status |
|------|--------|
| Identify deprecated APIs | pending |
| Find breaking changes | pending |
| Assess test coverage | pending |

### Phase 2: Preparation
| Task | Status |
|------|--------|
| Create backup branch | pending |
| Update dependencies | pending |
| Run compatibility checks | pending |

### Phase 3: Code Migration
| File | Status | Notes |
|------|--------|-------|
| | pending | |

### Phase 4: Testing
| Test Suite | Status | Pass/Fail |
|------------|--------|-----------|
| Unit | pending | |
| Integration | pending | |
| E2E | pending | |

### Phase 5: Verification
| Check | Status |
|-------|--------|
| All tests pass | pending |
| No new warnings | pending |
| Performance baseline met | pending |

---

## Checkpoint

| Field | Value |
|-------|-------|
| Commit | - |
| Branch | - |
| Last Phase | - |
| Last File | - |

---

## Rollback Info

| Field | Value |
|-------|-------|
| Backup Branch | - |
| Original Commit | - |
| Restore Command | `git checkout <branch>` |

---

## History

| Date | Phase | Action | Result |
|------|-------|--------|--------|
| | | | |

---

## Resume Instructions

To resume this migration:
```
/migrate --resume
```

To rollback:
```
git checkout <backup-branch>
```

To clear and restart:
```
/migrate --clear-state
/migrate <target>
```
