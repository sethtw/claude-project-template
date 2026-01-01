#!/usr/bin/env python3
"""
Post-write hook: Sync state file changes to state/_index.md.

When a state file (.claude/state/*.md) is updated, this hook
extracts the current status/progress and updates the "Active States"
table in state/_index.md.

Skips _index.md itself to prevent infinite loops.
"""

import json
import re
import sys
from pathlib import Path

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (  # type: ignore
    find_project_root,
    read_markdown_file,
    write_markdown_file,
    parse_table_rows,
    update_table_section,
    get_timestamp,
)


def is_state_file(file_path: str) -> bool:
    """Check if path is a state file (not _index.md)."""
    path = Path(file_path)

    # Must be in .claude/state/ directory
    parts = path.parts
    try:
        state_idx = parts.index("state")
        claude_idx = parts.index(".claude")
        # state must be directly under .claude
        if state_idx != claude_idx + 1:
            return False
    except ValueError:
        return False

    # Must be a .md file but not _index.md
    if not path.name.endswith(".md"):
        return False
    if path.name == "_index.md":
        return False

    return True


def extract_state_info(content: str) -> dict:
    """Extract status, progress, started from a state file."""
    info = {
        "status": "-",
        "progress": "-",
        "started": "-",
    }

    # Look for Status field in a table
    status_match = re.search(r"\| Status \| ([^|]+) \|", content)
    if status_match:
        info["status"] = status_match.group(1).strip()

    # Look for Progress field
    progress_match = re.search(r"\| Progress \| ([^|]+) \|", content)
    if progress_match:
        info["progress"] = progress_match.group(1).strip()

    # Look for Started field
    started_match = re.search(r"\| Started \| ([^|]+) \|", content)
    if started_match:
        info["started"] = started_match.group(1).strip()

    return info


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

    # Only process state files
    if not is_state_file(file_path):
        print("{}")
        sys.exit(0)

    try:
        project_root = find_project_root(file_path)
        if not project_root:
            print("{}")
            sys.exit(0)

        # Read the state file that was just written
        state_file_path = Path(file_path)
        state_content = read_markdown_file(state_file_path)

        if not state_content:
            print("{}")
            sys.exit(0)

        # Extract state info
        state_info = extract_state_info(state_content)

        # Get operation name from filename (e.g., "refactor_state.md" -> "refactor")
        operation_name = state_file_path.stem.replace("_state", "").replace("_", " ").title()

        # Get relative path to state file
        try:
            rel_state_path = state_file_path.relative_to(project_root)
        except ValueError:
            rel_state_path = state_file_path.name

        # Read state/_index.md
        index_path = project_root / ".claude" / "state" / "_index.md"
        index_content = read_markdown_file(index_path)

        if not index_content:
            print("{}")
            sys.exit(0)

        # Parse existing Active States table
        existing_rows = parse_table_rows(index_content, "Active States")

        # Filter out placeholder rows and find/update this operation
        real_rows = [r for r in existing_rows if r.get("Operation", "(none)") != "(none)"]

        # Check if this operation already exists
        found = False
        for row in real_rows:
            if row.get("State File", "") == str(rel_state_path) or row.get("Operation", "") == operation_name:
                # Update existing row
                row["Status"] = state_info["status"]
                row["Progress"] = state_info["progress"]
                row["Started"] = state_info["started"]
                found = True
                break

        if not found:
            # Add new row
            real_rows.append({
                "Operation": operation_name,
                "State File": str(rel_state_path),
                "Status": state_info["status"],
                "Progress": state_info["progress"],
                "Started": state_info["started"],
            })

        # Update the index
        headers = ["Operation", "State File", "Status", "Progress", "Started"]
        index_content = update_table_section(index_content, "Active States", real_rows, headers)
        write_markdown_file(index_path, index_content)

    except Exception as e:
        print(f"state-sync: {e}", file=sys.stderr)

    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
