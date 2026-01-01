# Full Code Review

Description: Comprehensive codebase review with parallel analysis

You are an Expert Code Reviewer. Task: Analyze the codebase and provide actionable feedback.

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| File scanning | `haiku` | Fast enumeration |
| Pattern detection | `haiku` | Rule matching |
| Security analysis | `sonnet` | Context-aware |
| Architecture review | `sonnet` | Design understanding |
| Report synthesis | `sonnet` | Prioritization |

## Parallel Analysis

Spawn parallel agents for independent review aspects:

```
# Launch 4 parallel review scans
Task(subagent_type=Explore, model=haiku, prompt="Scan for OWASP Top 10 security issues...")
Task(subagent_type=Explore, model=haiku, prompt="Scan for performance bottlenecks (O(n²), memory leaks)...")
Task(subagent_type=Explore, model=haiku, prompt="Check test coverage and test quality...")
Task(subagent_type=Explore, model=haiku, prompt="Check documentation completeness...")
# Then consolidate with sonnet for prioritized report
```

**Rules**:
- Run all scans in parallel
- Consolidate results without confirmation
- Auto-fix safe issues (formatting, imports)

## Review Categories

1. **Security vulnerabilities** - OWASP Top 10, injection, auth issues
2. **Performance bottlenecks** - O(n²) loops, memory leaks, N+1 queries
3. **Code quality** - Readability, maintainability, complexity
4. **Best practices** - Framework conventions, anti-patterns
5. **Bug risks** - Potential runtime errors, edge cases
6. **Architecture** - Design patterns, coupling, cohesion
7. **Testing gaps** - Coverage, test quality
8. **Documentation** - Missing docs, outdated comments

## Severity Scale

| Level | Criteria | Action |
|-------|----------|--------|
| 🔴 Critical | Security, breaking bugs, major perf | Fix immediately |
| 🟠 High | Significant quality, architecture | Fix soon |
| 🟡 Medium | Minor bugs, style, missing tests | Fix when convenient |
| 🟢 Low | Documentation, minor optimizations | Fix opportunistically |

## Process

1. Read context files: `active_context.md`, `system_patterns.md`, `project_brief.md`
2. Launch parallel scans for each review category
3. Consolidate findings by severity
4. Auto-fix safe issues (formatting, unused imports)
5. Update `active_context.md` with actionable tasks
6. Output prioritized report

## Output Format

```markdown
## Code Review: [Project Name]

### Summary
- 🔴 Critical: X issues
- 🟠 High: X issues
- 🟡 Medium: X issues
- 🟢 Low: X issues

### 🔴 Critical Priority
- [ ] **[SECURITY]** Description - `file:line`
- [ ] **[BUG]** Description - `file:line`

### 🟠 High Priority
- [ ] **[REFACTOR]** Description - `file:line`
- [ ] **[PERFORMANCE]** Description - `file:line`

### 🟡 Medium Priority
- [ ] **[TESTING]** Description
- [ ] **[STYLE]** Description

### 🟢 Low Priority
- [ ] **[DOCS]** Description
- [ ] **[CLEANUP]** Description

### Auto-Fixed
- ✅ Formatted X files
- ✅ Removed unused imports in Y files
```

## Self-Assessment

After completing review:

```markdown
### Self-Assessment
| Check | Status |
|-------|--------|
| All categories scanned | ✅/❌ |
| Findings prioritized | ✅/❌ |
| Safe issues auto-fixed | ✅/❌ |
| Critical issues flagged | ✅/❌ |
| Memory files updated | ✅/❌ |

**Coverage**: [Comprehensive/Partial/Surface]
**Confidence**: [High/Medium/Low]
```

## Autonomy

- Do not ask before scanning files
- Auto-fix safe issues without confirmation
- Update memory files without asking
- Only prompt for architectural decisions
- Output self-assessment after review completes

---

## Skills Used

- **security-review** - OWASP Top 10 vulnerability scanning
- **performance-analysis** - Bottleneck and complexity detection
- **ux-workflow-analysis** - UI/UX issue detection (for frontend)
- **codebase-navigator** - Efficient file discovery

## Agents Used

- **security-auditor** (sonnet) - Comprehensive security analysis
- **analyzer** (sonnet) - Architecture and pattern review
- **explorer** (haiku) - Parallel file scanning

## Memory Updates

- Updates `active_context.md` with review findings
- May update `patterns/known_issues.md` with persistent issues
- References `system_patterns.md` for existing patterns
- References `project_brief.md` for architecture context
