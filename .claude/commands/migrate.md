# Migration Command

Description: Framework/version migration with progress tracking

You are a Migration Specialist. Task: Migrate "$ARGUMENTS" (e.g., "React 17 to 18", "Express to Fastify").

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Dependency scanning | `haiku` | Package enumeration |
| Verification | `haiku` | Test running |
| Breaking change detection | `sonnet` | Understanding impact |
| Code transformation | `sonnet` | Semantic changes |
| **Major migrations** | `opus` | Cross-system coordination |
| **Migration planning** | `opus` | Risk assessment |

**Escalate to opus** for major framework migrations or when breaking changes span 10+ files.

## Parallel Analysis

Analyze migration impact in parallel:

```
Task(subagent_type=Explore, model=haiku, prompt="Find all imports of <old_api>...")
Task(subagent_type=Explore, model=haiku, prompt="Find deprecated patterns...")
Task(subagent_type=Explore, model=haiku, prompt="Check config files for updates...")
Task(subagent_type=Explore, model=haiku, prompt="Analyze test compatibility...")
```

## State Tracking

Create `.claude/state/migration_state.md`:

```markdown
## Migration: <source> → <target>

### Status
| Field | Value |
|-------|-------|
| Status | in_progress |
| Phase | 2 of 5 |
| Files Updated | 23/45 |
| Tests Passing | ✅ |

### Phases
1. [x] Dependency updates
2. [~] Breaking API changes (in progress)
3. [ ] Config updates
4. [ ] Test updates
5. [ ] Cleanup deprecated code

### Progress
| File | Status | Changes |
|------|--------|---------|
| `package.json` | ✅ | Version bumped |
| `src/App.tsx` | ✅ | New hooks API |
| `src/utils.ts` | 🔄 | In progress |

### Breaking Changes Applied
- [ ] `componentWillMount` → `useEffect`
- [x] `findDOMNode` → `useRef`
- [ ] Concurrent mode updates

### Rollback
Branch: `pre-migration-backup`
Commit: abc123
```

## Migration Phases

| Phase | Tasks | Model |
|-------|-------|-------|
| 1. Dependencies | Update package.json, lock files | haiku |
| 2. Breaking Changes | API updates, pattern changes | sonnet |
| 3. Config | Update configs, build settings | haiku |
| 4. Tests | Fix test compatibility | sonnet |
| 5. Cleanup | Remove deprecated, polish | haiku |

## Process

1. **Backup** - Create rollback branch
2. **Analyze** - Find all affected areas (parallel)
3. **Plan** - Create migration state file
4. **Execute** - Process phase by phase
5. **Verify** - Run tests after each phase
6. **Complete** - Clean up, update docs

## Batch Processing

- Process files in batches of 10
- Run tests after each batch
- Update state after each batch
- Support resume from any phase

## Output

```markdown
## Migration: $ARGUMENTS

### Summary
| Metric | Value |
|--------|-------|
| Files Affected | 45 |
| Breaking Changes | 12 |
| Estimated Effort | Medium |

### Phase 1: Dependencies ✅
- Updated `package.json`
- Regenerated lock file
- Tests: ✅ Passing

### Phase 2: Breaking Changes 🔄
Batch 1/4:
- ✅ `App.tsx` - Updated lifecycle methods
- ✅ `hooks/useAuth.ts` - New API
- ✅ Tests passing

Batch 2/4:
- 🔄 In progress...

### Rollback Available
```bash
git checkout pre-migration-backup
```

### Resume Command
```
/migrate --resume
```
```

## Self-Assessment

After each phase and at completion:

```markdown
### Self-Assessment
| Check | Status |
|-------|--------|
| All breaking changes handled | ✅/❌ |
| Tests pass | ✅/❌ |
| No deprecated APIs remain | ✅/❌ |
| Config files updated | ✅/❌ |
| Documentation updated | ✅/❌ |
| Rollback available | ✅/❌ |

**Migration Coverage**: [Complete/Partial/In Progress]
**Confidence**: [High/Medium/Low]
**Notes**: <areas needing manual testing>
```

## Autonomy

- Do not ask before scanning
- Create backup branch automatically
- Run tests after each batch
- Update state without confirmation
- Only pause on test failures or breaking changes needing decisions
- Support `--resume` to continue from state
- Output self-assessment after each phase

---

## Skills Used

- **codebase-navigator** - Finding all affected files
- **feature-integration** - Understanding migration impacts
- **api-design** - API compatibility analysis
- **database-patterns** - Data migration considerations

## Agents Used

- **explorer** (haiku) - Parallel impact scanning
- **analyzer** (sonnet) - Breaking change analysis
- **test-runner** (haiku) - Running tests after each phase

## State Tracking

Creates/updates `.claude/state/migration_state.md` for resume capability.

## Memory Updates

- Updates `active_context.md` with migration progress
- May update `patterns/architecture.md` with new patterns
- Updates `project_brief.md` with new tech stack versions
