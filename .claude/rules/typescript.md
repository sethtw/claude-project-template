---
paths: src/**/*.{ts,tsx}, lib/**/*.{ts,tsx}
---

# TypeScript Standards

> Applied automatically to TypeScript files in src/ and lib/

## Import Order

1. Node built-ins (`fs`, `path`, `crypto`)
2. External packages (`react`, `lodash`)
3. Internal modules (`@/lib/`, `@/utils/`)
4. Relative imports (`./`, `../`)

Add blank line between groups.

## Type Safety

### Required
- Explicit return types on exported functions
- No implicit `any` (enable `noImplicitAny`)
- Strict null checks enabled
- Use `unknown` over `any` for external data

### Avoid
- `any` without justification comment: `// any: reason`
- Type assertions (`as`) when type guards work
- Non-null assertions (`!`) in new code

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Interfaces | PascalCase, prefix with `I` optional | `User`, `IUserService` |
| Types | PascalCase | `UserRole`, `ApiResponse` |
| Enums | PascalCase, members UPPER_CASE | `Status.ACTIVE` |
| Functions | camelCase | `getUserById` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Files | kebab-case | `user-service.ts` |

## Patterns

### Prefer interfaces for object shapes
```typescript
// Good
interface User {
  id: string;
  name: string;
}

// Avoid (use type for unions/intersections)
type User = {
  id: string;
  name: string;
}
```

### Use discriminated unions for variants
```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };
```

### Exhaustive switch statements
```typescript
function handleStatus(status: Status): string {
  switch (status) {
    case Status.ACTIVE: return 'active';
    case Status.INACTIVE: return 'inactive';
    default:
      const _exhaustive: never = status;
      throw new Error(`Unhandled status: ${_exhaustive}`);
  }
}
```

## Error Handling

- Throw typed errors or use Result types
- Catch at boundaries, not everywhere
- Log with context: `logger.error('Failed', { userId, error })`

## Async Patterns

- Use async/await over raw Promises
- Always handle rejections
- Use `Promise.all` for parallel operations
- Add timeouts for external calls
