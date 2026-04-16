# Decisions Template

Scaffold for `DECISIONS.md`. Living doc — optional for any tier, worth creating for anything beyond a simple script or any project spanning multiple sessions.

`DECISIONS.md` is a lightweight log of non-obvious choices. It records what was decided, the reasoning at the time, and the alternatives rejected. It is NOT a formal ADR system — keep entries short. The goal is that a future agent or collaborator arriving cold can understand why the project looks the way it does.

Copy the content inside the code block below and adapt it to the project. Everything outside the code block is guidance for the agent, not part of the output.

---

```markdown
---
freshness: living
---
# Decisions

Non-obvious choices made in this project. Newest first. One entry per real decision — do not record obvious choices.

---

## YYYY-MM-DD — [Short decision title]

**Chose:** [What was decided.]
**Because:** [Why this was the right choice given the constraints at the time.]
**Over:** [What alternatives were considered and why they were rejected.]
**Revisit if:** [Conditions that would make this decision worth reconsidering. Optional — include only when a real trigger exists.]

---
```

---

## Notes for the agent

- Add an entry when: a non-obvious architectural or design choice is made; a real alternative was rejected; a future agent might plausibly propose the rejected approach again.
- Do NOT record: obvious choices ("used the standard library logger"), micro-decisions inside one function, or rationale that's already captured in `ARCHITECTURE.md`.
- Keep entries short. One decision = one entry = a handful of lines.
- Newest first. Never rewrite history — if a decision is superseded, add a new entry that references the old one.
