---
name: review
description: Review code changes, check project health, or verify contract compliance. Use for any review task.
---

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
REFRESH   → update living docs to match current reality (periodic maintenance)
```

Focused, Health, and Tier are **diagnostic** — they produce findings, not edits. Refresh is the only mode that writes to files, and it writes only to living docs (`PLAN.md`, `DECISIONS.md`, `RESEARCH.md`).

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

A well-built system has a natural shape. Every part earns its existence. Nothing is there "just in case" or because it was interesting to build. The question isn't "can I find something to remove?" — it's "has this solution found its natural form?"

For every change, ask:

- **Is this necessary?** Could the problem be solved without this code?
- **Is this the simplest version?** Could it be shorter, flatter, more direct?
- **Does this abstraction earn its keep?** Does it have two real use cases, or is it speculative?
- **Is there a new dependency?** Is the coupling worth it? Could you inline it instead?
- **Would a stranger understand this?** Without explanation, without context from the conversation that produced it?
- **Does the change feel inevitable?** Or does it feel like machinery bolted onto the system?

The default answer to "should we add this?" is no. Complexity is easy to add and hard to remove. A codebase with less code that does the same thing is always better.

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

## Mode 4 — Refresh

**When:** Periodically — when living docs have drifted from current reality, or at the start of a new session after multiple sessions of work have accumulated. Also useful after a Health Check flags stale living docs.

**Scope:** This mode **edits** living docs to match reality. It does **not** edit stable docs and does **not** write code. Stable drift is flagged, not fixed.

### What this mode does and does not do

| | Edits? | Scope |
|---|---|---|
| `PLAN.md` | ✅ | mark completed items, update "Up Next", move deferred items |
| `DECISIONS.md` | ✅ | add missing entries for recent design choices visible in git history |
| `RESEARCH.md` | ✅ | close resolved questions, update findings, prune stale content |
| `ARCHITECTURE.md` | ❌ | flag drift, do not edit |
| `CONTRACTS.md` | ❌ | flag drift, do not edit |
| Code / tests | ❌ | flag issues, do not edit |

If the project has no living docs, Refresh has nothing to do. Exit cleanly. If the project would benefit from one or more of them, suggest creating them directly from the templates in `skills/build/templates/` (`plan.md`, `decisions.md`, `research.md`) — do not route back to Bootstrap, which only runs on projects without `ARCHITECTURE.md`.

### Step 1: Gather reality

Establish what has changed since the living docs were last updated:

- Read recent git log (commits since the last update of each living doc)
- Read the current code structure at the level of modules/layers
- Read any Focused Review or Health Check reports that already exist

Do not read the entire codebase. You're looking for signals of change, not doing a full review.

### Step 2: Refresh `PLAN.md` (if it exists)

- Check off completed items — anything in "Up Next" that is now built, tested, and shipped
- Move completed phases/milestones from "Up Next" to "Completed"
- Update "Up Next" to reflect what's actually next given the current state (not wishful thinking from three sessions ago)
- Move anything deferred to "Deferred" with a one-line reason
- Prune "Completed" if it has grown into archaeology — keep enough history to understand the journey, not every checkmark forever

### Step 3: Refresh `DECISIONS.md` (if it exists)

- Scan recent commits for non-obvious architectural or design choices that were made but never recorded
- For each one, add an entry at the top (newest first): what was chosen, why, what was rejected
- Do not invent rationale — if you can't determine the "why" from context, flag it for the human instead of guessing
- Never rewrite old entries. Superseded decisions get a new entry that references the old one

### Step 4: Refresh `RESEARCH.md` (if it exists)

- Close open questions that have been answered. If the answer matters long-term, promote it to a Key Finding or a `DECISIONS.md` entry
- Update Key Findings with new information
- Prune findings that are no longer relevant
- Add sources for any research done since the last refresh

### Step 5: Flag stable drift

If you noticed during Steps 1–4 that stable docs (`ARCHITECTURE.md`, `CONTRACTS.md`) no longer match the code, **do not edit them**. List the drift at the end of your summary. The human decides whether to fix it directly or run a Health Check.

### Step 6: Report

Briefly state:
- Which living docs were refreshed and what was changed (file-by-file summary)
- What was flagged for the human (stable drift, missing rationale, questions without evidence)
- Suggested follow-ups (e.g. "consider running Health Check on the auth module — `ARCHITECTURE.md` no longer describes its flow")

Commit the living doc updates as a single commit with a message like `chore: refresh living docs`.

### Constraints

- **One file at a time.** Edit `PLAN.md` fully before touching `DECISIONS.md`. This keeps the changes auditable.
- **No speculation.** If you don't have evidence for an edit, don't make it.
- **No new content categories.** Don't invent new sections. Work within the existing template structure.
- **Terse.** Living docs should shrink when possible, not grow indefinitely. If a section can be tightened, tighten it.

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
