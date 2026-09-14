---
name: codebase-navigator
description: Search strategy for finding code fast — locating symbols, tracing dependencies both directions, and mapping unfamiliar structure. Use when the question is "where is X", "what calls Y", or "how does Z reach the UI", and whenever a search returns an empty result you are about to report as an absence.
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Codebase Navigator

> How to search, and how to know whether the search worked.

## Order of operations

1. **Glob for shape** — narrow to a directory or file pattern before grepping content.
2. **Grep for the symbol** — with a pattern specific enough that prose does not match it.
3. **Read only what the grep points at** — and read the whole file, not the matched region.

Fan out with parallel `explorer` agents when the search paths are genuinely independent:

```
explorer: every definition of <symbol>
explorer: every call site of <symbol> in source
explorer: every reference in tests, fixtures, and mocks
explorer: dynamic references — string imports, DI keys, route tables, reflection
```

One agent per independent path. Splitting one path across agents just duplicates work.

## Finding things

| Goal | Approach |
|------|----------|
| Entry points | `Glob: **/{main,index,app}.{ts,js,py,go,rs}` |
| Route definitions | Grep the router registration call, not the route strings |
| What this depends on | Grep imports **within** the file |
| What depends on this | Grep the module path and the exported name across the repo |
| A convention | Read the two most recently changed files in that directory |
| Where risk lives | Cross file size against `git log --name-only` change frequency |

## The three ways a search lies

An empty result is the least trustworthy output a search tool produces, because it looks the same
in every failure mode.

**1. The tool never looked.** `Grep` and `Glob` skip gitignored paths by default. A sweep for
secrets, build output, or anything under an ignored directory returns clean because it never read
the files. Prove reachability with a control: search the same scope for a string you know is
there. If the control comes back empty, the absence is not evidence.

**2. The pattern could not match.** A regex with an unescaped brace, a name that is actually
hyphenated, a symbol split across lines. Before believing a zero, run the pattern against a known
positive.

**3. It matched the wrong thing.** A hit inside a comment, a doc, a changelog, or a string literal
is not the symbol. This corrupts counts and, worse, corrupts *names* — a refactor driven by a
prose match renames the wrong identifier. Confirm each match is a declaration or a call.

There is a fourth, specific to this work: **documenting the needle breaks the search.** Once you
write the symbol you are hunting into a notes file in the repo, every later grep matches your own
notes. Search first, write second, or exclude your scratch paths explicitly.

## Reporting a search

```markdown
### Found: <query>
- `path` → `symbol` — definition
- `path` — 3 call sites

### Searched and not found
- <pattern>, across <scope> — control: searched for `<known string>`, got N hits, so the sweep reached the files
```

Every count carries its population. "12 call sites" and "12 call sites across 40 of 210 files"
are different claims, and only the second one can be acted on.

## Constraints

- **Never report an absence without a positive control.**
- Cite symbols, not line numbers — `:NN` is wrong after the next insertion above it.
- Prefer `Grep`/`Glob` to shell equivalents; they respect ignore files and return structure.
- Prefer `find` or `/bin/ls -1` over a bare `ls` — an alias can emit nothing through a pipe.
