#!/usr/bin/env python3
"""
Post-tool hook: Track slash command usage.

When the Skill tool is used (slash commands like /analyze, /implement, etc.),
this hook increments the "Commands Run" counter in state/_index.md.
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
    increment_counter,
)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("{}")
        sys.exit(0)

    # Only process Skill tool usage
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Skill":
        print("{}")
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    skill_name = tool_input.get("skill", "")

    if not skill_name:
        print("{}")
        sys.exit(0)

    try:
        # Find project root from current directory
        cwd = Path.cwd()
        project_root = find_project_root(str(cwd))
        if not project_root:
            # Try from script location
            script_dir = Path(__file__).parent.parent
            project_root = find_project_root(str(script_dir))

        if not project_root:
            print("{}")
            sys.exit(0)

        # Read state/_index.md
        index_path = project_root / ".claude" / "state" / "_index.md"
        content = read_markdown_file(index_path)

        if not content:
            print("{}")
            sys.exit(0)

        # Increment Commands Run counter
        content = increment_counter(content, "Current Session", "Commands Run", 1)

        # Write updated content
        write_markdown_file(index_path, content)

    except Exception as e:
        print(f"command-tracker: {e}", file=sys.stderr)

    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
