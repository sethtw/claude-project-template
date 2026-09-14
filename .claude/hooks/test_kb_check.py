#!/usr/bin/env python3
"""
Tests for kb_check.py.

Every finding kind gets a RED fixture that must produce it and a GREEN control that must not.
The controls are the point: a checker that reports nothing is indistinguishable from a checker
that cannot report anything, and only a fixture it demonstrably catches tells the two apart.

Run:  python .claude/hooks/test_kb_check.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "kb_check.py"

FAILURES = []


def sh(cwd, *args, **env):
    e = dict(os.environ)
    e.update(env)
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, env=e)


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return rel


def run_checker(root, *args):
    out = sh(root, sys.executable, str(root / ".claude/hooks/kb_check.py"), *args)
    return out.stdout, out.returncode


def findings(root):
    out, _ = run_checker(root, "--json")
    return json.loads(out)["findings"]


def build(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / ".claude/hooks").mkdir(parents=True, exist_ok=True)
    shutil.copy(CHECKER, root / ".claude/hooks/kb_check.py")
    sh(root, "git", "init", "-q", ".")
    sh(root, "git", "config", "user.email", "t@example.com")
    sh(root, "git", "config", "user.name", "t")
    write(root, "src/real.ts", "export const real = 1;\n")
    return root


def commit(root, *paths, date=None):
    sh(root, "git", "add", *paths)
    env = {}
    if date:
        env = {"GIT_COMMITTER_DATE": date, "GIT_AUTHOR_DATE": date}
    sh(root, "git", "commit", "-qm", "fixture", **env)


def expect(condition, label):
    if condition:
        print("  PASS  {}".format(label))
    else:
        print("  FAIL  {}".format(label))
        FAILURES.append(label)


def kinds_for(fs, path):
    return {f["kind"] for f in fs if f["path"].endswith(path)}


DOC_OK = (
    '---\nsources:\n  - "src/real.ts"\nverified: 2099-01-01\n---\n\n'
    "## Unverified\nnone -- all claims executed\n"
)


def test_docs():
    print("docs:")
    with tempfile.TemporaryDirectory() as td:
        root = build(Path(td))
        write(root, ".claude/docs/good.md", DOC_OK)
        write(root, ".claude/docs/orphan.md",
              '---\nsources:\n  - "src/gone/**/*.ts"\nverified: 2099-01-01\n---\n\n## Unverified\nn\n')
        write(root, ".claude/docs/bare.md", "# no frontmatter\n")
        write(root, ".claude/docs/nounver.md",
              '---\nsources:\n  - "src/real.ts"\nverified: 2099-01-01\n---\n\nbody\n')
        write(root, ".claude/docs/broken.md", '---\nsources:\n  - "src/real.ts"\n')
        commit(root, "src", ".claude")
        fs = findings(root)

        expect("orphaned" in kinds_for(fs, "orphan.md"), "orphaned fires on a glob matching nothing")
        expect("missing-unverified" in kinds_for(fs, "bare.md"), "missing-unverified fires with no frontmatter")
        expect("missing-unverified" in kinds_for(fs, "nounver.md"), "missing-unverified fires with no ## Unverified")
        expect("skipped" in kinds_for(fs, "broken.md"), "skipped fires on an unclosed fence")
        expect(kinds_for(fs, "good.md") == set(), "GREEN CONTROL: a correct doc produces no finding")
        expect(all(f["blocking"] for f in fs if f["kind"] in
                   ("orphaned", "missing-unverified", "skipped")), "those three kinds block")


def test_stale():
    print("stale:")
    with tempfile.TemporaryDirectory() as td:
        root = build(Path(td))
        write(root, ".claude/docs/good.md", DOC_OK)
        write(root, ".claude/docs/moved.md",
              '---\nsources:\n  - "src/real.ts"\nverified: 2020-01-01\n---\n\n## Unverified\nn\n')
        commit(root, "src", ".claude")
        fs = findings(root)
        expect("stale" in kinds_for(fs, "moved.md"), "stale fires when a source moved after verified:")
        expect(kinds_for(fs, "good.md") == set(), "GREEN CONTROL: a future verified: date is not stale")
        expect(not any(f["blocking"] for f in fs if f["kind"] == "stale"), "stale does NOT block")


def test_freshness_window():
    print("freshness window:")
    with tempfile.TemporaryDirectory() as td:
        root = build(Path(td))
        write(root, "src/old.ts", "old\n")
        commit(root, "src/old.ts", date="2024-01-01T00:00:00")
        # Source last moved 2024-01-01, verified after that, so the source-moved branch cannot
        # fire -- the only way to reach `stale` here is the freshness window itself.
        write(root, ".claude/docs/window.md",
              '---\nsources:\n  - "src/old.ts"\nverified: 2024-06-01\nfreshness: 30\n---\n\n## Unverified\nn\n')
        write(root, ".claude/docs/nowindow.md",
              '---\nsources:\n  - "src/old.ts"\nverified: 2024-06-01\n---\n\n## Unverified\nn\n')
        commit(root, ".claude")
        fs = findings(root)
        expect("stale" in kinds_for(fs, "window.md"), "stale fires on a lapsed freshness: window")
        expect(kinds_for(fs, "nowindow.md") == set(),
               "GREEN CONTROL: same dates without freshness: stays current")


def test_rules_and_skills():
    print("rules and skills:")
    with tempfile.TemporaryDirectory() as td:
        root = build(Path(td))
        write(root, ".claude/rules/dead.md", "---\npaths: nope/**/*.{ts,tsx}\n---\n# dead\n")
        write(root, ".claude/rules/live.md", "---\npaths: src/**/*.{ts,tsx}\n---\n# live\n")
        write(root, ".claude/skills/fat/SKILL.md",
              "---\nname: fat\n---\n" + "\n".join("line {}".format(i) for i in range(200)))
        write(root, ".claude/skills/lean/SKILL.md", "---\nname: lean\n---\nshort\n")
        commit(root, "src", ".claude")
        fs = findings(root)
        expect("dead-glob" in kinds_for(fs, "rules/dead.md"), "dead-glob fires on a glob matching no tracked file")
        expect(kinds_for(fs, "rules/live.md") == set(),
               "GREEN CONTROL: a rule whose brace glob DOES match is silent")
        expect("over-budget" in kinds_for(fs, "skills/fat/SKILL.md"), "over-budget fires above 150 lines")
        expect(kinds_for(fs, "skills/lean/SKILL.md") == set(), "GREEN CONTROL: a short skill is silent")


def test_dead_glob_needs_source():
    print("dead-glob blocking depends on there being source:")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        root.mkdir(parents=True, exist_ok=True)
        (root / ".claude/hooks").mkdir(parents=True, exist_ok=True)
        shutil.copy(CHECKER, root / ".claude/hooks/kb_check.py")
        sh(root, "git", "init", "-q", ".")
        sh(root, "git", "config", "user.email", "t@example.com")
        sh(root, "git", "config", "user.name", "t")
        write(root, ".claude/rules/dead.md", "---\npaths: src/**/*.ts\n---\n# dead\n")
        commit(root, ".claude")
        fs = findings(root)
        dead = [f for f in fs if f["kind"] == "dead-glob"]
        expect(dead and not dead[0]["blocking"],
               "GREEN CONTROL: on a repo with no tracked source, dead-glob does not block")


def test_links():
    print("links:")
    with tempfile.TemporaryDirectory() as td:
        root = build(Path(td))
        write(root, ".claude/docs/_index.md", "# Index\n\n[gone](nowhere.md)\n")
        write(root, ".claude/docs/note.md", DOC_OK + "\n[also gone](nothing.md)\n")
        commit(root, "src", ".claude")
        fs = findings(root)
        idx = [f for f in fs if f["kind"] == "dead-link" and f["path"].endswith("_index.md")]
        note = [f for f in fs if f["kind"] == "dead-link" and f["path"].endswith("note.md")]
        expect(idx and idx[0]["blocking"], "dead-link from an index file blocks")
        expect(note and not note[0]["blocking"], "dead-link from a non-index file does not block")

        # Untracked files must not be checked at all.
        write(root, ".claude/scratch/untracked.md", "[nope](gone.md)\n")
        fs2 = findings(root)
        expect(not any("untracked.md" in f["path"] for f in fs2),
               "GREEN CONTROL: an untracked file is not checked")


def test_write_and_prune():
    print("write and prune:")
    with tempfile.TemporaryDirectory() as td:
        root = build(Path(td))
        write(root, ".claude/docs/good.md", DOC_OK)
        write(root, ".claude/docs/orphan.md",
              '---\nsources:\n  - "src/gone/**/*.ts"\nverified: 2099-01-01\n---\n\n## Unverified\nn\n')
        commit(root, "src", ".claude")

        # An index with hand-written prose on BOTH sides of the generated region. The earlier
        # implementation kept only what preceded the table and regenerated the rest, silently
        # deleting the trailing section on every --write.
        write(root, ".claude/docs/_index.md",
              "# Analysis Docs\n\nPROSE ABOVE\n\n<!-- kb:registry:begin -->\n<!-- kb:registry:end -->\n\n"
              "## Maintenance\n\nPROSE BELOW\n")
        run_checker(root, "--write")
        table = (root / ".claude/docs/_index.md").read_text(encoding="utf-8")
        expect("| [good.md](good.md) |" in table, "--write renders a row per doc")
        expect("orphaned" in table, "--write carries each doc's status into the table")
        expect("PROSE ABOVE" in table, "--write preserves prose before the generated region")
        expect("PROSE BELOW" in table, "--write preserves prose AFTER the generated region")
        expect(table.count("<!-- kb:registry:begin -->") == 1,
               "--write does not duplicate the region markers")

        run_checker(root, "--write")
        twice = (root / ".claude/docs/_index.md").read_text(encoding="utf-8")
        expect(twice == table, "--write is idempotent")

        # No markers at all: the region must be appended, not silently dropped.
        write(root, ".claude/docs/_index.md", "# Analysis Docs\n\nONLY PROSE\n")
        run_checker(root, "--write")
        seeded = (root / ".claude/docs/_index.md").read_text(encoding="utf-8")
        expect("ONLY PROSE" in seeded and "| [good.md](good.md) |" in seeded,
               "--write seeds the region into an index that has no markers")

        out, _ = run_checker(root, "--prune")
        expect("pruned: .claude/docs/orphan.md" in out, "--prune names every deletion")
        expect(not (root / ".claude/docs/orphan.md").exists(), "--prune actually deletes")
        expect((root / ".claude/docs/good.md").exists(), "GREEN CONTROL: --prune spares a healthy doc")

        _, code = run_checker(root, "--brief")
        expect(code == 0, "--brief never fails a session start")


def main():
    if not CHECKER.exists():
        print("kb_check.py not found next to this test", file=sys.stderr)
        return 2
    for fn in (test_docs, test_stale, test_freshness_window, test_rules_and_skills,
               test_dead_glob_needs_source, test_links, test_write_and_prune):
        fn()
    print()
    if FAILURES:
        print("{} FAILED:".format(len(FAILURES)))
        for f in FAILURES:
            print("  - {}".format(f))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
