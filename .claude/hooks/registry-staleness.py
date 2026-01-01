#!/usr/bin/env python3
"""
Post-write hook: Mark registry entries as stale when source files change.

When a file outside .claude/ is modified, checks if it exists in _registry.md
and adds a staleness marker to indicate it needs re-indexing.

Staleness is indicated by adding a timestamp to a "Modified" column or
prefixing the entry with a warning marker.
"""

import json
import re
import sys
from pathlib import Path

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (  # type: ignore
    find_project_root,
    is_inside_claude_dir,
    read_markdown_file,
    write_markdown_file,
    get_timestamp,
)


def find_registry_entry(content: str, file_path: str, project_root: Path) -> tuple[str, str] | None:
    """
    Find a registry entry for the given file path.

    Returns (old_line, match_info) if found, None otherwise.
    """
    # Get various path representations to search for
    path = Path(file_path)

    try:
        rel_path = path.relative_to(project_root)
    except ValueError:
        rel_path = path

    # Patterns to search for in registry
    search_patterns = [
        str(rel_path),
        str(rel_path).replace("\\", "/"),
        path.name,
    ]

    for pattern in search_patterns:
        # Look for table row containing this path
        escaped = re.escape(pattern)
        row_match = re.search(rf"^\|[^|]*\| *{escaped} *\|.*$", content, re.MULTILINE)
        if row_match:
            return row_match.group(0), pattern

    return None


def mark_entry_stale(content: str, old_line: str, timestamp: str) -> str:
    """
    Mark a registry entry as stale by adding a modification indicator.

    Strategy: Add or update a "Modified" notation in the Notes column,
    or prepend with a warning emoji if no Notes column exists.
    """
    # Count columns in the line
    columns = old_line.split("|")
    num_columns = len([c for c in columns if c.strip() or c == ""])

    if num_columns >= 5:
        # Has enough columns - update the last column (Notes)
        parts = old_line.rsplit("|", 2)
        if len(parts) >= 2:
            # Preserve the structure but update notes
            notes_col = parts[-2].strip()
            if "Modified:" in notes_col:
                # Already has modification marker, update timestamp
                notes_col = re.sub(r"Modified: [\d\-: ]+", f"Modified: {timestamp}", notes_col)
            else:
                # Add modification marker
                if notes_col and notes_col != "-":
                    notes_col = f"{notes_col}; Modified: {timestamp}"
                else:
                    notes_col = f"Modified: {timestamp}"

            new_line = f"{parts[0]}| {notes_col} |"
            return content.replace(old_line, new_line)

    # Fallback: prepend warning emoji to the ID column if not already present
    if not old_line.startswith("| \u26a0"):
        # Find first column content
        first_col_match = re.match(r"\| *([^|]+) *\|", old_line)
        if first_col_match:
            first_col = first_col_match.group(1).strip()
            if not first_col.startswith("\u26a0"):
                new_first_col = f"\u26a0\ufe0f {first_col}"
                new_line = old_line.replace(f"| {first_col} |", f"| {new_first_col} |", 1)
                return content.replace(old_line, new_line)

    return content


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("{}")
        sys.exit(0)

    # Only process Write and Edit tools
    tool_name = input_data.get("tool_name", "")
    if tool_name not in ["Write", "Edit"]:
        print("{}")
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        print("{}")
        sys.exit(0)

    # Skip files inside .claude/ directory
    if is_inside_claude_dir(file_path):
        print("{}")
        sys.exit(0)

    try:
        project_root = find_project_root(file_path)
        if not project_root:
            print("{}")
            sys.exit(0)

        # Read _registry.md
        registry_path = project_root / ".claude" / "memory" / "_registry.md"
        content = read_markdown_file(registry_path)

        if not content:
            # No registry file exists yet
            print("{}")
            sys.exit(0)

        # Check if file exists in registry
        result = find_registry_entry(content, file_path, project_root)
        if not result:
            # File not in registry - nothing to mark stale
            print("{}")
            sys.exit(0)

        old_line, matched_pattern = result
        timestamp = get_timestamp()

        # Mark the entry as stale
        new_content = mark_entry_stale(content, old_line, timestamp)

        if new_content != content:
            write_markdown_file(registry_path, new_content)

    except Exception as e:
        print(f"registry-staleness: {e}", file=sys.stderr)

    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
