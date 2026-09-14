---
name: tdd
description: Strict red-green-refactor. Use when implementing any feature or bugfix where the expected behavior can be stated before the code exists — write the failing test first, watch it fail, then make it pass.
argument-hint: <feature or bug to implement>
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit, TodoWrite
---

# /tdd — Red, Green, Refactor

Implement with TDD: `$ARGUMENTS`

## The rule that carries all the value

**You must watch the test fail before you make it pass.**

A test written after the code passes on the first run, and a test that has never failed proves
nothing — it may be asserting something that was already true, calling nothing, or silently
skipped. The red is the only evidence the test is connected to the behavior.

If a new test passes immediately, that is a finding, not a convenience. Stop and find out why:

| Why it passed | How to tell |
|---------------|-------------|
| The behavior already exists | Search for it. You may not need this feature. |
| The test asserts a tautology | `expect(x).toBe(x)`, or a mock asserting its own return |
| The test never ran | Check the runner's count — a filtered or skipped test reports as green |
| A different guard satisfies it | Something upstream already rejects the input |

## 1. Find the real test command

Do not assume `npm test`. Read `package.json` scripts, `Makefile`, or the CI workflow. Note the
exact command — you will run it many times, and it has to be the same one each time.

## 2. RED — write the failing test

- One behavior per test. A test asserting four things tells you little when it fails.
- Name it for the behavior, not the function: `rejects a booking in the past`, not `test booking`.
- **Run it. Read the failure message.** It must fail for the intended reason — a test failing on
  an import error is not red, it is broken.

## 3. GREEN — minimal implementation

Write the least code that passes. Not the general solution, not the version with the options you
anticipate. Over-building here is how untested branches get born.

**Run the command. Read the count**, not just the exit code: `12 passed` when you expected 13
means one was skipped, and a skipped test in a green run is invisible.

## 4. REFACTOR — with the tests green

Improve names, extract duplication, tighten types. Run the tests after each change. If a refactor
turns them red, revert it — do not fix forward with the suite red.

## 5. Repeat

One behavior at a time. Track the list with `TodoWrite`.

## Report

```markdown
## TDD: <feature>

| Behavior | Red seen | Green | Refactored |
|----------|----------|-------|------------|
| rejects a booking in the past | yes — <the failure message> | yes | yes |

### Suite
`<exact command>` → N passed, M failed, K skipped, of N total

### Tests that passed before implementation
- <each one, and what it turned out to mean> — or "none"
```

## Constraints

- **No implementation before a red.** If you cannot make it fail, you do not yet know what you
  are building.
- **Never delete or weaken a test to get green.** A failing test is information.
- **Read the counts, not the exit code alone.** A suite that skipped your new test exits 0.
- Never pipe the test command through `tail` or `head` — piping replaces its exit status.
