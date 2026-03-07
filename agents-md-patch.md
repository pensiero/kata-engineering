# AGENTS.md — Engineering Section

> Add this section to your workspace AGENTS.md. It routes the agent to the right
> context for engineering tasks. Keep it thin — the intelligence lives in rules,
> skills, and per-project docs.

---

## Engineering

### Before Any Coding Task

1. Read the project's architecture docs if they exist (`ARCHITECTURE.md`, `CONTRACTS.md`, or equivalent at project root)
2. Read `rules/coding.md`
3. If the task involves writing tests, also read `rules/testing.md`

### Starting or Bootstrapping a Project

Use the `build` skill. It detects whether the project has structure and bootstraps if needed.

### Implementing Features, Fixes, or Changes

Use the `build` skill.

### Reviewing Code or Project Health

Use the `review` skill.

### When Scope Is Unclear

Research first. Do not mix exploration with implementation. Decide the approach, then implement in a focused step with clean context.

### Rules

Rules encode preferences and practices. They grow over time.

- `rules/coding.md` — read before writing code
- `rules/testing.md` — read before writing tests
- Add new rule files as needed; register them here with their trigger condition

### Consolidation

Periodically (every few weeks, or when agent performance degrades):
- Review rules for contradictions or bloat
- Merge overlapping rules
- Remove rules that no longer apply
- Verify skills still match your workflow
