# Development Patterns

> Single source of truth for development workflows, model selection, and autonomy settings.

## Autonomy Settings

Process all development operations without confirmation:
- Do not ask before reading files
- Do not pause between test/lint/build steps
- Auto-fix safe issues (formatting, imports, unused vars)
- Run test suites automatically
- Only prompt for destructive operations (file deletion, force push)

---

## Model Selection Matrix

| Task | Model | Rationale |
|------|-------|-----------|
| File scanning/searching | `haiku` | Fast pattern matching |
| Linting/formatting | `haiku` | Rule-based, structural |
| Dependency analysis | `haiku` | Package enumeration |
| Simple docs (JSDoc) | `haiku` | Templated patterns |
| Code generation | `sonnet` | Complex reasoning needed |
| Bug analysis | `sonnet` | Context understanding |
| Test generation | `sonnet` | Needs code understanding |
| Refactoring | `sonnet` | Semantic changes |
| Code review | `sonnet` | Quality requires depth |
| Complex docs (guides) | `sonnet` | Needs context |
| **Feature planning** | `opus` | Complex multi-system design |
| **Architecture design** | `opus` | Critical structural decisions |
| **Complex feature generation** | `opus` | Multi-file coordinated changes |
| **Risk assessment** | `opus` | Understanding downstream impacts |
| **UX workflow analysis** | `sonnet` | User journey validation |
| **Feature integration** | `opus` | Multi-system impact analysis |

**Hierarchy**: `haiku` for speed → `sonnet` for quality → `opus` for complexity.

### Escalation Rules

**Escalate to opus** when:
- Planning features that touch 5+ files or 3+ systems
- Making architectural decisions that are hard to reverse
- Generating complex features with many integration points
- Assessing risk for significant changes
- Analyzing cross-system integration impacts

**Stay with sonnet** when:
- Single-system changes
- Well-defined feature scope
- Clear implementation path

**Use haiku** when:
- Speed is priority over depth
- Pattern matching tasks
- File enumeration and discovery

---

## Parallel Processing

Spawn up to 4 agents for independent work:

```
# Example: Multi-aspect code review
Task(subagent_type=Explore, model=haiku, prompt="Scan for security issues...")
Task(subagent_type=Explore, model=haiku, prompt="Scan for performance issues...")
Task(subagent_type=Explore, model=haiku, prompt="Check test coverage...")
Task(subagent_type=Explore, model=haiku, prompt="Check documentation...")
# Consolidate with sonnet for prioritized report
```

**Rules**:
- Use parallel agents for independent operations
- Consolidate results after all complete
- No confirmation between agent spawns
- Max 4 concurrent agents

---

## Batch Processing

For large operations:

| Setting | Default | Purpose |
|---------|---------|---------|
| Batch size | 10 files | Manageable chunks |
| Test frequency | After each batch | Catch issues early |
| State updates | After each batch | Enable resume |
| Commit frequency | Per logical unit | Clean history |

**Resume support**: All long operations can be interrupted and resumed via `.claude/state/`.

---

## Development Workflow

### Plan-Execute-Verify Cycle
1. **Plan** in `active_context.md`
   - Define scope and success criteria
   - List files to modify
   - Identify integration points

2. **Execute** in atomic batches
   - No confirmation between steps
   - Update state after each batch
   - Auto-fix safe issues

3. **Verify** with tests
   - Run automatically after changes
   - Fix failures before continuing
   - Update active context

### Strict TDD Workflow
1. **Red**: Write failing test first
2. **Green**: Implement minimal solution
3. **Refactor**: Improve with tests passing
4. **Commit**: Auto-commit on green

### Atomic Commits
- **Format**: `feat:`, `fix:`, `chore:`, `docs:`, `test:`
- **Rule**: Tests must pass before commit
- **Scope**: One logical change per commit
- **Auto-stage**: Related files staged together

---

## Staged Execution Pattern (Cost Optimization)

For large implementations, use staged model execution to optimize costs:

### Token Cost Reference

| Model | Input | Output | Relative Cost |
|-------|-------|--------|---------------|
| Opus | $15/1M | $75/1M | 1x (baseline) |
| Sonnet | $3/1M | $15/1M | 5x cheaper |
| Haiku | $0.25/1M | $1.25/1M | 60x cheaper |

**Key insight**: Output tokens cost 5x input. Code generation = many output tokens.

### Five-Stage Execution

```
Stage 1: DISCOVER (Haiku)  → Find files, map structure      [Low cost]
Stage 2: PLAN (Opus)       → Design implementation          [High value]
Stage 3: WRITE (Sonnet)    → Generate code                  [Bulk output]
Stage 4: VERIFY (Sonnet)   → Run tests, basic review        [Quality check]
Stage 5: FIX (Opus)        → Fix issues (only if needed)    [Conditional]
```

### Cost Savings Example

| Approach | 50K Output Tokens | Est. Cost |
|----------|-------------------|-----------|
| All Opus | 50K × $75/1M | ~$3.75 |
| Staged (mostly Sonnet) | Mixed | ~$1.25 |
| **Savings** | | **~67%** |

### When to Use Staged Execution

**Use `/implement`** (staged) for:
- Features requiring 3+ new files
- Well-defined requirements
- Standard patterns (CRUD, API endpoints)
- Cost-conscious implementations

**Use `/architect`** (Opus throughout) for:
- Architectural exploration
- Unclear requirements
- Complex multi-system changes
- Critical decisions

### Stage Requirements

For staged execution to work well:

1. **Stage 2 (Plan)** must produce explicit instructions:
   - Exact file paths
   - Function signatures with types
   - Step-by-step order
   - Patterns to follow (with file references)

2. **Stage 3 (Write)** follows plan exactly:
   - No improvisation
   - Use specified patterns
   - Ask if plan unclear (rare)

3. **Stage 5 (Fix)** is conditional:
   - Only invoked if Stage 4 finds issues
   - Minimal, targeted fixes
   - Re-verify after fixes

---

## State Management

For long-running operations, use `.claude/state/`:

| State File | Purpose | Tracks |
|------------|---------|--------|
| `refactor_state.md` | Multi-file refactoring | Batches, files, tests |
| `migration_state.md` | Version migrations | Phases, rollback points |
| `review_state.md` | Ongoing reviews | Findings, severity |
| `implement_state.md` | Staged implementation | Stages, cost, progress |

### Resume Protocol
1. Check for existing state file
2. Load last checkpoint
3. Continue from interrupted position
4. Update state after each step

---

## Self-Assessment Pattern

After completing major work, perform verification:

```markdown
## Self-Assessment Checklist

### Completeness
- [ ] All planned tasks marked complete
- [ ] No TODO comments left unresolved
- [ ] All files listed in plan were modified
- [ ] Integration points wired correctly

### Quality
- [ ] Tests pass (run automatically)
- [ ] No new lint warnings introduced
- [ ] Error handling in place for edge cases
- [ ] No hardcoded values that should be configurable

### Verification
- [ ] Changes work end-to-end (not just unit level)
- [ ] Dependent systems still function
- [ ] No regressions in existing functionality

### Confidence
Rate: [High/Medium/Low]
Notes: <any concerns or areas needing human review>
```

**Trigger self-assessment after**:
- Feature implementations
- Multi-file refactors
- Migrations
- Any operation spanning 5+ files

---

## Key Constraints

### Safety
- Never delete files without confirmation
- Never use `rm -rf` or force operations
- Never force push to main/master
- Create backup branches for risky operations

### Efficiency
- Prefer editing existing files over creating new ones
- Use haiku for speed, sonnet for quality, opus for complexity
- Run tests automatically, don't ask
- Batch operations for consistency

### Quality
- All changes must have tests
- No new lint warnings
- Follow existing patterns in codebase
- Document non-obvious decisions

---

## Hook System Configuration

The project uses Claude Code hooks for automatic session tracking. Hooks are configured in `.claude/settings.local.json`.

### Hook Types

| Type | When It Runs | Purpose |
|------|--------------|---------|
| SessionStart | Session begins | Display welcome banner, initialize session |
| PreCompact | Before context compaction | Preserve critical WIP context |
| PostToolUse | After tool execution | Track changes automatically |

### SessionStart Hooks

```
1. session-history.py  → Archives previous session, resets counters
2. startup.sh          → Displays welcome banner
```

### PostToolUse Hooks

For `Write|Edit` operations (runs in sequence):
```
1. session-tracker.py  → Updates active_context.md
2. state-sync.py       → Updates state/_index.md
3. registry-staleness.py → Marks _registry.md entries stale
```

For `TodoWrite` operations:
```
1. todo-context-sync.py → Syncs todos to active_context.md
```

For `Skill` operations:
```
1. command-tracker.py  → Increments Commands Run counter
```

### Hook Scripts

All hooks located in `.claude/hooks/`:

| Script | Input | Output | Function |
|--------|-------|--------|----------|
| session-history.py | - | - | Archive previous session to history |
| startup.sh | - | Banner to stderr | Welcome message with command list |
| session-tracker.py | Tool result JSON | - | Log file edits to context |
| state-sync.py | Tool result JSON | - | Sync state file progress |
| registry-staleness.py | Tool result JSON | - | Mark modified files stale |
| todo-context-sync.py | Tool result JSON | - | Sync todo items |
| command-tracker.py | Tool result JSON | - | Increment Commands Run counter |
| state_utils.py | - | - | Shared utilities for hooks |

### Adding New Hooks

To add a new PostToolUse hook:

1. Create script in `.claude/hooks/`
2. Add to settings.local.json under appropriate matcher
3. Script receives JSON via stdin with tool_name and tool_input
4. Script outputs JSON (can be empty `{}`)
5. Use state_utils.py for common markdown operations

---

## Cross-References

- **Skills reference this**: All development skills
- **Commands reference this**: All slash commands
- **CLAUDE.md imports this**: Via @import
- **Updated when**: Workflow patterns change
