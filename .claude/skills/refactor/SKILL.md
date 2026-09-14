---
name: refactor
description: Coordinated multi-file refactoring with an explicit call-site inventory and a rollback point. Use when renaming, moving, or reshaping something used in more than a couple of places.
argument-hint: <what to refactor>
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit, TodoWrite
effort: high
---

# /refactor — Multi-File Refactor

Refactor: `$ARGUMENTS`

A refactor changes structure and **nothing else**. If behavior needs to change too, that is a
separate commit — mixing them makes the diff unreviewable and a bisect useless.

## 1. Inventory every call site before editing one

Spawn `explorer` agents in parallel across the search paths that differ:

```
explorer: every reference to <target> in source
explorer: every reference to <target> in tests, fixtures, and mocks
explorer: every reference in config, docs, generated files, and CI
explorer: dynamic references — string imports, reflection, DI container keys, route tables
```

**The dynamic sweep is the one that bites.** A rename that a type-checker approves can still break
a runtime lookup keyed by a string. Grep for the *name as text*, not just as a symbol.

Record the total. That number is the denominator for everything that follows.

## 2. Establish the rollback point

```bash
git status --short          # must be clean, or stash first
git rev-parse HEAD          # record this sha in the state file
```

A refactor started on a dirty tree cannot be cleanly reverted, and the revert is the safety net.

## 3. Take the baseline

Run the gates via `test-runner` **now**, before any edit. A suite that was already red gives you
no signal afterward — you cannot tell your breakage from the pre-existing kind.

If it is red, fix that first or record exactly which tests were failing and why.

## 4. Batch and verify

Work in batches of related files. After each batch:

- Run the gates. Green before the next batch.
- Update `.claude/state/refactor_state.md` with progress **as a fraction**: `12/47 call sites`.

For large refactors, track batches with `TodoWrite` so progress survives a compaction.

## 5. Verify the count, not just the suite

At the end, re-run the **same searches from step 1**. The old name should return zero — and prove
that zero is real by searching for the new name and getting the expected count back. A search that
returns nothing because it was malformed looks exactly like a completed refactor.

```markdown
| Search | Before | After | Expected |
|--------|--------|-------|----------|
| old name | 47 | 0 | 0 |
| new name | 0 | 47 | 47 |
```

If the two do not balance, something was deleted rather than renamed. Find it.

## Report

```markdown
## Refactor: <target>

| Metric | Value |
|--------|-------|
| Call sites found | N (source M, tests K, config J, dynamic I) |
| Call sites changed | N of N |
| Batches | K |
| Rollback point | <sha> |

### Gates
| Gate | Baseline | Final |
|------|----------|-------|

### Verification
| Search | Before | After |
|--------|--------|-------|

### Behavior changes
- **none** — or every one, called out explicitly
```

## Constraints

- **Structure only.** Any behavior change is named in the report, or it does not happen.
- **Never `git add -A`.** Stage explicit paths; a broad add sweeps in unrelated work.
- Report progress as a fraction. "12 files done" hides whether 12 is most or a tenth.
- If a batch goes red and the cause is not obvious in one pass, stop and report rather than
  editing further on a red baseline.
