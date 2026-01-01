#!/usr/bin/env python3
"""
Post-TodoWrite hook: Sync todo items to active_context.md.

Updates:
- "In Progress" table with in_progress todos
- "Completed This Session" table with newly completed todos

Provides session visibility into current work status.
"""

import json
import sys
from pathlib import Path

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (  # type: ignore
    find_project_root,
    read_markdown_file,
    write_markdown_file,
    update_table_section,
    add_table_row,
    get_timestamp,
)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("{}")
        sys.exit(0)

    # Only process TodoWrite tool
    tool_name = input_data.get("tool_name", "")
    if tool_name != "TodoWrite":
        print("{}")
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    todos = tool_input.get("todos", [])

    if not todos:
        print("{}")
        sys.exit(0)

    try:
        # Find project root from current working directory
        cwd = input_data.get("cwd", "")
        if cwd:
            project_root = find_project_root(cwd)
        else:
            # Fallback to script location
            project_root = find_project_root(str(Path(__file__)))

        if not project_root:
            print("{}")
            sys.exit(0)

        # Read active_context.md
        active_context_path = project_root / ".claude" / "memory" / "active_context.md"
        content = read_markdown_file(active_context_path)

        if not content:
            print("{}")
            sys.exit(0)

        # Extract in_progress todos for "In Progress" table
        in_progress_todos = [t for t in todos if t.get("status") == "in_progress"]
        in_progress_rows = []

        for todo in in_progress_todos:
            in_progress_rows.append({
                "Task": todo.get("content", "Unknown task"),
                "Status": "In Progress",
                "Notes": todo.get("activeForm", "-"),
            })

        # Update "In Progress" table
        in_progress_headers = ["Task", "Status", "Notes"]
        content = update_table_section(content, "In Progress", in_progress_rows, in_progress_headers)

        # For completed todos, we track them but don't overwrite existing entries
        # The session-tracker hook handles file completions; this handles task completions
        completed_todos = [t for t in todos if t.get("status") == "completed"]
        timestamp = get_timestamp()

        for todo in completed_todos:
            task_content = todo.get("content", "Unknown task")
            # Only add if it looks like a meaningful completion (not just file edits)
            if not task_content.startswith("Modified") and not task_content.startswith("Created"):
                new_row = {
                    "Task": f"Completed: {task_content[:50]}",
                    "Files": "-",
                    "Notes": timestamp,
                }
                content = add_table_row(content, "Completed This Session", new_row, ["Task", "Files", "Notes"])

        write_markdown_file(active_context_path, content)

    except Exception as e:
        print(f"todo-context-sync: {e}", file=sys.stderr)

    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
