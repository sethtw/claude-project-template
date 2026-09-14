---
name: architect
description: Produce an implementation plan for a feature without writing any code. Use before any change touching 3+ files or crossing a layer boundary; the plan hands off to /implement --planned.
argument-hint: <feature description>
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit
effort: high
---

# /architect — Plan Only

Plan: `$ARGUMENTS`

**This skill writes no source code.** It produces a plan explicit enough that the next session can
execute it without improvising. Use `/implement --planned` to run it.

## 1. Gather context in parallel

Spawn `explorer` agents concurrently — one per independent search path:

```
explorer: find every file in the area this feature touches, and name the layer each sits in
explorer: find the closest existing feature to this one, and the files that implement it
explorer: find the test roots and the test style used for that closest feature
explorer: find the error-handling, validation, and logging conventions in this area
```

Then read, in this order:

1. `.claude/memory/project_brief.md` — stack and architecture
2. `.claude/memory/patterns/architecture.md` — the conventions to follow
3. The closest existing feature's actual files — **this matters more than the memory files.**
   Memory describes intent; the code is what the next change has to match.

If memory still carries `<!-- template-default -->`, say so and plan from the code alone.

## 2. Analyze before deciding

Delegate depth to `analyzer` for any subsystem you are not going to read personally. For a feature
touching auth, user input, or external I/O, run `security-auditor` over the area **now** — a
design flaw found at plan time is free, and found at review time is a rewrite.

## 3. Write the plan

```markdown
## Implementation Plan: <feature>

### Summary
<2–3 sentences: what gets built, and where it lives>

### Complexity
| Factor | Rating | Evidence |
|--------|--------|----------|
| Files affected | Low/Med/High | N to create, M to modify |
| Layers crossed | Low/Med/High | <which> |
| Risk | Low/Med/High | <the specific thing that could go wrong> |

### Files to create
| File | Purpose | Key exports |
|------|---------|-------------|

### Files to modify
| File | Change | Risk |
|------|--------|------|

### Steps
#### Step N: <name>
- What to write, with complete type/function signatures — not a description of them
- **Follow the pattern in `<path>` → `<symbol>`** (name a real file that exists)
- How this step is verified

### Patterns to follow
| Concern | Established in | Use |
|---------|----------------|-----|
| Errors | `src/errors.ts` → `AppError` | … |

### Test plan
| Behavior | Test type | Where it goes |
|----------|-----------|---------------|

### Risks
| Risk | Mitigation |
|------|------------|

### Open questions
- <anything the plan could not settle from evidence — name it rather than guessing>
```

A step that says "add validation" is not a plan. A step that says "add a Zod schema matching
`CreateUserSchema` in `src/validators/user.ts`, rejecting empty `name`" is.

## 4. Save it

Write to `.claude/state/current_plan.md`, with a status line `| Status | pending |`.
`/implement --planned` reads that file and validates that header, so it is not optional.

## 5. Report

```markdown
## Plan created: <feature>

| Metric | Value |
|--------|-------|
| Files to create | N |
| Files to modify | M |
| Steps | K |
| Open questions | J |

Saved to `.claude/state/current_plan.md`

Next: `/implement --planned`
```

## Constraints

- **Plans only.** No source files, no `mkdir`, no commits.
- Every pattern reference names a file that exists — check it, do not recall it.
- Surface open questions as a section; a plan that hides its uncertainty transfers it silently
  to whoever executes it.
- No cost or model-tier tables. Set `effort` per skill and let the session's model stand.
