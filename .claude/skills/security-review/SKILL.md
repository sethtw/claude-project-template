---
name: security-review
description: Security analysis, vulnerability scanning, OWASP, authentication, authorization, injection prevention
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Security Review Skill

> Identifies security vulnerabilities using OWASP guidelines.

## When Activated

User mentions: "security review", "security scan", "vulnerability", "OWASP", "auth issues", "authentication", "injection", "XSS", "CSRF", "secrets", "credentials"

## OWASP Top 10 Checks

### A01: Broken Access Control
- Missing authorization checks
- IDOR (Insecure Direct Object References)
- Path traversal vulnerabilities
- CORS misconfiguration

### A02: Cryptographic Failures
- Hardcoded secrets/credentials
- Weak encryption algorithms
- Missing HTTPS enforcement
- Exposed sensitive data in logs

### A03: Injection
- SQL injection in queries
- NoSQL injection
- Command injection
- XSS (Cross-Site Scripting)

### A07: Authentication Failures
- Weak session management
- Missing session timeout
- Session fixation
- Credential stuffing vulnerable

## Scan Patterns

### Credential Detection
```regex
(?i)(password|secret|api.?key|token)\s*[:=]\s*['"]?[^'"}\s]+
```

### SQL Injection Vectors
```regex
\$\{.*\}.*(?:SELECT|INSERT|UPDATE|DELETE)
```

### XSS Patterns
```regex
innerHTML\s*=
dangerouslySetInnerHTML
```

## Severity Classification

| Severity | Description | Response Time |
|----------|-------------|---------------|
| Critical | RCE, auth bypass, data exposure | Immediate |
| High | Injection, privilege escalation | Same day |
| Medium | XSS, CSRF, session issues | This sprint |
| Low | Best practice violations | Backlog |

## Used By

### Commands
- `/review` - Quick security scan
- `/code-review` - Comprehensive review

### Agents
- **security-auditor** - Deep scanning

## Integration

- Uses sonnet for pattern analysis
- References security.md rules
- Follows OWASP guidelines
