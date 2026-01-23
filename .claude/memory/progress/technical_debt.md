# Technical Debt

> Prioritized list of known issues, limitations, and areas for improvement.

## Purpose

Track technical debt to:
- Prioritize refactoring efforts
- Document workarounds and their limitations
- Plan future improvements
- Prevent forgotten issues

---

## Priority Levels

| Priority | Definition | Timeline |
|----------|------------|----------|
| **Critical** | Blocks progress or causes failures | Address immediately |
| **High** | Significant impact on development | Address within 1-2 weeks |
| **Medium** | Moderate impact or workaround exists | Address within 1-2 months |
| **Low** | Minor inconvenience or nice-to-have | Address when convenient |

---

## Critical Priority

*No critical technical debt identified.*

---

## High Priority

*No high-priority technical debt identified.*

---

## Medium Priority

### Registry Split Threshold
**Issue**: Registry will become unwieldy at >500 files
**Impact**: Slower lookups, harder navigation
**Solution**: Implement split registry architecture (from saga-new)
**Effort**: 4 hours
**When**: When registry exceeds 500 files or 50KB

### Concepts Split Threshold
**Issue**: Concepts file will become unwieldy at >40 concepts
**Impact**: Slower lookups, harder navigation
**Solution**: Implement split concepts by category
**Effort**: 3 hours
**When**: When concepts exceed 40 entries or 40KB

---

## Low Priority

### Hook Performance Baseline
**Issue**: No baseline measurement for hook execution time
**Impact**: Can't verify 50-70% improvement claim
**Solution**: Add timing instrumentation to unified hook
**Effort**: 30 minutes
**When**: When profiling performance

---

## Resolved Debt

*No resolved debt yet.*

---

## Template Format

### [Title]
**Issue**: Description of the problem
**Impact**: How it affects development
**Solution**: Proposed fix
**Effort**: Estimated time
**When**: Conditions for addressing

---

## Cross-References

- Completed work: [completed_tasks.md](completed_tasks.md)
- Architecture decisions: [architecture_notes.md](architecture_notes.md)
- Current work: [../active_context.md](../active_context.md)
- Roadmap: [../progress.md](../progress.md)
