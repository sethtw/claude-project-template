#!/usr/bin/env python3
"""
Shared utilities for Claude Code state management hooks.

Provides common functions for:
- Finding project root
- Reading/writing markdown files
- Parsing/updating markdown tables
- Timestamp formatting
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional


def find_project_root(file_path: str) -> Optional[Path]:
    """Find project root by looking for .claude directory."""
    path = Path(file_path).resolve()

    # Walk up looking for .claude directory
    for parent in [path] + list(path.parents):
        claude_dir = parent / ".claude"
        if claude_dir.exists() and claude_dir.is_dir():
            return parent
    return None


def get_timestamp() -> str:
    """Get current timestamp in consistent format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_date() -> str:
    """Get current date in consistent format."""
    return datetime.now().strftime("%Y-%m-%d")


def read_markdown_file(path: Path) -> str:
    """Read markdown file content, return empty string if not exists."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except Exception:
        return ""


def write_markdown_file(path: Path, content: str) -> bool:
    """Write content to markdown file. Returns success status."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except Exception:
        return False


def is_inside_claude_dir(file_path: str) -> bool:
    """Check if file path is inside .claude directory."""
    path = Path(file_path)
    parts = path.parts
    return ".claude" in parts


def parse_table_rows(content: str, section_header: str) -> list[dict]:
    """
    Parse markdown table rows under a section header.

    Returns list of dicts with column values keyed by header names.
    """
    rows = []

    # Find the section
    pattern = rf"^##\s+{re.escape(section_header)}\s*$"
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return rows

    # Get content after section header
    section_start = match.end()
    remaining = content[section_start:]

    # Find next section or end
    next_section = re.search(r"^---\s*$|^##\s+", remaining, re.MULTILINE)
    if next_section:
        remaining = remaining[:next_section.start()]

    # Find table
    lines = remaining.strip().split("\n")
    header_line = None
    separator_found = False
    headers = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("|") and "|" in line[1:]:
            if header_line is None:
                # This is the header row
                header_line = line
                headers = [h.strip() for h in line.split("|")[1:-1]]
            elif not separator_found and re.match(r"^\|[\s\-:|]+\|$", line):
                # This is the separator row
                separator_found = True
            elif separator_found:
                # This is a data row
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if len(cells) == len(headers):
                    row = dict(zip(headers, cells))
                    rows.append(row)

    return rows


def update_table_section(
    content: str,
    section_header: str,
    new_rows: list[dict],
    headers: list[str]
) -> str:
    """
    Update a markdown table under a section header with new rows.

    Preserves the table structure and replaces rows.
    """
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

    # Build new table
    table_lines = ["\n"]

    # Header row
    header_row = "| " + " | ".join(headers) + " |"
    table_lines.append(header_row)

    # Separator row
    separator = "|" + "|".join(["------" for _ in headers]) + "|"
    table_lines.append(separator)

    # Data rows
    for row in new_rows:
        cells = [str(row.get(h, "-")) for h in headers]
        data_row = "| " + " | ".join(cells) + " |"
        table_lines.append(data_row)

    # If no rows, add placeholder
    if not new_rows:
        placeholder = "| " + " | ".join(["(none)" if i == 0 else "-" for i in range(len(headers))]) + " |"
        table_lines.append(placeholder)

    table_lines.append("")

    new_table = "\n".join(table_lines)

    # Replace section content
    return content[:section_start] + new_table + content[section_end:]


def add_table_row(
    content: str,
    section_header: str,
    new_row: dict,
    headers: list[str]
) -> str:
    """
    Add a single row to a markdown table, replacing placeholder if present.
    """
    # Parse existing rows
    existing_rows = parse_table_rows(content, section_header)

    # Filter out placeholder rows
    real_rows = [
        r for r in existing_rows
        if not any(v in ["(none)", "(none yet)", "-"] for v in r.values() if v == list(r.values())[0])
    ]

    # Check if first column value indicates placeholder
    filtered_rows = []
    for row in existing_rows:
        first_val = list(row.values())[0] if row else ""
        if first_val not in ["(none)", "(none yet)"]:
            filtered_rows.append(row)

    # Add new row
    filtered_rows.append(new_row)

    # Update table
    return update_table_section(content, section_header, filtered_rows, headers)


def update_key_value_table(content: str, section_header: str, key: str, value: str) -> str:
    """
    Update a key-value style table (| Field | Value |) under a section.
    """
    # Find the section and table
    pattern = rf"(^##\s+{re.escape(section_header)}.*?)(^\| {re.escape(key)} \|.*$)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

    if not match:
        # Try simpler pattern for the key row
        row_pattern = rf"^\| \*?\*?{re.escape(key)}\*?\*? \|.*$"
        row_match = re.search(row_pattern, content, re.MULTILINE)
        if row_match:
            old_row = row_match.group(0)
            # Extract the key format (may have ** for bold)
            key_match = re.search(r"\| (\*?\*?.*?\*?\*?) \|", old_row)
            if key_match:
                formatted_key = key_match.group(1)
                new_row = f"| {formatted_key} | {value} |"
                return content.replace(old_row, new_row)

    return content


def increment_counter(content: str, section_header: str, key: str, increment: int = 1) -> str:
    """
    Increment a numeric counter in a key-value table.
    """
    # Find the row with the counter
    row_pattern = rf"^\| {re.escape(key)} \| (\d+) \|$"
    match = re.search(row_pattern, content, re.MULTILINE)

    if match:
        current_value = int(match.group(1))
        new_value = current_value + increment
        old_row = match.group(0)
        new_row = f"| {key} | {new_value} |"
        return content.replace(old_row, new_row)

    return content
