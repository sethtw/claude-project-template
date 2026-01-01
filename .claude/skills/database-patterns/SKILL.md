---
name: database-patterns
description: Database design, queries, migrations, indexes, ORM patterns, schema design
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
model: sonnet
---

# Database Patterns Skill

> Best practices for database design, queries, and migrations.

## When Activated

User mentions: "database", "schema", "migration", "query", "SQL", "ORM", "index", "repository pattern", "foreign key", "relationship"

## Schema Design

### Naming Conventions
```sql
-- Tables: plural, snake_case
CREATE TABLE users (...)
CREATE TABLE order_items (...)

-- Columns: snake_case
user_id, created_at, is_active

-- Indexes: idx_table_columns
CREATE INDEX idx_users_email ON users(email);
```

### Common Column Patterns
```sql
id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
updated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
deleted_at  TIMESTAMP,  -- Soft delete
```

## Index Strategy

### When to Index
- Foreign keys
- Frequently filtered columns
- Columns used in ORDER BY
- Composite for common query patterns

### When NOT to Index
- Small tables (< 1000 rows)
- Rarely queried columns
- Frequently updated columns

## Query Patterns

### Avoid N+1
```typescript
// BAD
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// GOOD
const users = await User.findAll({ include: [{ model: Post }] });
```

## Migration Patterns

### Safe Migration Template
```typescript
export async function up(db) {
  await db.query('ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT "active"');
  await db.query('CREATE INDEX CONCURRENTLY idx_users_status ON users(status)');
}

export async function down(db) {
  await db.query('DROP INDEX IF EXISTS idx_users_status');
  await db.query('ALTER TABLE users DROP COLUMN IF EXISTS status');
}
```

## Used By

### Commands
- `/architect` - Schema planning
- `/migrate` - Database migrations
- `/implement` - Data layer implementation

### Agents
- **analyzer** - Query analysis

## Integration

- Uses sonnet for design reasoning
- References architecture.md patterns
- Follows performance-analysis for optimization
