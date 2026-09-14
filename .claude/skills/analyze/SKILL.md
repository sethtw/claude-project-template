---
name: analyze
description: Repo-wide survey — structure, dependencies, conventions, complexity hotspots, and tech debt. Use to orient on an unfamiliar codebase or to feed /architect; for one file or subsystem in depth, use /deep instead.
argument-hint: [path] (defaults to the whole repo)
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit
context: fork
agent: doc-writer
background: false
---

# /analyze — Repo Survey

Survey: `$ARGUMENTS` (the whole repo if empty)

This skill runs forked, so it sees none of the calling conversation. Everything it needs is below.

| Need | Use |
|------|-----|
| Orient on a whole codebase | `/analyze` |
| Map one surface for the next agent | `/initialize <surface>` |
| Understand one file or subsystem deeply | `/deep <target>` |

Breadth, not depth. This survey names where to look next; it does not settle anything.

## 1. Scan in parallel (`explorer`)

```
explorer: directory shape 2 levels deep, file counts by extension, the 10 largest source files
explorer: every manifest and lockfile, and the declared scripts in each
explorer: test roots, test framework config, and the ratio of test files to source files
explorer: every TODO / FIXME / HACK / XXX comment, with counts by directory
```

Prefer `find` or `/bin/ls -1` over a bare `ls` — a shell alias can emit nothing through a pipe.

## 2. Establish the stack from evidence

Read manifests and lockfiles. **Do not infer a framework from a file extension** — a `.ts` file
proves TypeScript, not React, and a dependency in `package.json` may be unused. Confirm a
framework by finding the code that imports it.

## 3. Find the conventions

Read the 3–7 most-imported modules. Record, as found:

- Error handling — custom classes, result types, or bare throws
- Validation — where input is checked, and whether consistently
- Logging — library, levels, structure
- Data access — ORM, query builder, raw queries; where transactions live
- Test style — framework, fixture approach, mocking

The point is that the **next** change should look like the code around it. Record the convention,
not your preference — and say so when there is no convention, which is itself the finding.

## 4. Find the hotspots

A hotspot is a file that is both **large and frequently changed** — size alone is not risk. Use
git to get the second half:

```bash
git log --format=format: --name-only --since=6.months | sort | uniq -c | sort -rn | head -20
```

Cross that against file size. A 500-line file nobody touches is stable; a 200-line file touched
weekly is where bugs live.

## 5. Report

```markdown
## Survey: <scope>

### Overview
| Metric | Value |
|--------|-------|
| Source files | N (of M total tracked) |
| Test files | N — covering K of M source directories |
| Languages | <from manifests, not extensions> |
| Framework | <confirmed by import, or "none found"> |

### Structure
<directory tree, 2 levels, with file counts>

### Conventions found
| Concern | Convention | Established in |
|---------|------------|----------------|
| Errors | … | `path` → `symbol` |

### Conventions NOT found
- <each area with no consistent approach — this is where drift starts>

### Hotspots (large AND frequently changed)
| File | Lines | Commits (6mo) | Why it matters |
|------|-------|---------------|----------------|

### Tech debt
| Marker | Count | Concentrated in |
|--------|-------|-----------------|
| TODO | N | `path/` |

### Recommended next steps
- `/deep <file>` — <the specific question it would answer>
- `/initialize <surface>` — <the surface nobody has mapped>

### Unverified
- <every claim made from reading alone, and the command that would confirm it>
```

## Constraints

- **Read-only.** Writes nothing outside `.claude/docs/` and only when asked.
- **Every count carries its population.** "45 source files" and "45 of 210 tracked files" are
  different claims.
- **An empty sweep is not a finding until the sweep is proven to work.** Before reporting "no
  TODOs", search for a string you know is present — search tools skip ignored paths silently.
- Report what you did not examine. A survey that lists only what it found reads as exhaustive.
