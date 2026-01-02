# Registry Cleanup

Description: Clean stale entries and maintain registry health

You are a Registry Maintainer. Task: Clean up the document registry by removing stale markers and deleted file entries.

## Purpose

The registry (`_registry.md`) tracks all indexed documents. Over time:
- Files get modified and marked as "stale" by `registry-staleness.py`
- Files get deleted but entries remain
- Orphaned concept references accumulate

This command cleans up these issues.

## Process

### Step 1: Identify Stale Entries

Read `.claude/memory/_registry.md` and find entries marked as stale:

```
| DOC_XXX | path/to/file.ts | L1 | ⚠️ stale |
```

### Step 2: Verify File Existence

For each entry in the registry:
1. Check if the file still exists at the specified path
2. If file exists but marked stale → Clear stale marker
3. If file doesn't exist → Remove entry entirely

### Step 3: Update Depth if Needed

For stale entries where file exists:
- If file was significantly modified → Reset to L0
- If file has minor changes → Keep current depth, remove stale marker

### Step 4: Clean Orphaned Concepts

Check `_concepts.md` for concepts that reference deleted files:
1. Find concepts pointing to non-existent DOC_XXX references
2. Remove or update those concept entries

### Step 5: Update Statistics

Update `_index.md` with new counts:
- Total Documents
- L0/L1/L2/L3 counts
- Concepts count

## Cleanup Modes

| Mode | Command | Behavior |
|------|---------|----------|
| Default | `/cleanup` | Preview changes only (dry run) |
| Apply | `/cleanup --apply` | Apply all changes |
| Stale only | `/cleanup --stale` | Only clear stale markers |
| Remove deleted | `/cleanup --deleted` | Only remove deleted file entries |

## Output Format

```markdown
## Registry Cleanup Report

### Summary
| Metric | Count |
|--------|-------|
| Entries scanned | X |
| Stale markers found | X |
| Deleted files found | X |
| Orphaned concepts | X |

### Stale Entries
| DOC | Path | Action |
|-----|------|--------|
| DOC_123 | src/old.ts | ✅ Marker cleared |
| DOC_456 | src/moved.ts | ❌ File deleted, entry removed |

### Orphaned Concepts
| Concept | Referenced DOC | Action |
|---------|----------------|--------|
| [[OldPattern]] | DOC_456 | Removed |

### Statistics Updated
| Metric | Before | After |
|--------|--------|-------|
| Total Documents | 150 | 145 |
| L0 | 100 | 95 |
| L1 | 30 | 30 |
| L2+ | 20 | 20 |
```

## Safety

- **Dry run by default**: Always preview before applying
- **No permanent deletion**: Entries are removed from registry, not files
- **Backup suggestion**: For large cleanups, suggest creating backup branch

## Autonomy

- Scan registry without confirmation
- Preview mode by default (require --apply to make changes)
- Update all affected files atomically

## Skills Used

- **codebase-navigator** - File existence verification

## Memory Updates

- Updates `_registry.md` (removes stale markers, deleted entries)
- Updates `_concepts.md` (removes orphaned concepts)
- Updates `_index.md` (refreshes statistics)

## Update Protocol

| Source | Action | Automatic |
|--------|--------|-----------|
| /cleanup --apply | Clears stale markers in _registry.md | Yes |
| /cleanup --apply | Removes deleted file entries | Yes |
| /cleanup --apply | Updates _index.md statistics | Yes |
| Manual | Run /cleanup periodically for maintenance | No |
