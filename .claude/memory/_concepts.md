# Concepts Index

> Graph of key concepts discovered across the codebase with cross-references.

## Concept Stats

| Metric | Count |
|--------|-------|
| Total Concepts | 0 |
| With 3+ References | 0 |
| Orphaned (1 ref) | 0 |

---

## How Concepts Work

Concepts are extracted during L2+ analysis and linked using `[[WikiLink]]` syntax.

### Discovery
- During `/deep` analysis, key concepts are identified
- Each concept gets an entry with source documents
- Cross-document relationships emerge naturally

### Navigation
- Click concept to see all documents that reference it
- Use concept clusters to understand domain areas
- Identify central concepts (most references)

---

## Concept Categories

### Architecture
> System design, patterns, structures

(none yet - run `/deep` on architecture files)

### Domain
> Business logic, domain models

(none yet - run `/deep` on domain files)

### Technical
> Implementation patterns, frameworks

(none yet - run `/deep` on source files)

### Infrastructure
> Build, deploy, operations

(none yet - run `/deep` on config files)

---

## Concept Entries

### Template

```markdown
## [[ConceptName]]

**Category**: Architecture / Domain / Technical / Infrastructure
**Importance**: Core / Supporting / Peripheral

### Definition
<1-2 sentences>

### Appears In
| DOC_ID | File | Context |
|--------|------|---------|
| DOC_XXX | path/to/file.ts | <how it's used> |

### Related Concepts
- [[RelatedConcept1]] - relationship
- [[RelatedConcept2]] - relationship

### Notes
<additional context, gotchas, evolution>
```

---

## Alphabetical Index

(empty - concepts added during L2+ analysis)

| Concept | Category | References | Importance |
|---------|----------|------------|------------|
| (none yet) | - | - | - |

---

## Concept Clusters

### Cluster: (name)
> (description of related concepts)

- [[Concept1]]
- [[Concept2]]
- [[Concept3]]

(clusters emerge as concepts are added)

---

## High-Reference Concepts

> Concepts appearing in 5+ documents (central to the codebase)

| Concept | References | Category |
|---------|------------|----------|
| (none yet) | | |

---

## Orphaned Concepts

> Concepts appearing in only 1 document (may need cleanup or expansion)

| Concept | Single Reference |
|---------|------------------|
| (none yet) | |

---

## Update Protocol

### During `/deep` analysis
1. Extract key concepts from document
2. Add [[WikiLinks]] in document entry
3. Create/update concept entry here
4. Update reference counts

### Periodic maintenance
- Review orphaned concepts
- Identify missing concepts from common terms
- Merge duplicate concepts
- Update cluster groupings
