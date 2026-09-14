# Analysis Docs

> Persisted output from `/deep` and `/initialize`.
> Maintained by `/index`. The frontmatter is the truth; the table below is derived from it.

## What belongs here

Analysis artifacts: subsystem maps, surface onboarding docs, traced data flows. Content that is
**derived and regenerable**.

Durable judgment — why the architecture is shaped this way, what was tried and abandoned — belongs
in `.claude/memory/`, not here.

## Every doc carries drift detection

```yaml
---
sources:
  - "src/auth/**/*.ts"     # what this doc describes
verified: 2026-09-14       # when someone last checked it against that source
freshness: 90              # optional: re-check after N days even if source is untouched
---
```

`python .claude/hooks/kb_check.py` compares each `sources:` glob against `git log` and flags a doc
whose source moved after its `verified:` date. A doc missing either field is a **blocking**
finding — not because the doc is wrong, but because drift cannot be detected for it at all, which
is worse. A `## Unverified` section is required for the same reason.

## What is deliberately NOT here

**Source files are not indexed.** No `DOC_XXX` IDs, no L0/L1/L2 depth tiers, no file-level
registry of the tree. A source registry is derivable from `grep` and `git log`, and in an active
repo it is stale within days — confidently wrong beats absent. To find source, use the `explorer`
agent or the `codebase-navigator` skill.

## Registry

Everything between the two `kb:registry` marker comments below is **generated**. `--write`
replaces only that region, so anything written above or below it survives. Do not hand-edit a row;
change the doc's frontmatter and re-run.

<!-- kb:registry:begin -->

| Doc | Subject | Scope | Analyzed | Status |
|-----|---------|-------|----------|--------|
| _(none yet)_ | | | | |

`Status`: `current` | `stale` (source moved since analysis) | `orphaned` (subject gone)

<!-- kb:registry:end -->

## Maintenance

```bash
python .claude/hooks/kb_check.py            # report drift, write nothing
python .claude/hooks/kb_check.py --write    # refresh the table from the docs' frontmatter
python .claude/hooks/kb_check.py --prune    # delete orphaned docs, naming each one
python .claude/hooks/test_kb_check.py       # prove the checker still detects what it claims to
```

Run the test suite after touching the checker. Every finding kind has a fixture that must produce
it **and** a control that must stay silent — a checker reporting nothing is otherwise
indistinguishable from one that cannot report anything.
