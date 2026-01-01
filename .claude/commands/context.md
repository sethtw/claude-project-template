# /context - Memory State

> Display current knowledge base state and active context.

## Purpose

Show a summary of the current memory state including:
- Knowledge base statistics
- Active context status
- Current session info
- Active operations

## Usage

```
/context                    # Show full context summary
/context --stats            # Just statistics
/context --session          # Current session only
/context --operations       # Active operations
```

## Process

### Step 1: Read Memory Files

Read key memory files:
- `_index.md` - Stats
- `_registry.md` - Document counts
- `active_context.md` - Session state
- `.claude/state/_index.md` - Active operations

### Step 2: Compile Summary

Aggregate information into a dashboard view.

## Output Format

```markdown
## Context Summary

### Knowledge Base Stats
| Metric | Count |
|--------|-------|
| Total Documents | 150 |
| L0 (Discovery) | 120 |
| L1 (Triage) | 20 |
| L2 (Summary) | 8 |
| L3 (Deep) | 2 |
| Concepts | 15 |
| Last Index | 2024-01-15 |

### Current Session
| Field | Value |
|-------|-------|
| Status | Active |
| Date | 2024-01-16 |
| Working On | Feature implementation |
| Branch | feature/user-auth |
| Files Modified | 5 |

### Active Operations
| Operation | State File | Progress |
|-----------|------------|----------|
| Refactor | refactor_state.md | 3/10 batches |

### Recent Activity
| Time | Action |
|------|--------|
| 10:30 | Indexed 15 files |
| 10:25 | Promoted user.ts to L2 |
| 10:20 | Started refactor operation |

### Quick Actions
- `/index` - Refresh codebase index
- `/deep <path>` - Analyze specific file
- Run pending refactor batches

### Memory Health
| Check | Status |
|-------|--------|
| Registry consistent | OK |
| Concepts linked | OK |
| No orphaned entries | OK |
| State files valid | OK |
```

## Autonomy

- Read-only operation
- No confirmations needed
- Fast execution

## Model Selection

| Phase | Model | Rationale |
|-------|-------|-----------|
| File reading | haiku | Fast I/O |
| Summary generation | haiku | Simple aggregation |

## Skills Used

- `codebase-navigator` - Quick file access

## Agents Used

- `explorer` - Fast file reading

## Memory Updates

None - read-only command.
