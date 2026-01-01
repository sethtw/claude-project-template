# Development Patterns

## Autonomy Settings

Process all development operations without confirmation:
- Do not ask before reading files
- Do not pause between test/lint/build steps
- Auto-fix safe issues (formatting, imports, unused vars)
- Run test suites automatically
- Only prompt for destructive operations

## Model Selection

Choose the right model for each task:

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| File scanning | `haiku` | Fast pattern matching |
| Linting/formatting | `haiku` | Rule-based checks |
| Dependency analysis | `haiku` | Package enumeration |
| Code generation | `sonnet` | Complex reasoning |
| Bug analysis | `sonnet` | Context understanding |
| Test generation | `sonnet` | Behavioral understanding |
| Refactoring | `sonnet` | Semantic changes |
| Code review | `sonnet` | Quality assessment |
| **Feature planning** | `opus` | Multi-system coordination |
| **Architecture design** | `opus` | Critical structural decisions |
| **Complex features** | `opus` | Multi-file coordinated changes |
| **Risk assessment** | `opus` | Downstream impact analysis |

**Hierarchy**: `haiku` for speed → `sonnet` for quality → `opus` for complexity.

**Escalate to opus** when:
- Planning touches 5+ files or 3+ systems
- Making hard-to-reverse architectural decisions
- Complex features with many integration points

## Parallel Processing

Spawn up to 4 agents for independent work:

```
# Multi-aspect analysis
Task(model=haiku, prompt="Scan for security issues...")
Task(model=haiku, prompt="Scan for performance issues...")
Task(model=haiku, prompt="Check test coverage...")
Task(model=haiku, prompt="Check documentation...")
```

**Rules**:
- Use parallel agents for independent operations
- Consolidate results after all complete
- No confirmation between agent spawns

## Batch Processing

Process large operations in batches:
- Default batch size: 10 files
- Run tests after each batch
- Update state after each batch
- Support resume from any point

## Development Workflow

### Plan-Execute-Verify Cycle
1. **Plan** in active_context.md
2. **Execute** in atomic batches (no pauses)
3. **Verify** with tests (auto-run)

### Strict TDD
1. Write failing test first
2. Implement minimal solution
3. Refactor with tests passing
4. Auto-commit on green

### Atomic Commits
- Conventional format: `feat:`, `fix:`, `chore:`
- Tests must pass before commit
- Auto-stage related files

## State Management

For long-running operations, use `.claude/state/`:
- `refactor_state.md` - Multi-file refactoring
- `migration_state.md` - Version migrations
- `review_state.md` - Ongoing reviews

Support `--resume` to continue from state.

## Self-Assessment Pattern

After major work, verify completeness:

1. **Completeness Check**
   - All planned tasks done
   - No unresolved TODOs
   - All files in plan modified
   - Integration points wired

2. **Quality Check**
   - Tests pass
   - No new lint warnings
   - Error handling in place
   - No hardcoded values

3. **Verification**
   - End-to-end works
   - No regressions
   - Dependent systems function

4. **Confidence Rating**
   - High/Medium/Low
   - Notes for human review

**Rule**: Output self-assessment after features, refactors, migrations, or 5+ file changes.

## Key Constraints

- Never delete files without confirmation
- Never use `rm -rf` or force operations
- Prefer editing existing files over creating new ones
- Use haiku for speed, sonnet for quality, opus for complexity
- Run tests automatically, don't ask
