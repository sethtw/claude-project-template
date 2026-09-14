---
name: context
description: Show the current state of the project knowledge base — memory population, analysis docs and their drift, active operations, and git status. Read-only dashboard.
argument-hint: [--docs] [--state]
allowed-tools: Bash, Read, Glob
disable-model-invocation: true
---

# /context — Knowledge-Base State

Read-only. Shows what this project's `.claude/` actually contains right now.

## Gather

```bash
python .claude/hooks/kb_check.py --json
grep -l 'template-default' .claude/memory/*.md .claude/memory/patterns/*.md 2>/dev/null
git status --short
git log --oneline -5
```

Read `.claude/memory/active_context.md` and `.claude/state/_index.md` for in-flight work.

The `kb_check --json` call is what makes this dashboard honest: statuses come from each doc's
frontmatter measured against git, not from a table someone last hand-edited.

## Report

```markdown
## Context

### Memory
| File | Status |
|------|--------|
| project_brief.md | populated / **template default** |
| product_context.md | populated / **template default** |
| patterns/architecture.md | populated / **template default** |

N of M memory files still carry the template default marker.

### Analysis docs
| Metric | Value |
|--------|-------|
| Docs | N |
| Current | N |
| Stale | N |
| Orphaned | N |
| Skipped (unreadable) | N |

Blocking findings: N — <listed, or "none">

### Active operations
| Operation | State file | Progress |
|-----------|------------|----------|

### Repo
| Field | Value |
|-------|-------|
| Branch | <name> |
| Uncommitted | N files |
| Last commit | <sha> <subject> |

### Suggested next
- <only when something concrete is stale or unmapped>
```

## Reading the output honestly

- **"Template default" is not a failure state.** A fresh clone is supposed to look like this.
  Run `/initialize` to bootstrap it.
- **Stale is not broken.** A doc may be honestly committed stale; it means the source moved since
  anyone checked, not that the doc is wrong.
- **Skipped is worse than stale.** A doc the checker could not read has no status at all — its
  silence is indistinguishable from health. Report skips as their own bucket, never folded into
  "current".
- **A count with no denominator reads as complete.** Always print "N of M".

## Constraints

- **Read-only.** This skill writes nothing.
- Report what `kb_check` actually returned. If it exited non-zero or could not run, say that
  instead of printing an empty dashboard — an empty table and a failed check look identical.
