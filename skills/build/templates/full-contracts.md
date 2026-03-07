# Full Tier — Contracts Template

Extends the standard contracts with governance rules, coupling enforcement, and structural verification.

---

```markdown
# Contracts

## Authority and Precedence

1. `ARCHITECTURE.md` (canonical system description)
2. `CONTRACTS.md` (this file — enforceable invariants)
3. Implementation/narrative docs

When documents conflict, higher-precedence sources win.

## Boundary Invariants

[Named invariants enforcing architectural boundaries. Each has a test.]

- **INV-LAYER-001**: [Layer A] modules must not import from [Layer B]
  - Enforced by: `tests/coupling-guardrails.test.*`
- **INV-LAYER-002**: [Presentation layer] must not implement independent canonical [operations]
  - Enforced by: `tests/coupling-guardrails.test.*`
- **INV-STRUCT-001**: no ambiguous ownership of [concern A] vs [concern B] vs [concern C]
  - Enforced by: `tests/structural-integrity.contract.test.*`

## Data Invariants

- **INV-DATA-001**: [canonical data constraint, e.g., "N keys in canonical order across state/UI/API"]
  - Enforced by: `tests/schema-validation.test.*`
- **INV-STORAGE-001**: canonical mutable state lives only in [defined location]
  - Enforced by: `tests/structural-integrity.contract.test.*`
- **INV-STATE-001**: runtime state is reconstructable from canonical artifacts
  - Enforced by: [test or manual verification procedure]

## Governance Invariants

[Rules about how changes flow through the system.]

- **INV-GOV-001**: minor updates auto-apply only after validator success and evidence-linked event emission
  - Enforced by: `tests/governance-contracts.test.*`
- **INV-GOV-002**: major updates set evaluation metadata before commit
  - Enforced by: `tests/governance-contracts.test.*`
- **INV-MAJOR-001**: every major update emits evaluation requirement metadata
  - Enforced by: `tests/governance-contracts.test.*`

## Schema Invariants

[Every canonical data structure has a schema. Code that produces/consumes it must conform.]

| Entity | Schema Location | Validation Test |
|--------|----------------|-----------------|
| [Entity 1] | `schemas/[file]` | `tests/schema-validation.test.*` |
| [Entity 2] | `schemas/[file]` | `tests/schema-validation.test.*` |

## Quality Gates

- [ ] All existing tests pass
- [ ] New behavior has test coverage (happy path + error path)
- [ ] Schema changes have validation tests
- [ ] No boundary invariants violated (run coupling guardrails)
- [ ] Structural integrity verified (docs match code)
- [ ] If major change: evidence provided, evaluation metadata set
- [ ] Docs updated (ARCHITECTURE.md, CONTRACTS.md, schemas) in same commit

## Verification Commands

```bash
# Run all tests (including contract tests)
[test command]

# Run coupling guardrail tests specifically
[command, e.g., "npm test -- --grep coupling"]

# Run structural integrity tests
[command]

# Run schema validation
[command]
```

## Change Governance

### Major change criteria
A change is major if any apply:
1. [Criterion from ARCHITECTURE.md]
2. [Criterion from ARCHITECTURE.md]
3. [Criterion from ARCHITECTURE.md]

### Major change requirements
- `evaluation_required = true`
- `evaluation_due_by = [timestamp]`
- Event log entry with rationale and evidence
- Cannot proceed without evaluation closure

### Minor change requirements
- Validator passes
- Evidence-linked event emitted
- Auto-applies after validation

## Test Coverage Map

[Which tests verify which invariants. This is the traceability matrix.]

| Invariant | Test File | What It Verifies |
|-----------|-----------|-----------------|
| INV-LAYER-001 | `tests/coupling-guardrails.test.*` | Import graph respects layer boundaries |
| INV-DATA-001 | `tests/schema-validation.test.*` | Data structures match schemas |
| INV-GOV-001 | `tests/governance-contracts.test.*` | Minor updates flow through validator |
| INV-GOV-002 | `tests/governance-contracts.test.*` | Major updates require evaluation |
| INV-STRUCT-001 | `tests/structural-integrity.contract.test.*` | Architecture doc matches code |

## Adding New Invariants

1. Add to this file with name (`INV-[DOMAIN]-xxx`)
2. Write a test that verifies it
3. Add to the test coverage map
4. If it's a governance rule, add to change governance section
5. Commit contract + test together
```

---

## Full tier contract expectations

Everything in standard tier, plus:
- Authority and precedence declaration
- Governance invariants with change classification rules
- Test coverage map (invariant ↔ test traceability)
- Major/minor change governance with evaluation requirements
- Structural integrity verification
