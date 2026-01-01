---
name: performance-analysis
description: Performance optimization, bottleneck identification, profiling, slow code, memory leaks
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

# Performance Analysis Skill

> Identifies performance bottlenecks and suggests optimizations.

## When Activated

User mentions: "slow", "performance", "optimize", "bottleneck", "profiling", "memory leak", "memory usage", "latency", "response time", "bundle size", "load time"

## Analysis Categories

### 1. Algorithm Complexity
- O(n^2) loops that could be O(n)
- Nested iterations over large datasets
- Repeated calculations (missing memoization)
- Unnecessary sorting/filtering

### 2. Database Performance
- N+1 query patterns
- Missing indexes on filtered columns
- SELECT * instead of specific columns
- Large result sets without pagination

### 3. Memory Issues
- Growing arrays in loops
- Unreleased event listeners
- Large objects in closures
- Missing cleanup in useEffect

### 4. Frontend Performance
- Unnecessary re-renders
- Missing virtualization for long lists
- Unoptimized images
- Large bundle sizes

## Detection Patterns

### N+1 Query Pattern
```typescript
// BAD
for (const user of users) {
  const posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
}

// GOOD
const usersWithPosts = await db.query(
  'SELECT u.*, p.* FROM users u LEFT JOIN posts p ON p.user_id = u.id'
);
```

### Missing Memoization
```typescript
// BAD
const total = items.reduce((sum, i) => sum + i.price, 0);

// GOOD
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items]);
```

## Used By

### Commands
- `/analyze` - Codebase analysis
- `/code-review` - Comprehensive review
- `/implement` - Stage 4 verification

### Agents
- **analyzer** - Deep analysis

## Integration

- Uses sonnet for pattern analysis
- References architecture.md for caching
- Profile before optimizing
