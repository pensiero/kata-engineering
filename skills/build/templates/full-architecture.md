# Full Tier — Architecture Template

Use this as a guide for full-tier projects. Extends the standard tier with governance, change classification, and deeper structural verification. Adapt to the domain.

---

```markdown
---
project_tier: full
---

# Architecture

## System Story

[What is this system in narrative form. Not just what it does — what it IS. Define the core entities and their relationships in plain language.]

### Canonical Entities

- **[Entity 1]**: [What it represents and its role in the system]
- **[Entity 2]**: [What it represents and its role in the system]
- **[Entity 3]**: [What it represents and its role in the system]

No document or module may redefine these semantics.

## Layer Model

[Non-overlapping layers with clear ownership. Every piece of code belongs to exactly one layer. No ambiguity.]

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

- [Layer A] modules must not depend on [Layer B] (transport/session/orchestration logic)
- [Layer C] must not implement independent [canonical operations] — it consumes [Layer B] contracts
- [Add all forbidden dependency directions]

## Data Model

### [Core Entity 1]
[Detailed description of the entity, its fields, their semantics, and valid ranges/values.]

Schema: `schemas/[entity].{ts,json,yaml}`

**Invariant:** `INV-DATA-001`: [canonical constraint, e.g., "canonical N keys in canonical order across state/UI/API"]

### [Core Entity 2]
[Detailed description.]

Schema: `schemas/[entity].{ts,json,yaml}`

## Data Ownership and State

[Where canonical mutable state lives. What is code/docs/fixtures (repository) vs runtime state.]

- Canonical mutable state: `[state location]`
- Repository holds: code, docs, schemas, fixtures, tests

**Invariant:** `INV-STORAGE-001`: canonical mutable state lives only in [defined location].
**Invariant:** `INV-STATE-001`: runtime state is reconstructable from canonical artifacts.

## Authoritative Mutation Path

[If the system has state mutations, define the ONE canonical path. All mutations flow through this path.]

```
[validator] → [governance/decision] → [applier] → [event log]
```

Any direct path outside this service is non-authoritative implementation debt.

## Change Classification

A change is **major** if any of these apply:
1. [Criterion 1, e.g., "data delta exceeds threshold"]
2. [Criterion 2, e.g., "more than N items changed in one batch"]
3. [Criterion 3, e.g., "any governance/policy value changed"]
4. [Criterion 4, e.g., "structural change to high-stakes component"]

Major changes must include:
- Evidence / rationale linking
- Evaluation metadata (who reviews, by when)
- Event log entry

Everything else is **minor** and auto-applies after validation.

## Key Decisions

### [Decision 1]
**Choice:** [what]
**Rationale:** [why, including rejected alternatives]

### [Decision 2]
**Choice:** [what]
**Rationale:** [why]

## Success Metrics

[How do you know the system is healthy?]

1. [Metric 1, e.g., "non-degrading quality score over time"]
2. [Metric 2, e.g., ">=90% of changes are evidence-linked"]
3. [Metric 3, e.g., "evaluation closure within target latency"]

## Repository Structure

[Contract-bound ownership map. Every directory has a clear owner.]

```
project/
  src/
    [layer-1]/     # [Owner/purpose]
    [layer-2]/     # [Owner/purpose]
    [layer-3]/     # [Owner/purpose]
  schemas/         # Data structure definitions
  tests/           # Verification baseline
  docs/            # Additional documentation
  ARCHITECTURE.md  # This file
  CONTRACTS.md     # Invariants and gates
```

## Running

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

## Change Discipline

Every meaningful change updates:
1. Code
2. Relevant tests (including contract tests)
3. Impacted docs (ARCHITECTURE.md, CONTRACTS.md, schemas)

No silent drift. Code and docs ship together.
Major changes require evidence and evaluation closure before commit.
```

---

## Full tier expectations

Everything in standard tier, plus:
- Layer model with explicit non-overlapping ownership
- Canonical entity definitions that no module may redefine
- Authoritative mutation path (if state exists)
- Change classification with major/minor governance
- Success metrics for system health
- Repository structure map with ownership
- Coupling guardrail tests enforcing forbidden dependencies
- Structural integrity tests verifying docs match code
