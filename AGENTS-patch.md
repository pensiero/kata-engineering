# Agent Instructions — Engineering Section

> Add this section to your global or workspace instruction file, such as
> `AGENTS.md` for Codex or `CLAUDE.md` for Claude. It routes the agent to the
> right context for engineering tasks. Keep it thin — the intelligence lives in
> rules, skills, and per-project docs.

---

## Engineering

### Before Any Task

1. Read the project's stable docs if they exist: `ARCHITECTURE.md`, `CONTRACTS.md`
2. Read any living docs that exist: `PLAN.md`, `DECISIONS.md`, `RESEARCH.md`
3. Read the central Kata rule files from this repository: `rules/coding.md` (and `rules/testing.md` if writing tests). Resolve those paths from the Kata Engineering repository root: the path in the `@.../AGENTS-patch.md` include directive (Claude), or the `Kata Engineering home:` line at the top of this section (Codex and other agents where the content is pasted).

### Pick the Right Skill

| Situation | Skill |
|---|---|
| The idea is fuzzy — needs clarification before building anything | `project-kickoff` |
| Starting a new project, or writing/modifying code on an existing one | `build` |
| Reviewing code, checking project health, or refreshing living docs | `review` |
| Filenames or folder layout no longer match the product vocabulary | `harmonize` |
| Setting up a knowledge base (not a codebase) for a stakeholder-heavy project — meetings, emails, documents | `knowledgebase-kickoff` |

`build` handles the full lifecycle: bootstrapping new projects (picking a tier, scaffolding docs), implementing features and fixes, and keeping docs current at the end of each task. You don't pick a phase — the skill handles it.

`review` has four modes: **Focused** (review a change), **Health** (periodic check), **Tier** (verify tier compliance), **Refresh** (update stale living docs to match reality). Specify the mode, or let the agent pick the sensible default for the situation.

`harmonize` has three modes: **Propose** (rename plan only), **Apply** (execute renames, update imports and doc refs), **Review** (fresh-eyes pass over a plan or applied diff). Always start in Propose unless an existing plan is being reviewed or applied.

### When Scope Is Unclear

Research first. Do not mix exploration with implementation. Decide the approach, then implement in a focused step with clean context.

### Rules

Rules encode preferences and practices. They grow over time.

- `rules/coding.md` — read before writing code, resolved from the Kata Engineering repository root
- `rules/testing.md` — read before writing tests, resolved from the Kata Engineering repository root
- Add new rule files as needed; register them here with their trigger condition

### Consolidation

Periodically (every few weeks, or when agent performance degrades):
- Review rules for contradictions or bloat
- Merge overlapping rules
- Remove rules that no longer apply
- Promote recurring lesson entries (captured by `build` Close in project docs) into rules; drop the originals
- Verify skills still match your workflow

When editing any rule, skill, or `AGENTS.md`:
- Write instructions, not descriptions — tell the agent what to do, don't restate what the code already shows
- Refer to artifacts by descriptive name (e.g. "the architecture doc", "the auth module"), not by exact path — paths churn, names survive
