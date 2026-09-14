# Development Patterns

> How work gets done in this repo: model and effort selection, the verification bar, and the
> autonomy boundary. Not project-specific — this file ships with the template and applies as-is.

## Model and effort selection

**Do not pin a model per task.** Earlier versions of this template assigned `haiku` to discovery,
`sonnet` to writing, and `opus` to planning. That is obsolete, and it was always the wrong lever:

- Model IDs move. A matrix naming specific tiers is wrong within a release or two, and a stale
  matrix silently downgrades work.
- The real cost driver is **context**, not tier. A discovery pass that reads forty files and
  concludes one sentence is expensive because those forty files stay in context — not because of
  which model read them.
- Pinning a reviewer or verifier below the author is how a broken change gets a clean report.

Use these instead:

| Lever | Where | What it does |
|-------|-------|--------------|
| `model: inherit` | Agent frontmatter | Subagent matches the session. The default choice. |
| `effort: low\|medium\|high\|xhigh\|max` | Skill or agent frontmatter | How hard to think, independent of model |
| `context: fork` | Skill frontmatter | Runs in a subagent; its reads never enter the caller's context |
| `background: false` | Skill frontmatter | With `context: fork`, wait for the result in this turn |

A forked skill sees **none** of the calling conversation, so it must restate everything it needs.

Set `effort: high` on planning, architecture, and audit skills. Leave everything else inheriting.

## Delegation

Spawn subagents when the work is genuinely independent — one per distinct search path, sent in a
single message so they run concurrently. Splitting one search across four agents duplicates work
and costs four contexts.

| Agent | Use for |
|-------|---------|
| `explorer` | Where is X, what calls Y, what exists |
| `analyzer` | How does X work, what breaks if I change Y, review this |
| `test-runner` | Run the real gates, diagnose a red to a root cause |
| `security-auditor` | Any diff touching auth, input parsing, queries, paths, or external I/O |

## The verification bar

**Evidence before assertion.** These are the standing rules, and they are the ones most often
skipped under time pressure:

1. **Never claim a gate passed that you did not run.** A gate with no command in this project is
   reported NOT RUN, on its own row — never omitted, never implied green.
2. **Never pipe a gate through `tail` or `head`.** Piping replaces the command's exit status with
   the pipe's, so a crash or a timeout reads as a clean arrival. Read the exit code first.
3. **An absence needs a positive control.** An empty grep, a zero count, a log with no line — each
   is indistinguishable from an instrument that could not match, or never looked. Search for
   something you know is present before reporting that something is not.
4. **A count with no denominator reads as complete.** Report "8 of 19", and report skips as their
   own bucket. Skips are never a random sample.
5. **Separate what code says from what it does.** Reading establishes the former only. Anything
   needing runtime goes under `Unverified` with the command that would settle it.
6. **Cite symbols, not line numbers.** `auth.ts` → `validateSession()` survives the next edit.

## Autonomy

Proceed without asking:

- Reading files, searching, running read-only commands
- Running tests, type checks, and linters
- Fixing formatting, imports, and unused variables
- Writing to `.claude/docs/` and the state files

Ask first:

- Deleting files, force-pushing, rewriting history
- Changing a public interface other code depends on
- Anything outward-facing: publishing, deploying, sending
- Widening a permission or a security boundary

Stop and report rather than continuing:

- The same root cause failed twice — a third blind attempt is guessing
- The gates were red before you started and you cannot separate your breakage from theirs
- A decision needs information you do not have; state the assumption or ask

## Commits

- Stage **explicit paths**. Never `git add -A` or `git add .` — a broad add sweeps in whatever
  else is in the tree, including another session's in-progress work.
- One logical change per commit. A refactor and a behavior change in one diff is unreviewable.
- No agent attribution footers. The author of record is the human.
