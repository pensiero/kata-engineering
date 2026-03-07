# Standard Tier — Contracts Template

Contracts is a reference document, not a narrative. Optimized for lookup: authority first, then invariants by domain, then gates, then verification. A reader looks things up here — they don't read it cover to cover.

---

```markdown
# Contracts

## Boundary Invariants

[Named invariants enforcing architectural boundaries. Each must be testable. If you can't write a test for it, it's a guideline, not an invariant.]

- **INV-[DOMAIN]-001**: [What must always be true]
  - Enforced by: `tests/[test-file]`
- **INV-[DOMAIN]-002**: [What must always be true]
  - Enforced by: `tests/[test-file]`

## Schema Invariants

[Data structures with formal definitions. Code that produces or consumes this data must conform.]

| Entity | Schema | Validation Test |
|--------|--------|-----------------|
| [Entity 1] | `schemas/[file]` | `tests/schema-validation.test.*` |
| [Entity 2] | `schemas/[file]` | `tests/schema-validation.test.*` |

## Quality Gates

[What must be true before any change ships.]

- [ ] All existing tests pass
- [ ] New behavior has test coverage (happy path + error path)
- [ ] Schema changes have validation tests
- [ ] No boundary invariants violated
- [ ] Docs updated if architecture or contracts changed

## Verification

```bash
# Run all tests
[command]

# Verify specific invariants (if applicable)
[command]
```

## Adding Invariants

When a new boundary or rule should be enforced:
1. Add it here with a name (`INV-[DOMAIN]-xxx`)
2. Write a test that verifies it
3. Reference the test in this file
4. Commit contract + test together
```
