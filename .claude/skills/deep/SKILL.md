---
name: deep
description: Deep analysis of a file, directory, or subsystem — purpose, public interface, data flow across layer boundaries, patterns, and gotchas. Persists to .claude/docs/ unless --no-save.
argument-hint: <file|dir|subject> [--no-save]
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit
context: fork
agent: doc-writer
background: false
---

# /deep — Deep Analysis

Analyze in depth: `$ARGUMENTS`

Read-only with respect to source. The only files this skill may write are `.claude/docs/<subject>.md`
and `.claude/docs/_index.md`. It **persists by default** — pass `--no-save` for a throwaway read.

This skill runs forked, so it sees none of the calling conversation. Everything it needs is below.

## Process

**1. Scope the target.**

- A **file** → read it whole (use `offset`/`limit` above ~200 lines, after grepping for the region).
- A **directory** → list it, identify the 3–5 load-bearing files, read those deeply. Prefer `find`
  or `/bin/ls -1` over a bare `ls` — a shell alias (eza, exa, lsd) can emit nothing through a pipe.
- A **subject** that spans layers → spawn `explorer` agents in parallel to locate the surface, then read.

**2. Trace the layer boundary.** Read `.claude/memory/project_brief.md` for this project's
architecture, then name where the target sits in it and which direction its dependencies run.
A module that reaches *backwards* across a declared boundary is a finding, not a detail.

If `project_brief.md` is empty, say so — an analysis that invents an architecture is worse than
one that reports the architecture is undocumented.

**3. Analyze.** Cover: purpose and responsibilities; public interface (exports, CLI verbs, HTTP
routes, events); dependencies both directions; patterns used; and **gotchas** — non-obvious
behavior, implicit coupling, edge cases.

Delegate rather than do it all inline:
- `explorer` — locating files and tracing imports
- `analyzer` — depth on a subsystem you are not going to read personally
- `security-auditor` — if the target handles auth, input parsing, secrets, or external I/O
- `test-runner` — if a behavioral claim needs a suite to back it

**4. Report inline** in the format below.

**5. Persist** — always, unless `--no-save`.

## Output format

```markdown
---
sources:
  - "<repo-relative path or glob this analysis describes>"
verified: <YYYY-MM-DD>
status: current
---

## Deep Analysis: <subject>

### Purpose
<2–3 sentences>

### Key components
| Name | Role | Location |
|------|------|----------|
| `X` | … | `path` (name the symbol, not a line number) |

### Public interface
<exports, CLI verbs, HTTP routes, events, published types>

### Data flow
1. `path` — <step>
2. `path` — <step>

### Dependencies
- **Imports**: <list>
- **Imported by**: <list>

### Patterns
- <pattern, and where it is established>

### Gotchas
- <non-obvious behavior, with a file and symbol>

### Unverified
- <claims made from reading alone, and the command that would confirm each>

### Recommendations
- <if any>
```

The frontmatter is not decoration: `python .claude/hooks/kb_check.py` reads `sources:`/`verified:`
to detect when this doc has drifted, and a doc missing either one is a BLOCKING finding — drift
cannot be detected for it at all. Same for `## Unverified`: write `none — all claims executed` if
that is true, but never omit the section.

The **Unverified** section is mandatory. Reading a file establishes what the code *says*, not what
it *does* at runtime — a default in source is only a default, and a config layer can shadow it
silently.

Cite symbols, not line numbers. `auth.ts` + `validateSession()` survives the next edit; `auth.ts:45`
is wrong the moment anyone inserts a line above it.

## Persisting (default; `--no-save` to skip)

Write to `.claude/docs/<subject>.md` using a descriptive kebab-case filename that names the subject:

- `auth-session-flow.md`, `payment-webhooks.md`, `build-pipeline.md`
- **not** `DOC_123.md`, `analysis_789.md`, `notes.md`

Then register it in `.claude/docs/_index.md` — one row, newest analysis date. Run `/index` if the
index has drifted.

If the doc already exists, **read it first and merge**. Do not overwrite an existing analysis with
a narrower one; note what changed and when.

## Constraints

- Never write to `CLAUDE.md`, `.claude/memory/`, or any source file.
- Keep it to 1–2 pages. A deep analysis is a briefing, not a book report.
- Evidence before assertion — every finding carries a file, a symbol, or a pasted command.
- Report a count with its population: "7 of 12 call sites" not "7 call sites".
- No "pre-existing" excuse: a broken thing found while analyzing is in scope to surface.
