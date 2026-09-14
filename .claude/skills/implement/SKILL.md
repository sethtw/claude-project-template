---
name: implement
description: Execute a feature end to end — discover, plan (or load an /architect plan), write, verify, fix. Use for any multi-file change; pass --planned to run an existing plan from .claude/state/current_plan.md.
argument-hint: <feature> | --planned | --fresh <feature>
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit, TodoWrite
effort: high
---

# /implement — Staged Execution

Implement: `$ARGUMENTS`

| Mode | Trigger | Stages |
|------|---------|--------|
| Planned | `--planned` | 1, 3, 4, 5 — loads `.claude/state/current_plan.md` |
| Fresh | `--fresh <feature>` | all — ignores any saved plan |
| Default | `<feature>` | all, but offers a saved plan if one is `pending` |

Track the stages with `TodoWrite` so progress survives a compaction.

## Why stages, not model tiers

The stages exist to **isolate context**, not to downgrade models. Discovery reads a lot and
concludes little, so it belongs in a forked subagent whose reads never enter the main context.
Writing needs the plan and the conventions, not the 40 files discovery opened.

Do not pin a stage to a cheap model. Pinning the verifier below the writer is how a broken
implementation gets a clean report. Set `effort` and let the session's model stand.

## Stage 1 — Discover (`explorer`, parallel)

```
explorer: find the files this feature touches and the layer each sits in
explorer: find the closest existing feature and the files that implement it
explorer: find the test root and test style for that feature
explorer: find the error-handling and validation conventions in this area
```

## Stage 2 — Plan (skipped with `--planned`)

Run `/architect` and use its output, or produce the same structure inline. Save to
`.claude/state/current_plan.md`.

**With `--planned`, validate before writing a line:**

| Check | On failure |
|-------|------------|
| `.claude/state/current_plan.md` exists | Stop: "No plan found. Run /architect first." |
| It has a `\| Status \|` row | Stop: "Plan has no status row — regenerate with /architect." |
| Status is not `complete` | Stop: "Plan is already complete. Use --fresh." |
| It lists at least one file | Stop: "Plan specifies no files." |
| It lists at least one step | Stop: "Plan has no steps." |

Fail loudly on each. A plan that silently half-loads produces an implementation nobody can audit.

## Stage 3 — Write

Execute the steps in order. Rules:

- **Follow the plan.** A deviation is a decision — state it in the report, do not bury it.
- **Match the surrounding code**, not your preference. The pattern the plan names is the contract.
- **No unrequested features.** Scope creep in stage 3 is invisible until review.
- Commit at each logical unit, staging **explicit paths** — never `git add -A`, which sweeps in
  whatever else is in the tree.

## Stage 4 — Verify (`test-runner`)

Delegate to `test-runner`. It finds this project's real gates rather than assuming `npm test`.

| Check | Reported as |
|-------|-------------|
| Tests | passed / failed / skipped, with the total |
| Types | clean / N errors |
| Lint | clean / N errors |
| Files from the plan | present / missing, by name |
| Integration points | wired / not wired |

A gate with no command in this project is reported NOT RUN, on its own row. Never omitted, never
implied to have passed.

## Stage 5 — Fix (only if stage 4 is red)

Diagnose to a root cause before editing. Re-run a single failure in isolation first — parallel
suites manufacture failures, and a contention timeout is not a bug in the code under test.

After fixing, **re-run the exact command that failed.** A different command passing is not
evidence that this one does.

If stage 5 fails twice on the same root cause, stop and report. A third blind attempt is guessing.

## Report

```markdown
## Implemented: <feature>

| Stage | Result |
|-------|--------|
| Discover | N files found |
| Plan | loaded from /architect | written fresh | skipped |
| Write | N of M steps complete |
| Verify | <gate results, with populations> |
| Fix | not needed | N issues resolved |

### Files
| File | Created/Modified | Covered by a test |
|------|------------------|-------------------|

### Deviations from the plan
- <each one, with why> — or "none"

### Not done
- <anything in scope that was left out, and why>
```

## Constraints

- **Never report completion on unrun gates.** Evidence before assertion.
- **Report what was left out.** Scaling the work down is the user's call, not yours.
- Stage explicit paths in every commit.
- No attribution footers in commit messages.
