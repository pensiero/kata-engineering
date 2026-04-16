# New Project — Agent Prompt

Copy this file and fill in the placeholders for your project.

---

## Context

You are starting a new project from scratch using the Kata Engineering framework. The framework gives you coding principles, testing practices, a structured build workflow, and architecture templates that scale with project complexity.

**Read the framework before writing any code.** Understanding the principles first means you build correctly from the start — not retrofitting structure onto a mess later.

## Setup

Before doing anything, read these files in this order:

1. **The framework:**
   - `[KATA_PATH]/rules/coding.md` — your coding principles
   - `[KATA_PATH]/rules/testing.md` — your testing principles
   - `[KATA_PATH]/skills/build/SKILL.md` — the build skill (your workflow)

2. **The templates** (read the tier that fits — plus the living-doc templates if relevant):
   - Architecture (pick the tier): `[KATA_PATH]/skills/build/templates/architecture-light.md`, `architecture-standard.md`, or `architecture-full.md`
   - Contracts (standard or full): `[KATA_PATH]/skills/build/templates/contracts-standard.md`, or `contracts-full.md`
   - Living docs (optional, any tier): `[KATA_PATH]/skills/build/templates/plan.md`, `decisions.md`, `research.md`

## The Project

**What:** [Describe what the project is — not features, but what it IS. What problem exists and what role this system plays.]

**Who:** [Who is this for? Personal tool, shared library, production service, experiment?]

**Complexity:** [Expected lifespan and scale. Weekend script? Long-running personal project? Production system?]

## Your Task

### Phase 1 — Bootstrap

Follow the build skill's Phase 0 (Bootstrap):

1. Based on the project description above, recommend a tier (light / standard / full) and explain why
2. Scaffold the architecture docs using the appropriate template:
   - Light: `ARCHITECTURE.md`
   - Standard: `ARCHITECTURE.md` + `CONTRACTS.md` + schema definitions
   - Full: everything in standard + coupling guardrails + structural integrity tests + governance
3. Write **The Story** section first — clear, direct prose. Two to four sentences. Define what the system IS, not what it does. Every word should be load-bearing.
4. Fill in the remaining sections based on the project description — but only sections that earn their place. Don't include a section just because the template has it.

Present the scaffolded docs to the human before proceeding.

### Phase 2 — Initial Structure

With the architecture docs approved:

1. Create the directory structure described in the architecture doc
2. Define schemas for core data structures (standard/full)
3. Write initial tests:
   - Light: at minimum happy-path coverage
   - Standard: schema validation + boundary tests + happy path + error paths
   - Full: everything in standard + coupling guardrail tests
4. Verify all tests pass

### Phase 3 — Build

Now start implementing. Follow the build skill's phases:

- **Orient** — re-read the architecture docs you just created. Understand the scope of what you're building first.
- **Build** — schema-first, tests alongside code, follow existing patterns, minimal changes
- **Verify** — run tests, check contracts, simplicity check
- **Close** — update docs if architecture evolved during implementation

Work in small increments. Each increment should leave the project in a working state.

### Phase 4 — Create living docs (if applicable)

Living docs capture state that changes over the life of the project. Create the ones that make sense:

- `PLAN.md` (from `skills/build/templates/plan.md`) — if the project has multiple phases or significant deferred scope.
- `DECISIONS.md` (from `skills/build/templates/decisions.md`) — if the project involves non-obvious design choices, or will span multiple sessions.
- `RESEARCH.md` (from `skills/build/templates/research.md`) — if the project has meaningful unknowns, or a Research Brief exists from kickoff.

None are required. Create only the ones that will pay for themselves. Each one is a living doc — keep it current on every Close.

## Rules

- **Architecture first, code second** — the docs are the blueprint, not an afterthought
- **Ask before guessing** — if the project description is ambiguous, ask. Don't assume.
- **Start minimal** — you can always add complexity. Removing it is harder.
- **Tests alongside code** — not after. Not later. Alongside.
- **Follow the framework's rules** — read `rules/coding.md` and `rules/testing.md` and actually follow them
- **Don't gold-plate** — build what's needed now, not what might be needed someday
