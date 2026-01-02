# System Patterns Index

> Navigation hub for development patterns and standards.

## Pattern Files

| File | Description | When to Read |
|------|-------------|--------------|
| [architecture.md](patterns/architecture.md) | Project structure, error handling | Understanding codebase |
| [development.md](patterns/development.md) | Workflow, model selection, autonomy | Planning work |
| [testing.md](patterns/testing.md) | Test patterns, coverage | Writing tests |
| [known_issues.md](patterns/known_issues.md) | Outstanding issues, quick fixes | Debugging |

## Rules (Path-Scoped)

Located in `.claude/rules/`:

| Rule | Applies To | Purpose |
|------|------------|---------|
| [typescript.md](../rules/typescript.md) | `src/**/*.{ts,tsx}` | TypeScript standards |
| [testing.md](../rules/testing.md) | `**/*.test.{ts,tsx}` | Test conventions |
| [security.md](../rules/security.md) | `**/auth/**/*`, `**/api/**/*` | Security requirements |

## Skills

Located in `.claude/skills/`:

| Skill | Model | Trigger Keywords |
|-------|-------|------------------|
| tdd-workflow | sonnet | TDD, test first, red-green |
| security-review | sonnet | security, vulnerability, OWASP |
| performance-analysis | sonnet | slow, optimize, bottleneck |
| api-design | sonnet | REST, endpoint, schema |
| database-patterns | sonnet | query, migration, index |
| feature-integration | opus | plan feature, integration, scope |
| ux-workflow-analysis | sonnet | UI issues, layout, z-index |
| codebase-navigator | haiku | find, where is, explore |

### Skill Activation by Command

| Command | Primary Skills | Secondary Skills | Model |
|---------|----------------|------------------|-------|
| /initialize | codebase-navigator | - | haiku/sonnet |
| /index | codebase-navigator | - | haiku |
| /analyze | codebase-navigator, performance-analysis | database-patterns | haiku/sonnet |
| /deep | codebase-navigator | feature-integration | sonnet/opus |
| /architect | feature-integration | codebase-navigator | opus |
| /implement | tdd-workflow, performance-analysis | security-review | sonnet/opus |
| /tdd | tdd-workflow | - | sonnet |
| /test-gen | tdd-workflow | - | sonnet |
| /code-review | security-review, performance-analysis | ux-workflow-analysis | sonnet |
| /review | security-review | - | sonnet |
| /refactor | performance-analysis | codebase-navigator | sonnet/opus |
| /migrate | feature-integration | codebase-navigator | sonnet/opus |
| /cleanup | codebase-navigator | - | haiku |

## Agents

Located in `.claude/agents/`:

| Agent | Model | Purpose |
|-------|-------|---------|
| explorer | haiku | Fast codebase search |
| analyzer | sonnet | Deep code analysis |
| security-auditor | sonnet | Security scanning |
| test-runner | haiku | Test execution |

## Hooks (Auto-Tracking)

The project uses Claude Code hooks (`.claude/settings.local.json`) for automatic context tracking:

| Hook | Trigger | Updates | Purpose |
|------|---------|---------|---------|
| session-history.py | Session start | state/_index.md, active_context.md | Archives previous session, resets counters |
| startup.sh | Session start | - | Displays welcome banner with commands |
| session-tracker.py | File Write/Edit | active_context.md | Logs file modifications |
| state-sync.py | State file Write/Edit | state/_index.md | Syncs operation progress |
| registry-staleness.py | Source file Write/Edit | _registry.md | Marks modified files as stale |
| todo-context-sync.py | TodoWrite | active_context.md | Syncs todo items to context |
| command-tracker.py | Skill tool | state/_index.md | Increments "Commands Run" counter |

### Hook Configuration

Defined in `.claude/settings.local.json`:
- **SessionStart** - Runs at session start
- **PreCompact** - Runs before context compaction (preserves WIP context)
- **PostToolUse** - Runs after Write, Edit, or TodoWrite tools

### What Hooks Track Automatically

1. **File modifications** → "Completed This Session" table in active_context.md
2. **State file updates** → "Active States" table in state/_index.md
3. **Source file changes** → Staleness markers in _registry.md
4. **Todo progress** → "In Progress" and "Completed This Session" tables

See [development.md](patterns/development.md) for detailed hook configuration.

---

## Critical Rules (Quick Reference)

### Safety
- Never delete files without confirmation
- Never use `rm -rf` or force operations
- Create backup branches for risky operations

### Efficiency
- Haiku for speed, Sonnet for quality, Opus for complexity
- Run tests automatically
- Batch operations for consistency

### Quality
- All changes must have tests
- Follow existing patterns
- Self-assess after major work

---

## When to Read Which File

| Task | Read |
|------|------|
| Understanding codebase structure | [architecture.md](patterns/architecture.md) |
| Planning work, model selection | [development.md](patterns/development.md) |
| Writing tests | [testing.md](patterns/testing.md) |
| Debugging known issues | [known_issues.md](patterns/known_issues.md) |
| TypeScript conventions | [.claude/rules/typescript.md](../rules/typescript.md) |
| Security requirements | [.claude/rules/security.md](../rules/security.md) |

---

## Cross-References

- **Used by**: All slash commands
- **Updates**: When patterns change
- **See also**: [Knowledge Index](_index.md)
