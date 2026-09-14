---
name: test-gen
description: Generate tests for existing untested code. Use when adding coverage to a module that already works; for new code, use /tdd instead so the test comes first.
argument-hint: <file or module>
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit, TodoWrite
---

# /test-gen — Test Generation

Generate tests for: `$ARGUMENTS`

Tests written against existing code have a specific failure mode: they lock in current behavior,
**including the bugs**. A generated test that passes on the first run has proven nothing except
that the code does what the code does.

## 1. Read the code before designing the tests

Do not generate from signatures. Read the implementation and find:

- Every branch, including the error paths and the early returns
- What the function actually does on empty, null, zero, and boundary inputs
- What it depends on — and therefore what has to be faked

## 2. Match the project's existing test style

```
explorer: find the test roots, the framework, and the two most recently written test files
```

Read those two files. Fixture approach, mocking style, assertion library, naming, file location —
match them. A test that is correct but stylistically foreign is a permanent source of friction.

If there are no tests yet, say so; you are establishing the convention, and that deserves a
sentence in the report rather than a silent choice.

## 3. Generate, one behavior per test

| Category | Required | Notes |
|----------|----------|-------|
| Happy path | Yes | The documented, intended use |
| Boundaries | Yes | Empty, single, maximum, zero, negative |
| Error paths | Yes | Each throw or error return, separately |
| Integration | If it crosses a boundary | Real collaborators where cheap |

## 4. Prove each test is connected

This is the step that separates a real test from a decorative one. For each test, **break the code
it covers and confirm the test goes red.**

```bash
# 1. Back the file up by COPY -- not `git stash`, which also moves anything else uncommitted
cp src/target.ts /tmp/target.backup
# 2. Make one surgical change that should break exactly this behavior
# 3. Run the suite -- the covering test must fail
# 4. Restore from the copy
cp /tmp/target.backup src/target.ts
```

Restore from the **copy**, never `git checkout --`: that discards any other uncommitted work in
the file and destroys the baseline you were comparing against.

Watch the count of failures too. If one mutation reds six tests, those six are coupled to an
implementation detail rather than to six behaviors — that is worth reporting.

If a mutation reds nothing, the test does not test what its name says.

## Report

```markdown
## Tests generated: <target>

| Metric | Value |
|--------|-------|
| Testable units | N |
| Units covered | K of N |
| Tests written | M |
| Branches covered | J of L |

### Mutation check
| Test | Mutation applied | Went red |
|------|------------------|----------|
| rejects an empty name | removed the length guard | yes |
| returns the default | changed the default value | **NO — test is not connected** |

### Not covered
- <each unit or branch left untested, and why>

### Behavior worth questioning
- <anything the code does that looks like a bug the tests now enshrine>
```

## Constraints

- **A test that has never failed is unproven.** Report the mutation result per test.
- **Never `git checkout --` to restore a mutated file.** Copy first, restore from the copy.
- **Report coverage as a fraction**, and list what was skipped as its own bucket.
- Do not fix the code here. If a test reveals a bug, report it — changing behavior under cover of
  "adding tests" hides it from review.
