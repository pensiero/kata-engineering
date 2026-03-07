# Testing Rules

Read this before writing tests. These complement `rules/coding.md`.

---

## Test Philosophy

Tests verify **contracts and behavior**, not implementation details. A test should answer: "does this system uphold its promises?" — not "does this function call that function in this order?"

Tests are **completion criteria**. A task is not done until:
- All existing tests pass
- New tests cover the new behavior
- For standard/full tier projects: relevant invariants have test coverage

---

## What To Test

### Always (any tier)
- **Happy path** — the core functionality works as intended
- **Error paths** — failures are handled, not swallowed; error messages are useful
- **Input validation** — invalid/malformed inputs produce clear errors, not crashes

### Standard tier and above
- **Schema validation** — data structures match their defined schemas
- **Boundary invariants** — modules don't cross architectural boundaries (coupling tests)
- **Named invariants** — each invariant in `CONTRACTS.md` has a corresponding test

### Full tier
- **Structural integrity** — architecture doc matches actual code structure
- **Coupling guardrails** — import graph respects declared boundaries
- **Change governance** — major changes trigger required gates
- **Cross-layer integration** — at least one test per boundary that exercises the real dependency chain

---

## How To Test

### Test real behavior, not mocks
- Unit tests with mocks prove logic in isolation — that's necessary but not sufficient
- For any code that crosses a boundary (calls another module, writes to storage, triggers a hook), write at least one test that uses real dependencies
- If every dependency is mocked, the test proves nothing about integration

### Test contracts, not implementation
- Test what the function promises (its contract), not how it does it internally
- If refactoring breaks your test but doesn't change behavior, the test was too coupled
- Good test: "given this input, expect this output." Bad test: "expect function A to call function B with argument C"

### Test failure modes
- What happens when the database is unavailable?
- What happens when the input is malformed?
- What happens when a downstream service returns an error?
- Tests for these don't need to be exhaustive — but the critical paths should be covered

### Make tests readable
- A new person should understand what's being verified by reading the test name and body
- Test names describe the scenario and expected outcome: `"major mutation requires evidence"`, not `"test case 7"`
- Arrange-Act-Assert structure (or equivalent) — clearly separate setup, action, and verification

---

## Test Integrity

### Never edit tests to make them pass
- If a test fails, the code is probably wrong — not the test
- If the test IS genuinely wrong (testing stale behavior, wrong assumptions), explain WHY before changing it
- "Made the test match the new behavior" is not an explanation — "the test assumed X but requirement changed to Y because Z" is

### Tests are not optional
- "I'll add tests later" means tests won't be added
- Write the test alongside the code, or write it first
- If you truly can't test something (rare), document why and what manual verification is needed

### Keep tests fast
- Slow tests get skipped. Fast tests get run constantly.
- Mock expensive external calls (network, heavy computation) but keep internal integration real
- If the test suite takes more than 30 seconds for a small project, something is wrong

---

## Test Maintenance

### Tests evolve with contracts
- When a contract changes, update the test in the same commit
- When a new invariant is added to `CONTRACTS.md`, add a corresponding test
- Dead tests (testing removed features) should be removed, not left to rot

### Coverage is a signal, not a goal
- 100% coverage with shallow tests is worse than 70% coverage with meaningful tests
- Cover the critical paths and contracts — that's where bugs hurt most
- If a test doesn't verify a contract or meaningful behavior, question whether it's needed
