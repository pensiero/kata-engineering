# Engram Rework — Agent Prompt

## Context

You are reworking the Engram project to align with a new engineering framework. The project has working code, passing tests, and solid architectural thinking — but the documentation and project structure need to be reworked to follow new principles.

**Do not rewrite working code for the sake of rewriting.** The goal is to bring the project's documentation, contracts, and structure in line with the framework — not to rebuild from scratch.

## Setup

Before doing anything, read these files in this order:

1. **The framework:**
   - `/Users/oscar/Projects/agents-framework/rules/coding.md` — your coding principles
   - `/Users/oscar/Projects/agents-framework/rules/testing.md` — your testing principles
   - `/Users/oscar/Projects/agents-framework/skills/build/SKILL.md` — the build skill (your workflow)
   - `/Users/oscar/Projects/agents-framework/skills/review/SKILL.md` — the review skill

2. **The architecture templates** (read all, you'll need them for reference):
   - `/Users/oscar/Projects/agents-framework/skills/build/templates/full-architecture.md`
   - `/Users/oscar/Projects/agents-framework/skills/build/templates/full-contracts.md`
   - `/Users/oscar/Projects/agents-framework/skills/build/templates/plan.md`

3. **The existing Engram project** — read thoroughly:
   - `/Users/oscar/Projects/engram/ARCHITECTURE.md`
   - `/Users/oscar/Projects/engram/ARCHITECTURE_CONTRACT.md`
   - `/Users/oscar/Projects/engram/IMPLEMENTATION.md`
   - `/Users/oscar/Projects/engram/IMPLEMENTATION_CONTRACT.md`
   - All files under `/Users/oscar/Projects/engram/schemas/`
   - All files under `/Users/oscar/Projects/engram/tests/` (read at least the first 30-50 lines of each to understand what they verify)
   - The directory structure: `find /Users/oscar/Projects/engram -type f | grep -v node_modules | grep -v .git | sort`
   - Key source files in `engine/`, `intake/`, `console/` — read enough to understand the actual architecture, not just what the docs say

## Your Task

You are performing a **brownfield bootstrap** — the project exists, works, and has architectural thinking, but its documentation needs to be restructured to follow the framework's principles.

### Phase 1 — Understand What Actually Exists

Read the entire codebase. Don't trust the existing docs blindly — verify that the code matches what the docs describe. Note any drift between docs and reality.

Produce a brief assessment:
- What is the actual architecture? (Does it match what ARCHITECTURE.md says?)
- What invariants are actually enforced by tests? (Do the contract docs match the test suite?)
- What is dead, stale, or aspirational in the current docs?
- What is the natural tier for this project? (Given its complexity, governance model, and test suite — is this light, standard, or full?)

Present this assessment to the human before proceeding.

### Phase 2 — Rewrite Architecture Documentation

Rewrite `ARCHITECTURE.md` following the narrative principle from the framework:

**Order by understanding dependency.** Each section should require only the context from sections before it. A reader — human or agent — should never encounter something that requires knowledge they haven't been given yet.

Use the full-tier template's canonical section names. For Engram, the natural reading order likely maps closely to the template, but preserve reality over template purity — if a section doesn't earn its place, cut it.

Specific guidance:
- **The Story** — clear, direct prose. Two to four sentences — not bullet points, not a literary essay. Define what Engram IS, not what it does. Every word should be load-bearing.
- **Canonical Entities** — the characters (Engram, Construct, Overseer). What each one is, what it means, what it does not mean.
- **The Structure** — layers, ownership, forbidden coupling. Now that the reader knows what exists.
- **The Data** — what state exists, where it lives, what shape it takes. Reference schemas.
- **The Flow** — mutation paths, intake pipeline, state lifecycle. Now that boundaries are understood.
- **The Governance** — change classification, major/minor criteria, evaluation gates.
- **The Decisions** — why this shape, key decisions and their rationale, including rejected alternatives. Now that the reader understands the structure the decisions shaped.
- **The Measures** — how you know the system is healthy.
- **Working With This Project** — repo map, commands, verification, change discipline.

**Important constraints:**
- Preserve all architectural DECISIONS from the existing docs — they were hard-won. Restructure their presentation, don't lose their content.
- If the existing docs describe something aspirational (not yet built), move it to PLAN.md — don't mix aspirational and actual in ARCHITECTURE.md.
- If the existing docs describe something that the code contradicts, flag it. The human decides which is right.

### Phase 3 — Rewrite Contracts

Replace `ARCHITECTURE_CONTRACT.md` with `CONTRACTS.md` following the full-tier contracts template.

- Every invariant that has a test: include it with a reference to the test
- Every invariant claimed but NOT tested: flag it. The human decides whether to add a test or remove the claim
- Map the traceability: invariant → test → what it verifies
- Include governance rules (major/minor change classification) from the existing docs
- Include quality gates and verification commands

### Phase 4 — Create PLAN.md

Convert the existing `IMPLEMENTATION.md` into a `PLAN.md`:
- What's been completed (move from IMPLEMENTATION.md's "stable and enforced" + phase descriptions)
- What's up next (from IMPLEMENTATION.md's "open work queue" + deferred items)
- What's deferred and why
- Prioritization principles

### Phase 5 — Assess Code Alignment

With the new docs in place, review the actual code against the framework's coding rules:

- Are there unnecessary abstractions? Files that don't earn their existence?
- Are there boundary violations the tests don't catch?
- Are there patterns that contradict each other?
- Is there dead code?

**Do not fix anything in this phase.** Produce a findings list. The human decides what to act on.

### Phase 6 — Clean Up Redundant Files

Propose which old doc files can be removed:
- `ARCHITECTURE_CONTRACT.md` → replaced by `CONTRACTS.md`
- `IMPLEMENTATION.md` → replaced by `PLAN.md`
- `IMPLEMENTATION_CONTRACT.md` → absorbed into `CONTRACTS.md`
- Any other files that are now redundant

**Do not delete anything.** List what you'd remove and why. The human decides.

## Rules

- **Ask before acting** on anything destructive or ambiguous
- **Present each phase's output** before moving to the next
- **Preserve hard-won decisions** — restructure, don't reinvent
- **Flag drift** between docs and code — don't silently resolve it
- **Follow the framework's rules** — read `rules/coding.md` and `rules/testing.md` and actually follow them
- **Don't gold-plate** — the goal is alignment with the framework, not perfection
