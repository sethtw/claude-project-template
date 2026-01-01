# Testing Patterns

> Test organization, conventions, and coverage strategies.

## Test Organization

### Directory Structure
```
tests/
├── unit/                 # Fast, isolated tests
│   ├── services/         # Service layer tests
│   ├── utils/            # Utility function tests
│   └── models/           # Model/validation tests
├── integration/          # Component interaction tests
│   ├── api/              # API endpoint tests
│   └── repositories/     # Database tests
└── e2e/                  # Full user flow tests
    ├── auth/             # Authentication flows
    └── features/         # Feature-specific flows
```

### File Naming
| Pattern | Location | Purpose |
|---------|----------|---------|
| `*.test.ts` | Next to source | Unit tests |
| `*.spec.ts` | tests/ directory | Integration/E2E |
| `__mocks__/*.ts` | Module directory | Manual mocks |
| `fixtures/*.ts` | tests/ | Test data |

---

## Unit Test Patterns

### Structure (AAA Pattern)
```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('creates user with valid data', async () => {
      // Arrange
      const userData = { email: 'test@example.com', name: 'Test' };
      const mockRepo = { create: jest.fn().mockResolvedValue({ id: '1', ...userData }) };
      const service = new UserService(mockRepo);

      // Act
      const result = await service.createUser(userData);

      // Assert
      expect(result.id).toBeDefined();
      expect(result.email).toBe(userData.email);
      expect(mockRepo.create).toHaveBeenCalledWith(userData);
    });

    it('throws ValidationError for invalid email', async () => {
      // Arrange
      const userData = { email: 'invalid', name: 'Test' };
      const service = new UserService(mockRepo);

      // Act & Assert
      await expect(service.createUser(userData))
        .rejects.toThrow(ValidationError);
    });
  });
});
```

### Mocking Best Practices
```typescript
// Mock at boundaries, not internal modules
jest.mock('../external/payment-gateway');

// Use dependency injection for testability
const mockRepo = {
  findById: jest.fn(),
  create: jest.fn(),
};
const service = new UserService(mockRepo);

// Reset mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});
```

---

## Integration Test Patterns

### API Testing
```typescript
describe('POST /api/users', () => {
  it('creates user and returns 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })
      .expect(201);

    expect(response.body.data.id).toBeDefined();
    expect(response.body.data.email).toBe('test@example.com');
  });

  it('returns 400 for invalid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid' })
      .expect(400);

    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

### Database Testing
```typescript
describe('UserRepository', () => {
  beforeAll(async () => {
    await db.migrate.latest();
  });

  beforeEach(async () => {
    await db('users').truncate();
  });

  afterAll(async () => {
    await db.destroy();
  });

  it('creates and retrieves user', async () => {
    const repo = new UserRepository(db);

    const created = await repo.create({ email: 'test@example.com' });
    const retrieved = await repo.findById(created.id);

    expect(retrieved).toEqual(created);
  });
});
```

---

## E2E Test Patterns

### User Flow Testing
```typescript
describe('User Registration Flow', () => {
  it('completes full registration', async () => {
    // Navigate to registration
    await page.goto('/register');

    // Fill form
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    // Verify redirect
    await expect(page).toHaveURL('/dashboard');

    // Verify user state
    await expect(page.locator('.user-email')).toHaveText('test@example.com');
  });
});
```

---

## Coverage Requirements

| Metric | Target | Critical Paths |
|--------|--------|----------------|
| Statements | 80% | 95% |
| Branches | 75% | 90% |
| Functions | 80% | 95% |
| Lines | 80% | 95% |

### Focus Areas
1. **Critical paths** - Authentication, payments, data mutations
2. **Business logic** - Service layer, validators
3. **Edge cases** - Error handling, boundary conditions

### Low Priority
- Configuration files
- Type definitions
- Generated code

---

## Test Data Patterns

### Factories
```typescript
// factories/user.ts
export const createUser = (overrides: Partial<User> = {}): User => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  createdAt: new Date(),
  ...overrides,
});

// Usage in tests
const user = createUser({ email: 'specific@example.com' });
```

### Fixtures
```typescript
// fixtures/users.ts
export const validUser = {
  email: 'valid@example.com',
  name: 'Valid User',
};

export const invalidEmails = [
  'invalid',
  'missing@domain',
  '@nodomain.com',
  '',
];
```

---

## What Tests Catch

| Bug Type | Unit | Integration | E2E |
|----------|------|-------------|-----|
| Logic errors | Yes | | |
| Type mismatches | Yes | | |
| API contract violations | | Yes | |
| Database issues | | Yes | |
| UI rendering | | | Yes |
| User flow breaks | | | Yes |
| Performance regressions | | | Yes |

---

## Cross-References

- **Skills**: tdd-workflow for test-first patterns
- **Rules**: testing.md for conventions
- **Agents**: test-runner for execution
