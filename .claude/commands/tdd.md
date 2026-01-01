# TDD Command

Description: Strict Red-Green-Refactor cycle with auto-verification

You are a TDD Architect. Task: Implement "$ARGUMENTS" using strict TDD.

## Model Selection

| Phase | Model | Rationale |
|-------|-------|-----------|
| Test design | `sonnet` | Understanding requirements |
| Test writing | `sonnet` | Quality test code |
| Implementation | `sonnet` | Minimal correct code |
| Refactoring | `sonnet` | Semantic improvements |
| File scanning | `haiku` | Fast lookups |

## Batch Test Generation

For multiple test cases, generate in parallel:

```
# If testing multiple units
Task(subagent_type=general-purpose, model=sonnet, prompt="Write tests for happy path...")
Task(subagent_type=general-purpose, model=sonnet, prompt="Write tests for edge cases...")
Task(subagent_type=general-purpose, model=sonnet, prompt="Write tests for error handling...")
```

## TDD Cycle

### 🔴 Red (Test First)
1. Create test file for "$ARGUMENTS"
2. Write failing test(s)
3. Run tests - confirm failure
4. **Do not proceed until tests fail**

### 🟢 Green (Minimal Implementation)
1. Write minimal code to pass tests
2. Do not over-engineer
3. Run tests - confirm pass
4. **Do not proceed until tests pass**

### 🔵 Refactor (Optimize)
1. Review code for improvements
2. Refactor while keeping tests green
3. Run tests after each change
4. Auto-commit when stable

## Process

1. Read context: `active_context.md`, `testing.md`
2. Design test cases (sonnet)
3. Write failing tests
4. Run tests (auto, no confirmation)
5. Implement minimal solution
6. Run tests (auto)
7. Refactor
8. Run tests (auto)
9. Update `active_context.md`
10. Auto-commit with conventional message

## Output

```markdown
## TDD: $ARGUMENTS

### Tests Written
- `test/feature.test.ts` - X test cases
  - ✅ Happy path
  - ✅ Edge cases
  - ✅ Error handling

### Implementation
- `src/feature.ts` - Minimal implementation

### Refactoring
- Extracted helper function
- Improved naming

### Final Status
✅ All tests passing (X/X)
```

## Self-Assessment

After TDD cycle completes:

```markdown
### Self-Assessment
| Check | Status |
|-------|--------|
| Tests cover happy path | ✅/❌ |
| Tests cover edge cases | ✅/❌ |
| Tests cover error handling | ✅/❌ |
| Implementation minimal | ✅/❌ |
| Refactoring done | ✅/❌ |
| All tests green | ✅/❌ |

**Test Quality**: [Comprehensive/Adequate/Minimal]
**Confidence**: [High/Medium/Low]
```

## Autonomy

- Run tests automatically at each phase
- Do not ask before running tests
- Auto-commit on green
- Only pause if tests fail unexpectedly
- Output self-assessment after cycle completes
