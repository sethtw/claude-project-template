#!/usr/bin/env python3
"""
Knowledge-base drift checker.

Answers one question: can this repo's .claude/ knowledge base still be trusted?

A doc that describes source which has since moved is worse than no doc, because it reads as
current. This finds those, plus the docs that cannot be checked at all.

Usage:
    python .claude/hooks/kb_check.py            # report findings, write nothing
    python .claude/hooks/kb_check.py --write    # also refresh statuses + regenerate the index
    python .claude/hooks/kb_check.py --json     # machine-readable findings
    python .claude/hooks/kb_check.py --brief    # one-line session-start summary
    python .claude/hooks/kb_check.py --prune    # delete orphaned docs, naming each one

Exit codes: 0 = no blocking findings, 1 = blocking findings, 2 = could not run.

Stdlib only. No YAML dependency: the frontmatter parsed here is a deliberately small subset
(scalars plus '- ' lists), and anything it cannot parse becomes a `skipped` finding rather
than a silent pass.
"""

import argparse
import datetime as dt
import glob as globlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKILL_LINE_BUDGET = 150

# Findings that must not reach a commit. `stale` is absent on purpose: a doc may be honestly
# committed stale. `skipped` IS blocking -- silence is not a clean result.
BLOCKING = {"orphaned", "missing-unverified", "dead-glob", "skipped",
            "fork-agent-missing", "fork-tool-gap"}

INDEX_FILES = {"_index.md", "MEMORY.md", "CLAUDE.md", "README.md"}

QUOTE_CHARS = ('"', "'")


# --------------------------------------------------------------------------- infrastructure


def find_repo_root(start):
    for d in [start, *start.parents]:
        if (d / ".claude").is_dir():
            return d
    return start


def git(repo, *args):
    """Run a git command. Returns None when git cannot answer -- never a fabricated empty."""
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=str(repo),
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout


def tracked_files(repo):
    out = git(repo, "ls-files")
    if out is None:
        return None
    return [line for line in out.splitlines() if line]


def last_commit_date(repo, path):
    """Latest commit date touching `path`, as a date. None if git has no record."""
    out = git(repo, "log", "-1", "--format=%cI", "--", path)
    if out is None:
        return None
    stamp = out.strip()
    if not stamp:
        return None
    try:
        return dt.datetime.fromisoformat(stamp).date()
    except ValueError:
        return None


# --------------------------------------------------------------------------- frontmatter

_SCALAR = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
_ITEM = re.compile(r"^\s*-\s+(.*)$")


def parse_frontmatter(text):
    """Return (dict, body). Raises ValueError on a fence this parser cannot handle."""
    if not text.startswith("---"):
        return {}, text
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("frontmatter fence opened but never closed")

    data = {}
    key = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        item = _ITEM.match(raw)
        if item and key is not None:
            if not isinstance(data.get(key), list):
                data[key] = []
            data[key].append(_unquote(item.group(1)))
            continue
        scalar = _SCALAR.match(raw)
        if scalar:
            key = scalar.group(1)
            value = scalar.group(2).strip()
            data[key] = _unquote(value) if value else []
            continue
        raise ValueError("unparseable frontmatter line: " + raw.strip()[:60])

    return data, "\n".join(lines[end + 1:])


def _unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in QUOTE_CHARS:
        return value[1:-1]
    return value


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if v]
    return [value] if value else []


# --------------------------------------------------------------------------- checks


def finding(kind, path, detail, **extra):
    f = {"kind": kind, "path": path, "detail": detail, "blocking": kind in BLOCKING}
    f.update(extra)
    return f


def check_doc(repo, rel, findings):
    """A .claude/docs/ analysis doc: must declare what it describes and when it was checked."""
    full = repo / rel
    try:
        text = full.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        findings.append(finding("skipped", rel, "could not read: {}".format(exc)))
        return None
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as exc:
        findings.append(finding("skipped", rel, str(exc)))
        return None

    sources = as_list(fm.get("sources"))
    verified = fm.get("verified")

    if not sources or not verified:
        missing = " and ".join(
            m for m, ok in (("sources:", sources), ("verified:", verified)) if not ok
        )
        findings.append(
            finding("missing-unverified", rel,
                    "no {} -- drift cannot be detected at all".format(missing))
        )
        return None

    if "## Unverified" not in body:
        findings.append(finding("missing-unverified", rel, "no '## Unverified' section"))

    matched = []
    newest = None
    for pattern in sources:
        for hit in globlib.glob(str(repo / pattern), recursive=True):
            try:
                rel_hit = str(Path(hit).relative_to(repo)).replace(os.sep, "/")
            except ValueError:
                continue
            matched.append(rel_hit)
            when = last_commit_date(repo, rel_hit)
            if when and (newest is None or when > newest):
                newest = when

    if not matched:
        findings.append(
            finding("orphaned", rel,
                    "every sources: glob matches nothing ({} pattern(s)): {}".format(
                        len(sources), ", ".join(sources)))
        )
        return {"rel": rel, "fm": fm, "status": "orphaned", "matched": 0}

    try:
        verified_date = dt.date.fromisoformat(str(verified))
    except ValueError:
        findings.append(
            finding("skipped", rel, "verified: is not an ISO date: {!r}".format(verified))
        )
        return None

    status = "current"
    if newest and newest > verified_date:
        status = "stale"
        findings.append(
            finding("stale", rel,
                    "{} source(s) matched; newest commit {} is after verified: {}".format(
                        len(matched), newest, verified_date))
        )

    window = fm.get("freshness")
    if window and status == "current":
        try:
            days = int(str(window))
            age = (dt.date.today() - verified_date).days
            if age > days:
                status = "stale"
                findings.append(
                    finding("stale", rel,
                            "freshness window {}d lapsed ({}d since verified:)".format(days, age))
                )
        except ValueError:
            findings.append(
                finding("skipped", rel, "freshness: is not an integer: {!r}".format(window))
            )

    return {"rel": rel, "fm": fm, "status": status, "matched": len(matched)}


def check_skill_budget(repo, findings):
    for path in sorted(repo.glob(".claude/skills/*/SKILL.md")):
        rel = str(path.relative_to(repo)).replace(os.sep, "/")
        try:
            n = len(path.read_text(encoding="utf-8").split("\n"))
        except (OSError, UnicodeDecodeError) as exc:
            findings.append(finding("skipped", rel, "could not read: {}".format(exc)))
            continue
        if n > SKILL_LINE_BUDGET:
            findings.append(
                finding("over-budget", rel, "{} lines > {} budget".format(n, SKILL_LINE_BUDGET))
            )


def _tool_set(raw):
    """Parse a `tools:`/`allowed-tools:` value into a set of bare tool names.

    `Agent(explorer, analyzer)` narrows WHICH agent types may be spawned but still grants the
    Agent tool, so the parenthesised part is dropped for this comparison.
    """
    if isinstance(raw, list):
        raw = ",".join(raw)
    names = set()
    for part in re.split(r"[,\s]+", re.sub(r"\([^)]*\)", "", str(raw))):
        part = part.strip()
        if part:
            names.add(part)
    return names


def check_fork_agents(repo, findings):
    """A skill that forks into a subagent gets that SUBAGENT's tools, not its own allowed-tools.

    `allowed-tools` pre-approves permission for tools that are already available; it cannot add a
    tool to a subagent's allowlist. So a skill declaring Write and forking into an agent whose
    `tools:` omits Write reads, concludes, and then silently fails to save -- and the skill still
    reports success, because nothing in it ever learns the write was impossible.

    This check exists because the obvious version -- "does the named agent exist?" -- answers a
    different question and passes on exactly this bug.
    """
    agents = {}
    agent_dir = repo / ".claude/agents"
    if agent_dir.is_dir():
        for path in sorted(agent_dir.rglob("*.md")):
            rel = str(path.relative_to(repo)).replace(os.sep, "/")
            try:
                fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, ValueError) as exc:
                findings.append(finding("skipped", rel, "could not parse: {}".format(exc)))
                continue
            name = fm.get("name") or path.stem
            # An omitted `tools:` inherits every tool available to subagents -- None means
            # "unrestricted", which is different from an empty allowlist.
            agents[name] = _tool_set(fm["tools"]) if fm.get("tools") else None

    for path in sorted(repo.glob(".claude/skills/*/SKILL.md")):
        rel = str(path.relative_to(repo)).replace(os.sep, "/")
        try:
            fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            continue  # already reported by the budget check
        if str(fm.get("context", "")).strip() != "fork":
            continue
        named = str(fm.get("agent", "")).strip()
        if not named:
            continue
        if named not in agents:
            findings.append(
                finding("fork-agent-missing", rel,
                        "context: fork names agent '{}', which has no definition".format(named)))
            continue
        granted = agents[named]
        if granted is None:
            continue  # agent inherits everything
        needed = _tool_set(fm.get("allowed-tools", ""))
        gap = sorted(needed - granted)
        if gap:
            findings.append(
                finding("fork-tool-gap", rel,
                        "declares {} but forks into agent '{}', whose tools: omits {} "
                        "-- allowed-tools cannot grant a subagent a tool it lacks".format(
                            ", ".join(sorted(needed)), named, ", ".join(gap))))


def check_rule_globs(repo, tracked, findings):
    """A rule whose paths: glob matches no tracked file can never load. It is dead weight."""
    if tracked is None:
        findings.append(finding("skipped", ".claude/rules/", "git ls-files unavailable"))
        return
    has_source = repo_has_source(tracked)
    for path in sorted(repo.glob(".claude/rules/*.md")):
        rel = str(path.relative_to(repo)).replace(os.sep, "/")
        try:
            fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            findings.append(finding("skipped", rel, "could not parse: {}".format(exc)))
            continue
        raw = fm.get("paths", "")
        if isinstance(raw, list):
            raw = "\n".join(raw)
        patterns = _split_patterns(str(raw))
        if not patterns:
            continue
        dead = [p for p in patterns if not _any_tracked_match(p, tracked)]
        if len(dead) == len(patterns):
            f = finding("dead-glob", rel,
                        "no tracked file matches: {}".format(", ".join(dead)))
            # A rule matching nothing is only a defect if there is source to match. On a fresh
            # template clone there is none, and a gate that is red on a clean checkout teaches
            # people to ignore it.
            f["blocking"] = has_source
            if not has_source:
                f["detail"] += " (not blocking: repo has no tracked source outside .claude/)"
            findings.append(f)


def _split_patterns(raw):
    """Split a paths: value on commas and newlines -- but never on a comma inside {a,b}."""
    out, buf, depth = [], [], 0
    for ch in raw:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        if (ch in ",\n") and depth == 0:
            out.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    out.append("".join(buf).strip())
    return [p for p in out if p]


def repo_has_source(tracked):
    """True when the repo tracks anything that is not .claude/ config or a root dotfile."""
    if not tracked:
        return False
    for f in tracked:
        if f.startswith(".claude/") or f.startswith(".github/"):
            continue
        if "/" not in f and (f.startswith(".") or f.endswith(".md")):
            continue
        return True
    return False


def _any_tracked_match(pattern, tracked):
    # Brace expansion first -- fnmatch has no {a,b} support, and rules use it heavily.
    for expanded in _expand_braces(pattern):
        regex = _glob_to_regex(expanded)
        if any(regex.match(f) for f in tracked):
            return True
    return False


def _expand_braces(pattern):
    m = re.search(r"\{([^{}]*)\}", pattern)
    if not m:
        return [pattern]
    out = []
    for option in m.group(1).split(","):
        out.extend(_expand_braces(pattern[:m.start()] + option + pattern[m.end():]))
    return out


def _glob_to_regex(pattern):
    out = []
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(out) + "$")


LINK = re.compile(r"\[[^\]]*\]\(([^)]+\.md)(?:#[^)]*)?\)")


def check_links(repo, tracked, findings):
    """A broken link from an index file is blocking -- an index is a promise the target exists."""
    # Untracked files are not part of the shipped knowledge base. `git ls-files` lists staged
    # files too, so a doc reaches this check as soon as it is `git add`ed -- in time for the
    # pre-commit gate, without scratch directories generating permanent noise.
    known = set(tracked) if tracked is not None else None
    seen = set()
    candidates = list((repo / ".claude").rglob("*.md")) + list(repo.glob("*.md"))
    for path in sorted(candidates):
        rel = str(path.relative_to(repo)).replace(os.sep, "/")
        if rel in seen or "/node_modules/" in rel:
            continue
        seen.add(rel)
        if known is not None and rel not in known:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            findings.append(finding("skipped", rel, "could not read: {}".format(exc)))
            continue
        is_index = path.name in INDEX_FILES
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                f = finding("dead-link", rel, "-> {}".format(target))
                f["blocking"] = is_index
                findings.append(f)


# --------------------------------------------------------------------------- index rendering


BEGIN = "<!-- kb:registry:begin -->"
END = "<!-- kb:registry:end -->"

DEFAULT_INDEX = [
    "# Analysis Docs",
    "",
    "> Persisted output from `/deep` and `/initialize`.",
    "> Maintained by `/index`. The frontmatter is the truth; this table is derived.",
    "",
    BEGIN,
    END,
    "",
]


def render_index(repo, docs):
    """Replace ONLY the delimited region, so hand-written sections on either side survive.

    An earlier version kept everything before the '## Registry' heading and regenerated the rest.
    That silently deleted every section AFTER the table on each --write. Explicit delimiters make
    the generated region a bounded thing rather than "the tail of the file".
    """
    path = repo / ".claude/docs/_index.md"
    existing = None
    if path.exists():
        try:
            existing = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            existing = None
    if existing is None:
        existing = list(DEFAULT_INDEX)

    # Whole-line matches only: the file may quote these markers in prose explaining them.
    try:
        i = next(n for n, line in enumerate(existing) if line.strip() == BEGIN)
        j = next(n for n, line in enumerate(existing) if line.strip() == END)
        if j < i:
            raise StopIteration
        before, after = existing[:i + 1], existing[j:]
    except StopIteration:
        before, after = existing + ["", BEGIN], [END, ""]

    rows = [
        "",
        "| Doc | Subject | Scope | Analyzed | Status |",
        "|-----|---------|-------|----------|--------|",
    ]
    for d in sorted(docs, key=lambda x: x["rel"]):
        name = Path(d["rel"]).name
        fm = d["fm"]
        subject = fm.get("subject") or Path(d["rel"]).stem.replace("-", " ")
        scope = ", ".join("`{}`".format(s) for s in as_list(fm.get("sources"))) or "-"
        rows.append("| [{}]({}) | {} | {} | {} | {} |".format(
            name, name, subject, scope, fm.get("verified", "-"), d["status"]))
    if len(rows) == 3:
        rows.append("| _(none yet)_ | | | | |")
    rows += [
        "",
        "`Status`: `current` | `stale` (source moved since analysis) | `orphaned` (subject gone)",
        "",
    ]
    return "\n".join(before + rows + after).rstrip() + "\n"


# --------------------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description="Knowledge-base drift checker")
    ap.add_argument("--write", action="store_true", help="regenerate .claude/docs/_index.md")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    ap.add_argument("--brief", action="store_true", help="one-line summary for SessionStart")
    ap.add_argument("--prune", action="store_true", help="delete orphaned docs, naming each")
    args = ap.parse_args()

    repo = find_repo_root(Path.cwd())
    if not (repo / ".claude").is_dir():
        print("kb_check: no .claude/ directory found", file=sys.stderr)
        return 2

    findings = []
    tracked = tracked_files(repo)

    docs_dir = repo / ".claude/docs"
    doc_paths = sorted(
        p for p in docs_dir.glob("*.md") if not p.name.startswith("_")
    ) if docs_dir.is_dir() else []

    docs = []
    for path in doc_paths:
        rel = str(path.relative_to(repo)).replace(os.sep, "/")
        result = check_doc(repo, rel, findings)
        if result:
            docs.append(result)

    check_skill_budget(repo, findings)
    check_fork_agents(repo, findings)
    check_rule_globs(repo, tracked, findings)
    check_links(repo, tracked, findings)

    # Population, not a bare count: skips are their own bucket and are never a random sample.
    total = len(doc_paths)
    read_ok = len(docs)
    skipped = total - read_ok
    stale = sum(1 for d in docs if d["status"] == "stale")
    orphaned = sum(1 for d in docs if d["status"] == "orphaned")
    blocking = [f for f in findings if f["blocking"]]

    if args.prune:
        for d in docs:
            if d["status"] == "orphaned":
                (repo / d["rel"]).unlink()
                print("pruned: {} (every sources: glob matched nothing)".format(d["rel"]))
        docs = [d for d in docs if d["status"] != "orphaned"]

    if args.write and docs_dir.is_dir():
        (docs_dir / "_index.md").write_text(render_index(repo, docs), encoding="utf-8")

    if args.json:
        print(json.dumps({
            "findings": findings,
            "population": {
                "docs": total, "read": read_ok, "skipped": skipped,
                "stale": stale, "orphaned": orphaned,
            },
        }, indent=2))
        return 1 if blocking else 0

    if args.brief:
        print("kb: {} finding(s) over {} doc(s) -- {} blocking, {} skipped, {} stale".format(
            len(findings), total, len(blocking), skipped, stale))
        return 0  # never fail a session start

    print("kb check: {} of {} doc(s) read; {} stale, {} orphaned, {} skipped".format(
        read_ok, total, stale, orphaned, skipped))
    if not findings:
        print("no findings.")
        return 0
    for f in sorted(findings, key=lambda x: (not x["blocking"], x["kind"], x["path"])):
        mark = "BLOCKING" if f["blocking"] else "        "
        print("  {} {:<19} {}: {}".format(mark, f["kind"], f["path"], f["detail"]))
    print("\n{} blocking of {} finding(s).".format(len(blocking), len(findings)))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
