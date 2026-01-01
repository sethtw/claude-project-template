---
paths: **/*.test.{ts,tsx,js,jsx}, **/*.spec.{ts,tsx,js,jsx}, __tests__/**/*
---

# Testing Standards

> Applied automatically to test files

## Test Structure

### Naming
- Describe what, not how: `'returns user when found'`
- Use present tense: `'validates email format'`
- Be specific: `'throws ValidationError for empty name'`

### Organization
```typescript
describe('UserService', () => {
  describe('getUserById', () => {
    it('returns user when found', async () => {});
    it('returns null when not found', async () => {});
    it('throws on invalid id format', async () => {});
  });
});
```

## Test Categories

### Unit Tests
- Test single function/method in isolation
- Mock external dependencies
- Fast execution (<100ms each)
- Located next to source: `user.ts` → `user.test.ts`

### Integration Tests
- Test multiple components together
- Use real dependencies where possible
- Located in `__tests__/integration/`

### E2E Tests
- Test full user flows
- Use test database
- Located in `e2e/` or `__tests__/e2e/`

## AAA Pattern

```typescript
it('calculates total with tax', () => {
  // Arrange
  const cart = new Cart();
  cart.addItem({ price: 100 });

  // Act
  const total = cart.getTotal({ includeTax: true });

  // Assert
  expect(total).toBe(107); // 7% tax
});
```

## Assertions

### Prefer specific matchers
```typescript
// Good
expect(result).toEqual({ id: 1, name: 'Test' });
expect(array).toHaveLength(3);
expect(fn).toHaveBeenCalledWith('arg');

// Avoid
expect(result.id === 1).toBe(true);
expect(array.length).toBe(3);
```

### Error assertions
```typescript
await expect(fn()).rejects.toThrow(ValidationError);
expect(() => parse(invalid)).toThrow('Invalid format');
```

## Mocking

### Mock at boundaries
```typescript
// Mock external services, not internal modules
jest.mock('../services/api');

// Use dependency injection for testability
const service = new UserService(mockRepository);
```

### Reset between tests
```typescript
beforeEach(() => {
  jest.clearAllMocks();
});
```

## Coverage

| Metric | Target |
|--------|--------|
| Statements | 80% |
| Branches | 75% |
| Functions | 80% |
| Lines | 80% |

Focus on critical paths, not 100% coverage.

## Test Data

- Use factories for complex objects
- Keep test data close to tests
- Use realistic but anonymized data
- Clean up after integration tests
