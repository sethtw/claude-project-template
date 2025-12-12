# Development Patterns

## Development Workflow

### Plan-Execute-Verify Cycle
1. **Plan** in active_context.md
2. **Execute** in atomic batches
3. **Verify** with tests

### Strict TDD
1. Write failing test first
2. Implement minimal solution
3. Refactor with tests passing

### Atomic Commits
- Conventional format: `feat:`, `fix:`, `chore:`
- Tests must pass before commit

## Key Constraints
- Never delete files without confirmation
- Never use `rm -rf`
- Prefer editing existing files over creating new ones
