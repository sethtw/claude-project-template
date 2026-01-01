# State Tracking

This directory tracks progress for long-running operations that may span multiple sessions.

## Active States

| Operation | State File | Status | Progress |
|-----------|------------|--------|----------|
| (none) | - | - | - |

## State Files

| File | Purpose |
|------|---------|
| `refactor_state.md` | Multi-file refactoring progress |
| `migration_state.md` | Version/framework migration progress |
| `review_state.md` | Ongoing code review findings |

## Usage

State files are automatically created by commands like `/refactor` and `/migrate`.

To resume an operation:
```
/refactor --resume
/migrate --resume
```

To clear state:
```
/refactor --clear-state
```

## State File Format

```markdown
## Operation: <name>

### Status
| Field | Value |
|-------|-------|
| Status | not_started / in_progress / paused / complete |
| Phase | X of Y |
| Progress | X% |

### Checkpoint
Commit: <hash>
Branch: <name>

### History
| Date | Action | Result |
|------|--------|--------|
```
