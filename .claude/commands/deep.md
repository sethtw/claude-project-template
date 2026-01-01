# /deep - Deep Analysis

> Promote files from L0/L1 to L2/L3 with comprehensive analysis.

## Purpose

Perform deep analysis on specific files or directories, extracting:
- Key concepts and relationships
- Code patterns and complexity
- Integration points
- Known issues and TODOs

## Usage

```
/deep src/services/user.ts          # Analyze single file to L2
/deep src/services/user.ts --l3     # Full L3 analysis
/deep src/services/                 # Analyze directory to L2
/deep src/api/ --l3                 # Full L3 on directory
```

## Process

### Step 1: Check Current Depth

Read registry to find current depth of target:

```markdown
| DOC_ID | Path | Current Depth |
|--------|------|---------------|
| DOC_123 | src/services/user.ts | L0 |
```

### Step 2: Analyze (sonnet)

For L2 (Summary):
- Extract key concepts
- Identify relationships
- Note patterns used
- Assess complexity

For L3 (Deep):
- All of L2 plus:
- Full outline with sections
- Key code excerpts
- Integration points (calls/called by)
- Known issues and TODOs
- Edge cases

### Step 3: Extract Concepts

Identify key concepts and add WikiLinks:

```markdown
### Key Concepts
- [[UserService]] - Core user management
- [[Authentication]] - JWT-based auth
- [[Repository Pattern]] - Data access abstraction
```

### Step 4: Update Registry

Update file's registry entry with new depth:

```markdown
## DOC_123: user.ts

| Field | Value |
|-------|-------|
| Path | src/services/user.ts |
| Type | code |
| Depth | L2 |
| Complexity | medium |
| Last Analyzed | 2024-01-15 |

### Summary
UserService provides core user management including creation, authentication, and profile updates.

### Key Concepts
- [[UserService]] - Core service
- [[Authentication]] - JWT handling

### Related Documents
- DOC_124 (auth.ts) - Uses for token validation
- DOC_125 (user.test.ts) - Test coverage
```

### Step 5: Update Concepts Index

Add new concepts to `_concepts.md`:

```markdown
## [[UserService]]

**Category**: Domain
**Importance**: Core

### Definition
Core service for user management operations.

### Appears In
| DOC_ID | File | Context |
|--------|------|---------|
| DOC_123 | user.ts | Main implementation |
| DOC_125 | user.test.ts | Test subject |
```

## Output Format

```markdown
## Deep Analysis: src/services/user.ts

### Promoted to: L2

### Summary
UserService provides core user management including CRUD operations, authentication integration, and profile management.

### Key Findings
1. **Complexity**: Medium (12 methods, 350 lines)
2. **Dependencies**: 4 external, 3 internal
3. **Test Coverage**: 85%

### Concepts Extracted
- [[UserService]]
- [[Authentication]]
- [[Repository Pattern]]

### Relationships
- **Calls**: AuthService, UserRepository, Logger
- **Called by**: UserController, AuthController

### Recommendations
- Consider splitting profile methods to ProfileService
- Add input validation at service boundary
```

## Autonomy

- Analyze without confirmation
- Update registry automatically
- Create concept entries automatically
- Only pause for complex architectural decisions

## Model Selection

| Phase | Model | Rationale |
|-------|-------|-----------|
| L2 analysis | sonnet | Needs understanding |
| L3 analysis | sonnet/opus | Complex reasoning |
| Concept extraction | sonnet | Pattern recognition |
| Registry update | haiku | Structural update |

## Skills Used

- `codebase-navigator` - Finding relationships
- `feature-integration` - Understanding connections

## Agents Used

- `analyzer` - Deep code analysis

## Memory Updates

- Updates `_registry.md` with promoted entry
- Updates `_concepts.md` with new concepts
- Updates `_index.md` with depth counts
- Updates `active_context.md` with analysis results
