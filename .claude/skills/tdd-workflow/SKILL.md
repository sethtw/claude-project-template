---
name: tdd-workflow
description: TDD, test-driven development, writing tests first, red-green-refactor
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
model: sonnet
---

# TDD Workflow Skill

> Enforces strict test-driven development: Red → Green → Refactor

## When Activated

User mentions: "TDD", "test first", "test-driven", "red green refactor", "write tests before code", "failing test first"

## Core Process

### 1. Red Phase (Write Failing Test)
1. Understand the requirement
2. Write a test that fails for the right reason
3. Run test - confirm it fails
4. Do NOT write implementation yet

### 2. Green Phase (Minimal Implementation)
1. Write ONLY enough code to pass
2. No optimization, no extras
3. Run test - confirm it passes
4. Commit on green

### 3. Refactor Phase (Improve)
1. Tests still passing? Proceed
2. Improve code quality
3. Remove duplication
4. Run tests after each change
5. Commit when clean

## Test Patterns

### Unit Test Structure (AAA)
```typescript
describe('FeatureName', () => {
  describe('methodName', () => {
    it('should do X when Y', () => {
      // Arrange - setup
      const input = createTestInput();

      // Act - execute
      const result = methodUnderTest(input);

      // Assert - verify
      expect(result).toBe(expected);
    });
  });
});
```

### Test Naming
- `it('should [expected behavior] when [condition]')`
- `it('throws ValidationError for invalid email')`
- `it('returns null when user not found')`

## Commands Integration

When used with `/tdd`:
1. Generate test file first
2. Run test (expect failure)
3. Generate implementation
4. Run test (expect pass)
5. Offer refactoring suggestions
6. Auto-commit on green

## Autonomy Rules

- Never skip the red phase
- Never write implementation before test
- Run tests automatically between phases
- Auto-commit only when green
- Stop if tests fail after green phase

## Used By

### Commands
- `/tdd` - Primary command
- `/test-gen` - Test generation
- `/implement` - Stage 4 verification

### Agents
- **test-runner** - Test execution

## Integration

- Works with testing.md patterns
- Uses sonnet for test reasoning
- Auto-runs tests via Bash
