# Standard Tier — Architecture Template

Use this as a guide when bootstrapping a standard-tier project. The sections below demonstrate the narrative principle: each builds on what came before. Adapt the structure to your project's natural story — the reading order matters more than the specific headings.

**Principle:** order by understanding dependency. A reader should never encounter something that requires context they haven't been given yet.

---

```markdown
---
project_tier: standard
---

# [Project Name]

## The Story

[The premise, written as clear, direct prose. Two to four sentences — not bullet points, not a literary essay. Define what the system IS, not what it does. "A persistent identity blueprint" tells you more than "a system that manages identity data." Every word should be load-bearing.]

[This section sets the frame for everything that follows. Every architectural decision should make sense in light of what's written here.]

## The Concepts

[Now that the reader knows what the system is, introduce what exists inside it. The entities, abstractions, or components that a newcomer needs to know before understanding how they interact.]

[For each concept: what is it, what does it mean, what is its role. Not how it's implemented — what it IS.]

- **[Concept 1]** — [what it represents and why it exists]
- **[Concept 2]** — [what it represents and why it exists]
- **[Concept 3]** — [what it represents and why it exists]

[If core data structures have schemas, reference them here: "defined in `schemas/[file]`"]

## The Structure

[Now that the reader knows what exists, explain how these things are allowed to interact. What owns what. What must never depend on what.]

### Ownership

| Component | Owns | Location |
|-----------|------|----------|
| [Component 1] | [its responsibilities] | `src/[path]` |
| [Component 2] | [its responsibilities] | `src/[path]` |

### Forbidden Coupling

[These are the walls. Crossing them is an architectural violation.]

- [Component A] must not import from [Component B] — [why]
- [Component C] must not directly access [resource D] — [why]

## The Flow

[Now that the reader knows the concepts and the boundaries, show how data/control actually moves through the system. This should feel like a natural consequence of the structure described above.]

[Describe the primary paths: what triggers what, how data transforms, where state lives. If the system has a lifecycle or pipeline, describe it here.]

[Keep it concrete. "A request arrives at X, which validates it against Y, then passes it to Z for processing" — not abstract descriptions of possible flows.]

## The Decisions

[Now that the reader understands the system, explain why it has this particular shape. Decisions only make sense in context — that's why this section comes after the structure, not before.]

### [Decision 1]
**Choice:** [what was chosen]
**Why:** [rationale, including rejected alternatives]

### [Decision 2]
**Choice:** [what was chosen]
**Why:** [rationale]

## Working With This Project

### Repository Map

```
project/
  src/
    [component-1]/   # [purpose]
    [component-2]/   # [purpose]
  schemas/           # Data structure definitions
  tests/             # Test baseline
  ARCHITECTURE.md    # This file
  CONTRACTS.md       # Invariants and gates
```

### Commands

```bash
# How to run
[command]

# How to test
[command]

# How to verify contracts hold
[command, or "see CONTRACTS.md"]
```

### Change Discipline

Every meaningful change updates:
1. Code
2. Relevant tests
3. Impacted docs (this file, CONTRACTS.md, schemas)

Code and docs ship together. No silent drift.
```

---

## Notes for the agent

- The sections above are ONE example of the narrative principle for a typical multi-module project. Your project's natural story may be different.
- Ask: "what does a reader need to understand first? what depends on that?" — and build the reading order accordingly.
- A library might flow: The Story → The Interface → The Contracts → The Internals → Usage.
- A data pipeline might flow: The Story → Sources → Transformations → Destinations → Failure Modes.
- A CLI tool might flow: The Story → Commands → Configuration → Extension.
- The principle is constant. The sections adapt.
