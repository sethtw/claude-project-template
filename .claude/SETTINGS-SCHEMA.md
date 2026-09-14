# Claude Code configuration in this repo

> Where each setting lives, and why. **Schema details are not duplicated here** — they live at
> [code.claude.com/docs/en/settings-reference](https://code.claude.com/docs/en/settings-reference)
> and change faster than a copy in a repo can track. A stale local copy of a vendor schema is
> worse than a link: it is read as authoritative and audited by nobody.

## Which file

| File | Applies to | Committed |
|------|-----------|-----------|
| `.claude/settings.json` | Everyone who clones this repo | **Yes** |
| `.claude/settings.local.json` | You, in this project only | No — gitignored |
| `~/.claude/settings.json` | You, in every project | n/a |

Precedence, highest first: managed → `--settings` flag → project local → **shared project** →
user. Local sits above shared, so a personal override needs no commit.

Put hooks and the team permission baseline in `.claude/settings.json`. That is the whole point of
a template — a clone should inherit the wiring without anyone copying a file. Start from
`.claude/settings.local.json.example` for personal overrides.

Two things that do not work from a project file, and will silently not apply:

- `permissions.defaultMode` values `auto` and `bypassPermissions` — set those in user or managed
  settings, or pass `--permission-mode` for one session.
- `permissions.allow`, `additionalDirectories`, and most `env` values wait until the person
  trusts the folder. `deny` and `ask` rules apply immediately.

## Permission rules in this repo

`.claude/settings.json` deliberately ships **no bare `Bash` allow rule**. A bare tool name matches
every command, which would make the granular entries beside it decorative — the exact shape the
previous version of this template had.

Wildcard placement is load-bearing. `Bash(git log *)` allows only `git log`; `Bash(git *)` allows
every git subcommand including `push` and `reset`. Put the `*` after the subcommand, not before —
Claude Code warns at startup about a rule with a wildcard earlier than that.

Use canonical tool names. The subagent tool is **`Agent`**, not `Task`; there is no `Update` or
`Search` tool. A rule naming a tool that does not exist silently allows nothing. The current list
is at [tools-reference](https://code.claude.com/docs/en/tools-reference).

## Hooks in this repo

| Hook | Event | Does |
|------|-------|------|
| `session-history.py` | SessionStart (startup) | Archives the previous session, resets counters |
| `session_start_brief.py` | SessionStart (startup, resume) | Prints repo state, knowledge-base drift, and how much memory is still template default |
| `unified-post-write.py` | PostToolUse `Write\|Edit` | Logs edits to `active_context.md`, syncs state |
| `todo-context-sync.py` | PostToolUse `TodoWrite` | Mirrors todos into `active_context.md` |
| `command-tracker.py` | PostToolUse `Skill` | Increments the commands-run counter |
| `kb_check.py` | Not a hook — run by `/index`, or wire to pre-commit | Knowledge-base drift check |

`session_start_brief.py` deliberately does **not** print a menu of available commands. Claude Code
already enumerates `.claude/skills/`, and a hand-maintained menu drifts the moment a skill is
renamed, then advertises something that no longer exists.

All hooks invoke `python`. On a system where that resolves to Python 2 or is absent, change the
commands in `.claude/settings.json` to `python3`.

## Verifying a change applied

Settings reload without a restart. To confirm a rule is live, trigger it — a permission you think
you granted but did not looks identical to one you never wrote until something prompts.
