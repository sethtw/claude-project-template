# Memory Index

> Navigation hub for durable project knowledge. Start here.

## The bar for this directory

`.claude/memory/` holds **judgment that cannot be re-derived** — why the architecture is shaped
this way, what was tried and abandoned, which constraints are real. It is hand-curated, and
`/initialize` writes here exactly once, on a fresh clone.

Derived, regenerable analysis belongs in `.claude/docs/` instead, where `/index` can detect when
it has drifted. Anything recoverable from `grep` and `git log` belongs in neither.

A file still carrying `<!-- template-default -->` has never been filled in. Treat its contents as
placeholder, not as fact — an agent that reads "(not set)" as a researched answer is worse off
than one that reads nothing.

## Core

| File | Purpose | When to read |
|------|---------|--------------|
| [Project Brief](project_brief.md) | Stack, architecture, commands | New to the project |
| [Product Context](product_context.md) | Problem, users, goals | Planning a feature |
| [Active Context](active_context.md) | Current session work | Every session start |
| [Progress](progress.md) | Roadmap, milestones | Status check |

## Patterns

| File | Read when |
|------|-----------|
| [System Patterns](system_patterns.md) | Index of the pattern files below |
| [Architecture](patterns/architecture.md) | Structure, error handling, config |
| [Development](patterns/development.md) | **Always** — model/effort selection, the verification bar, autonomy |
| [Testing](patterns/testing.md) | Writing or reviewing tests |
| [Known Issues](patterns/known_issues.md) | Debugging, or before blaming your own change |

## Progress detail

| File | Purpose |
|------|---------|
| [Completed Tasks](progress/completed_tasks.md) | Historical log |
| [Technical Debt](progress/technical_debt.md) | Known issues, prioritized |
| [Architecture Notes](progress/architecture_notes.md) | Design decisions and rationale |

## Elsewhere in `.claude/`

| Location | Holds | Maintained by |
|----------|-------|---------------|
| `.claude/docs/` | Derived analysis with drift detection | `/deep`, `/initialize`, `/index` |
| `.claude/rules/` | Path-scoped coding standards | Hand-written |
| `.claude/skills/` | Workflow and domain skills | Hand-written |
| `.claude/agents/` | Subagent definitions | Hand-written |
| `.claude/state/` | In-flight operation state | `/architect`, `/implement`, `/refactor`, `/migrate` |

## What is deliberately not here

**A registry of source files.** No `DOC_XXX` IDs, no L0–L3 depth tiers, no per-file index of the
tree. Such a registry is derivable from `grep` and `git log`, so it earns no place in curated
memory, and in an active repo it is stale within days. A confidently wrong index is worse than no
index. To find source, use the `explorer` agent or the `codebase-navigator` skill.
