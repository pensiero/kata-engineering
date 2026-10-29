---
name: build
description: Implement features, fix bugs, start new projects, or bootstrap project structure. Use for any coding task — writing or modifying code on any project, even small edits.
---

# Build Skill

Use for implementing features, fixing bugs, starting new projects, or bootstrapping project structure.
NOT for: reviewing code (use `review` skill), researching without implementing, or non-coding tasks.

**Central rules:** this skill ships with the Kata Engineering repository. Resolve this skill directory's real path (it is usually symlinked into the agent's global skills directory); the rules live two levels up, at the repository root. Read `rules/coding.md` before writing code and `rules/testing.md` before writing tests. This skill gives the flow; the rules give the how.

---

## Phases

Scale each phase to the change: a one-line fix is Orient, Build, Verify and Close in minutes.

```
BOOTSTRAP → only when starting or restructuring a project
ORIENT    → read project context, understand scope
BUILD     → implement the change
VERIFY    → check contracts, run tests, impact check
CLOSE     → update docs, capture lessons, commit
```

---

## Phase 0 — Bootstrap

**Trigger:** the project has no `ARCHITECTURE.md` (or equivalent architecture doc) at its root, and you are starting a new project, restructuring an existing one, or the human asks for it.

A small change in a repo without architecture docs skips Bootstrap: make the change, and mention at the end that the project could use one. If the project already has architecture docs, skip to Phase 1.

> **Coming from `project-kickoff`?** Its brief is at the top of `PLAN.md` (or in the conversation) — read it before starting Bootstrap. It answers the questions in Step 2, so skip straight to Step 3. Your job here is scaffolding the project structure, not revisiting strategy. The kickoff prompt, if present, is the right input for this phase.

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

Three tiers scale ceremony with complexity. Recommend one based on project intent:

**Light** — scripts, utilities, experiments, weekend projects
- `ARCHITECTURE.md` with project purpose, structure overview, and how to run/test
- Tests covering the any-tier baseline in `rules/testing.md`
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
- Change governance: what makes a change major in this project, and what it requires before it ships
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
- `ARCHITECTURE.md` (from `templates/architecture-light.md`)
- Initial test file

**Standard tier scaffolds:**
- `ARCHITECTURE.md` (from `templates/architecture-standard.md`)
- `CONTRACTS.md` (from `templates/contracts-standard.md`)
- Schema definitions for core data structures
- Test baseline: schema validation, boundary invariants, happy path

**Full tier scaffolds:**
- `ARCHITECTURE.md` (from `templates/architecture-full.md`)
- `CONTRACTS.md` (from `templates/contracts-full.md`)
- Coupling guardrail tests
- Structural integrity tests
- Complete test baseline

**Any tier, optionally:**
- `PLAN.md` (from `templates/plan.md`) — when the project has phased work, sequencing, deferred scope, or meaningful unknowns. Create it if the human asks for planning, or if the project clearly has multiple phases ahead. If the kickoff brief lists unknowns, fold them into the plan's Open Questions section. Not required by default. A project that keeps its work in a `TRACKER.json` (`tracker` skill) uses the tracker for the tracking half.
- `DECISIONS.md` (from `templates/decisions.md`) — when the project will involve multiple sessions or non-obvious design choices. Lightweight: a running log of choices and their reasoning. Not required by default, but worth creating for anything beyond a simple script.

### Writing architecture docs — the narrative principle

Architecture documentation follows one rule: **order by understanding dependency.** Each section should require only the context established by the sections before it. A reader — human or agent — should never encounter something that needs knowledge they haven't been given yet.

When writing or updating architecture docs, ask: "if someone read only up to this point, would they have enough context to understand what comes next?" If not, something is missing or misordered.

This also prevents the append-over-append problem. New information doesn't go at the bottom — it goes where it belongs in the narrative. "Where does this fit in the story?" is the organizing question.

The specific sections vary by project. A library's natural story is different from a data pipeline's, which is different from a web application's. The principle is constant: **build understanding sequentially.** The templates in `skills/build/templates/` demonstrate this principle for typical projects — use them as starting points, but adapt the structure to the project's natural story.

### Tier upgrades

When upgrading from a lower tier (e.g., light → standard):
1. Read the current `ARCHITECTURE.md` and any existing docs
2. Generate the additional artifacts required by the new tier
3. Integrate existing content — don't discard what's there
4. Update the `project_tier` in frontmatter

---

## Phase 1 — Orient

**Goal:** Understand the project and task before writing any code.

### Step 1: Read project docs

**Stable docs — describe what the project is and what must hold true:**
- Read `ARCHITECTURE.md` — understand the system, boundaries, ownership
- Read `CONTRACTS.md` — understand invariants and quality gates

**Living docs — describe current state and recent thinking:**
- If `PLAN.md` or `TRACKER.json` exists — check what's been completed, what's next, and any open questions touching your task. This tells you where the project stands.
- If `DECISIONS.md` exists — scan recent entries. They tell you why earlier choices were made and what was rejected, so you don't re-litigate solved problems.

**Task-specific:**
- If a task contract exists (`{TASK}_CONTRACT.md`), read it — it defines completion.
- Scope your reading: for a small change, you don't need to internalize the entire architecture. Read the sections relevant to the area you're changing.

### Step 2: Understand the task

- What exactly is being asked? What does "done" look like?
- Which modules/layers does this touch?
- Which contracts and invariants are relevant?

### Step 3: Decide the approach

If the approach is clear, proceed to Phase 2. If not, explore — read, spike, try alternatives in code — and converge before you finish (`rules/coding.md`, "Clarify, then explore freely").

### Step 4: Check for tier-specific requirements

| Tier | Before coding, also verify... |
|------|------------------------------|
| Light | Tests exist and pass |
| Standard | Schemas defined for any new data structures. Relevant invariants identified. |
| Full | Change classification determined (major/minor). If major: governance requirements understood. |

---

## Phase 2 — Build

**Goal:** Implement the change. Minimal, focused, tested.

Follow `rules/coding.md` "While Writing Code" (schema-first, tests alongside code, existing patterns, minimal changes, no premature abstraction) and `rules/testing.md`. Note unrelated issues instead of fixing them. Commit each complete chunk of work as you go (`rules/coding.md`, "Commit discipline").

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
- If this is a major change: verify the project's requirements for major changes are met
- Check structural integrity: does `ARCHITECTURE.md` still accurately describe the system?

### Step 3: System-wide impact and simplicity

Run the system-wide impact check and the Simplify checklist from `rules/coding.md` against the diff as a whole. Fix anything that fails before declaring done.

### Step 4: Task contract verification

If a task contract exists (`{TASK}_CONTRACT.md`):
- Walk through every criterion. Each must be satisfied
- Run every verification step listed in the contract
- The task is NOT complete until the contract says it is

---

## Phase 4 — Close

**Goal:** Leave the project better than you found it.

### Step 1: Update documentation

Stable vs. living doc discipline is canonical in `rules/coding.md` ("Two kinds of docs"). Action checklist for Close:

**Stable** (only if design actually changed):
- `ARCHITECTURE.md` — new module/layer, changed data flow, changed boundary/ownership
- `CONTRACTS.md` — invariant added/changed/dropped, gate modified, schema or verification command changed
- Schemas — whenever data shape changed

**Living** (check every Close):
- `PLAN.md` — mark completed, update "Up Next", move deferred, close answered open questions
- `TRACKER.json` (if the project has one) — move items, write outcomes and refs, rebuild its page (`tracker` skill)
- `DECISIONS.md` — add entry for non-obvious choices a future agent might re-litigate

All doc updates ship in the same commit as the code they document.

### Step 2: Capture lessons — the compounding loop

If the human corrected you during this task — rejected an approach, restated a preference, fixed a misunderstanding — the correction must outlive the session. Route it by scope:

- **Project-specific** (a convention, a constraint, a "we don't do X here") → add a one-line entry to the project's instruction file (`AGENTS.md` / `CLAUDE.md`) or `DECISIONS.md`, whichever fits. Ships in the same commit.
- **Universal** (a practice that would apply to any project) → propose a one-line addition to the Kata `rules/` files. Rules are stable docs — never edit them silently. Present the proposed line; the human approves.

The bar: the lesson must generalize. Ask "would this have changed how I approached the task from the start?" If no, skip it. One line per lesson — every rule line is loaded into context on every future session, so it must earn its place.

Most tasks have no corrections. Then this step is a no-op — do not manufacture lessons.

### Step 3: Commit

Commit the finished work — code, tests and docs together — if it isn't committed yet. Don't leave finished work uncommitted.

### Step 4: Summary

Briefly state:
- What was built/changed
- Which contracts/invariants were verified
- Any new invariants or architecture decisions added
- Any observations or follow-up work noted (but not done — no scope creep)
