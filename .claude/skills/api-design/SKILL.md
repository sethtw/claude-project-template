---
name: api-design
description: REST API design, GraphQL, endpoint design, request/response schemas, HTTP methods
allowed-tools: Read, Grep, Glob, Edit, Write
model: sonnet
---

# API Design Skill

> Best practices for REST and GraphQL API design.

## When Activated

User mentions: "REST", "API endpoint", "GraphQL schema", "request/response", "HTTP methods", "status codes", "API versioning"

## REST Design Principles

### URL Structure
```
GET    /users           # List users
POST   /users           # Create user
GET    /users/:id       # Get user
PATCH  /users/:id       # Update user
DELETE /users/:id       # Delete user
GET    /users/:id/posts # User's posts
```

### HTTP Methods
| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Read | Yes |
| POST | Create | No |
| PUT | Replace | Yes |
| PATCH | Update | Yes |
| DELETE | Remove | Yes |

### Status Codes
| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable |
| 500 | Server Error |

## Response Format

### Success
```json
{
  "data": { "id": "123", "email": "user@example.com" },
  "meta": { "timestamp": "2024-01-15T10:30:00Z" }
}
```

### Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [{ "field": "email", "message": "Invalid format" }]
  }
}
```

## Validation Pattern

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
});
```

## Used By

### Commands
- `/architect` - API planning
- `/migrate` - API versioning
- `/implement` - API implementation

### Agents
- **analyzer** - API analysis

## Integration

- Uses sonnet for design reasoning
- References architecture.md patterns
- Follows security.md for auth
