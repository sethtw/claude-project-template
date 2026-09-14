---
name: index
description: Refresh the .claude/docs registry and report knowledge-base drift. Wraps .claude/hooks/kb_check.py.
argument-hint: [--check] [--prune]
allowed-tools: Bash, Read, Edit
disable-model-invocation: true
---

# /index — Knowledge-Base Registry

The algorithm is **not in this file.** It lives in `.claude/hooks/kb_check.py`, where it is
covered by `.claude/hooks/test_kb_check.py` and can run in a pre-commit gate and at session
start. This skill is the human-facing handle on it.

```bash
python .claude/hooks/kb_check.py --write    # default: refresh the index, print findings
python .claude/hooks/kb_check.py            # --check: report drift, write nothing
python .claude/hooks/kb_check.py --json     # machine-readable findings
```

Exit code 0 = no blocking findings, 1 = blocking findings, 2 = could not run. Read the exit code;
never pipe this through `tail` or `head` and judge by what survived.

## What it checks

| Finding | Means | Blocks a commit? |
|---|---|---|
| `dead-link` | A cited `*.md` resolves nowhere | Only from an index file (`_index.md`/`CLAUDE.md`/`README.md`) |
| `stale` | A doc's sources moved after its `verified:` date, or a `freshness:` window lapsed | No — a doc may be honestly committed stale |
| `orphaned` | Every `sources:` glob matches nothing | Yes |
| `missing-unverified` | A doc has no `sources:`/`verified:` frontmatter, or no `## Unverified` | Yes |
| `over-budget` | A `SKILL.md` exceeds 150 lines | No |
| `dead-glob` | A rule's `paths:` glob matches no tracked file — the rule can never load | Yes, unless the repo tracks no source at all |
| `skipped` | The checker could not read or parse something | Yes — silence is not a clean result |

Untracked files are not checked. `git ls-files` lists staged files, so a new doc enters the check
the moment it is `git add`ed — in time for a pre-commit gate, without scratch directories
generating permanent noise.

## Then regenerate the registry

`--write` rewrites the `.claude/docs/_index.md` table from each doc's frontmatter. **The
frontmatter is the truth and the table is derived** — never hand-edit a status into the table,
change it in the doc and re-run.

Report counts **with the population**: "N docs, of M present; K stale, J skipped." A bare count is
not a result — it reads as complete whatever it actually swept, and skips are never a random sample.

## `--prune`

Delete docs whose every source glob matches nothing (`orphaned`), and **announce every deletion by
name**. A silent prune is indistinguishable from "nothing was there."

## What is deliberately NOT indexed

Source files. No `DOC_XXX` IDs, no L0/L1/L2 depth tiers, no file-level registry of the tree. Such
a registry is derivable from `grep` and `git log`, so it earns no place in memory, and in an
active repo it is stale within days — confidently wrong beats absent. To find source, use the
`explorer` agent or the `codebase-navigator` skill.
