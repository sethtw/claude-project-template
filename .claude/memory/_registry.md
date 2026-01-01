# Document Registry

> Central index of all documents with their extraction depth and metadata.

## Registry Stats

| Depth | Count | Percentage |
|-------|-------|------------|
| L0 (Discovery) | 0 | - |
| L1 (Triage) | 0 | - |
| L2 (Summary) | 0 | - |
| L3 (Deep) | 0 | - |
| **Total** | **0** | 100% |

Last scan: Never
Next available ID: DOC_001

---

## Quick Filters

### By Type
- [Source Code](#source-code)
- [Tests](#tests)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Memory Files](#memory-files)

### By Depth
- [L3 (Deep Analysis)](#l3-entries)
- [L2 (Summary)](#l2-entries)
- [L1 (Triage)](#l1-entries)
- [L0 (Discovery)](#l0-entries)

---

## L3 Entries
> Fully analyzed documents with deep understanding

(none yet)

---

## L2 Entries
> Summarized documents with key concepts extracted

(none yet)

---

## L1 Entries
> Triaged documents with brief summaries

(none yet)

---

## L0 Entries
> Discovered documents pending deeper analysis

(none yet)

---

## Source Code

| DOC_ID | Path | Depth | Lines | Last Modified |
|--------|------|-------|-------|---------------|
| (run `/index` to populate) | | | | |

---

## Tests

| DOC_ID | Path | Depth | Lines | Last Modified |
|--------|------|-------|-------|---------------|
| (run `/index` to populate) | | | | |

---

## Configuration

| DOC_ID | Path | Depth | Lines | Last Modified |
|--------|------|-------|-------|---------------|
| (run `/index` to populate) | | | | |

---

## Documentation

| DOC_ID | Path | Depth | Lines | Last Modified |
|--------|------|-------|-------|---------------|
| (run `/index` to populate) | | | | |

---

## Memory Files

| DOC_ID | Path | Depth | Purpose |
|--------|------|-------|---------|
| (memory files indexed separately) | | | |

---

## Update Protocol

### After `/index` scan
1. Add new L0 entries
2. Update line counts for existing
3. Mark deleted files as [REMOVED]
4. Update stats table

### After `/deep` analysis
1. Promote specified files to L2/L3
2. Add detailed entries to appropriate section
3. Update cross-references

### Periodic maintenance
- Archive entries for deleted files
- Demote stale L3→L2→L1 entries
- Consolidate large sections into separate files

---

## ID Allocation Status

| Range | Purpose | Used | Available |
|-------|---------|------|-----------|
| DOC_001-099 | Memory | 0 | 99 |
| DOC_100-4999 | Source | 0 | 4900 |
| DOC_5000-6999 | Tests | 0 | 2000 |
| DOC_7000-7999 | Config | 0 | 1000 |
| DOC_8000-8999 | Docs | 0 | 1000 |
| DOC_9000+ | Other | 0 | unlimited |
