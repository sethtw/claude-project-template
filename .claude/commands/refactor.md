# Multi-File Refactor

Description: Coordinated refactoring across multiple files with state tracking

You are a Refactoring Expert. Task: Refactor "$ARGUMENTS" across the codebase.

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| File scanning | `haiku` | Find affected files |
| Impact analysis | `sonnet` | Understand dependencies |
| Code transformation | `sonnet` | Semantic changes |
| Verification | `haiku` | Run tests |
| **Large refactors (10+ files)** | `opus` | Coordinated semantic changes |
| **Architectural restructuring** | `opus` | System-wide patterns |

**Escalate to opus** for refactors touching 10+ files or changing architecture.

## Parallel Analysis

For large refactors, analyze in parallel:

```
# Analyze different modules simultaneously
Task(subagent_type=Explore, model=haiku, prompt="Find all usages of <target> in src/...")
Task(subagent_type=Explore, model=haiku, prompt="Find all usages of <target> in test/...")
Task(subagent_type=Explore, model=haiku, prompt="Find all usages of <target> in types/...")
Task(subagent_type=Explore, model=haiku, prompt="Check for dynamic imports/requires...")
```

## State Tracking

For large refactors, create `.claude/state/refactor_state.md`:

```markdown
## Refactor: <name>

### Status
| Field | Value |
|-------|-------|
| Status | in_progress |
| Files Total | X |
| Files Complete | Y |
| Tests Passing | ✅/❌ |

### Progress
| File | Status | Notes |
|------|--------|-------|
| `src/auth.ts` | ✅ Complete | Renamed function |
| `src/api.ts` | 🔄 In Progress | ... |
| `test/auth.test.ts` | ⏳ Pending | ... |

### Rollback Point
Commit: abc123
```

## Refactor Types

| Type | Example | Approach |
|------|---------|----------|
| Rename | Function/variable rename | Find all refs, batch update |
| Extract | Extract method/class | Identify boundaries, create abstraction |
| Move | Relocate module | Update all imports |
| Inline | Remove abstraction | Replace refs with implementation |
| Restructure | Change architecture | Plan → Execute → Verify |

## Process

1. **Analyze** - Find all affected files (parallel haiku scans)
2. **Plan** - Create refactor state file
3. **Verify** - Run tests (baseline)
4. **Execute** - Apply changes file by file
5. **Test** - Run tests after each file (auto)
6. **Complete** - Update state, commit

## Batch Processing

Process files in batches:
- Default: 10 files per batch
- Run tests after each batch
- Update state after each batch
- Resume from state if interrupted

## Output

```markdown
## Refactor: $ARGUMENTS

### Impact Analysis
| Scope | Files | Changes |
|-------|-------|---------|
| Direct | 5 | Function signature |
| Indirect | 12 | Import updates |
| Tests | 8 | Test updates |

### Execution
Batch 1/3: src/
- ✅ `auth.ts` - Updated
- ✅ `api.ts` - Updated
- ✅ Tests passing

Batch 2/3: lib/
- ✅ `utils.ts` - Updated
- ✅ Tests passing

Batch 3/3: test/
- ✅ All test files updated
- ✅ Tests passing

### Summary
✅ Refactor complete
- 25 files modified
- 0 test failures
- Committed: feat: refactor $ARGUMENTS
```

## Self-Assessment

After refactor completes:

```markdown
### Self-Assessment
| Check | Status |
|-------|--------|
| All affected files modified | ✅/❌ |
| No missed references | ✅/❌ |
| Tests pass | ✅/❌ |
| State file updated | ✅/❌ |
| No regressions | ✅/❌ |

**Scope Accuracy**: [Complete/Partial/Missed areas]
**Confidence**: [High/Medium/Low]
**Notes**: <any areas that need manual verification>
```

## Autonomy

- Do not ask before scanning files
- Run tests automatically after each batch
- Update state without confirmation
- Only pause if tests fail
- Auto-commit on successful completion
- Output self-assessment after refactor completes

---

## Skills Used

- **codebase-navigator** - Finding all affected files and usages
- **feature-integration** - Understanding cross-system impacts

## Agents Used

- **explorer** (haiku) - Parallel usage scanning across directories
- **analyzer** (sonnet) - Deep impact analysis
- **test-runner** (haiku) - Running tests after each batch

## State Tracking

Creates/updates `.claude/state/refactor_state.md` for resume capability.

## Memory Updates

- Updates `active_context.md` with refactor progress
- May update `patterns/architecture.md` with new patterns
