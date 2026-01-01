---
name: codebase-navigator
description: Codebase exploration, file search, pattern discovery, architecture understanding, dependency tracing
allowed-tools: Read, Grep, Glob, Task
model: haiku
---

# Codebase Navigator Skill

> Efficiently explore and understand codebases.

## When Activated

User mentions: "find", "where is", "how does", "show me", "explore", "navigate", "understand codebase"

## Navigation Strategies

### 1. Entry Point Discovery

```bash
# Find main entry points
Glob pattern: "**/main.{ts,js,py}", "**/index.{ts,js,py}", "**/app.{ts,js,py}"

# Find configuration files
Glob pattern: "**/{package,tsconfig,webpack,vite}.{json,js,ts}"

# Find route definitions
Grep pattern: "router\.|Route|createBrowserRouter|express\(\)"
```

### 2. Feature Location

```bash
# By feature name
Grep: "FeatureName|featureName|feature_name|feature-name"

# By file pattern
Glob: "**/feature/**/*", "**/features/{name}/**/*"

# By export
Grep: "export.*FeatureName"
```

### 3. Dependency Tracing

**Upstream** (what this depends on):
```bash
Grep in file: "import.*from|require\("
```

**Downstream** (what depends on this):
```bash
Grep: "from ['\"].*{filename}|require\(['\"].*{filename}"
```

### 4. Pattern Discovery

```bash
# Find similar implementations
Grep: "class.*extends|implements"

# Find hooks/middleware
Grep: "use[A-Z]|before|after|middleware"

# Find event handlers
Grep: "on[A-Z].*=|addEventListener|emit\("
```

## Search Efficiency

### Start Broad, Then Narrow

```
1. Glob for file types: "**/*.ts"
2. Grep for general term: "user"
3. Grep for specific: "getUserById"
4. Read specific file
```

### Use Parallel Searches

```
Task(model=haiku, prompt="Find all files in src/api/")
Task(model=haiku, prompt="Find all files importing UserService")
Task(model=haiku, prompt="Find all test files for users")
```

### Know Common Structures

| Pattern | Typical Location |
|---------|-----------------|
| Routes | `src/routes/`, `src/api/` |
| Components | `src/components/`, `src/ui/` |
| Services | `src/services/`, `src/lib/` |
| Types | `src/types/`, `src/@types/` |
| Utils | `src/utils/`, `src/helpers/` |
| Tests | `__tests__/`, `*.test.ts` |
| Config | Root, `config/` |

## Quick Reference Queries

### "How does X work?"
1. Find X definition: `Grep: "class X|function X|const X"`
2. Find X usage: `Grep: "X\(|new X"`
3. Find X tests: `Glob: "**/*X*.test.ts"`

### "Where is X used?"
1. Find imports: `Grep: "import.*X.*from"`
2. Find references: `Grep: "X\.|X\(|<X"`

### "What calls X?"
1. Find function calls: `Grep: "X\("`
2. Trace up the call chain

### "What does X depend on?"
1. Read X file
2. List imports
3. Trace each import

## Output Format

```markdown
## Navigation: <Query>

### Files Found
| File | Relevance | Key Content |
|------|-----------|-------------|
| src/services/user.ts | High | UserService class |
| src/api/users.ts | High | API endpoints |
| src/types/user.ts | Medium | Type definitions |

### Architecture Notes
- UserService is the core business logic
- API layer is thin, delegates to service
- Types are shared across modules

### Suggested Deep Dives
- `src/services/user.ts` - Main logic
- `__tests__/user.test.ts` - Behavior examples
```

## Used By

### Commands
- `/index` - Codebase scanning
- `/deep` - File analysis
- `/context` - Navigation
- `/analyze` - Codebase exploration
- `/implement` - Stage 1 discovery
- `/refactor` - Finding affected files
- `/test-gen` - Finding testable units
- `/migrate` - Finding migration targets
- `/initialize` - Initial codebase scan

### Agents
- **explorer** - Primary skill

## Integration

- Primary skill for exploration queries
- Uses haiku for speed
- Populates registry when scanning
- Updates `active_context.md` with findings
