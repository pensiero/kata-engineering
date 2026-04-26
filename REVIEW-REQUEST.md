# Review Request: Evolving Kata Engineering into an Init + Maintain System

> **⚠️ Historical document.** This was the handoff brief used to gather review feedback *before* the evolution described here was implemented. The repository has since been updated based on that review, and paths referenced below (e.g. `meta-prompts/project-kickoff.md`, `skills/build/templates/light.md`) no longer exist. See `README.md` for the current state. This file is retained for historical reference only; do not use it to evaluate the current repo.

---

This document is a handoff prompt for another LLM. Its purpose is to review, critique, and improve a proposed evolution of the `kata-engineering` project.

The goal is **not** to blindly implement what is written here. The goal is to deeply review:
- how the current framework works
- what problems it currently solves well
- what gaps were identified
- what changes are being considered
- whether those changes are actually the right ones
- how to reshape the plan if needed before implementation

Please read this document carefully and treat it as a high-context review brief.

---

## What Kata Engineering Is

`kata-engineering` is a methodology/framework project for AI-assisted software engineering.

It currently contains:
- coding rules
- testing rules
- build workflow guidance
- review workflow guidance
- architecture and contracts templates by project tier
- example prompts for greenfield project creation and project review
- a project-kickoff meta-prompt that turns a rough idea into a structured starting point

The repo structure relevant to this discussion includes:

- `meta-prompts/project-kickoff.md`
- `examples/greenfield-project-prompt.md`
- `examples/review-prompt.md`
- `rules/coding.md`
- `rules/testing.md`
- `skills/build/SKILL.md`
- `skills/review/SKILL.md`
- `skills/build/templates/light.md`
- `skills/build/templates/standard.md`
- `skills/build/templates/standard-contracts.md`
- `skills/build/templates/full.md`
- `skills/build/templates/full-contracts.md`
- `skills/build/templates/plan.md`

---

## Current Understanding of the Existing Framework

### 1. Philosophy layer

These files act like constitutional rules:

- `rules/coding.md`
- `rules/testing.md`

They establish:
- simplicity bias
- anti-premature abstraction discipline
- schema-first thinking
- tests as completion criteria
- documentation co-evolves with code
- verification discipline
- anti-stagnation behavior

These are considered strong and likely should remain mostly intact.

### 2. Workflow layer

These files define how work happens:

- `skills/build/SKILL.md`
- `skills/review/SKILL.md`

`build` currently covers:
- Bootstrap
- Orient
- Build
- Verify
- Close

`review` currently covers:
- Focused review
- Health check
- Tier compliance

These are also considered strong, but may need better scope separation and expansion of the overall system model.

### 3. Scaffolding / bootstrapping layer

These files help initialize and use the methodology:

- `meta-prompts/project-kickoff.md`
- `examples/greenfield-project-prompt.md`
- `examples/review-prompt.md`
- architecture/contracts templates

This layer is strong on project setup and thought structuring.

---

## Why This Review Exists

The framework appears strong at:
1. initializing projects
2. bootstrapping architecture and discipline
3. guiding implementation
4. auditing projects for drift or health

However, it appears weaker at a different but equally important problem:

> How do projects stay understandable, well-documented, and current across many sessions of human + agent collaboration?

The working hypothesis is that Kata Engineering currently handles:
- initialization well
- implementation discipline well
- review reasonably well

But it does **not yet fully handle maintenance of living project artifacts**.

That missing maintenance layer is the main focus of the proposed evolution.

---

## Origin of the Discussion

This proposal emerged from a broader discussion about AI-assisted project workflows.

The initial idea was a project-start workflow based on artifacts such as:
- prompt refinement
- planning
- research
- checklist generation

That idea evolved into a stronger artifact model centered not on prompts alone, but on durable project artifacts.

The artifact model discussed includes:
- Project Brief
- Research Brief
- Execution Plan
- Quality Gates
- Refined Kickoff Prompt
- optionally: Decision Log
- optionally: Steering / Principles

A key conclusion from the discussion:

> Prompts are ephemeral. Artifacts are memory.

Another key conclusion:

> A healthy AI-assisted project needs two operating loops: initialization and maintenance.

This led to examining existing projects and frameworks, including:
- the Engram project, to map existing docs to artifact roles
- the `kata-engineering` project, to understand whether it could be evolved instead of creating a new system from scratch

The answer was: **evolve Kata Engineering rather than replace it.**

---

## Related Research and External Inspiration

### 1. Claude Code / Magic Docs inspiration

One important influence is the idea of **Magic Docs**, reportedly observed in Claude Code internal behavior and later discussed in public analyses after the source leak.

The rough behavior described:
- markdown files with a special header such as `# MAGIC DOC: ...` are recognized as tracked docs
- when such a doc is read, it becomes eligible for later refresh
- when the system is idle, a background agent updates the file based on recent work/context
- the updater is restricted to that specific file only
- the update aims to keep the doc terse, current, architecture-focused, and high-signal
- it is not supposed to turn the doc into a changelog

This mechanism is considered interesting and worth exploring, especially for **state docs**, not for every doc indiscriminately.

### 2. Karpathy gist / persistent wiki research model

Another major influence is the knowledge-base pattern described in Karpathy’s gist about using LLMs to maintain persistent personal or research wikis.

Key ideas from that model:
- raw sources are stored immutably
- an LLM-maintained wiki is built and incrementally updated from those sources
- the wiki is structured, linked, and persistent
- the LLM performs maintenance, cross-linking, and synthesis
- index files and logs help navigation
- answers to questions can be filed back into the wiki as durable artifacts
- periodic linting/health checks keep the knowledge base coherent

This matters because any future research artifact support in Kata Engineering should likely support **persistent, compounding research state**, not merely a one-off research brief.

---

## Key Conceptual Shift Proposed

A major conceptual shift proposed during the discussion is the explicit separation of **law docs** and **state docs**.

### Law docs
These are normative, slow-changing, authoritative docs.
They describe what must be true.

Examples:
- `ARCHITECTURE.md`
- `CONTRACTS.md`
- `SECURITY.md`
- coding rules
- testing rules
- stable subsystem contracts

Characteristics:
- authoritative
- changed intentionally
- often validated by tests or explicit review
- should not be casually self-mutated by maintenance agents

### State docs
These are descriptive, faster-changing docs.
They describe what is true right now.

Examples:
- `PLAN.md`
- `RESEARCH.md`
- `DECISIONS.md`
- `NEXT.md` / backlog docs
- synthesis docs
- current status docs

Characteristics:
- can become stale quickly
- should be refreshed regularly
- are the natural target for doc-maintenance workflows
- can be updated by constrained agents if done carefully

### Mixed docs
Some docs sit between the two:
- `README.md`
- `DECISIONS.md`

These require care but the law/state distinction is still considered useful.

This separation is seen as one of the highest-leverage clarifications Kata Engineering could adopt.

---

## Evaluation of the Existing Kata Engineering Files

### `meta-prompts/project-kickoff.md`

Observed role:
- strategy/initiation layer
- turns rough ideas into structured starting artifacts

What it currently does:
- asks clarifying questions if needed
- produces:
  - Project Summary
  - Critical Critique
  - Key Questions & Assumptions
  - Project Brief
  - Research Brief
  - Project Shape
  - Execution Plan
  - Recommended First 3 Actions
  - Quality Gates
  - Refined Kickoff Prompt

Assessment:
- strong for project shaping
- strong on critique and ambiguity reduction
- likely valuable as a pre-architecture initiation step

Concern identified:
- possible overlap with `build` skill Phase 0 (Bootstrap)

Current resolution:
- do **not** merge them, but separate their responsibilities more clearly:
  - `project-kickoff` = strategy / pre-architecture framing
  - `build` bootstrap = repository/project scaffolding based on clarified intent

### `examples/greenfield-project-prompt.md`

Observed role:
- operational bridge from concept into project scaffolding
- tells an agent to read the framework, pick a tier, scaffold docs, then build

Assessment:
- good at practical project startup
- architecture-first discipline is strong
- likely remains useful

Concern identified:
- currently more aligned to initialization and build than to long-term maintenance

### `examples/review-prompt.md`

Observed role:
- periodic project health review prompt
- evaluates drift, contract health, tier compliance, complexity, plan status

Assessment:
- strong diagnostic/review artifact
- valuable as a health-check tool

Concern identified:
- review detects drift, but does not itself define a doc-refresh or maintenance mechanism

### `rules/coding.md`

Observed role:
- stable law-level project engineering philosophy

Assessment:
- strong and likely should remain mostly unchanged
- good place to possibly clarify when law docs vs state docs should be updated

### `rules/testing.md`

Observed role:
- stable law-level testing philosophy

Assessment:
- strong and likely should remain mostly unchanged
- could eventually connect better to artifact categories

### `skills/build/SKILL.md`

Observed role:
- implementation operating system
- bootstrap/orient/build/verify/close

Assessment:
- strong and central to the framework
- probably the correct place for bootstrapping project artifacts and architecture docs

Potential evolution:
- clarify how it consumes outputs from `project-kickoff`
- explicitly recognize law docs vs state docs
- possibly scaffold more state docs for multi-session projects

### `skills/review/SKILL.md`

Observed role:
- diagnostic/audit operating system
- focused review, health check, tier compliance

Assessment:
- should remain review-oriented, not maintenance-oriented

Important conclusion from discussion:
- if a separate maintenance workflow is added, it must **not** overlap heavily with `review`
- `review` should judge and diagnose
- maintenance should refresh state artifacts

### `skills/build/templates/*`

Assessment overall:
- the architecture and contracts templates are strong
- `plan.md` is useful but likely too narrow as the only clear state-doc template
- likely missing templates for `DECISIONS.md` and research-oriented state artifacts

---

## Major Gaps Identified

The following gaps were proposed as the key areas for improvement.

### 1. No explicit maintenance operating system

Current framework has:
- strategy/initiation (`project-kickoff`)
- bootstrapping/build (`build`)
- review (`review`)

It does not yet appear to have a clear equivalent for:
- distilling recent work into project state
- refreshing living docs
- keeping state docs current over time

### 2. No first-class state-doc taxonomy

The framework clearly models architecture and contracts.
It does not yet strongly model the broader family of state docs.

Potential state docs discussed:
- `PLAN.md`
- `RESEARCH.md`
- `DECISIONS.md`
- `NEXT.md` / backlog-like doc
- subsystem-level state docs

### 3. No tracked-doc / Magic Doc style maintenance mechanism

There is currently no explicit notion of:
- tracked docs
- docs eligible for background refresh
- file-scoped doc-updater behavior
- “keep this doc current but not verbose” conventions

### 4. Research support is underdeveloped

Research is currently present as a conceptual artifact via the kickoff prompt, but not as a robust persistent wiki / compounding knowledge system.

### 5. Potential responsibility overlap between kickoff and bootstrap

The newly added `project-kickoff` prompt may overlap with `build` Bootstrap if responsibilities are not clearly separated.

Current thinking:
- this is a real issue
- but it can be resolved through a cleaner pipeline rather than deleting one of them

---

## Candidate Evolution Path (Not Yet Implemented)

Nothing below has been implemented yet. These are candidate changes to review critically.

### Candidate change A: clarify the operating pipeline

Potential clean workflow:

1. **Kickoff**
   - interrogate rough idea
   - clarify scope and uncertainty
   - produce initial artifacts

2. **Build/Bootstrap**
   - scaffold actual project docs and structure
   - choose tier
   - generate architecture/contracts files
   - begin implementation

3. **Maintain** (possibly new)
   - refresh state docs only
   - distill recent work into current project memory
   - keep tracked docs current

4. **Review**
   - audit health, drift, complexity, compliance
   - produce findings and recommendations

Important: `maintain` and `review` must have clearly separated scopes.

### Candidate change B: add explicit law/state taxonomy to the framework

This would likely affect:
- docs
- prompts
- build skill guidance
- templates

It may become a core concept of the framework.

### Candidate change C: add `DECISIONS.md` as a lightweight artifact

Potential goal:
- preserve major design intent without heavy ADR overhead

Requirement from discussion:
- keep it simple, do not overcomplicate it

### Candidate change D: improve research support

This should likely be shaped by the Karpathy persistent-wiki model, not just “do some research and summarize it once”.

Potential features to support:
- raw immutable sources
- LLM-maintained compiled wiki
- index and log
- synthesis and open questions
- periodic lint/health checks
- filing useful outputs back into the knowledge base

### Candidate change E: adopt Claude-style `MAGIC DOC` conventions

Potential principles:
- use the exact `# MAGIC DOC:` style header or something intentionally aligned with it
- only certain docs should be marked this way
- likely state docs, not foundational law docs
- updater should be constrained to one file
- updates should be terse, high-signal, current, not changelog-like

### Candidate change F: refine kickoff vs bootstrap separation

Potential boundary:
- kickoff = strategic framing, before scaffolding
- bootstrap = converting approved framing into concrete project structure

---

## Important Constraints and Opinions from the Discussion

### On `maintain` vs `review`
A separate maintenance workflow should not become “review but with edits”.
That would be redundant and confusing.

Preferred distinction:
- `review` = diagnose / judge / recommend
- `maintain` = refresh current project state docs only

### On `DECISIONS.md`
Should remain lightweight.
Avoid heavy ADR bureaucracy.

### On research
Must not stop at a one-time brief.
Should support persistent compounding knowledge as described in the Karpathy gist.

### On Magic Docs
Interest is explicitly in borrowing the Claude-style mechanism quite faithfully, especially:
- tracked markdown docs
- later background update
- file-scoped updater permissions
- terse, current, architecture-focused updates

### On overlap between kickoff and build bootstrap
Overlap is acknowledged as real.
The currently favored solution is to separate responsibilities rather than discard one component.

---

## What You Should Review

Please review this proposal deeply and critically.

### Part 1 — Understand the current framework
Based on the described files and roles, evaluate whether the understanding of `kata-engineering` is accurate.

Questions to answer:
- Is the current framework being characterized correctly?
- Are any file roles misunderstood?
- Are there hidden strengths already present that make some proposed additions unnecessary?
- Are there existing weaknesses not captured here?

### Part 2 — Evaluate the law/state split
Questions to answer:
- Is law vs state a good core distinction for this framework?
- Where does it work well?
- Where does it create ambiguity?
- Which docs belong in each category?
- Are there better names or models?

### Part 3 — Evaluate the skill boundaries
Questions to answer:
- Is the proposed pipeline clean?
- Are kickoff and bootstrap properly separated?
- Should there really be a separate maintenance skill, or can maintenance be folded elsewhere without causing overlap?
- If maintain exists, what exact scope should it have?
- How should review remain distinct?

### Part 4 — Evaluate the artifact model
Questions to answer:
- Which project artifacts should be first-class in Kata Engineering?
- Which are mandatory vs optional?
- Is `DECISIONS.md` worth adding?
- Is `RESEARCH.md` a single file, or should the framework support a larger research system?

### Part 5 — Evaluate Magic Docs usage
Questions to answer:
- Should Kata Engineering adopt Magic Docs semantics directly?
- Which docs should be eligible?
- Which docs should never be auto-maintained?
- What are the failure modes of such a system?
- How should safety boundaries work?

### Part 6 — Evaluate implementation priority
Questions to answer:
- If these changes are good, what should be implemented first?
- What should be deferred?
- What is the smallest high-leverage improvement?
- What should be avoided because it adds too much complexity too early?

---

## Suggested Output Format for Your Review

Please structure your response as:

1. **Assessment of the current framework**
2. **Assessment of the proposed conceptual model**
3. **Critique of the proposed changes**
4. **Recommended changes to the plan**
5. **Suggested responsibility boundaries for kickoff / build / maintain / review**
6. **Suggested artifact taxonomy (law docs, state docs, mixed docs)**
7. **Suggested approach to research support**
8. **Suggested approach to Magic Docs**
9. **Recommended implementation order**
10. **Any major disagreements with the proposal**

Please be opinionated and critical. Do not rubber-stamp the plan.

---

## Important Review Principles

- Prefer clarity over agreement
- Prefer smaller, sharper changes over grand framework bloat
- If some idea is attractive but wrong, say so directly
- If the plan should be simplified, simplify it
- If a proposed new skill is unnecessary, say so
- If a concept is already present in the framework and only needs reframing, say that
- Avoid ceremonial complexity
- Optimize for a framework that remains elegant and usable in real projects

---

## Current Status

As of now:
- nothing has been changed yet
- this is still a design / review phase
- the intent is to let another model challenge the direction before implementation begins

Your job is to help decide what should actually be built, not to assume the current proposal is correct.
