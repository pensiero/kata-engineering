# Full Tier — Architecture Template

Use this as a guide for full-tier projects. Extends the standard tier with governance, change classification, structural verification, and deeper precision. The narrative principle is critical here — a complex system's docs must build understanding sequentially, or they become impenetrable.

**Principle:** order by understanding dependency. Each section requires only the context from sections before it.

---

```markdown
---
project_tier: full
---

# [Project Name]

## The Story

[The premise, written as prose. Not what the system does — what it IS. What problem exists in the world, and what role this system plays. Write this so a reader who's never seen the project understands its purpose and feels the integrity worth protecting.]

[This is the most important section. Every architectural decision, every boundary, every invariant should make sense as a consequence of what's written here. If a proposed change contradicts this story, it's the wrong change — or the story needs to evolve.]

### Canonical Entities

[The characters. Define them precisely — what each one is, what it means, what it does not mean. These definitions are authoritative. No module or document may redefine them inconsistently.]

- **[Entity 1]**: [definition and role in the system]
- **[Entity 2]**: [definition and role in the system]
- **[Entity 3]**: [definition and role in the system]

## The Structure

[Now that the reader knows what the system is and what exists inside it, show how it's organized. Non-overlapping layers with clear ownership. Every piece of code belongs to exactly one layer.]

### [Layer 1] (`src/[path]`)
**Owns:**
- [Responsibility 1]
- [Responsibility 2]

### [Layer 2] (`src/[path]`)
**Owns:**
- [Responsibility 1]
- [Responsibility 2]

### [Layer 3] (`src/[path]`)
**Owns:**
- [Responsibility 1]
- [Responsibility 2]

### Forbidden Coupling

[The walls. What must never depend on what. These are the most load-bearing constraints in the system.]

- [Layer A] must not depend on [Layer B] — [why this matters]
- [Layer C] must not implement independent [canonical operations] — [why]

## The Data

[What state exists, where it lives, what shape it takes. Reference schemas.]

### [Core Entity 1]
[Fields, semantics, valid ranges. What each field means, not just what type it is.]

Schema: `schemas/[entity].{ts,json,yaml}`
**Invariant:** `INV-DATA-001`: [canonical constraint]

### Data Ownership

- Canonical mutable state lives in: [location]
- Repository holds: code, docs, schemas, fixtures, tests

**Invariant:** `INV-STORAGE-001`: canonical mutable state lives only in [defined location].

## The Flow

[How things move through the system. Now that the reader knows the layers, the data, and the boundaries, show the primary paths.]

### Authoritative Path

[If the system has state mutations, define the ONE canonical path.]

```
[step 1] → [step 2] → [step 3] → [step 4]
```

Any path outside this is non-authoritative implementation debt.

### [Other significant flows]

[Describe other primary paths through the system. Each should feel like a natural consequence of the structure described above.]

## The Governance

[How changes are classified and controlled.]

### Change Classification

A change is **major** if any apply:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

**Major changes require:**
- Evidence and rationale
- Evaluation metadata (reviewer, deadline)
- Event log entry
- Evaluation closure before proceeding

Everything else is **minor** — auto-applies after validation.

## The Decisions

[Why the system has this particular shape. Decisions make sense only after the reader understands the structure they shaped.]

### [Decision 1]
**Choice:** [what]
**Why:** [rationale, including rejected alternatives]

### [Decision 2]
**Choice:** [what]
**Why:** [rationale]

## The Measures

[How you know the system is healthy.]

1. [Metric 1 and target]
2. [Metric 2 and target]
3. [Metric 3 and target]

## Working With This Project

### Repository Map

```
project/
  src/
    [layer-1]/     # [owner/purpose]
    [layer-2]/     # [owner/purpose]
    [layer-3]/     # [owner/purpose]
  schemas/         # Data structure definitions
  tests/           # Verification baseline
  ARCHITECTURE.md  # This file
  CONTRACTS.md     # Invariants and gates
```

### Commands

```bash
# Run / start
[command]

# Test
[command]

# Verify contracts
[command]

# Verify structural integrity
[command]
```

### Change Discipline

Every meaningful change updates:
1. Code
2. Relevant tests (including contract tests)
3. Impacted docs (this file, CONTRACTS.md, schemas)

No silent drift. Code and docs ship together.
Major changes require evidence and evaluation closure before commit.
```

---

## Notes for the agent

- The sections above follow the narrative principle: Story → Structure → Data → Flow → Governance → Decisions → Measures → Practice. Each depends on what came before.
- For your specific project, the natural story may differ. A system without governance needs no governance section. A system without a mutation path needs no authoritative path section. Adapt.
- The story section is the most important. It's not decoration — it's the frame that makes every other section coherent. Write it with care. It should read like the opening of a good explanation, not like a spec.
- Full-tier docs are longer. Fight the urge to let them become a dump. Every section should earn its place. If a section exists only because the template had it, delete it.
