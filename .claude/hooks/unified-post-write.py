#!/usr/bin/env python3
"""
Unified post-write hook: Combines session tracking, state syncing, and registry staleness.

Runs all three operations in parallel using ThreadPoolExecutor for 50-70% faster execution.

Operations:
1. Session Tracker - Updates active_context.md with file modifications
2. State Sync - Syncs state file changes to state/_index.md
3. Registry Staleness - Marks registry entries as stale when source files change

Features:
- Parallel execution via ThreadPoolExecutor
- Session rotation (MAX_SESSION_ENTRIES=50)
- Silent success, error-only reporting
- Skips .claude/ directory files appropriately
"""

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from state_utils import (  # type: ignore
    find_project_root,
    is_inside_claude_dir,
    read_markdown_file,
    write_markdown_file,
    add_table_row,
    parse_table_rows,
    update_table_section,
    increment_counter,
    get_timestamp,
)

# Configuration
MAX_SESSION_ENTRIES = 50


# ============================================================================
# SESSION TRACKER
# ============================================================================

def track_session(file_path: str, tool_name: str, project_root: Path) -> None:
    """Update active_context.md with file modifications and increment counter."""
    # Skip files inside .claude/ directory
    if is_inside_claude_dir(file_path):
        return

    try:
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

            # Session rotation: keep only last MAX_SESSION_ENTRIES entries
            existing_rows = parse_table_rows(content, "Completed This Session")
            # Filter out placeholder rows
            real_rows = [r for r in existing_rows if r.get("Task", "(none)") != "(none)"]

            if len(real_rows) > MAX_SESSION_ENTRIES:
                # Keep only the most recent entries
                trimmed_rows = real_rows[-MAX_SESSION_ENTRIES:]
                content = update_table_section(content, "Completed This Session", trimmed_rows, headers)

            write_markdown_file(active_context_path, content)

        # Update Documents Touched counter in state/_index.md
        state_index_path = project_root / ".claude" / "state" / "_index.md"
        state_content = read_markdown_file(state_index_path)

        if state_content:
            state_content = increment_counter(state_content, "Current Session", "Documents Touched")
            write_markdown_file(state_index_path, state_content)

    except Exception as e:
        print(f"session-tracker: {e}", file=sys.stderr)


# ============================================================================
# STATE SYNC
# ============================================================================

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


def sync_state(file_path: str, project_root: Path) -> None:
    """Sync state file changes to state/_index.md."""
    # Only process state files
    if not is_state_file(file_path):
        return

    try:
        # Read the state file that was just written
        state_file_path = Path(file_path)
        state_content = read_markdown_file(state_file_path)

        if not state_content:
            return

        # Extract state info
        state_info = extract_state_info(state_content)

        # Get operation name from filename (e.g., "refactor_state.md" -> "Refactor")
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
            return

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


# ============================================================================
# REGISTRY STALENESS
# ============================================================================

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
    if not old_line.startswith("| ⚠"):
        # Find first column content
        first_col_match = re.match(r"\| *([^|]+) *\|", old_line)
        if first_col_match:
            first_col = first_col_match.group(1).strip()
            if not first_col.startswith("⚠"):
                new_first_col = f"⚠️ {first_col}"
                new_line = old_line.replace(f"| {first_col} |", f"| {new_first_col} |", 1)
                return content.replace(old_line, new_line)

    return content


def mark_registry_stale(file_path: str, project_root: Path) -> None:
    """Mark registry entries as stale when source files change."""
    # Skip files inside .claude/ directory
    if is_inside_claude_dir(file_path):
        return

    try:
        # Read _registry.md
        registry_path = project_root / ".claude" / "memory" / "_registry.md"
        content = read_markdown_file(registry_path)

        if not content:
            # No registry file exists yet
            return

        # Check if file exists in registry
        result = find_registry_entry(content, file_path, project_root)
        if not result:
            # File not in registry - nothing to mark stale
            return

        old_line, matched_pattern = result
        timestamp = get_timestamp()

        # Mark the entry as stale
        new_content = mark_entry_stale(content, old_line, timestamp)

        if new_content != content:
            write_markdown_file(registry_path, new_content)

    except Exception as e:
        print(f"registry-staleness: {e}", file=sys.stderr)


# ============================================================================
# MAIN
# ============================================================================

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

    try:
        project_root = find_project_root(file_path)
        if not project_root:
            print("{}")
            sys.exit(0)

        # Run all three operations in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(track_session, file_path, tool_name, project_root),
                executor.submit(sync_state, file_path, project_root),
                executor.submit(mark_registry_stale, file_path, project_root),
            ]
            # Wait for all to complete (errors are already logged to stderr in each function)
            for future in futures:
                future.result()  # This will raise if any function raised

    except Exception as e:
        # Log unexpected errors
        print(f"unified-post-write: {e}", file=sys.stderr)

    # Always return empty object (silent mode)
    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
