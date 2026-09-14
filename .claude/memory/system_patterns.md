# System Patterns Index

> Navigation hub for the patterns, skills, agents, and rules in this repo.

## Pattern files

| File | Read when |
|------|-----------|
| [architecture.md](patterns/architecture.md) | Structure, error handling, config |
| [development.md](patterns/development.md) | **Always** — model/effort selection, verification bar, autonomy |
| [testing.md](patterns/testing.md) | Writing or reviewing tests |
| [known_issues.md](patterns/known_issues.md) | Debugging, or before blaming your own change |

## Workflow skills

Invoke with `/<name>`. Each carries its own frontmatter; none pin a model tier.

| Skill | Use for |
|-------|---------|
| `/initialize` | Bootstrap a fresh clone, or map an unmapped surface into `.claude/docs/` |
| `/analyze` | Repo-wide survey: structure, conventions, hotspots, debt |
| `/deep` | One file or subsystem in depth, persisted with drift detection |
| `/index` | Knowledge-base drift report and registry refresh |
| `/context` | Read-only dashboard: memory population, doc drift, active operations |
| `/architect` | Implementation plan, no code |
| `/implement` | Execute a plan: discover → write → verify → fix |
| `/tdd` | Red-green-refactor for new behavior |
| `/test-gen` | Coverage for code that already exists |
| `/refactor` | Multi-file structural change with a call-site inventory |
| `/migrate` | Framework or version upgrade with phase tracking |

## Domain skills

Loaded by name when relevant; not usually invoked directly.

| Skill | Covers |
|-------|--------|
| `codebase-navigator` | Search strategy, and when an empty result is not evidence |
| `wiring-audit` | Built-but-not-connected: dead exports, facade UIs, half-adopted patterns |
| `api-design` | REST and GraphQL endpoint design |
| `database-patterns` | Schema, queries, migrations, indexes |
| `performance-analysis` | Bottlenecks, profiling, memory |
| `security-audit` | OWASP, authn/authz, injection, secrets |
| `ux-workflow-analysis` | User journeys, layout, accessibility |

`security-audit` is named to avoid colliding with Claude Code's built-in `/security-review`.
Likewise, this template ships no `/code-review` or `/review` — the built-in `/code-review` covers
both, with effort levels and a `--fix` mode.

## Agents

| Agent | Use for |
|-------|---------|
| `explorer` | Where is X, what calls Y, what exists |
| `analyzer` | How does X work, what breaks if I change Y, review this |
| `test-runner` | Run the real gates, diagnose a red to a root cause |
| `security-auditor` | Diffs touching auth, input parsing, queries, paths, external I/O |

All four use `model: inherit` — a subagent matches the calling session rather than being pinned to
a cheaper tier. Pinning a reviewer below the author is how a review becomes a rubber stamp.

## Path-scoped rules

`.claude/rules/*.md` load automatically for files matching their `paths:` frontmatter.

| Rule | Applies to |
|------|-----------|
| `typescript.md` | `src/**/*.{ts,tsx}`, `lib/**/*.{ts,tsx}` |
| `testing.md` | Test files |
| `security.md` | Auth, API, middleware |

Edit the `paths:` globs to match this project's real layout. A rule whose glob matches no tracked
file can never load — `python .claude/hooks/kb_check.py` reports that as `dead-glob`.

## Hooks

| Hook | Event | Writes |
|------|-------|--------|
| `session-history.py` | SessionStart | Archives the prior session, resets counters |
| `session_start_brief.py` | SessionStart | Nothing — prints repo and knowledge-base state |
| `unified-post-write.py` | Write/Edit | `active_context.md`, `state/_index.md` |
| `todo-context-sync.py` | TodoWrite | `active_context.md` |
| `command-tracker.py` | Skill | `state/_index.md` counter |

Full detail in [SETTINGS-SCHEMA.md](../SETTINGS-SCHEMA.md).
