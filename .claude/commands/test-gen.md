# Test Generator

Description: Batch test generation for modules

You are a Test Engineer. Task: Generate comprehensive tests for "$ARGUMENTS".

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Code analysis | `haiku` | Fast structure parsing |
| Test design | `sonnet` | Understanding behavior |
| Test writing | `sonnet` | Quality test code |
| Coverage check | `haiku` | File scanning |

## Parallel Test Generation

Generate tests for multiple units simultaneously:

```
# For a module with multiple exports
Task(subagent_type=general-purpose, model=sonnet, prompt="Generate tests for UserService.create()...")
Task(subagent_type=general-purpose, model=sonnet, prompt="Generate tests for UserService.update()...")
Task(subagent_type=general-purpose, model=sonnet, prompt="Generate tests for UserService.delete()...")
Task(subagent_type=general-purpose, model=sonnet, prompt="Generate tests for UserService edge cases...")
```

## Test Categories

For each function/method, generate:

| Category | Description | Priority |
|----------|-------------|----------|
| Happy Path | Normal successful operation | 🔴 Required |
| Edge Cases | Boundary conditions, empty inputs | 🔴 Required |
| Error Handling | Invalid inputs, exceptions | 🔴 Required |
| Integration | Cross-module behavior | 🟡 If applicable |
| Performance | Load/stress conditions | 🟢 Optional |

## Process

1. **Analyze** - Parse module structure (haiku)
2. **Identify** - List all testable units
3. **Design** - Plan test cases per unit (sonnet)
4. **Generate** - Write tests in parallel
5. **Verify** - Run tests, ensure they fail appropriately
6. **Report** - Coverage summary

## Batch Processing

For large modules:
- Generate tests in batches of 5 functions
- Run tests after each batch
- Track coverage incrementally

## Output

```markdown
## Test Generation: $ARGUMENTS

### Analysis
| Metric | Value |
|--------|-------|
| Functions | 12 |
| Already Tested | 3 |
| To Generate | 9 |

### Generated Tests

#### UserService
| Function | Tests | Coverage |
|----------|-------|----------|
| create() | 5 | 100% |
| update() | 4 | 100% |
| delete() | 3 | 100% |
| findById() | 3 | 100% |

#### Test File
`test/services/UserService.test.ts`
- 15 test cases
- 3 describe blocks
- Edge cases covered

### Coverage Report
| File | Statements | Branches | Functions |
|------|------------|----------|-----------|
| UserService.ts | 95% | 88% | 100% |

### Run Results
✅ 15/15 tests passing
```

## Self-Assessment

After test generation completes:

```markdown
### Self-Assessment
| Check | Status |
|-------|--------|
| Happy path tests written | ✅/❌ |
| Edge cases covered | ✅/❌ |
| Error handling tested | ✅/❌ |
| All tests passing | ✅/❌ |
| No existing tests broken | ✅/❌ |

**Coverage Quality**: [Comprehensive/Adequate/Minimal]
**Confidence**: [High/Medium/Low]
**Notes**: <scenarios that may need additional tests>
```

## Autonomy

- Do not ask before analyzing code
- Generate tests without confirmation
- Run tests automatically
- Only pause if existing tests break
- Auto-stage generated test files
- Output self-assessment after test generation
