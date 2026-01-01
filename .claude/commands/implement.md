# Staged Implementation

Description: Cost-optimized feature implementation using staged model execution

You are a Development Orchestrator. Task: Implement "$ARGUMENTS" using staged model execution for cost optimization.

## Execution Modes

| Mode | Usage | Stages Run | When to Use |
|------|-------|------------|-------------|
| **Default** | `/implement <feature>` | All 5 stages | Standalone implementation |
| **--planned** | `/implement --planned` | 1, 3, 4, 5 (skip 2) | After `/architect` |
| **--fresh** | `/implement --fresh <feature>` | All 5 stages | Ignore existing plan |

### Mode Detection

```
if $ARGUMENTS contains "--planned":
    → Load plan from .claude/state/current_plan.md
    → Skip Stage 2 (Plan)
    → Proceed to Stage 3 (Write)

elif $ARGUMENTS contains "--fresh":
    → Ignore any existing plan
    → Run all 5 stages

else (default):
    → Check for .claude/state/current_plan.md
    → If exists and < 1 hour old: prompt to use it
    → Otherwise: Run all 5 stages
```

## Cost Optimization Strategy

| Stage | Model | Purpose | Token Profile |
|-------|-------|---------|---------------|
| 1. Discover | `haiku` | Find files, map structure | Low in/out |
| 2. Plan | `opus` | Design implementation | Medium in, low out |
| 3. Write | `sonnet` | Generate code | Medium in, **high out** |
| 4. Verify | `sonnet` | Run tests, basic review | Medium in/out |
| 5. Fix | `opus` | Fix issues (if needed) | Medium in, low out |

### Cost Comparison

| Workflow | Stages | Est. Cost |
|----------|--------|-----------|
| Full `/implement` | 1→2→3→4→5 | ~$1.10 |
| `/architect` + `/implement --planned` | (1→2) + (1→3→4→5) | ~$0.85 |
| All-Opus implementation | N/A | ~$3.50 |

**Using `--planned` saves ~$0.25-0.35** by reusing the `/architect` plan.

---

## Stage 1: Discover (Haiku)

**Always runs** - Quick file discovery.

```
Task(subagent_type=Explore, model=haiku, prompt="Find all files related to <feature area>...")
Task(subagent_type=Explore, model=haiku, prompt="Map existing patterns in <target directory>...")
Task(subagent_type=Explore, model=haiku, prompt="Find test patterns for similar features...")
Task(subagent_type=Explore, model=haiku, prompt="Check dependencies and imports...")
```

**Output**: File list, patterns found, integration points

---

## Stage 2: Plan (Opus)

**Skipped with `--planned`** - Uses existing plan from `/architect`.

### If Running Stage 2:

Create detailed implementation plan with:
- Exact file paths to create/modify
- Function signatures with types
- Step-by-step implementation order
- Expected test cases
- Error handling patterns to use

Save plan to `.claude/state/current_plan.md`.

### If Using `--planned`:

```
Read plan from: .claude/state/current_plan.md

Verify plan exists and contains:
- [ ] Files to create/modify
- [ ] Implementation steps
- [ ] Patterns to follow

If plan invalid or missing:
- ERROR: "No valid plan found. Run /architect first or use /implement without --planned"
```

---

## Stage 3: Write (Sonnet)

Execute the plan step-by-step:

```
Task(subagent_type=general-purpose, model=sonnet, prompt="
Execute this implementation plan step by step.
Follow the exact specifications provided.
Do not deviate from the plan unless there's an error.

PLAN:
<plan from Stage 2 or current_plan.md>

Start with Step 1 and proceed through all steps.
Write all code files specified.
Run tests after implementation.
")
```

### Writing Rules for Sonnet
- Follow plan exactly - do not add unrequested features
- Use specified patterns from existing code
- Write tests as specified
- Commit after each logical unit

---

## Stage 4: Verify (Sonnet)

Run verification checks:

```
Task(subagent_type=general-purpose, model=sonnet, prompt="
Verify the implementation:
1. Run all tests: `npm test`
2. Run type check: `npx tsc --noEmit`
3. Run linter: `npm run lint`
4. Check all files from plan exist
5. Verify integration points wired

Report any failures or issues.
")
```

### Verification Checklist
- [ ] All tests pass
- [ ] No type errors
- [ ] No lint errors
- [ ] All planned files created
- [ ] Integration points connected

---

## Stage 5: Fix (Opus) - Conditional

**Only invoke if Stage 4 found issues.**

```
Task(subagent_type=general-purpose, model=opus, prompt="
Issues were found in the implementation:
<issues from Stage 4>

Original plan:
<plan>

Analyze the issues and fix them. Focus on:
1. Root cause of each failure
2. Minimal fix to resolve
3. Verify fix doesn't break other things
")
```

---

## State Tracking

Create/update `.claude/state/implement_state.md`:

```markdown
## Implementation: $ARGUMENTS

### Status
| Field | Value |
|-------|-------|
| Status | in_progress |
| Mode | planned / fresh / default |
| Stage | 3 of 5 |
| Plan Source | /architect / self |
| Started | <timestamp> |

### Stage Results
| Stage | Status | Output |
|-------|--------|--------|
| 1. Discover | ✅ | Found 12 related files |
| 2. Plan | ⏭️ SKIPPED (--planned) | Using existing plan |
| 3. Write | 🔄 | 4/6 files complete |
| 4. Verify | ⏳ | Pending |
| 5. Fix | ⏳ | Pending |

### Checkpoint
Last file: `src/services/feature.ts`
Last step: Step 3 of 6
```

---

## Output

```markdown
## Implementation Complete: $ARGUMENTS

### Execution Mode
- Mode: `--planned` (used existing /architect plan)
- Plan source: `.claude/state/current_plan.md`

### Cost Summary
| Stage | Model | Est. Tokens | Est. Cost |
|-------|-------|-------------|-----------|
| Discover | haiku | 5K | $0.01 |
| Plan | ⏭️ | SKIPPED | $0.00 |
| Write | sonnet | 40K | $0.60 |
| Verify | sonnet | 10K | $0.15 |
| Fix | opus | 0 | $0.00 |
| **Total** | | 55K | **$0.76** |

### Savings
- vs full /implement: Saved $0.30 (skipped Stage 2)
- vs all-Opus: Saved $2.74 (~78%)

### Files Created
| File | Lines | Tests |
|------|-------|-------|
| src/services/feature.ts | 85 | ✅ |
| src/api/feature.ts | 42 | ✅ |
| tests/feature.test.ts | 120 | N/A |

### Verification
- Tests: ✅ All passing
- Types: ✅ No errors
- Lint: ✅ Clean

### Commit
`feat: implement $ARGUMENTS`
```

---

## Workflow Examples

### Workflow A: Quick Implementation (Standalone)
```
/implement add user preferences API
```
Runs all 5 stages. Good for simple, well-understood features.

### Workflow B: Planned Implementation (Recommended for Complex Features)
```
/architect add OAuth2 authentication
# Review plan, make adjustments if needed
/implement --planned
```
Separates planning (Opus-heavy) from execution (Sonnet-heavy).

### Workflow C: Re-implementation (After Plan Changes)
```
/architect add OAuth2 authentication
# Manually edit .claude/state/current_plan.md
/implement --planned
```
Uses modified plan.

### Workflow D: Fresh Start (Ignore Previous Plan)
```
/implement --fresh add new payment flow
```
Ignores any existing plan, creates new one.

---

## Self-Assessment

```markdown
### Implementation Assessment
| Check | Status |
|-------|--------|
| All planned files created | ✅/❌ |
| All tests passing | ✅/❌ |
| No type/lint errors | ✅/❌ |
| Follows existing patterns | ✅/❌ |
| Integration points wired | ✅/❌ |
| Cost optimization achieved | ✅/❌ |

**Quality**: [High/Medium/Low]
**Cost Efficiency**: [Optimal/Good/Suboptimal]
**Mode Used**: [--planned/--fresh/default]
```

---

## When to Use Each Mode

| Scenario | Recommended Mode |
|----------|------------------|
| Simple feature, clear requirements | `/implement <feature>` |
| Complex feature, want to review plan | `/architect` → `/implement --planned` |
| Requirements changed after planning | `/implement --fresh <feature>` |
| Iterating on previous implementation | `/implement --planned` |
| Cost is primary concern | `/architect` → `/implement --planned` |

---

## Autonomy

- Do not ask between stages
- Update state after each stage
- Only pause if Stage 5 fails twice
- Auto-commit on successful implementation
- With `--planned`: fail fast if plan missing/invalid

---

## Skills Used

- **feature-integration** (opus) - Stage 2 planning (when not --planned)
- **codebase-navigator** (haiku) - Stage 1 discovery
- **tdd-workflow** (sonnet) - Stage 3 test writing
- **performance-analysis** (sonnet) - Stage 4 verification

## Agents Used

- **explorer** (haiku) - Parallel file discovery
- **analyzer** (sonnet) - Code writing and verification
- **test-runner** (haiku) - Test execution

## Memory Updates

- Creates/updates `implement_state.md` for resume
- Reads `current_plan.md` when using --planned
- Updates `active_context.md` with progress
