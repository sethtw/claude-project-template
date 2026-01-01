---
paths: **/auth/**/*.{ts,tsx,js}, **/api/**/*.{ts,tsx,js}, src/middleware/**/*
---

# Security Standards

> Applied automatically to authentication, API, and middleware code

## Input Validation

### Validate at boundaries
```typescript
// API endpoint - validate incoming data
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const validated = schema.parse(req.body);
```

### Sanitize before output
- HTML: Escape or use safe templating
- SQL: Use parameterized queries only
- Shell: Never interpolate user input

## Authentication

### Password handling
- Hash with bcrypt/argon2 (cost factor 12+)
- Never log passwords or tokens
- Use constant-time comparison

### Session management
- Regenerate session ID on login
- Set secure cookie flags: `httpOnly`, `secure`, `sameSite`
- Implement session timeout (idle + absolute)

### JWT patterns
```typescript
// Short-lived access tokens
const accessToken = jwt.sign(payload, secret, { expiresIn: '15m' });

// Longer refresh tokens (stored securely)
const refreshToken = jwt.sign({ userId }, secret, { expiresIn: '7d' });
```

## Authorization

### Check at every endpoint
```typescript
// Always verify permissions
if (!user.hasPermission('users:read')) {
  throw new ForbiddenError();
}
```

### Avoid security by obscurity
- Don't rely on hidden URLs
- Don't trust client-side checks
- Validate ownership of resources

## API Security

### Rate limiting
```typescript
// Per-user limits
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  keyGenerator: (req) => req.user?.id || req.ip,
});
```

### CORS configuration
```typescript
// Explicit origins, not '*'
const corsOptions = {
  origin: ['https://app.example.com'],
  credentials: true,
};
```

### Request validation
- Validate Content-Type
- Limit request body size
- Timeout long requests

## Secrets Management

### Never commit secrets
- Use environment variables
- Add to `.gitignore`: `.env`, `*.pem`, `credentials.json`
- Use secrets manager in production

### Rotate regularly
- API keys: 90 days
- Signing keys: 1 year
- Passwords: On compromise or employee departure

## OWASP Top 10 Checklist

| Vulnerability | Mitigation |
|--------------|------------|
| Injection | Parameterized queries, input validation |
| Broken Auth | Strong passwords, MFA, session management |
| Sensitive Data | Encryption at rest/transit, minimal collection |
| XXE | Disable XML external entities |
| Broken Access | Check permissions on every request |
| Misconfiguration | Security headers, disable debug |
| XSS | Output encoding, CSP headers |
| Insecure Deserialization | Validate before deserializing |
| Known Vulnerabilities | Keep dependencies updated |
| Insufficient Logging | Log security events, monitor |

## Security Headers

```typescript
// helmet.js configuration
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
    },
  },
  hsts: { maxAge: 31536000 },
}));
```

## Logging

### Log security events
- Authentication attempts (success/failure)
- Authorization failures
- Input validation failures
- Rate limit triggers

### Never log
- Passwords or tokens
- Full credit card numbers
- Personal health information
- Encryption keys
