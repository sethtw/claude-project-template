#!/usr/bin/env python3
"""
Session start hook: Archive previous session to history.

When a new session starts, this hook:
1. Archives "Completed This Session" from active_context.md to state/_index.md
2. Resets the "Completed This Session" table
3. Resets session counters (Documents Touched, Commands Run)
4. Generates a session summary row in Session History
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (  # type: ignore
    find_project_root,
    read_markdown_file,
    write_markdown_file,
    parse_table_rows,
    add_table_row,
    get_date,
)


def reset_session_table(content: str, section_header: str, headers: list[str]) -> str:
    """Reset a table to its empty state with placeholder row."""
    # Find the section
    pattern = rf"(^##\s+{re.escape(section_header)}\s*$)"
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return content

    section_start = match.end()

    # Find next section or separator
    remaining = content[section_start:]
    next_section = re.search(r"^---\s*$|^##\s+", remaining, re.MULTILINE)

    if next_section:
        section_end = section_start + next_section.start()
    else:
        section_end = len(content)

    # Build empty table
    table_lines = ["\n"]

    # Header row
    header_row = "| " + " | ".join(headers) + " |"
    table_lines.append(header_row)

    # Separator row
    separator = "|" + "|".join(["------" for _ in headers]) + "|"
    table_lines.append(separator)

    # Placeholder row
    placeholder = "| " + " | ".join(["(none)" if i == 0 else "-" for i in range(len(headers))]) + " |"
    table_lines.append(placeholder)

    table_lines.append("")
    new_table = "\n".join(table_lines)

    return content[:section_start] + new_table + content[section_end:]


def reset_counter(content: str, key: str, value: int = 0) -> str:
    """Reset a counter in a key-value table."""
    row_pattern = rf"^\| {re.escape(key)} \| \d+ \|$"
    match = re.search(row_pattern, content, re.MULTILINE)

    if match:
        old_row = match.group(0)
        new_row = f"| {key} | {value} |"
        return content.replace(old_row, new_row)

    return content


def generate_session_summary(completed_tasks: list[dict]) -> str:
    """Generate a brief summary of completed tasks."""
    if not completed_tasks:
        return "No tasks completed"

    # Count task types
    file_edits = sum(1 for t in completed_tasks if "Created/Updated" in t.get("Task", ""))
    completions = sum(1 for t in completed_tasks if "Completed:" in t.get("Task", ""))
    modified = sum(1 for t in completed_tasks if "Modified" in t.get("Task", ""))

    parts = []
    if file_edits > 0:
        parts.append(f"{file_edits} files")
    if completions > 0:
        parts.append(f"{completions} tasks")
    if modified > 0:
        parts.append(f"{modified} edits")

    return ", ".join(parts) if parts else "Session completed"


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    try:
        # Find project root
        cwd = Path.cwd()
        project_root = find_project_root(str(cwd))
        if not project_root:
            script_dir = Path(__file__).parent.parent
            project_root = find_project_root(str(script_dir))

        if not project_root:
            print("{}")
            sys.exit(0)

        # Read active_context.md
        context_path = project_root / ".claude" / "memory" / "active_context.md"
        context_content = read_markdown_file(context_path)

        if not context_content:
            print("{}")
            sys.exit(0)

        # Parse "Completed This Session" table
        completed_tasks = parse_table_rows(context_content, "Completed This Session")

        # Filter out placeholder rows
        real_tasks = [t for t in completed_tasks if t.get("Task", "(none)") != "(none)"]

        # If there were tasks in the previous session, archive them
        if real_tasks:
            # Read state/_index.md
            state_index_path = project_root / ".claude" / "state" / "_index.md"
            state_content = read_markdown_file(state_index_path)

            if state_content:
                # Generate session summary
                summary = generate_session_summary(real_tasks)

                # Get date from first task if available, or use today
                session_date = get_date()
                if real_tasks and "Notes" in real_tasks[0]:
                    # Try to extract date from notes (format: YYYY-MM-DD HH:MM)
                    notes = real_tasks[0].get("Notes", "")
                    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", notes)
                    if date_match:
                        session_date = date_match.group(1)

                # Add to Session History
                history_row = {
                    "Session": f"Session-{datetime.now().strftime('%Y%m%d')}",
                    "Date": session_date,
                    "Focus": f"{len(real_tasks)} items",
                    "Outcome": summary,
                }

                state_content = add_table_row(
                    state_content,
                    "Session History",
                    history_row,
                    ["Session", "Date", "Focus", "Outcome"]
                )

                # Reset Documents Touched and Commands Run counters
                state_content = reset_counter(state_content, "Documents Touched", 0)
                state_content = reset_counter(state_content, "Commands Run", 0)

                write_markdown_file(state_index_path, state_content)

            # Reset "Completed This Session" table in active_context.md
            context_content = reset_session_table(
                context_content,
                "Completed This Session",
                ["Task", "Files", "Notes"]
            )

            write_markdown_file(context_path, context_content)

    except Exception as e:
        print(f"session-history: {e}", file=sys.stderr)

    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
