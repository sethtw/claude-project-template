# Architectural Planner

Description: Generate implementation plan without writing code

You are a Senior Software Architect. Task: Create a detailed implementation plan for "$ARGUMENTS".

**This command PLANS ONLY. Use `/implement --planned` to execute the plan.**

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Context gathering | `haiku` | Fast file reads |
| Dependency mapping | `haiku` | Structural analysis |
| Architecture analysis | `sonnet` | Design decisions |
| Plan synthesis | `opus` | Complex multi-system reasoning |

## Parallel Context Gathering

Launch parallel discovery agents:

```
Task(subagent_type=Explore, model=haiku, prompt="Read architecture patterns...")
Task(subagent_type=Explore, model=haiku, prompt="Read current progress...")
Task(subagent_type=Explore, model=haiku, prompt="Analyze existing codebase structure...")
Task(subagent_type=Explore, model=haiku, prompt="Check for related implementations...")
```

## Process

### 1. Context Audit
Read in parallel:
- `.claude/memory/system_patterns.md`
- `.claude/memory/product_context.md`
- `.claude/memory/progress.md`
- `.claude/memory/active_context.md`

### 2. Deep Analysis (Opus)
- Identify ALL files to create/modify
- List external dependencies needed
- Map integration points across systems
- Assess complexity and risks
- Design error handling strategy
- Plan test coverage

### 3. Create Detailed Plan

The plan MUST be explicit enough for Sonnet to execute without improvisation:

```markdown
## Implementation Plan: $ARGUMENTS

### Summary
<2-3 sentence description of what will be built>

### Complexity Assessment
| Factor | Rating | Notes |
|--------|--------|-------|
| Files affected | Low/Med/High | X files |
| Systems touched | Low/Med/High | X systems |
| Risk level | Low/Med/High | <reason> |

### Files to Create
| File | Purpose | Key Exports |
|------|---------|-------------|
| `src/services/feature.ts` | Core logic | `createFeature()`, `getFeature()` |
| `src/api/feature.ts` | API endpoints | `POST /features`, `GET /features/:id` |
| `tests/feature.test.ts` | Unit tests | Test suites for each function |

### Files to Modify
| File | Changes | Risk |
|------|---------|------|
| `src/routes.ts` | Add feature routes | Low |
| `src/types/index.ts` | Add Feature types | Low |

### Implementation Steps

#### Step 1: Type Definitions
Create types in `src/types/feature.ts`:
```typescript
export interface Feature {
  id: string;
  name: string;
  createdAt: Date;
  // ... complete interface
}

export interface CreateFeatureDTO {
  name: string;
  // ... complete DTO
}
```

#### Step 2: Service Layer
Create `src/services/feature.ts`:
- Function: `createFeature(data: CreateFeatureDTO): Promise<Feature>`
  - Validate input using Zod
  - Call repository
  - Return created feature
- Function: `getFeature(id: string): Promise<Feature | null>`
  - Call repository
  - Return feature or null
- Follow pattern from: `src/services/user.ts`

#### Step 3: API Endpoints
Create `src/api/feature.ts`:
- `POST /features` → calls `createFeature`
- `GET /features/:id` → calls `getFeature`
- Error handling: Use `AppError` pattern from `src/api/users.ts`
- Validation: Use Zod middleware pattern

#### Step 4: Tests
Create `tests/feature.test.ts`:
- Test `createFeature` with valid data → returns Feature
- Test `createFeature` with invalid data → throws ValidationError
- Test `getFeature` with valid ID → returns Feature
- Test `getFeature` with invalid ID → returns null

#### Step 5: Integration
- Add routes to `src/routes.ts`
- Export types from `src/types/index.ts`
- Update API documentation

### Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| (none needed) | | |

### Patterns to Follow
- Error handling: `src/errors.ts` → `AppError` class
- Validation: `src/validators/` → Zod schemas
- Repository: `src/repositories/` → Data access pattern
- Response format: `{ data: ... }` wrapper

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| <risk 1> | <mitigation> |

### Test Plan
| Test Type | Coverage | Priority |
|-----------|----------|----------|
| Unit | All public functions | High |
| Integration | API endpoints | High |
| E2E | User flow | Medium |
```

### 4. Save Plan

Save the plan to TWO locations:

1. **State file** (for /implement handoff):
   `.claude/state/current_plan.md`

2. **Active context** (for session awareness):
   `.claude/memory/active_context.md`

### 5. Output Summary

```markdown
## Plan Created: $ARGUMENTS

### Quick Stats
| Metric | Value |
|--------|-------|
| Files to create | X |
| Files to modify | Y |
| Implementation steps | Z |
| Estimated complexity | Low/Medium/High |

### Plan saved to:
- `.claude/state/current_plan.md`
- `.claude/memory/active_context.md`

### Next Steps

**To implement this plan (cost-optimized):**
```
/implement --planned
```

**To implement with fresh planning (if requirements changed):**
```
/implement --fresh $ARGUMENTS
```

**To review/modify the plan first:**
```
Read .claude/state/current_plan.md
```
```

## DO NOT Execute

**IMPORTANT**: This command creates plans only. It does NOT:
- Write implementation code
- Create files
- Run tests
- Make commits

Use `/implement --planned` to execute the plan.

## Self-Assessment

```markdown
### Plan Quality Assessment
| Check | Status |
|-------|--------|
| All affected files identified | ✅/❌ |
| Steps are explicit (not vague) | ✅/❌ |
| Patterns referenced with file paths | ✅/❌ |
| Types/interfaces fully specified | ✅/❌ |
| Test cases defined | ✅/❌ |
| Risks identified | ✅/❌ |

**Plan Completeness**: [High/Medium/Low]
**Sonnet Executability**: [Ready/Needs Detail/Too Vague]
```

## Autonomy

- Do not ask for approval to start planning
- Gather context automatically
- Create comprehensive plan
- Save plan without confirmation
- DO NOT proceed to implementation
- Suggest `/implement --planned` as next step

---

## Skills Used

- **feature-integration** (opus) - Multi-system planning and impact analysis
- **codebase-navigator** - Understanding existing structure
- **api-design** - API endpoint planning
- **database-patterns** - Data layer planning
- **ux-workflow-analysis** - UI/UX considerations

## Agents Used

- **explorer** (haiku) - Fast parallel context gathering
- **analyzer** (sonnet) - Architecture analysis

## Memory Updates

- Creates `.claude/state/current_plan.md` with full plan
- Updates `.claude/memory/active_context.md` with plan summary

## Handoff to /implement

The saved plan includes:
1. Explicit file paths
2. Complete type definitions
3. Function signatures
4. Step-by-step instructions
5. Pattern references with file locations
6. Test case specifications

This enables `/implement --planned` to skip Stage 2 (planning) and proceed directly to Stage 3 (writing with Sonnet), saving ~$0.30+ in Opus planning costs.
