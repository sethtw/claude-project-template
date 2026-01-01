#!/usr/bin/env python3
"""
Post-write hook: Track file modifications in active_context.md.

Updates:
- "Completed This Session" table in active_context.md
- "Documents Touched" counter in state/_index.md

Skips files inside .claude/ directory (metadata files).
"""

import json
import sys
from pathlib import Path

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (  # type: ignore
    find_project_root,
    is_inside_claude_dir,
    read_markdown_file,
    write_markdown_file,
    add_table_row,
    increment_counter,
    get_timestamp,
)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Not valid JSON, skip
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

        # Update active_context.md
        active_context_path = project_root / ".claude" / "memory" / "active_context.md"
        content = read_markdown_file(active_context_path)

        if content:
            # Get relative path for display
            try:
                rel_path = Path(file_path).relative_to(project_root)
            except ValueError:
                rel_path = Path(file_path).name

            filename = Path(file_path).name
            timestamp = get_timestamp()

            # Determine action based on tool
            action = "Modified" if tool_name == "Edit" else "Created/Updated"

            # Add row to "Completed This Session" table
            new_row = {
                "Task": f"{action} {filename}",
                "Files": str(rel_path),
                "Notes": timestamp,
            }
            headers = ["Task", "Files", "Notes"]

            content = add_table_row(content, "Completed This Session", new_row, headers)
            write_markdown_file(active_context_path, content)

        # Update Documents Touched counter in state/_index.md
        state_index_path = project_root / ".claude" / "state" / "_index.md"
        state_content = read_markdown_file(state_index_path)

        if state_content:
            state_content = increment_counter(state_content, "Current Session", "Documents Touched")
            write_markdown_file(state_index_path, state_content)

    except Exception as e:
        # Log error to stderr (visible to user) but don't fail the hook
        print(f"session-tracker: {e}", file=sys.stderr)

    # Always return empty object (silent mode)
    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
