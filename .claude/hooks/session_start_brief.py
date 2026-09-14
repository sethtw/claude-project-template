#!/usr/bin/env python3
"""
SessionStart hook: a short, honest orientation line.

stdout is added to Claude's context, so it stays small on purpose. Notably absent: a list of
available skills and commands. Claude Code already enumerates those from `.claude/skills/`, and a
hand-maintained menu is worse than none -- it drifts the moment a skill is added or renamed, and
then confidently advertises a command that no longer exists.

What Claude cannot derive on its own is state: how much of the knowledge base is populated,
whether it has drifted, and what is uncommitted. That is what this prints.

stderr is shown to the user and is not added to context.
"""

import json
import subprocess
import sys
from pathlib import Path

# Kept out of prose everywhere it is explained -- see the whole-line match below.
MARKER = "<!-- template-default -->"


def find_root(start):
    for d in [start, *start.parents]:
        if (d / ".claude").is_dir():
            return d
    return None


def run(root, *args):
    try:
        out = subprocess.run(args, cwd=str(root), capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def main():
    try:
        json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        pass  # A hook with no payload still has useful work to do.

    root = find_root(Path.cwd())
    if root is None:
        print("{}")
        return 0

    lines = []

    branch = run(root, "git", "rev-parse", "--abbrev-ref", "HEAD")
    dirty = run(root, "git", "status", "--porcelain")
    if branch:
        n = len([x for x in (dirty or "").splitlines() if x])
        lines.append("repo: {} | {}".format(branch, "clean" if n == 0 else "{} uncommitted".format(n)))

    # Knowledge-base drift. --brief never fails a session start, but it CAN fail to run at all
    # (no python on PATH under this name, a syntax error). Saying so beats printing nothing,
    # which is indistinguishable from a clean result.
    checker = root / ".claude/hooks/kb_check.py"
    if checker.exists():
        brief = run(root, sys.executable, str(checker), "--brief")
        lines.append(brief if brief else "kb: checker did not run -- `python .claude/hooks/kb_check.py` to see why")

    # How much of the template is still unfilled. A fresh clone should say so out loud rather
    # than let an agent treat placeholder memory as researched fact.
    #
    # The match is a WHOLE LINE, not a substring. Documenting a marker breaks a substring search
    # for it: _index.md and the /initialize skill both quote this marker in prose explaining what
    # it means, and a naive `in` test counts those explanations as unfilled files.
    memory = list((root / ".claude/memory").rglob("*.md")) if (root / ".claude/memory").is_dir() else []
    defaults = []
    for p in memory:
        try:
            body = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if any(line.strip() == MARKER for line in body.splitlines()):
            defaults.append(p.name)
    if defaults:
        shown = sorted(defaults)[:3]
        lines.append(
            "memory: {} of {} file(s) still template defaults ({}{}) -- run /initialize".format(
                len(defaults), len(memory), ", ".join(shown),
                ", ..." if len(defaults) > 3 else ""))

    if lines:
        print("\n".join(lines))
        print("\n".join(lines), file=sys.stderr)
    else:
        print("{}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
