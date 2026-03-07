# Review Skill

Use for reviewing code changes, checking project health, or verifying contract compliance.

NOT for: implementing changes (use `build` skill), bootstrapping projects, or research tasks.

---

## Modes

Select based on what's needed:

```
FOCUSED   → review specific changes (after a coding session, before merge)
HEALTH    → broader project health check (periodic, or when something feels off)
TIER      → verify project meets its declared tier requirements
```

---

## Mode 1 — Focused Review

**When:** After implementing changes. Before merging. When you want a second opinion on recent work.

### Step 1: Observe

Walk through the changes neutrally. Describe what you see — don't hunt for problems.

**Frame it as:** "What does this code do?" — not "What's wrong with this code?"

This matters. If you look for bugs, you'll manufacture them (sycophancy). If you observe behavior, real issues surface naturally.

For each changed file:
- What is the intent of this change?
- How does it interact with the rest of the system?
- What state does it read or write?

### Step 2: Check contracts

Read the project's `CONTRACTS.md` (or equivalent). For each invariant relevant to the changed area:
- Does the invariant still hold?
- If a new boundary was created, is there an invariant for it?
- Run verification commands if available

### Step 3: Simplify

For every change, ask:

- **Is this necessary?** Could the problem be solved without this code?
- **Is this the simplest version?** Could it be shorter, flatter, more direct?
- **Does this abstraction earn its keep?** Does it have two real use cases, or is it speculative?
- **Is there a new dependency?** Is the coupling worth it? Could you inline it instead?
- **Would a stranger understand this?** Without explanation, without context from the conversation that produced it?

Be ruthless here. Complexity is easy to add and hard to remove. The default answer to "should we add this?" is no.

### Step 4: Report

Structure findings by severity:

**🔴 Must fix** — breaks contracts, violates boundaries, introduces bugs, loses data
**🟡 Should fix** — unnecessary complexity, missing tests, unclear code, minor architectural violations
**🔵 Consider** — style improvements, potential simplifications, documentation gaps

For each finding:
- **What:** describe the issue with evidence (file, line, specific code)
- **Why:** explain the consequence — not "this is bad" but "this means X can happen"
- **How:** suggest a concrete fix, not a vague direction

If there are no findings: say so. "No issues found" is a valid review outcome. Don't manufacture findings to justify the review.

---

## Mode 2 — Health Check

**When:** Periodic project review. When complexity feels like it's creeping. When a new person would struggle to understand the codebase.

### Step 1: Architecture accuracy

Read `ARCHITECTURE.md`. Then read the actual code structure.

- Does the architecture doc describe the system as it actually is?
- Are there modules or patterns that exist in code but aren't documented?
- Are there documented boundaries that are violated in practice?
- Are there dead zones — code that doesn't belong to any described layer?

### Step 2: Contract health

Read `CONTRACTS.md`. For each invariant:

- Does the invariant still apply? (requirements may have changed)
- Is there a passing test for it?
- Are there boundaries in the code that SHOULD have invariants but don't?

### Step 3: Complexity audit

Walk through the codebase module by module:

- **File count and size** — are files growing too large? Are there too many files for the complexity?
- **Abstraction count** — how many layers of indirection between a request and its effect? Each layer should earn its existence
- **Pattern consistency** — is there one way to do things, or have multiple patterns accumulated?
- **Dead code** — files, functions, or modules that nothing uses
- **Dependency health** — unused dependencies, outdated dependencies, dependencies that could be inlined

### Step 4: Stagnation check

Look at recent changes (git log, conversation context):

- Is the same approach being tried repeatedly without success?
- Are workarounds accumulating instead of fixing root causes?
- Is the architecture being stretched beyond what it was designed for?
- Should the project tier be upgraded (or downgraded)?

### Step 5: Report

Structure as:

1. **Architecture accuracy** — match/drift between docs and code
2. **Contract health** — coverage, freshness, gaps
3. **Complexity assessment** — where is unnecessary complexity accumulating?
4. **Stagnation signals** — patterns that suggest the project needs a different approach
5. **Recommendations** — prioritized actions, each with concrete steps

---

## Mode 3 — Tier Compliance

**When:** After a tier upgrade. Periodically for standard/full projects. When preparing for a handoff.

### Check against tier requirements

**Light tier:**
- [ ] `ARCHITECTURE.md` exists with project purpose, structure, and run commands
- [ ] Tests exist and pass
- [ ] At minimum: happy-path test coverage

**Standard tier** (everything in light, plus):
- [ ] `ARCHITECTURE.md` has layer boundaries, ownership, forbidden dependencies, data model, key decisions
- [ ] `CONTRACTS.md` exists with named invariants, quality gates, verification commands
- [ ] Core data structures have schema definitions
- [ ] Schema validation tests exist
- [ ] Boundary/coupling tests exist
- [ ] Happy path + error path test coverage
- [ ] Docs co-evolve with code (check recent commits: did code changes include doc updates?)

**Full tier** (everything in standard, plus):
- [ ] Layer model has explicit non-overlapping ownership
- [ ] Canonical entity definitions exist
- [ ] Change classification rules defined (major/minor)
- [ ] Governance invariants with tests
- [ ] Coupling guardrail tests verify forbidden dependencies
- [ ] Structural integrity tests verify docs match code
- [ ] Test coverage map traces invariants to tests
- [ ] Major changes have evidence and evaluation metadata

### Report

List each requirement as ✅ met / ❌ not met / ⚠️ partially met.

For each gap: describe what's missing and what to do about it.

---

## Review Principles

### Neutral observation over bug hunting
Describe behavior. Real issues surface from honest observation. Manufactured issues surface from looking for trouble.

### Evidence over opinion
Every finding needs a file, a line, a specific piece of code. "This feels wrong" is not a finding.

### Actionable over vague
"Refactor this" is useless. "Extract the validation logic from `handler.ts:42-67` into `validators/input.ts` because it's reused in `api.ts:31`" is actionable.

### Simplicity bias
When in doubt, recommend removing code rather than adding it. The codebase that doesn't exist has zero bugs.

### Proportional depth
A small utility doesn't need the same review depth as a core system module. Scale your effort with the risk.
