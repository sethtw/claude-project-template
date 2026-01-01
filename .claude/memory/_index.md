# Knowledge Base Index

> Master navigation hub for the project knowledge system. Start here to find any information.

## Quick Stats

| Metric | Count | Last Updated |
|--------|-------|--------------|
| Total Documents | 0 | - |
| L0 (Discovery) | 0 | - |
| L1 (Triage) | 0 | - |
| L2+ (Analyzed) | 0 | - |
| Concepts | 0 | - |

---

## Navigation

### Core Memory
| File | Purpose | When to Read |
|------|---------|--------------|
| [Active Context](active_context.md) | Current session work | Every session start |
| [Project Brief](project_brief.md) | Tech stack, architecture | New to project |
| [Product Context](product_context.md) | Business goals, users | Feature planning |
| [Progress](progress.md) | Roadmap, milestones | Status check |

### Indices
| Index | Purpose | Location |
|-------|---------|----------|
| [Schemas](_schemas.md) | L0-L3 depth definitions | .claude/memory/ |
| [Registry](_registry.md) | All indexed documents | .claude/memory/ |
| [Concepts](_concepts.md) | Key concepts graph | .claude/memory/ |
| [Patterns](system_patterns.md) | Development patterns | .claude/memory/ |
| [State](../state/_index.md) | Active operations | .claude/state/ |

### Skills & Agents
| Directory | Purpose |
|-----------|---------|
| [Skills](../skills/) | Semantic discovery skills |
| [Agents](../agents/) | Specialized subagents |
| [Rules](../rules/) | Path-scoped standards |
| [Commands](../commands/) | Slash command definitions |

---

## Session Quick Actions

### Starting a Session
1. Read this index for orientation
2. Check [Active Context](active_context.md) for last session's state
3. Review any [active operations](../state/_index.md)

### Finding Information
- **By file path**: Check [Registry](_registry.md)
- **By concept**: Check [Concepts](_concepts.md)
- **By pattern**: Check [Patterns](system_patterns.md)

### Deepening Knowledge
- Use `/index` to scan codebase to L0
- Use `/deep <path>` to analyze specific files to L2/L3
- Use `/context` to see current memory state

---

## Update Protocol

This index is updated:
- After `/index` scans (document counts)
- After `/deep` analysis (depth promotions)
- After concept extraction (concept counts)
- Manually when adding new indices

---

## Cross-References

- **Skills load this**: codebase-navigator, feature-integration
- **Commands reference this**: /initialize, /index, /deep, /context, /analyze
- **Updated by**: /initialize, /index, /deep commands
