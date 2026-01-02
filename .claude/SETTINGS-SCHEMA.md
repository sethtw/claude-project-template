# Settings Schema Documentation

> Schema reference for `.claude/settings.local.json` configuration.

## Overview

The `settings.local.json` file configures Claude Code behavior for this project:
- **Permissions**: Pre-approved tools that don't require user confirmation
- **Hooks**: Scripts that run automatically in response to events
- **MCP Servers**: Enabled Model Context Protocol servers

---

## Schema Structure

```json
{
  "permissions": {
    "allow": ["<permission patterns>"]
  },
  "hooks": {
    "<HookType>": [
      {
        "matcher": "<trigger pattern>",
        "hooks": [
          {
            "type": "command",
            "command": "<shell command>"
          }
        ]
      }
    ]
  },
  "enabledMcpjsonServers": ["<server names>"]
}
```

---

## Permissions

### Format

Permissions use pattern matching to pre-approve tool usage:

| Pattern | Description | Example |
|---------|-------------|---------|
| `ToolName` | Approve tool entirely | `Read`, `Write`, `Edit` |
| `ToolName(prefix:*)` | Approve with prefix match | `Bash(git:*)` |
| `ToolName(**/pattern)` | Approve with glob | `Read(**/src/**/*.ts)` |
| `mcp__server__tool` | Approve MCP tool | `mcp__filesystem__read_file` |

### Common Patterns

```json
"allow": [
  "Read",                    // All file reads
  "Write",                   // All file writes
  "Edit",                    // All file edits
  "Bash(git:*)",             // Git commands only
  "Bash(npm:*)",             // NPM commands only
  "Task",                    // Agent spawning
  "TodoWrite",               // Todo management
  "Glob",                    // File pattern matching
  "Grep"                     // Content search
]
```

### Bash Command Patterns

Pre-approved bash commands use `Bash(command:*)` format:

| Category | Patterns |
|----------|----------|
| Version Control | `Bash(git:*)` |
| Node.js | `Bash(node:*)`, `Bash(npm:*)`, `Bash(yarn:*)` |
| Python | `Bash(python:*)`, `Bash(pip:*)`, `Bash(uv:*)` |
| Docker | `Bash(docker:*)`, `Bash(docker-compose:*)` |
| Kubernetes | `Bash(kubectl:*)`, `Bash(helm:*)` |
| File Operations | `Bash(ls:*)`, `Bash(cat:*)`, `Bash(mkdir:*)` |

---

## Hooks

### Hook Types

| Type | Trigger | Use Case |
|------|---------|----------|
| `SessionStart` | Session begins | Welcome messages, initialization |
| `PreCompact` | Before context compaction | Preserve critical state |
| `PostToolUse` | After tool execution | Track changes, sync state |
| `PreToolUse` | Before tool execution | Validation, interception |
| `Notification` | On notifications | Custom handling |
| `Stop` | Session ends | Cleanup, finalization |

### Matcher Patterns

| Matcher | Triggers On | Example |
|---------|-------------|---------|
| `startup` | Session start (SessionStart only) | Initial setup |
| `auto` | Automatic compaction | Context management |
| `manual` | Manual compaction | User-triggered |
| `Write\|Edit` | Write or Edit tools | File tracking |
| `TodoWrite` | Todo list changes | Todo sync |
| Tool name | Specific tool | Custom handlers |

### Hook Command Format

```json
{
  "type": "command",
  "command": "<shell command>"
}
```

Commands receive JSON input via stdin and should output JSON.

### Current Project Hooks

| Hook | Trigger | Script | Purpose |
|------|---------|--------|---------|
| `session-history.py` | SessionStart | `.claude/hooks/session-history.py` | Archive previous session, reset counters |
| `startup.sh` | SessionStart | `.claude/hooks/startup.sh` | Display welcome banner |
| `session-tracker.py` | Write\|Edit | `.claude/hooks/session-tracker.py` | Log file changes to active_context.md |
| `state-sync.py` | Write\|Edit | `.claude/hooks/state-sync.py` | Sync state files to _index.md |
| `registry-staleness.py` | Write\|Edit | `.claude/hooks/registry-staleness.py` | Mark modified files as stale |
| `todo-context-sync.py` | TodoWrite | `.claude/hooks/todo-context-sync.py` | Sync todos to active_context.md |
| `command-tracker.py` | Skill | `.claude/hooks/command-tracker.py` | Increment Commands Run counter |

### Hook Execution Order

**SessionStart** hooks run sequentially:
1. `session-history.py` - Archives previous session
2. `startup.sh` - Displays welcome banner

**PostToolUse** with `Write|Edit` matcher, hooks run sequentially:
1. `session-tracker.py` - Updates active_context.md
2. `state-sync.py` - Updates state/_index.md
3. `registry-staleness.py` - Updates _registry.md

**PostToolUse** with `Skill` matcher:
1. `command-tracker.py` - Increments Commands Run

---

## MCP Servers

### Format

```json
"enabledMcpjsonServers": ["server1", "server2"]
```

### Available Servers

Servers are defined in `.mcp.json`:

| Server | Purpose | Required Env |
|--------|---------|--------------|
| `filesystem` | Local file system access | None |
| `github` | GitHub API integration | `GITHUB_TOKEN` |

---

## Adding New Hooks

### 1. Create Hook Script

```python
#!/usr/bin/env python3
# .claude/hooks/my-hook.py

import json
import sys

def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    tool_output = input_data.get("tool_output", "")

    # Process...

    # Output JSON (can be empty)
    print(json.dumps({}))

if __name__ == "__main__":
    main()
```

### 2. Register in settings.local.json

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [
      // ... existing hooks ...
      {
        "type": "command",
        "command": "python .claude/hooks/my-hook.py"
      }
    ]
  }
]
```

### 3. Test Hook

Run a Write/Edit operation and verify hook executes.

---

## Troubleshooting

### Hook Not Running

1. Check matcher pattern matches tool name
2. Verify script path is correct (relative to project root)
3. Check script has execute permissions
4. Look for syntax errors in JSON

### Hook Runs But Fails Silently

1. Add error logging to script
2. Check stdout/stderr for errors
3. Verify script outputs valid JSON
4. Test script independently: `echo '{"tool_name":"Edit"}' | python .claude/hooks/my-hook.py`

### "1/3 done" But Not "3/3"

Indicates a hook in the chain is failing. Check:
1. Each hook script individually
2. Hook dependencies (files being modified exist)
3. Python environment and imports

---

## Cross-References

- **Hooks documented in**: `.claude/memory/system_patterns.md`
- **Hook scripts located in**: `.claude/hooks/`
- **Development patterns**: `.claude/memory/patterns/development.md`
