---
name: initialize
description: Onboard a project or an unfamiliar surface. On a fresh clone it bootstraps .claude/memory/ and the CLAUDE.md project section once; after that it is additive and maps one surface into .claude/docs/.
argument-hint: <package|path|surface> [--quick] [--update]
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit
context: fork
agent: analyzer
background: false
---

# /initialize — Onboard a Project or a Surface

Onboard: `$ARGUMENTS`

This skill runs forked, so it sees none of the calling conversation. Everything it needs is below.

## Pick the mode first — this is not optional

Run this check before anything else:

```bash
grep -rlx -- '<!-- template-default -->' .claude/memory/ 2>/dev/null | sort
```

| Result | Mode | What you may write |
|--------|------|--------------------|
| Marker present **and** `$ARGUMENTS` empty | **Bootstrap** | `.claude/memory/*`, the CLAUDE.md project section, `.claude/docs/` |
| Marker absent, **or** `$ARGUMENTS` names a surface | **Surface** | `.claude/docs/` only |

The marker is an HTML comment alone on its own line in each memory file this template ships
unpopulated. Its absence means a human has written there.

**Use `-x`.** Several files — this skill included — quote the marker in prose explaining what it
means, so a substring search matches its own documentation and reports fully-written files as
empty. Whole-line matching is what makes the check mean what it says.

**In Surface mode this skill never writes `CLAUDE.md` or `.claude/memory/`.** Curated memory
encodes judgment that no auto-detection pass can reconstruct; a command that regenerates it from
file-extension counting destroys the most valuable content in the repo. Bootstrap is the one
exception, and it runs once.

| Need | Use |
|------|-----|
| Bootstrap a fresh clone | `/initialize` (no arguments, marker present) |
| Map a surface nobody has documented | `/initialize <surface>` |
| Analyze one file or subsystem in depth | `/deep <target>` |
| See what has already been analyzed | `/index` |

If `$ARGUMENTS` is empty and the marker is **absent**, do not scan the whole repo and do not ask.
**Print the unmapped candidates and stop** — every top-level source directory absent from the
scope column of `.claude/docs/_index.md`. A list is cheaper than a question and blocks nobody.

## Phases

### 1 — Discover (parallel, `explorer`)

Spawn `explorer` agents concurrently:

```
explorer: enumerate <surface> — files by type, directory shape 2 levels deep, largest files
explorer: find entry points, barrel exports, and the public interface of <surface>
explorer: find tests covering <surface>, and name every test root you found
explorer: find what OUTSIDE <surface> imports it, and what it imports
```

Prefer `find` or `/bin/ls -1` over a bare `ls` — a shell alias can emit nothing through a pipe.

In **Bootstrap** mode add: config files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
lockfiles, CI workflows), the README, and the declared scripts. Those are the only trustworthy
source for the tech-stack table; do not infer a framework from a file extension.

### 2 — Locate the boundary

Name which layer owns this surface and how execution reaches it, e.g.

```
HTTP route → controller → service → repository → database
```

Name the surface's dependency direction. A surface that reaches *backwards* across a boundary is
a finding.

### 3 — Read the load-bearing files (`analyzer`)

Not everything. The 3–7 files that establish the surface's contracts: entry point, the
most-imported module, the type/schema definitions, and one representative test. Delegate to
`analyzer` for depth.

Under `--quick`, stop after this phase and emit a structural map only.

### 4 — Detect patterns

What conventions does this surface already establish? Error handling; logging; how state is
loaded; how writes happen; test style and fixture approach; naming.

The point is that the **next** change here should look like the code around it. Record the
convention, not your preference.

### 5 — Gate check

Record which gates actually cover this surface — read them from the project's scripts and CI
config, never from memory:

```bash
sed -n '/"scripts"/,/}/p' package.json 2>/dev/null
ls .github/workflows/ 2>/dev/null
```

Do not run full suites here unless asked; note which gate *would* cover it, and say plainly when
nothing does.

### 6 — Write

Write `.claude/docs/<surface>.md` in the format below, then add its row to `.claude/docs/_index.md`.

In **Bootstrap** mode also populate the memory files, replacing the `<!-- template-default -->`
marker in each file you fill. Leave the marker in any file you could not populate from evidence —
a half-filled brief that still claims template status is honest; one that drops the marker while
guessing is not.

Under `--update`, read the existing doc first and **merge** — preserve hand-written additions,
update what has moved, and note what changed. Never silently overwrite.

## Output

Both templates — the persisted `.claude/docs/<surface>.md` doc and the summary printed to the
user — are in [references/output-format.md](references/output-format.md). Read it when you reach
phase 6.

## Constraints

- In Surface mode, writes only under `.claude/docs/`. Never a source file, in either mode.
- **Additive.** `--update` merges; nothing silently overwrites.
- Record conventions **as found**, not as preferred.
- Report gaps honestly — an onboarding doc that hides what is unclear is worse than none.
- No "pre-existing" excuse: a broken thing found while mapping gets surfaced.
- Separate measured from inferred; the `Unverified` section is mandatory.
