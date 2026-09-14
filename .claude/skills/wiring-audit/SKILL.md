---
name: wiring-audit
description: Find features that were built but never connected — dead exports, unreachable routes, UI that renders but calls nothing, config read by no one, and plans abandoned mid-implementation. Use when something "should work but doesn't", before trusting a feature list, or after a large merge.
allowed-tools: Read, Grep, Glob, Bash, Agent
effort: high
---

# Wiring Audit

> Code that exists is not code that runs. This finds the gap.

A facade is the expensive failure: a surface that looks complete, passes review, and is wired to
nothing. It survives because every individual piece is correct — only the *connection* is missing,
and nothing in the diff shows an absence.

## What to look for

| Symptom | Check |
|---------|-------|
| Dead export | A symbol exported and imported nowhere |
| Orphan route | A handler defined but not registered on the router |
| Facade UI | A component that renders state it never fetches, or a button with no handler |
| Dead config | A settings key read by no code, or written by no code |
| Abandoned migration | The new path added, the old path still doing the work |
| Half-adopted pattern | 3 of 11 call sites converted, no tracking of the other 8 |
| Unreachable branch | A condition that cannot be true given the callers |

## Method

**1. Enumerate the writers, not the readers.** Readers announce themselves — they import the
thing. Writers do not, and a value with no writer is the tell for a feature that was never
connected. For any piece of state that looks wrong, list everything that *sets* it before
explaining anything about what reads it.

**2. Compare declaration to use, both directions.**

```
explorer: every exported symbol in <area>, and its import count
explorer: every route handler defined, and every route registered
explorer: every config key defined, and every key read
```

The interesting output is the asymmetry, not either list.

**3. Distrust a check that reads what the code *says*.** An arch test that greps for a call
matches the text of the call, not its execution — it ships green on the exact bug it was written
for. Where it matters, exercise the path: start it, hit it, watch the effect.

**4. A count of converted call sites needs its denominator.** "Migrated 8 files" is not progress
without the total. Report `8 of 19`, and list the 11.

## The trap this audit walks into

An audit that finds nothing is the expected result of both a clean codebase and a broken audit.
Before reporting "all wiring is connected", verify your own instrument: pick something you *know*
is connected and confirm the sweep detects it, then pick something you know is not — introduce a
throwaway unused export — and confirm the sweep flags it. A sweep that cannot find a planted
defect cannot certify its absence.

Delete the planted defect before reporting. Say in the report that you planted one.

## Report

```markdown
## Wiring Audit: <scope>

Instrument control: planted an unused export in `<path>`, sweep detected it. Removed.

### Disconnected
| Thing | Declared in | Expected consumer | Status |
|-------|-------------|-------------------|--------|
| `sendDigest()` | `src/jobs/digest.ts` | a scheduler registration | **no caller** |

### Partially adopted
| Pattern | Converted | Remaining |
|---------|-----------|-----------|
| new error type | 8 of 19 | <listed> |

### Verified connected
- <what you checked and found genuinely wired — this is the denominator>

### Not checked
- <areas the sweep did not reach, and why>
```

## Constraints

- **Control the instrument before trusting a null result.**
- Report counts with their population, and skips as their own bucket.
- A dead export is a finding, not a deletion. Report it; let the owner decide.
