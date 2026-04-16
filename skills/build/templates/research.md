# Research Template

Scaffold for `RESEARCH.md`. Living doc — optional for any tier. Create it when the project has meaningful unknowns at the start, or when a Research Brief was produced during kickoff.

`RESEARCH.md` is a running record of findings, open questions, and sources. It is NOT a changelog or a final research report — it should reflect the current state of understanding. Stale research is misleading; prune aggressively.

Copy the content inside the code block below and adapt it to the project. Everything outside the code block is guidance for the agent, not part of the output.

---

```markdown
---
freshness: living
---
# Research

Current state of what is known, what is still open, and where the information came from. Keep it current — stale research is misleading.

## Key Findings

<!-- What is now known that shapes design or implementation decisions.
     Update as new information arrives. Remove findings that become irrelevant. -->

- [Finding — one line. Reference a source below if needed.]

## Open Questions

<!-- What still needs to be figured out. Remove each item when resolved.
     If the resolution matters, add a Key Finding or a DECISIONS.md entry. -->

- [Question — why it matters, what answering it would unblock.]

## Sources

<!-- Links, docs, papers, experiments consulted.
     One line per source: [link or name] — why it was consulted / what it contributed. -->

- [Source] — [what it contributed]
```

---

## Notes for the agent

- Findings are what is known, not what was learned in a single session. Phrase them as stable statements.
- Open Questions get removed when answered. If the answer matters long-term, promote it to a Finding or a Decision.
- Sources are annotated one-liners — enough for a future agent to know whether to re-consult.
- This is not a research paper. If a section is empty, leave it empty. Do not invent content.
