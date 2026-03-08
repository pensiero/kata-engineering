# Build Skill

Use for implementing features, fixing bugs, starting new projects, or bootstrapping project structure.

NOT for: reviewing code (use `review` skill), researching without implementing, or non-coding tasks.

---

## Phases

Every coding task follows these phases. No phase is optional — but some are fast.

```
BOOTSTRAP → only when project lacks architecture docs
ORIENT    → read project context, understand scope
BUILD     → implement the change
VERIFY    → check contracts, run tests, impact check
CLOSE     → update docs, verify completion
```

---

## Phase 0 — Bootstrap

**Trigger:** The project has no `ARCHITECTURE.md` (or equivalent architecture doc) at its root.

If the project already has architecture docs, skip to Phase 1.

### Step 1: Detect project state

Is this a **greenfield** project (empty or near-empty) or a **brownfield** project (existing code without architecture docs)?

**Greenfield:** proceed to Step 2.

**Brownfield:**
1. Read the codebase — directory structure, key files, dependencies, entry points
2. Draft an `ARCHITECTURE.md` that describes **what actually exists** — don't impose aspirational structure
3. Identify architectural boundaries that are already present (even if informal)
4. Identify architectural debt — places where boundaries are unclear or violated
5. Present the draft to the human for review and refinement
6. Once approved, proceed to Step 3

### Step 2: Understand project intent

Ask (or read from README/brief):
- What is this project? What problem does it solve?
- Who is it for? (personal tool, shared library, production service)
- What's the expected lifespan and complexity?

### Step 3: Select tier

Three tiers scale ceremony with complexity. Present them and recommend based on project intent:

**Light** — scripts, utilities, experiments, weekend projects
- `ARCHITECTURE.md` with project purpose, structure overview, and how to run/test
- Basic test file with at minimum happy-path coverage
- Minimal ceremony, maximum speed

**Standard** — personal projects with persistence, APIs, or multiple modules
- `ARCHITECTURE.md` with system purpose, layer boundaries, ownership, key decisions
- `CONTRACTS.md` with named invariants, quality gates, verification commands
- Schema definitions for core data structures
- Test baseline: schema validation + boundary tests + happy path + error paths

**Full** — production systems, projects with governance/compliance needs, complex domains
- Everything in Standard
- Coupling guardrail tests verifying import boundaries
- Structural integrity tests verifying docs match code
- Change classification (major/minor) with governance rules
- Evaluation gates for major changes
- Detailed invariant registry with cross-references to tests

The tier is recorded in `ARCHITECTURE.md` frontmatter:

```yaml
---
project_tier: standard  # light | standard | full
---
```

### Step 4: Scaffold

Use the templates in `skills/build/templates/` as guides (not copy-paste). Adapt to the specific project.

**Light tier scaffolds:**
- `ARCHITECTURE.md` (from `templates/light.md`)
- Initial test file

**Standard tier scaffolds:**
- `ARCHITECTURE.md` (from `templates/standard.md`)
- `CONTRACTS.md` (from `templates/standard-contracts.md`)
- Schema definitions for core data structures
- Test baseline: schema validation, boundary invariants, happy path

**Full tier scaffolds:**
- `ARCHITECTURE.md` (from `templates/full.md`)
- `CONTRACTS.md` (from `templates/full-contracts.md`)
- Coupling guardrail tests
- Structural integrity tests
- Complete test baseline

**Any tier, optionally:**
- `PLAN.md` (from `templates/plan.md`) — when the project has phased work, sequencing, or deferred scope. Create it if the human asks for planning, or if the project clearly has multiple phases ahead. Not required by default.

### Writing architecture docs — the narrative principle

Architecture documentation follows one rule: **order by understanding dependency.** Each section should require only the context established by the sections before it. A reader — human or agent — should never encounter something that needs knowledge they haven't been given yet.

When writing or updating architecture docs, ask: "if someone read only up to this point, would they have enough context to understand what comes next?" If not, something is missing or misordered.

This also prevents the append-over-append problem. New information doesn't go at the bottom — it goes where it belongs in the narrative. "Where does this fit in the story?" is the organizing question.

The specific sections vary by project. A library's natural story is different from a data pipeline's, which is different from a web application's. The principle is constant: **build understanding sequentially.** The templates in `skills/build/templates/` demonstrate this principle for typical projects — use them as starting points, but adapt the structure to the project's natural story.

**Get human approval** before proceeding. The bootstrap sets the foundation — it should be right.

### Tier upgrades

When upgrading from a lower tier (e.g., light → standard):
1. Read the current `ARCHITECTURE.md` and any existing docs
2. Generate the additional artifacts required by the new tier
3. Integrate existing content — don't discard what's there
4. Update the `project_tier` in frontmatter
5. Get human approval

---

## Phase 1 — Orient

**Goal:** Understand the project and task before writing any code.

### Step 1: Read project docs

- Read `ARCHITECTURE.md` — understand the system, boundaries, ownership
- Read `CONTRACTS.md` — understand invariants and quality gates
- If `PLAN.md` exists — check what's been completed and what's next. This tells you where the project stands
- If a task contract exists (`{TASK}_CONTRACT.md`), read it — it defines completion
- Scope your reading: for a small change, you don't need to internalize the entire architecture. Read the sections relevant to the area you're changing.

### Step 2: Understand the task

- What exactly is being asked? What does "done" look like?
- Which modules/layers does this touch?
- Which contracts and invariants are relevant?

### Step 3: Decide the approach

**If the approach is clear:** proceed to Phase 2.

**If the approach is unclear:**
- Research options FIRST — do not start implementing while still exploring
- If research requires significant context (reading docs, evaluating libraries, comparing approaches), do it as a separate step
- Settle on an approach, state it clearly, then proceed to Phase 2 with clean focus
- Do not carry exploration context (rejected alternatives, comparison notes) into the implementation

### Step 4: Check for tier-specific requirements

| Tier | Before coding, also verify... |
|------|------------------------------|
| Light | Tests exist and pass |
| Standard | Schemas defined for any new data structures. Relevant invariants identified. |
| Full | Change classification determined (major/minor). If major: governance requirements understood. |

---

## Phase 2 — Build

**Goal:** Implement the change. Minimal, focused, tested.

### Core discipline

1. **Schema-first** — if the change involves data structures, define types/schemas before writing logic
2. **Tests alongside code** — write tests as you implement, not after. See `rules/testing.md`
3. **Follow existing patterns** — read similar code in the project first. Match conventions exactly
4. **Minimal changes** — do the least that solves the problem. Touch the fewest files
5. **No premature abstraction** — don't build for hypothetical future needs

### While building

- If something could be simpler, make it simpler
- If you're creating a new file, ask: does this concern already have a home?
- If you're adding a dependency, ask: is this worth the coupling?
- If you find an unrelated issue, note it — don't fix it now. Scope creep kills quality

### Incremental commits

Commit when a logical unit is complete and tests pass:
- Meaningful commit message describing the complete change
- Stage only related files
- Don't batch unrelated changes

---

## Phase 3 — Verify

**Goal:** Prove the change is correct, safe, and simple.

### Step 1: Run tests

- Run the full test suite. All tests must pass
- Run any new tests you wrote. They must pass
- If tests fail, fix the code — not the tests (unless the test is genuinely wrong; explain why)

### Step 2: Check contracts

**Light tier:** verify tests pass. That's sufficient.

**Standard tier:**
- For each invariant in `CONTRACTS.md` that your changes could affect: verify it holds
- If you added new boundaries or data structures: add corresponding invariants
- Run verification commands listed in `CONTRACTS.md`

**Full tier:**
- Everything in Standard
- Run coupling guardrail tests
- If this is a major change: verify governance requirements are met (evidence, evaluation metadata)
- Check structural integrity: does `ARCHITECTURE.md` still accurately describe the system?

### Step 3: System-wide impact

Ask yourself (see `rules/coding.md` for the full checklist):
- What fires when this runs? (hooks, callbacks, middleware — two levels out)
- Can failure leave broken state? (partial writes, orphaned records)
- What other interfaces need the same change? (parity check)

Skip for leaf-node changes with no callbacks, state, or parallel interfaces.

### Step 4: Simplicity check

Step back from the details. Look at the change as a whole.

A good change has a natural shape — it feels like the obvious way to solve the problem. If it feels forced, convoluted, or "clever," something is wrong. The goal is not to make something that works — it's to find the solution that couldn't reasonably be simpler.

Concretely:
- For each new file: is it necessary? Could this live in an existing file?
- For each new abstraction: does it have two concrete use cases, or is it premature?
- For each new dependency: is the coupling worth it?
- Read your diff as if you're seeing it for the first time: would a stranger understand it without explanation?
- Read your diff as a whole: does this feel like the natural solution, or does it feel like machinery bolted on?

### Step 5: Task contract verification

If a task contract exists (`{TASK}_CONTRACT.md`):
- Walk through every criterion. Each must be satisfied
- Run every verification step listed in the contract
- The task is NOT complete until the contract says it is

---

## Phase 4 — Close

**Goal:** Leave the project better than you found it.

### Step 1: Update documentation

- If architecture changed → update `ARCHITECTURE.md`
- If invariants were added/changed/removed → update `CONTRACTS.md`
- If schemas changed → update schema definitions
- If `PLAN.md` exists → check off completed items, update "Up Next" if scope changed
- All doc updates in the same commit as the code change

### Step 2: Final commit

- Ensure all changes (code + tests + docs) are committed
- Commit message describes the complete change
- No uncommitted work left behind

### Step 3: Summary

Briefly state:
- What was built/changed
- Which contracts/invariants were verified
- Any new invariants or architecture decisions added
- Any observations or follow-up work noted (but not done — no scope creep)

---

## After Context Compaction

If your context gets compacted mid-task:

1. Re-read the task scope (what are you trying to do?)
2. Re-read the files most relevant to your current work
3. Re-read any task contract if one exists
4. Do NOT rely on memory — verify by re-reading

This is critical. Compaction loses nuance. Re-reading prevents drift.

---

## Anti-Patterns To Catch

These are common agent failure modes. If you notice yourself doing any of these, stop:

- **Helper/utility files that serve one caller** — inline the logic instead
- **Abstract base classes with one implementation** — delete the base class
- **Configuration where constants would do** — hardcode it until you need flexibility
- **Error handling for impossible cases** — handle what can actually happen
- **Logging/monitoring before the feature works** — make it work first
- **Over-normalized data structures** — denormalize unless you have a concrete reason
- **Building "for the future"** — build for now. Refactor when the future arrives
- **Multiple patterns for the same concern** — pick one, migrate the others
