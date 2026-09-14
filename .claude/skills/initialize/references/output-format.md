# initialize — output formats

Three templates for the `/initialize` skill: the persisted surface doc, the summary printed to
the user, and the Bootstrap-mode memory population. Read this file when you reach phase 6.

## 1. The persisted doc — `.claude/docs/<surface>.md`

```markdown
---
sources:
  - "<repo-relative path or glob this surface covers>"
verified: <YYYY-MM-DD>
status: current
---

# Surface: <name>

> <one-line identity> · Layer: `<api|service|data|ui|tooling>` · Mapped: <date>

## Purpose
<2–3 sentences: what this surface is responsible for>

## Structure
| Path | Role |
|------|------|

## Entry points
- `path` → `symbol()` — <how execution reaches this surface>

## Public interface
<exports, CLI verbs, HTTP routes, events, published types>

## Dependencies
- **Depends on**: <list>
- **Depended on by**: <list>
- **Crosses a declared boundary?** <yes/no — and where>

## Conventions established here
- <pattern, with the file that establishes it>

## Gates covering this surface
| Gate | Command | Covers |
|------|---------|--------|

## Gotchas
- <non-obvious behavior — file and symbol, not a line number>

## Gaps
- <untested paths, missing docs, unclear ownership, suspected dead wiring>

## Unverified
- <claims from reading alone + the command that would confirm each>
```

Cite symbols, not line numbers: `:NN` is wrong the moment anyone inserts a line above it.

The `sources:`/`verified:` frontmatter is read by `python .claude/hooks/kb_check.py` to detect
drift; a doc missing either is a BLOCKING finding. `## Unverified` is mandatory — write
`none — all claims executed` if that is true, but never omit it.

## 2. The summary printed to the user

```markdown
# Surface Onboarded: <name>

| Field | Value |
|-------|-------|
| Mode | bootstrap / surface |
| Layer | <layer> |
| Files | N |
| Tests | N of N source files have a covering test |
| Crosses a boundary | yes/no |
| Gates covering it | <named> / none found |

## Written
- `.claude/docs/<surface>.md`
- `.claude/docs/_index.md` (+1 row)

## Key findings
- <2–4 bullets>

## Gaps found
- <what is missing or suspicious>

## Next
- `/deep <the most complex file>` for depth
- <specific follow-up>
```

Every count carries its population. "12 files" and "12 of 40 files" are different claims, and a
bare count reads as complete whatever it actually swept.

## 3. Bootstrap-mode memory population

Only in Bootstrap mode, and only from evidence you read this run.

| File | Fill from | Leave the marker if |
|------|-----------|---------------------|
| `project_brief.md` | Manifests, lockfiles, scripts, CI config | No manifest found |
| `product_context.md` | README, docs/, package description | No prose docs exist |
| `patterns/architecture.md` | Directory shape + the 3–7 load-bearing files | Fewer than 3 source files |
| `patterns/testing.md` | Test roots, test framework config, one real test | No tests found |
| `patterns/known_issues.md` | `TODO`/`FIXME`/`HACK` comments, with counts | Sweep returned nothing **and** you confirmed the pattern matches elsewhere |
| `progress.md` | Open issues, CHANGELOG, roadmap docs | Nothing to read |

An empty sweep is not a finding until you have shown the sweep can find something. Before writing
"no TODOs", grep for a string you know is present to prove the search reaches the files at all —
`.gitignore`d paths are skipped silently by most search tools.

### The CLAUDE.md project section

Bootstrap writes **only** between these markers, which the shipped CLAUDE.md already contains:

```markdown
<!-- initialize:begin -->
<!-- initialize:end -->
```

Everything outside them is hand-written and stays untouched. Put the project name, a one-line
description, the verified development commands, and the key directories inside. Nothing else.
