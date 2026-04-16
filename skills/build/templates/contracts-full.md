# Contracts Template — Full Tier

Scaffold for `CONTRACTS.md` in full-tier projects. Extends the standard contracts with governance, precedence, and a traceability matrix. This is a reference document — optimized for lookup, not narrative reading.

Copy the content inside the code block below and adapt it to the project. Everything outside the code block is guidance for the agent, not part of the output.

---

```markdown
# Contracts

## Authority

Precedence when documents conflict:
1. `ARCHITECTURE.md` (canonical system description)
2. `CONTRACTS.md` (this file — enforceable invariants)
3. Other docs (implementation narratives, guides)

## Boundary Invariants

- **INV-LAYER-001**: [boundary rule]
  - Enforced by: `tests/coupling-guardrails.test.*`
- **INV-LAYER-002**: [boundary rule]
  - Enforced by: `tests/coupling-guardrails.test.*`
- **INV-STRUCT-001**: [structural ownership rule]
  - Enforced by: `tests/structural-integrity.contract.test.*`

## Data Invariants

- **INV-DATA-001**: [canonical data constraint]
  - Enforced by: `tests/schema-validation.test.*`
- **INV-STORAGE-001**: [state location constraint]
  - Enforced by: `tests/structural-integrity.contract.test.*`

## Governance Invariants

- **INV-GOV-001**: [minor update flow rule]
  - Enforced by: `tests/governance-contracts.test.*`
- **INV-GOV-002**: [major update requirement]
  - Enforced by: `tests/governance-contracts.test.*`

## Schema Invariants

| Entity | Schema | Validation Test |
|--------|--------|-----------------|
| [Entity 1] | `schemas/[file]` | `tests/schema-validation.test.*` |
| [Entity 2] | `schemas/[file]` | `tests/schema-validation.test.*` |

## Quality Gates

- [ ] All existing tests pass
- [ ] New behavior has test coverage (happy path + error path)
- [ ] Schema changes have validation tests
- [ ] No boundary invariants violated (coupling guardrails pass)
- [ ] Structural integrity verified (docs match code)
- [ ] If major change: evidence provided, evaluation metadata set
- [ ] Docs updated in same commit

## Verification

```bash
# All tests
[command]

# Coupling guardrails
[command]

# Structural integrity
[command]

# Schema validation
[command]
```

## Change Governance

### Major criteria
A change is major if any apply:
1. [From ARCHITECTURE.md]
2. [From ARCHITECTURE.md]
3. [From ARCHITECTURE.md]

### Major requirements
- Evidence / rationale linked
- Evaluation metadata set (reviewer, deadline)
- Event log entry
- Cannot proceed without evaluation closure

### Minor requirements
- Validator passes
- Evidence-linked event emitted
- Auto-applies after validation

## Traceability

| Invariant | Test | Verifies |
|-----------|------|----------|
| INV-LAYER-001 | `tests/coupling-guardrails.test.*` | Import graph respects boundaries |
| INV-DATA-001 | `tests/schema-validation.test.*` | Data matches schemas |
| INV-GOV-001 | `tests/governance-contracts.test.*` | Minor updates validate correctly |
| INV-GOV-002 | `tests/governance-contracts.test.*` | Major updates require evaluation |
| INV-STRUCT-001 | `tests/structural-integrity.contract.test.*` | Docs match code |

## Adding Invariants

1. Add here with name (`INV-[DOMAIN]-xxx`)
2. Write a test
3. Add to the traceability table
4. If governance rule: add to change governance section
5. Commit contract + test together
```
