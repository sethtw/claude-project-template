# Architecture Patterns

> Project structure, error handling, and architectural decisions.

## Project Structure

### Standard Layout
```
src/
├── api/              # API routes/endpoints
│   ├── routes/       # Route definitions
│   └── middleware/   # API middleware
├── services/         # Business logic layer
├── models/           # Data models/entities
├── repositories/     # Data access layer
├── utils/            # Shared utilities
├── types/            # TypeScript type definitions
└── config/           # Configuration management

tests/
├── unit/             # Unit tests
├── integration/      # Integration tests
└── e2e/              # End-to-end tests

.claude/
├── memory/           # Context and patterns
├── skills/           # Semantic skills
├── agents/           # Specialized agents
├── rules/            # Path-scoped standards
├── commands/         # Slash commands
└── state/            # Operation state
```

### Layer Dependencies
```
API Layer (routes, controllers)
    ↓
Service Layer (business logic)
    ↓
Repository Layer (data access)
    ↓
Database / External Services
```

**Rule**: Dependencies flow downward only. Lower layers never import from higher layers.

---

## Error Handling

### Error Types
```typescript
// Base error class
class AppError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number = 500,
    public details?: unknown
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Specific errors
class ValidationError extends AppError {
  constructor(message: string, details?: unknown) {
    super('VALIDATION_ERROR', message, 400, details);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super('UNAUTHORIZED', message, 401);
  }
}
```

### Error Handling Pattern
```typescript
// Service layer: throw errors
async function getUser(id: string): Promise<User> {
  const user = await userRepo.findById(id);
  if (!user) throw new NotFoundError('User');
  return user;
}

// API layer: catch and respond
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await getUser(req.params.id);
    res.json({ data: user });
  } catch (error) {
    next(error);
  }
});

// Error middleware: format response
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      error: {
        code: error.code,
        message: error.message,
        details: error.details,
      }
    });
  }
  // Log unexpected errors, return generic message
  logger.error('Unexpected error', { error });
  res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
});
```

---

## Configuration Management

### Environment-Based Config
```typescript
// config/index.ts
const config = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),
  database: {
    url: process.env.DATABASE_URL,
    pool: {
      min: parseInt(process.env.DB_POOL_MIN || '2', 10),
      max: parseInt(process.env.DB_POOL_MAX || '10', 10),
    },
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '15m',
  },
};

// Validate required config
const required = ['DATABASE_URL', 'JWT_SECRET'];
for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required env var: ${key}`);
  }
}

export default config;
```

---

## Dependency Injection

### Simple DI Pattern
```typescript
// Define interfaces
interface UserRepository {
  findById(id: string): Promise<User | null>;
  create(data: CreateUserDTO): Promise<User>;
}

// Service receives dependencies
class UserService {
  constructor(private userRepo: UserRepository) {}

  async getUser(id: string): Promise<User> {
    const user = await this.userRepo.findById(id);
    if (!user) throw new NotFoundError('User');
    return user;
  }
}

// Wire up in composition root
const userRepo = new PostgresUserRepository(db);
const userService = new UserService(userRepo);
```

---

## Caching Strategy

### Cache Layers
| Layer | Tool | TTL | Use Case |
|-------|------|-----|----------|
| Request | In-memory | Request lifetime | Dedupe within request |
| Application | Redis | Minutes-Hours | Frequently accessed data |
| HTTP | CDN/Browser | Hours-Days | Static assets, API responses |

### Cache Pattern
```typescript
async function getUserCached(id: string): Promise<User> {
  const cacheKey = `user:${id}`;

  // Check cache
  const cached = await cache.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Fetch from DB
  const user = await userRepo.findById(id);
  if (!user) throw new NotFoundError('User');

  // Store in cache
  await cache.set(cacheKey, JSON.stringify(user), 'EX', 300); // 5 min

  return user;
}
```

---

## Logging

### Log Levels
| Level | When to Use |
|-------|-------------|
| error | Exceptions, failures requiring attention |
| warn | Unexpected but recoverable situations |
| info | Significant events (startup, requests) |
| debug | Detailed diagnostic information |

### Structured Logging
```typescript
logger.info('User created', {
  userId: user.id,
  email: user.email,
  requestId: req.id,
});
```

---

## Cross-References

- **Skills**: architecture patterns used by feature-integration
- **Rules**: security.md for auth patterns
- **Updated by**: /analyze command
