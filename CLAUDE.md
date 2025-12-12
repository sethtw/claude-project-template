# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code project template with a memory bank system for maintaining context across sessions. The project is currently a blank template awaiting implementation.

## Memory Bank Structure

The `.claude/memory/` directory contains context files that should be read and updated during development:

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

## Slash Commands

Available in `.claude/commands/`:

| Command | Description |
|---------|-------------|
| `/plan <feature>` | Generate implementation plan in active_context.md without writing code |
| `/tdd <feature>` | Strict Red-Green-Refactor cycle |
| `/review` | Security and style review on staged changes |
| `/code-review` | Full codebase review with prioritized findings |

## Development Workflow

### Plan-Execute-Verify Cycle
1. Plan in `active_context.md`
2. Execute in atomic batches
3. Verify with tests

### Strict TDD
1. Write failing test first
2. Implement minimal solution
3. Refactor with tests passing

### Commits
- Conventional format: `feat:`, `fix:`, `chore:`
- Tests must pass before commit

## Key Constraints

- Never delete files without confirmation
- Never use `rm -rf`
- Prefer editing existing files over creating new ones
