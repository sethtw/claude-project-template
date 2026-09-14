# CLAUDE.md

Guidance for Claude Code in this repository. Loaded at the start of every session, so it stays
short — detail lives in the files it points at.

<!-- initialize:begin -->
<!-- `/initialize` writes the project name, description, verified commands, and key directories
     between these two markers on a fresh clone. Everything outside them is hand-written. -->

## Project

(Not yet initialized. Run `/initialize` to populate this section and `.claude/memory/`.)

<!-- initialize:end -->

## Start here

| Resource | Purpose |
|----------|---------|
| @.claude/memory/_index.md | Knowledge base navigation |
| @.claude/memory/patterns/development.md | Model/effort selection, the verification bar, autonomy |
| @.claude/memory/project_brief.md | Stack, architecture, commands |
| @.claude/memory/active_context.md | Current session state |

A memory file still carrying `<!-- template-default -->` has never been filled in. Its contents
are placeholders, not facts — do not cite them as researched answers.

## The verification bar

These are the rules that get skipped under time pressure, and they are the ones that matter:

1. **Never claim a gate passed that you did not run.** A gate with no command in this project is
   reported NOT RUN, on its own row — never omitted, never implied green.
2. **Never pipe a gate through `tail` or `head`.** Piping replaces the command's exit status with
   the pipe's, so a crash or a timeout reads as a clean arrival.
3. **An absence needs a positive control.** An empty grep, a zero count, a log with no line — each
   is indistinguishable from an instrument that could not match or never looked. Prove the search
   works on something you know is there before reporting that something is not.
4. **A count with no denominator reads as complete.** Report "8 of 19", and report skips as their
   own bucket. Skips are never a random sample.
5. **Separate what the code says from what it does.** Reading establishes the former only.
6. **Cite symbols, not line numbers.** `auth.ts` → `validateSession()` survives the next edit.

Full detail: @.claude/memory/patterns/development.md

## Skills

Invoke with `/<name>`. Full list with descriptions: @.claude/memory/system_patterns.md

| Getting oriented | Building | Maintaining |
|------------------|----------|-------------|
| `/initialize` `/analyze` `/deep` | `/architect` `/implement` `/tdd` | `/refactor` `/migrate` `/test-gen` |
| `/context` `/index` | | |

**Not shipped here on purpose:** `/code-review` and `/review` — Claude Code's built-in
`/code-review` covers both, with effort levels, `--fix`, and PR comments. The security skill is
named `security-audit` to avoid colliding with the built-in `/security-review`.

## Memory architecture

| Directory | Holds | Written by |
|-----------|-------|------------|
| `.claude/memory/` | Judgment that cannot be re-derived | Humans; `/initialize` once, on a fresh clone |
| `.claude/docs/` | Derived analysis, with drift detection | `/deep`, `/initialize`, `/index` |
| `.claude/state/` | In-flight operation state | `/architect`, `/implement`, `/refactor`, `/migrate` |
| `.claude/rules/` | Path-scoped coding standards | Humans |

**There is no source-file registry.** No `DOC_XXX` IDs, no L0–L3 depth tiers. Such an index is
derivable from `grep` and `git log` and goes stale within days, and a confidently wrong index is
worse than none. To find source, use the `explorer` agent or the `codebase-navigator` skill.

Every doc in `.claude/docs/` declares `sources:` and `verified:` frontmatter plus an
`## Unverified` section. `python .claude/hooks/kb_check.py` uses those to detect drift; a doc
missing them is a blocking finding, because drift cannot be detected for it at all.

## Autonomy

Proceed without asking: reading, searching, running tests and linters, fixing formatting, writing
to `.claude/docs/` and the state files.

Ask first: deleting files, force-pushing, rewriting history, changing a public interface, anything
outward-facing, widening a permission.

Stop and report: the same root cause failed twice; the gates were red before you started; a
decision needs information you do not have.

## Commits

- Stage **explicit paths**. Never `git add -A` or `git add .` — a broad add sweeps in whatever
  else is in the tree, including another session's in-progress work.
- One logical change per commit. A refactor and a behavior change in one diff is unreviewable.
- **No agent attribution.** No `Co-Authored-By` lines for Claude, no "Generated with" footers.
  The author of record is the human.

## Configuration

Shared config — hooks and the permission baseline — is committed in `.claude/settings.json`.
Personal overrides go in `.claude/settings.local.json`, which is gitignored; start from
`.claude/settings.local.json.example`. Details: @.claude/SETTINGS-SCHEMA.md
