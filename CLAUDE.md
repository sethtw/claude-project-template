# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Quick Reference

| Resource | Purpose |
|----------|---------|
| @.claude/memory/_index.md | Knowledge base navigation |
| @.claude/memory/active_context.md | Current session state |
| @.claude/memory/project_brief.md | Project overview |
| @.claude/memory/system_patterns.md | Pattern index |

## Autonomy Settings

Process all operations without confirmation:
- Do not ask before reading files
- Do not pause between test/lint/build steps
- Auto-fix safe issues (formatting, imports, unused vars)
- Run test suites automatically
- Only prompt for destructive operations (file deletion, force push)

## Model Selection

See @.claude/memory/patterns/development.md for full matrix.

**Quick guide**: `haiku` for speed → `sonnet` for quality → `opus` for complexity

**Escalate to opus** when:
- Planning features that touch 5+ files or 3+ systems
- Making architectural decisions that are hard to reverse
- Complex features with many integration points

## Memory Architecture

### Knowledge Base (new)
| Index | Purpose |
|-------|---------|
| `_index.md` | Master navigation hub |
| `_schemas.md` | L0-L3 depth definitions |
| `_registry.md` | Document index |
| `_concepts.md` | Concept graph |

### Session Context
| File | Purpose |
|------|---------|
| `active_context.md` | Current session work |
| `project_brief.md` | Tech stack, architecture |
| `progress.md` | Roadmap, milestones |

### Patterns & Rules
- `.claude/memory/patterns/` - Development patterns
- `.claude/rules/` - Path-scoped coding standards
- `.claude/skills/` - Semantic skills
- `.claude/agents/` - Specialized subagents

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/initialize` | **First run**: Comprehensive codebase scan, populate all memory |
| `/index` | Scan codebase to L0 registry |
| `/deep` | Deepen file to L2/L3 analysis |
| `/context` | Show memory state |
| `/architect` | Generate implementation plan |
| `/implement` | **Cost-optimized**: Staged execution (Haiku→Opus→Sonnet→Sonnet→Opus) |
| `/tdd` | Strict Red-Green-Refactor |
| `/review` | Quick staged changes review |
| `/code-review` | Full codebase review |
| `/analyze` | Codebase analysis |
| `/refactor` | Multi-file refactoring |
| `/test-gen` | Batch test generation |
| `/migrate` | Framework/version migration |

## Key Constraints

- Never delete files without confirmation
- Never use `rm -rf` or force operations
- Prefer editing existing files over creating new ones
- Use haiku for speed, sonnet for quality, opus for complexity
- Run tests automatically, don't ask

## Detailed Documentation

For comprehensive patterns and workflows, see:
- @.claude/memory/patterns/development.md - Full model selection, workflows
- @.claude/memory/patterns/architecture.md - Architecture patterns
- @.claude/memory/patterns/testing.md - Test patterns
- @.claude/state/_index.md - State tracking for long operations
