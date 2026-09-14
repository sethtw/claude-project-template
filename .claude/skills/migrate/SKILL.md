---
name: migrate
description: Framework or dependency version migration with phase tracking and a rollback point. Use for "React 17 to 18", "Express to Fastify", a major version bump, or any upgrade with breaking changes.
argument-hint: <from> to <to>
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit, TodoWrite, WebFetch
effort: high
---

# /migrate — Version or Framework Migration

Migrate: `$ARGUMENTS`

## 1. Get the real breaking-change list

**Read the upstream changelog or migration guide. Do not migrate from memory.** A model's
recollection of a framework's breaking changes is a hypothesis, and version-specific details are
exactly what it gets wrong. Fetch the actual release notes for the exact versions involved.

Record: the source version, the target version, and where the list came from.

## 2. Inventory the impact

```
explorer: every import of the packages being migrated
explorer: every use of the APIs named in the breaking-change list
explorer: config files, build config, and CI that pin or configure these packages
explorer: test setup, mocks, and fixtures that touch these packages
```

For each breaking change, record the call-site count. **A breaking change with zero call sites is
still worth listing** — as a line reading "0 sites, not applicable", so the next reader knows it
was checked rather than missed.

## 3. Rollback point and baseline

```bash
git status --short      # clean, or stash
git rev-parse HEAD      # record this
```

Run the gates via `test-runner` **before** touching anything. Without a baseline you cannot tell
migration breakage from what was already red.

## 4. Phase the work

Record phases in `.claude/state/migration_state.md` and track them with `TodoWrite`:

1. Dependency versions — bump and install, nothing else
2. Breaking API changes — one change class per commit
3. Config and build changes
4. Test and fixture updates
5. Remove deprecated usage the new version tolerates but warns on

Run the gates after each phase. A migration that only runs its tests at the end cannot tell you
which phase broke it.

## 5. Verify the version actually changed

This is the step that gets skipped. A `package.json` edit is not an installed version:

```bash
# Confirm what is actually resolved, not what is declared
npm ls <package> 2>/dev/null || pip show <package> 2>/dev/null
```

A lockfile that was not regenerated, or a transitive pin elsewhere in the tree, leaves the old
version installed while every file says otherwise — and the suite passes, because it is still
testing the old version.

## Report

```markdown
## Migration: <from> → <to>

Breaking changes sourced from: <URL or file>

| Metric | Value |
|--------|-------|
| Breaking changes in the guide | N |
| Applicable to this repo | K of N |
| Call sites updated | M of M |
| Rollback point | <sha> |

### Breaking changes
| Change | Sites | Status |
|--------|-------|--------|
| <change> | 12 | done |
| <change> | 0 | not applicable |

### Version verification
| Package | Declared | Actually resolved |
|---------|----------|-------------------|

### Gates
| Gate | Baseline | Final |
|------|----------|-------|

### Deferred
- <anything not migrated, and why>
```

## Constraints

- **Never migrate from recalled API knowledge.** Fetch the changelog; cite it.
- **Verify the resolved version, not the declared one.**
- Every breaking change appears in the table, including the ones that did not apply.
- Stage explicit paths per phase. One phase, one commit.
