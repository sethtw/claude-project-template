# Known Issues

> Outstanding issues, deferred items, and common quick fixes.

## Active Issues

| ID | Issue | Severity | Workaround | Target Fix |
|----|-------|----------|------------|------------|
| (none) | No active issues | - | - | - |

---

## Recent Fixes

| ID | Issue | Fix Date | Solution |
|----|-------|----------|----------|
| (none) | No recent fixes | - | - |

---

## Deferred Items

> Items intentionally postponed with rationale.

| Item | Reason Deferred | Revisit When |
|------|-----------------|--------------|
| (none) | No deferred items | - |

---

## Common Quick Fixes

### Build Issues

**Issue**: `Cannot find module`
```bash
# Solution: Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue**: TypeScript errors after dependency update
```bash
# Solution: Rebuild TypeScript cache
rm -rf dist/ .tsbuildinfo
npm run build
```

### Test Issues

**Issue**: Tests failing with stale data
```bash
# Solution: Clear test database
npm run test:db:reset
```

**Issue**: Timeout errors in integration tests
```typescript
// Solution: Increase timeout for slow tests
jest.setTimeout(30000); // 30 seconds
```

### Database Issues

**Issue**: Migration failed
```bash
# Solution: Rollback and retry
npm run migrate:rollback
npm run migrate:latest
```

**Issue**: Connection pool exhausted
```typescript
// Solution: Ensure connections are released
const client = await pool.connect();
try {
  // ... operations
} finally {
  client.release(); // Always release
}
```

### Runtime Issues

**Issue**: Memory leak in development
```bash
# Solution: Restart with heap limit
node --max-old-space-size=4096 app.js
```

**Issue**: Port already in use
```bash
# Solution: Find and kill process
lsof -i :3000
kill -9 <PID>
```

---

## Environment-Specific Issues

### Development
| Issue | Solution |
|-------|----------|
| (none) | - |

### Staging
| Issue | Solution |
|-------|----------|
| (none) | - |

### Production
| Issue | Solution |
|-------|----------|
| (none) | - |

---

## Technical Debt Log

| Item | Impact | Effort | Priority |
|------|--------|--------|----------|
| (none) | - | - | - |

---

## Issue Template

When adding new issues:

```markdown
### ISSUE-XXX: Brief Title

**Severity**: Critical / High / Medium / Low
**Status**: Active / Investigating / Workaround / Resolved

**Description**:
What is happening?

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Observe issue

**Expected Behavior**:
What should happen?

**Workaround**:
Temporary solution if available.

**Root Cause** (if known):
Why this happens.

**Fix**:
How to resolve permanently.
```

---

## Cross-References

- **Updated by**: `/review`, `/code-review` commands
- **Skills**: security-review for vulnerability issues
