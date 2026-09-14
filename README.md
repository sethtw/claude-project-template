# claude-project-template

A starting `.claude/` for a new project: skills, subagents, path-scoped rules, hooks, and a
knowledge base that can tell you when it has gone stale.

## Use it

```bash
git clone https://github.com/sethtw/claude-project-template.git my-project
cd my-project && rm -rf .git && git init
claude
/initialize
```

`/initialize` reads the repo and fills `.claude/memory/` plus the project section of `CLAUDE.md`.
It does that **once** — on a fresh clone, detected by a marker in the unfilled memory files. After
that it is additive and writes only to `.claude/docs/`, so it can never overwrite curated
judgment with auto-detected guesses.

## What is in here

| Path | Holds |
|------|-------|
| `CLAUDE.md` | Loaded every session. Deliberately short. |
| `.claude/skills/` | 18 skills: `/initialize` `/analyze` `/deep` `/index` `/context` `/architect` `/implement` `/tdd` `/test-gen` `/refactor` `/migrate`, plus domain skills |
| `.claude/agents/` | `explorer` `analyzer` `test-runner` `security-auditor` — all `model: inherit` |
| `.claude/memory/` | Curated judgment. Hand-written; `/initialize` seeds it once. |
| `.claude/docs/` | Derived analysis with drift detection. Written by `/deep`. |
| `.claude/rules/` | Path-scoped standards, loaded automatically by glob |
| `.claude/hooks/` | Session start, post-write sync, and the knowledge-base checker |
| `.claude/settings.json` | Shared hooks and permission baseline. Committed. |

## The knowledge base can tell you when it is wrong

Every doc in `.claude/docs/` declares what source it describes and when it was last checked:

```yaml
---
sources: ["src/auth/**/*.ts"]
verified: 2026-09-14
---
```

`python .claude/hooks/kb_check.py` compares those globs against `git log` and reports drift. A doc
with no `sources:`/`verified:` is a **blocking** finding — not because it is wrong, but because
drift cannot be detected for it at all, which is worse than being wrong loudly.

```bash
python .claude/hooks/kb_check.py            # report drift
python .claude/hooks/kb_check.py --write    # refresh the registry table
python .claude/hooks/test_kb_check.py       # 30 checks; every finding kind has a control
```

The test suite exists because a checker that reports nothing is indistinguishable from one that
*can* report nothing. Each finding kind has a fixture that must trigger it and a green control
that must stay silent.

## Design decisions worth knowing before you change things

**No source-file registry.** No `DOC_XXX` IDs, no L0–L3 depth tiers. An index of the tree is
derivable from `grep` and `git log`, and goes stale within days — a confidently wrong index is
worse than none.

**No model tiering.** Agents use `model: inherit`; skills set `effort` instead. Pinning a verifier
below the author is how a broken change gets a clean report, and a matrix naming specific model
tiers is wrong within a release or two.

**No `/code-review` or `/review`.** Claude Code ships `/code-review` with effort levels, `--fix`,
and PR comments. The security skill is named `security-audit` to avoid colliding with the built-in
`/security-review`.

**No filesystem MCP server.** Built-in `Read`/`Glob`/`Grep` already cover local files, scoped to
the session's working directories. A filesystem server duplicates them and needs a hardcoded
absolute path that is wrong in every clone.

**No hand-maintained command menu at session start.** Claude Code enumerates `.claude/skills/`
already; a static menu drifts and then advertises commands that no longer exist. The session hook
prints what Claude *cannot* derive — repo state, knowledge-base drift, and how much memory is
still unfilled.

## Requirements

Python 3.8+ on `PATH` as `python` for the hooks. If yours is `python3`, change the hook commands
in `.claude/settings.json`. Git is required for drift detection — the checker reads commit dates.
