# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Autonomy Settings

Process all development operations without confirmation:
- Do not ask before reading files
- Do not pause between test/lint/build steps
- Auto-fix safe issues (formatting, imports, unused vars)
- Run test suites without asking
- Only prompt for destructive operations (file deletion, force push)

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| File scanning/searching | `haiku` | Fast pattern matching |
| Linting/formatting | `haiku` | Rule-based, structural |
| Dependency analysis | `haiku` | Package enumeration |
| Code generation | `sonnet` | Complex reasoning needed |
| Bug analysis | `sonnet` | Context understanding |
| Test generation | `sonnet` | Needs code understanding |
| Refactoring | `sonnet` | Semantic changes |
| Code review | `sonnet` | Quality requires depth |
| Simple docs (JSDoc) | `haiku` | Templated patterns |
| Complex docs (guides) | `sonnet` | Needs context |
| **Feature planning** | `opus` | Complex multi-system design |
| **Architecture design** | `opus` | Critical structural decisions |
| **Complex feature generation** | `opus` | Multi-file coordinated changes |
| **Risk assessment** | `opus` | Understanding downstream impacts |

**Hierarchy**: `haiku` for speed → `sonnet` for quality → `opus` for complexity.

**Escalate to opus** when:
- Planning features that touch 5+ files or 3+ systems
- Making architectural decisions that are hard to reverse
- Generating complex features with many integration points
- Assessing risk for significant changes

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

## Project Overview

This is a Claude Code project template with a memory bank system for maintaining context across sessions.

## Memory Bank Structure

The `.claude/memory/` directory contains context files:

| File | Purpose |
|------|---------|
| `active_context.md` | Current session work, completed tasks, next steps |
| `project_brief.md` | Project overview, tech stack, architecture highlights |
| `progress.md` | Roadmap, milestones, lessons learned |
| `system_patterns.md` | Index to pattern files |

Pattern files in `.claude/memory/patterns/`:
- `architecture.md` - Error handling, project structure patterns
- `development.md` - TDD workflow, atomic commits, key constraints
- `testing.md` - Test organization by type
- `known_issues.md` - Outstanding issues, deferred items

Progress tracking in `.claude/memory/progress/`:
- `completed_tasks.md` - Detailed log of completed work
- `technical_debt.md` - Known issues and deferred items
- `architecture_notes.md` - Key architectural decisions

State tracking in `.claude/state/` (for long operations):
- `refactor_state.md` - Multi-file refactoring progress
- `migration_state.md` - Version/framework migration progress

## Slash Commands

Available in `.claude/commands/`:

| Command | Description |
|---------|-------------|
| `/plan <feature>` | Generate implementation plan without writing code |
| `/tdd <feature>` | Strict Red-Green-Refactor cycle |
| `/review` | Quick security and style review on staged changes |
| `/code-review` | Full codebase review with parallel analysis |
| `/analyze` | Codebase analysis with parallel scanning |
| `/refactor <scope>` | Multi-file refactoring with state tracking |
| `/test-gen <module>` | Batch test generation |
| `/migrate <target>` | Framework/version migration with progress tracking |

## Development Workflow

### Plan-Execute-Verify Cycle
1. Plan in `active_context.md`
2. Execute in atomic batches (no confirmation between steps)
3. Verify with tests (auto-run)

### Strict TDD
1. Write failing test first
2. Implement minimal solution
3. Refactor with tests passing
4. Auto-commit on green

### Commits
- Conventional format: `feat:`, `fix:`, `chore:`
- Tests must pass before commit
- Auto-stage related files

## Self-Assessment Pattern

After completing major work (features, refactors, migrations), perform verification:

```
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

**Rule**: Always output a self-assessment block after completing:
- Feature implementations
- Multi-file refactors
- Migrations
- Any operation spanning 5+ files

## Key Constraints

- Never delete files without confirmation
- Never use `rm -rf` or force operations
- Prefer editing existing files over creating new ones
- Use haiku for speed, sonnet for quality, opus for complexity
