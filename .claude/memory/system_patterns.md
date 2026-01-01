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

## Agents

Located in `.claude/agents/`:

| Agent | Model | Purpose |
|-------|-------|---------|
| explorer | haiku | Fast codebase search |
| analyzer | sonnet | Deep code analysis |
| security-auditor | sonnet | Security scanning |
| test-runner | haiku | Test execution |

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
