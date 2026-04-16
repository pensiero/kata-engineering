# Brownfield Rework — Agent Prompt

Copy this file and fill in the placeholders for your project.

---

## Context

You are reworking **[PROJECT NAME]** to align with the Kata Engineering framework. The project has working code and solid thinking — but the documentation and project structure need to be restructured to follow new principles.

**Do not rewrite working code for the sake of rewriting.** The goal is to bring the project's documentation, contracts, and structure in line with the framework — not to rebuild from scratch.

## Setup

Before doing anything, read these files in this order:

1. **The framework:**
   - `[KATA_PATH]/rules/coding.md` — your coding principles
   - `[KATA_PATH]/rules/testing.md` — your testing principles
   - `[KATA_PATH]/skills/build/SKILL.md` — the build skill (your workflow)
   - `[KATA_PATH]/skills/review/SKILL.md` — the review skill

2. **The templates** (read the tier that fits — plus the living-doc templates if relevant):
   - Architecture (pick the tier): `[KATA_PATH]/skills/build/templates/architecture-light.md`, `architecture-standard.md`, or `architecture-full.md`
   - Contracts (standard or full): `[KATA_PATH]/skills/build/templates/contracts-standard.md`, or `contracts-full.md`
   - Living docs (optional, any tier): `[KATA_PATH]/skills/build/templates/plan.md`, `decisions.md`, `research.md`

3. **The existing project** — read thoroughly:
   - Any existing architecture or design docs
   - Any existing contract, implementation, or roadmap docs
   - All schema definitions
   - All test files (at least the first 30-50 lines of each to understand what they verify)
   - The directory structure: `find [PROJECT_PATH] -type f | grep -v node_modules | grep -v .git | sort`
   - Key source files — read enough to understand the actual architecture, not just what the docs say

## Your Task

You are performing a **brownfield bootstrap** — the project exists, works, and has architectural thinking, but its documentation needs to be restructured to follow the framework's principles.

### Phase 1 — Understand What Actually Exists

Read the entire codebase. Don't trust the existing docs blindly — verify that the code matches what the docs describe. Note any drift between docs and reality.

Produce a brief assessment:
- What is the actual architecture? (Does it match what the docs say?)
- What invariants are actually enforced by tests? (Do the docs match the test suite?)
- What is dead, stale, or aspirational in the current docs?
- What is the natural tier for this project? (Given its complexity, governance model, and test suite — is this light, standard, or full?)

Present this assessment to the human before proceeding.

### Phase 2 — Rewrite Architecture Documentation

Rewrite `ARCHITECTURE.md` following the narrative principle from the framework:

**Order by understanding dependency.** Each section should require only the context from sections before it. A reader — human or agent — should never encounter something that requires knowledge they haven't been given yet.

Use the template's canonical section names for the chosen tier. The natural reading order depends on the project — preserve reality over template purity. If a section doesn't earn its place, cut it.

Specific guidance:
- **The Story** — clear, direct prose. Two to four sentences — not bullet points, not a literary essay. Define what the project IS, not what it does. Every word should be load-bearing.
- **Canonical Entities** (standard/full) — the core concepts. What each one is, what it means, what it does not mean.
- **The Structure** — layers, ownership, forbidden coupling. Now that the reader knows what exists.
- **The Data** (standard/full) — what state exists, where it lives, what shape it takes. Reference schemas.
- **The Flow** — how things move through the system. Now that boundaries are understood.
- **The Governance** (full only) — change classification, major/minor criteria, evaluation gates.
- **The Decisions** — why this shape, key decisions and their rationale, including rejected alternatives.
- **The Measures** (full only) — how you know the system is healthy.
- **Working With This Project** — repo map, commands, verification, change discipline.

**Important constraints:**
- Preserve all architectural DECISIONS from the existing docs — they were hard-won. Restructure their presentation, don't lose their content.
- If the existing docs describe something aspirational (not yet built), move it to PLAN.md — don't mix aspirational and actual in ARCHITECTURE.md.
- If the existing docs describe something that the code contradicts, flag it. The human decides which is right.

### Phase 3 — Rewrite Contracts

If the project warrants standard or full tier, create `CONTRACTS.md` following the appropriate contracts template.

- Every invariant that has a test: include it with a reference to the test
- Every invariant claimed but NOT tested: flag it. The human decides whether to add a test or remove the claim
- Map the traceability: invariant → test → what it verifies
- Include governance rules if applicable (full tier)
- Include quality gates and verification commands

### Phase 4 — Create living docs (if applicable)

Living docs capture state that changes over the life of the project. Create the ones that make sense:

- `PLAN.md` (from `skills/build/templates/plan.md`) — if the project has phased work, sequencing, or deferred scope.
- `DECISIONS.md` (from `skills/build/templates/decisions.md`) — if the project has hard-won design choices worth preserving as a log (separate from their presence in `ARCHITECTURE.md`'s Decisions section). Useful when non-obvious rationale is scattered across old docs.
- `RESEARCH.md` (from `skills/build/templates/research.md`) — if the project has ongoing investigation or unresolved questions.

None are required. Create only the ones that will pay for themselves.

### Phase 5 — Assess Code Alignment

With the new docs in place, review the actual code against the framework's coding rules:

- Are there unnecessary abstractions? Files that don't earn their existence?
- Are there boundary violations the tests don't catch?
- Are there patterns that contradict each other?
- Is there dead code?

**Do not fix anything in this phase.** Produce a findings list. The human decides what to act on.

### Phase 6 — Clean Up Redundant Files

Propose which old doc files can be removed — anything now superseded by the new ARCHITECTURE.md, CONTRACTS.md, or PLAN.md.

**Do not delete anything.** List what you'd remove and why. The human decides.

## Rules

- **Ask before acting** on anything destructive or ambiguous
- **Present each phase's output** before moving to the next
- **Preserve hard-won decisions** — restructure, don't reinvent
- **Flag drift** between docs and code — don't silently resolve it
- **Follow the framework's rules** — read `rules/coding.md` and `rules/testing.md` and actually follow them
- **Don't gold-plate** — the goal is alignment with the framework, not perfection
