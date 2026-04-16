# Project Review — Agent Prompt

Copy this file and fill in the placeholders for your project.

Use this for periodic health checks on projects already built with Kata Engineering principles. Not for reviewing a single code change (just ask your agent to review it) — this is for stepping back and evaluating the whole project.

---

## Context

You are reviewing **[PROJECT NAME]**, a project built following Kata Engineering principles. It has an `ARCHITECTURE.md`, possibly `CONTRACTS.md` and `PLAN.md`, and a test suite. Your job is to assess whether the project is healthy, the docs are accurate, and nothing has drifted.

## Setup

Before doing anything, read these files in this order:

1. **The framework:**
   - `[KATA_PATH]/rules/coding.md` — coding principles
   - `[KATA_PATH]/rules/testing.md` — testing principles
   - `[KATA_PATH]/skills/review/SKILL.md` — the review skill (your workflow)

2. **The project docs:**
   - Stable docs: `[PROJECT_PATH]/ARCHITECTURE.md`, `[PROJECT_PATH]/CONTRACTS.md` (if it exists)
   - Living docs (all optional): `[PROJECT_PATH]/PLAN.md`, `[PROJECT_PATH]/DECISIONS.md`, `[PROJECT_PATH]/RESEARCH.md`

3. **The project itself:**
   - The directory structure: `find [PROJECT_PATH] -type f | grep -v node_modules | grep -v .git | sort`
   - Key source files — read enough to understand the actual state, not just what the docs say
   - All test files — at least the first 30-50 lines of each

## Your Task

### Phase 1 — Architecture Accuracy

Read `ARCHITECTURE.md`. Then read the actual code.

- Does the architecture doc describe the system as it actually is today?
- Are there modules, patterns, or flows that exist in code but aren't documented?
- Are there documented boundaries that are violated in practice?
- Are there dead zones — code that doesn't belong to any described layer?
- Is **The Story** still accurate? Has the project evolved beyond its original premise?

Produce a drift report: what matches, what doesn't.

### Phase 2 — Contract Health

If `CONTRACTS.md` exists:

- For each invariant: does it still apply? Is there a passing test?
- Are there boundaries in the code that should have invariants but don't?
- Are there invariants claimed but not tested?
- Run all verification commands listed in the contracts

If `CONTRACTS.md` doesn't exist but the tier suggests it should: flag it.

### Phase 3 — Tier Compliance

Read the `project_tier` from `ARCHITECTURE.md` frontmatter. Check against tier requirements:

**Light:**
- [ ] `ARCHITECTURE.md` exists and describes the project clearly
- [ ] Tests exist and pass

**Standard** (everything in light, plus):
- [ ] Layer boundaries, ownership, and forbidden coupling defined
- [ ] `CONTRACTS.md` exists with named invariants and verification commands
- [ ] Core data structures have schema definitions
- [ ] Schema validation, boundary, happy path, and error path tests

**Full** (everything in standard, plus):
- [ ] Coupling guardrail tests verify forbidden dependencies
- [ ] Structural integrity tests verify docs match code
- [ ] Change classification rules defined
- [ ] Governance invariants with tests

Report each as ✅ met / ❌ not met / ⚠️ partially met.

### Phase 4 — Complexity Audit

Walk through the codebase:

- Are files growing too large? Too many files for the complexity?
- How many layers of indirection between a request and its effect?
- Is there one way to do things, or have multiple patterns accumulated?
- Dead code — files, functions, or modules that nothing uses?
- Dependencies that could be inlined or removed?

### Phase 5 — Living Doc Check

Living docs go stale quickly. For each one that exists:

**`PLAN.md`:**
- Is "completed" up to date with what's actually built?
- Does "up next" still make sense given the current state?
- Are there deferred items that should be reconsidered?

**`DECISIONS.md`:**
- Do the recorded decisions still reflect the current code?
- Are there recent design choices (visible in git history) that should have been recorded but weren't?

**`RESEARCH.md`:**
- Are "open questions" still open, or have they been silently resolved?
- Do "key findings" still reflect current understanding?

If a living doc is clearly stale, flag it. If a living doc is absent but obviously needed, suggest creating it.

**Do not edit the docs in this phase.** This is review — if the human wants them refreshed, use the review skill's Refresh mode (or invoke it directly).

### Phase 6 — Report

Structure the full report as:

1. **Architecture accuracy** — match/drift between docs and code
2. **Contract health** — coverage, freshness, gaps
3. **Tier compliance** — checklist results
4. **Complexity assessment** — where is unnecessary complexity accumulating?
5. **Living doc status** — `PLAN.md`, `DECISIONS.md`, `RESEARCH.md`: current, stale, or missing
6. **Recommendations** — prioritized list of actions, each with concrete steps

## Rules

- **Observe, don't hunt** — describe behavior neutrally. Real issues surface from honest observation.
- **Evidence over opinion** — every finding needs a file, a line, a specific piece of code
- **Actionable over vague** — "refactor this" is useless. Describe what to do and where.
- **Don't fix anything** — this is a review, not an implementation session. Produce findings. The human decides what to act on.
- **Simplicity bias** — when in doubt, recommend removing code rather than adding it
- **Proportional depth** — scale effort with the project's complexity and tier
