# Standard Tier — Contracts Template

Use this as a guide when creating a project's `CONTRACTS.md`. Every invariant should be testable. If you can't test it, it's a guideline, not an invariant.

---

```markdown
# Contracts

## Boundary Invariants

[Named invariants that enforce architectural boundaries. Each should have a corresponding test.]

- **INV-[NAME]-001**: [What must always be true about this boundary]
  - Enforced by: `tests/[test-file]`
- **INV-[NAME]-002**: [What must always be true]
  - Enforced by: `tests/[test-file]`

### Naming convention
- `INV-LAYER-xxx` for layer boundary rules
- `INV-DATA-xxx` for data integrity rules
- `INV-API-xxx` for API contract rules
- Use a naming convention that fits your domain — consistency matters more than the specific format

## Schema Invariants

[Data structures that have formal definitions. Any code that produces or consumes this data must conform to the schema.]

- [Entity/structure name]: defined in `schemas/[file]`
- [Entity/structure name]: defined in `schemas/[file]`

## Quality Gates

[What must be true before any change ships. These are enforced by the build skill's verify phase.]

- [ ] All existing tests pass
- [ ] New behavior has test coverage (happy path + error path)
- [ ] Schema changes have corresponding validation tests
- [ ] No boundary invariants violated
- [ ] Docs updated if architecture or contracts changed

## Verification

[Commands that prove contracts hold. The build skill runs these during verify phase.]

```bash
# Run all tests
[test command]

# Verify specific invariants (if applicable)
[specific commands]
```

## Adding New Invariants

When you discover a new boundary or rule that should be enforced:
1. Add it to this file with a name (INV-xxx-xxx)
2. Write a test that verifies it
3. Reference the test here
4. Commit contract + test together
```

---

## Standard tier contract expectations

- Named invariants for architectural boundaries (at least: layer separation, data ownership)
- Schema definitions referenced for core data structures
- Quality gates that define "ready to ship"
- Verification commands that can be run mechanically
- Each invariant traceable to a test
