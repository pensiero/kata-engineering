# Plan Template

Scaffold for `PLAN.md`. Living doc — optional for any tier, useful when multiple sessions will work on the project over time.

PLAN.md records the journey: what's been done, what's next, what's deferred. It is NOT architecture (what the system is), contracts (what must hold true), or reasoning about why decisions were made (that lives in `ARCHITECTURE.md` or `DECISIONS.md`).

If the plan disappeared, the project could still be understood and maintained from architecture + contracts + tests. The plan makes pickup faster, not survival possible.

Copy the content inside the code block below and adapt it to the project. Everything outside the code block is guidance for the agent, not part of the output.

---

```markdown
---
freshness: living
---
# Plan

What we're building, in what order, and what's done.

- `ARCHITECTURE.md` describes what the system is and why.
- `CONTRACTS.md` describes what must hold true.
- This file describes what we're doing and what comes next.

---

## Completed

### [Phase/Milestone 1 — Name]
- [x] [What was built]
- [x] [What was built]
- [x] [What was built]

### [Phase/Milestone 2 — Name]
- [x] [What was built]
- [x] [What was built]

---

## Up Next

### [Phase/Milestone 3 — Name]
- [ ] [What needs to be done]
- [ ] [What needs to be done]
- [ ] [What needs to be done]

---

## Deferred

[Things explicitly decided to NOT do now, and why. This prevents future agents from re-proposing work that was intentionally postponed.]

- [Deferred item] — [why it's deferred]
- [Deferred item] — [why it's deferred]

---

## Prioritization

[What principles guide ordering. These help an agent make good decisions about what to work on next when the human isn't available to direct.]

1. [Principle 1]
2. [Principle 2]
3. [Principle 3]
```

---

## When to create a PLAN.md

- The project will be built over multiple sessions
- There are clear phases or milestones
- Multiple people (or agents) might pick up work at different times

## When NOT to create one

- Weekend project you'll finish in one session
- The "plan" is just a single task (use a task contract instead)
- The project is in maintenance mode (no planned new work)

## Keeping it alive

- When you complete work: check off items, move phases to Completed
- When scope changes: update Up Next, add to Deferred with rationale
- When priorities shift: update the Prioritization section
- Prune completed phases periodically — keep enough history to understand the journey, not so much that the file becomes archaeology
