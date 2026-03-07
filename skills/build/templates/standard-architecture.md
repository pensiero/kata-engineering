# Standard Tier — Architecture Template

Use this as a guide when bootstrapping a standard-tier project. Every section below should exist in the project's `ARCHITECTURE.md`, adapted to the specific domain.

---

```markdown
---
project_tier: standard
---

# Architecture

## System Purpose

[What is this system? What problem does it solve? Who is it for?]
[Keep this to 2-4 sentences. If you need more, the system might be too complex for its goal.]

## Boundaries

### Layer Model

[Define the layers/modules and what each owns. Every piece of code should belong to exactly one layer.]

| Layer | Owns | Location |
|-------|------|----------|
| [Layer 1] | [What it's responsible for] | `src/[path]` |
| [Layer 2] | [What it's responsible for] | `src/[path]` |

### Forbidden Dependencies

[What CANNOT depend on what. This is the most important section — it defines the boundaries that keep the system clean.]

- [Layer A] must not import from [Layer B]
- [Module X] must not directly access [resource Y]

### Data Ownership

[Where does canonical state live? What module owns writes to what data?]

## Data Model

[Core entities, their relationships, and their schemas. Reference schema files if they exist.]

### [Entity 1]
- [Key fields and their meaning]
- Schema: `schemas/[entity].ts` (or equivalent)

### [Entity 2]
- [Key fields and their meaning]
- Schema: `schemas/[entity].ts`

## Key Decisions

[Record architectural decisions with rationale. This is how new contributors understand WHY the system is shaped this way.]

### [Decision 1]
**Choice:** [what was chosen]
**Rationale:** [why — including what alternatives were considered and rejected]

### [Decision 2]
**Choice:** [what was chosen]
**Rationale:** [why]

## Running

```bash
# How to run
[command]

# How to test
[command]

# How to verify contracts
[command, or "see CONTRACTS.md"]
```

## Change Discipline

Every meaningful change updates:
1. Code
2. Relevant tests
3. Impacted docs (this file, CONTRACTS.md, schemas)

Code and docs ship together. No silent drift.
```

---

## Standard tier expectations

- Architecture doc describes the real system (layers, boundaries, data model, decisions)
- Contracts doc defines named invariants and quality gates
- Core data structures have schema definitions
- Test baseline: schema validation, boundary invariants, happy path, error paths
- Docs co-evolve with code
