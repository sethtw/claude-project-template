# /index - Codebase Indexing

> Scan the codebase and populate the L0 document registry.

## Purpose

Discover all files in the codebase and create L0 (discovery) entries in the document registry. This enables the progressive depth system for context management.

## Usage

```
/index                    # Index entire codebase
/index src/               # Index specific directory
/index --update           # Update existing entries only
/index --prune            # Index + remove orphaned concepts
```

## Process

### Step 1: Scan Files (haiku - parallel)

Launch parallel explorer agents to scan different areas:

```
Task(subagent_type=explorer, model=haiku, prompt="Scan src/ for all files, return: path, type, language, line count")
Task(subagent_type=explorer, model=haiku, prompt="Scan tests/ for all test files")
Task(subagent_type=explorer, model=haiku, prompt="Scan config files in root")
Task(subagent_type=explorer, model=haiku, prompt="Scan .claude/ for memory and command files")
```

### Step 2: Allocate Document IDs

Assign DOC_XXX IDs based on reserved ranges:
- DOC_001-099: Memory files
- DOC_100-4999: Source code
- DOC_5000-6999: Tests
- DOC_7000-7999: Config
- DOC_8000-8999: Docs
- DOC_9000+: Other

### Step 3: Update Registry

For each file, create L0 entry:

```markdown
| DOC_ID | Path | Type | Language | Lines | Last Modified |
|--------|------|------|----------|-------|---------------|
| DOC_100 | src/index.ts | code | typescript | 45 | 2024-01-15 |
```

### Step 4: Update Index Stats

Update `.claude/memory/_index.md` with new counts:

```markdown
| Metric | Count |
|--------|-------|
| Total Documents | 150 |
| L0 (Discovery) | 150 |
| L1 (Triage) | 0 |
| L2+ (Analyzed) | 0 |
```

### Step 5: Concept Maintenance (if --prune flag)

When running `/index --prune`, also maintain the concept graph:

1. **Identify Orphaned Concepts**: Find concepts in `_concepts.md` that reference deleted DOC_XXX entries
2. **Update Concept References**: For concepts with stale references, either:
   - Update to point to new DOC_XXX if file was renamed
   - Remove concept if all referenced files are deleted
3. **Merge Duplicate Concepts**: If same concept has multiple entries, consolidate
4. **Update Concept Stats**: Update `_index.md` with current concept count

```markdown
### Concept Maintenance
| Action | Count |
|--------|-------|
| Orphaned concepts removed | 3 |
| References updated | 5 |
| Duplicates merged | 1 |
| Total concepts after cleanup | 42 |
```

## Output Format

```markdown
## Index Complete

### Scan Summary
| Area | Files | Lines |
|------|-------|-------|
| src/ | 45 | 3,200 |
| tests/ | 22 | 1,100 |
| config | 8 | 250 |
| docs | 12 | 800 |
| **Total** | **87** | **5,350** |

### Registry Updated
- New entries: 87
- Updated entries: 0
- Next available ID: DOC_188

### Recommendations
- Run `/deep src/index.ts` to analyze entry point
- Run `/deep src/services/` for business logic analysis
```

## Autonomy

- Scan files without confirmation
- Create registry entries automatically
- Update index stats automatically
- Only pause if conflicts detected

## Model Selection

| Phase | Model | Rationale |
|-------|-------|-----------|
| File scanning | haiku | Fast enumeration |
| ID allocation | haiku | Simple logic |
| Registry update | haiku | Structural update |

## Skills Used

- `codebase-navigator` - Efficient file discovery

## Agents Used

- `explorer` - Parallel file scanning

## Memory Updates

- Updates `_registry.md` with new entries
- Updates `_index.md` with stats
- Updates `active_context.md` with scan results
