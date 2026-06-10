# Kata Engineering (型)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A minimal practice for building software with AI agents.*

It gives your projects a small amount of structure:
- Contracts, guardrails, workflows and practices stored in markdown that keep projects coherent while leaving agents free to explore
- **5 workflow skills**: [project-kickoff](./skills/project-kickoff) · [build](./skills/build) · [review](./skills/review) · [harmonize](./skills/harmonize) · [knowledgebase-kickoff](./skills/knowledgebase-kickoff)
- **1 setup skill**: [kata-init](./skills/kata-init)
- **a tiny routing patch** for [AGENTS.md](./AGENTS-patch.md) (or any other file loaded at runtime)

> **Zero footprint.** No install, no dependencies, no external services.
> Just markdown files loaded by your agent at runtime. Boring in the best way.

## How it works

1. the agent's global instruction file routes the agent to the right skill
2. project docs define architecture, contracts, and constraints
3. the agent builds or reviews within those boundaries
4. as the project grows, you can move from **Light** to **Standard** to **Full** tiers
5. living docs (`PLAN.md`, `DECISIONS.md`, `RESEARCH.md`) capture state that evolves — refreshed as you work, or in one pass via the review skill's Refresh mode

## Works with

![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-2563EB?style=flat&logo=openai&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-000000?style=flat&logo=cursor&logoColor=white)
![OpenClaw](https://img.shields.io/badge/🦞_OpenClaw-FF5A2D?style=flat)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-4285F4?style=flat&logo=google-gemini&logoColor=white)
![Any markdown agent](https://img.shields.io/badge/✨_any_agent_that_reads_text-FFBD16?style=flat)

## Why This Exists

Have you also noticed that AI agents often start well, then drift?

They explore alternatives and follow the conventions for a while, then gradually drift. Complexity crept in. 
The original shape of the project gets blurred. Fragility appears in random places. 
Instructions like use schemas, enforce invariants, or write are quietly forgotten. 
The agent would get stuck on the same approach and stop exploring.

A common reaction is to add more: more specialized agents, more orchestration, more complex setups. 
In practice this often makes things worse. Complex setups age badly and quickly become obsolete in a fast-moving agent ecosystem.

- _A few months ago_: we used few-shot prompting and asked agents to "act like a professional chef" in order to get a recipe
- _Yesterday_: we carefully hand-crafted and orchestrated dozens of specialized agents
- _Today_: models can generate those agent instructions for us
- _Tomorrow_: the model will likely create and run multiple agents under the hood from a single prompt

If a pattern works, frameworks eventually automate it.
Over-engineering agents may become obsolete sooner than you think. So, KISS 💋.

So the real need is not more control. It is better structure.
Kata Engineering gives agents elegant boundaries without over-constraining them. The architecture persists. Decisions are recorded. Constraints are testable. The agent remains free to explore, but not free to quietly deform the project.

A project's docs are not only for humans. They are loaded into agent context on every session — they are the codebase, too. That is why the discipline below treats them as load-bearing artifacts, not afterthought documentation.
 
## Older Than Software

In martial arts, a kata (型) is a sequence of movements practiced until they become instinct — correct form achieved not through supervision, but through deeply internalized principle. Elegance comes from discipline. Nothing is added that doesn't belong.

[Dave Thomas](https://en.wikipedia.org/wiki/Dave_Thomas_%28programmer%29) introduced the [concept of code kata](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer) to help developers practice and refine their craft. Kata Engineering extends that idea to AI agents.

## Structure

This repository is itself a light-tier Kata project — all docs, no code. This README serves as its architecture doc.

```
kata-engineering/
├── README.md                          # This file — also the repo's architecture doc
├── INITIAL_PROMPT.md                  # Origin story: the prompt that started this project
├── AGENTS-patch.md                    # Routing section to add to workspace AGENTS.md
├── rules/
│   ├── coding.md                      # Universal coding practices
│   └── testing.md                     # Universal testing practices
├── skills/
│   ├── kata-init/
│   │   └── SKILL.md                   # Global setup for Codex and Claude
│   ├── project-kickoff/
│   │   └── SKILL.md                   # Optional first step: refine an idea before building
│   ├── build/
│   │   ├── SKILL.md                   # Build skill (bootstrap + orient + build + verify + close)
│   │   └── templates/                 # Project scaffolding templates
│   │       ├── architecture-light.md      # Stable docs — tiered
│   │       ├── architecture-standard.md
│   │       ├── architecture-full.md
│   │       ├── contracts-standard.md
│   │       ├── contracts-full.md
│   │       ├── plan.md                    # Living docs — tier-agnostic
│   │       ├── decisions.md
│   │       └── research.md
│   ├── review/
│   │   └── SKILL.md                   # Review skill (focused + health + tier + refresh)
│   ├── harmonize/
│   │   └── SKILL.md                   # Harmonize filenames and folder layout for product-readability
│   └── knowledgebase-kickoff/
│       ├── SKILL.md                   # Bootstrap a knowledge base for stakeholder-heavy projects
│       └── templates/                 # KB scaffolding (SCHEMA, CLAUDE, PLAN, ingest-sources skill, …)
└── examples/
    ├── greenfield-project-prompt.md   # Prompt for starting a new project from scratch
    ├── brownfield-rework-prompt.md    # Prompt for reworking an existing project
    └── review-prompt.md               # Prompt for a full project health review
```

## Skills

There are five workflow skills. The first four are used in sequence for new projects, and independently for ongoing work; `knowledgebase-kickoff` bootstraps knowledge bases rather than codebases. The separate `kata-init` skill is only for installing or refreshing the global Codex/Claude setup.

### `project-kickoff` — optional starting point

Use this before `build` when the idea is fuzzy. It interrogates the concept, challenges weak assumptions, and produces a Project Brief, Research Brief, and Execution Plan. It ends with a refined prompt ready to hand to the build skill.

Skip it when the idea is already clear.

### `build` — the implementation loop

The core skill. Covers the full lifecycle of a coding task:

- **Bootstrap** (once, on new projects) — pick a tier, scaffold architecture docs and living docs
- **Orient** — read project context, understand scope
- **Build** — implement the change
- **Verify** — run tests, check contracts, simplicity check
- **Close** — update affected docs, capture lessons, commit

The agent determines which phase to start from automatically. On a new project with no docs, it starts at Bootstrap. On an existing project, it starts at Orient.

Close runs the **compounding loop**: corrections received during the task are routed into the project's docs (project-specific lessons) or proposed as additions to the central rules (universal lessons), so the practice improves with every session instead of repeating mistakes.

### `review` — four modes

| Mode | When | Edits files? |
|---|---|:---:|
| **Focused** | After a change, before merge | No |
| **Health** | Periodic, or when something feels off | No |
| **Tier** | After a tier upgrade, before a handoff | No |
| **Refresh** | When living docs have drifted from reality | Yes — living docs only |

Focused, Health, and Tier are diagnostic: they produce findings, not edits. Refresh is the only mode that writes, and it writes only to living docs (`PLAN.md`, `DECISIONS.md`, `RESEARCH.md`).

### `harmonize` — three modes

| Mode | When | Edits files? |
|---|---|:---:|
| **Propose** | First pass — surface rename candidates without touching anything | No |
| **Apply** | Execute approved renames, update imports + doc refs, run tests | Yes |
| **Review** | Fresh-eyes pass over a plan or applied diff produced by another agent | No |

Use when filenames and folder layout no longer match the product vocabulary — names that mislead, undersell what a file owns, or reflect historical accidents. The skill insists on building independent assumptions before reading any prior plan, so the fresh-eyes signal stays honest.

### `knowledgebase-kickoff` — knowledge bases, not codebases

Bootstraps a project whose deliverable is current knowledge rather than code: raw sources (emails, transcripts, documents) flow into LLM-maintained entity pages, forming a queryable, auditable source of truth. Scaffolds the folder skeleton, `SCHEMA`/`CLAUDE`/`README` docs, and an `ingest-sources` skill for the new project. Use it for stakeholder-heavy projects — many meetings, suppliers to hold accountable, decisions to trace.

## Docs: stable vs living

Project docs fall into two categories with different discipline:

**Stable docs** describe what the project IS and what MUST hold true. They change only when the underlying design changes. Casual edits erode their authority.

**Living docs** describe current state. They go stale quickly — staleness is a defect. They are checked on every Close phase and can be batch-refreshed via the review skill's Refresh mode.

| | Kind | Light | Standard |    Full     |
|---|---|:---:|:---:|:-----------:|
| `ARCHITECTURE.md` | stable | ✓ | ✓ |      ✓      |
| `CONTRACTS.md` | stable | | ✓ |      ✓      |
| Schema definitions | stable | | ✓ |      ✓      |
| Coupling guardrail tests | stable | | |      ✓      |
| Structural integrity tests | stable | | |      ✓      |
| Change governance | stable | | |      ✓      |
| `DECISIONS.md` | living | optional | optional |      ✓      |
| `PLAN.md` | living | optional | optional | recommended |
| `RESEARCH.md` | living | optional | optional |      optional      |

Use **light** for scripts and personal tools. **Standard** for projects with APIs, persistence, or multiple modules. **Full** for production systems that need governance.

## Global setup

For Codex and Claude, prefer a single global setup instead of copying skills and
patching every project. Clone this repository once, then run the **`kata-init`**
skill from the repository root — or ask your agent to follow
[`skills/kata-init/SKILL.md`](./skills/kata-init/SKILL.md). It symlinks the
skills into each agent's global skills directory and wires `AGENTS-patch.md`
into the agent's global instruction file.

The wiring mechanism differs per agent. Claude Code expands `@path` includes
natively, so edits to this repository are picked up automatically. Codex does
not expand includes ([openai/codex#6038](https://github.com/openai/codex/issues/6038)),
so `kata-init` pastes the patch content between managed markers instead —
re-run `kata-init` after editing `AGENTS-patch.md` to refresh it.

Project-level `AGENTS.md` or `CLAUDE.md` files stay focused on
project-specific constraints.

### Agent bootstrap prompt

If you want an agent to initialize a computer from GitHub, use a prompt like:

> Clone `https://github.com/pensiero/kata-engineering` into a sensible local
> projects directory, then follow `skills/kata-init/SKILL.md` from the cloned
> repository to configure the agents installed on this machine. Do not add
> duplicate global instructions that are already configured.

### Other agents

For other agents, apply the same principle: reference this repository from the
agent's global configuration — via an include if the tool supports it,
otherwise by pasting `AGENTS-patch.md` content between managed markers the way
`kata-init` does for Codex. Only copy `skills/` or `rules/` when the tool
supports neither includes nor symlinks.

## Usage

Once deployed, your agent picks up the right skill automatically via AGENTS.md. Just work naturally — no special syntax needed. If a project has no architecture docs yet, the agent will bootstrap them before proceeding — even for small tasks.

The following are sample prompts:

**New project from a rough idea** *(uses project-kickoff, then build)*
> _I want to build a CLI tool that syncs files between two directories. Help me think it through first. Use project-kickoff skill._

**New project with a clear idea** *(uses build directly)*
> _I want to build a CLI tool that syncs files between two directories. It's a personal utility, keep it light._

**Feature on an existing project**
> _Add pagination to the /users endpoint._

**Existing project with no docs yet**
> _This project has no architecture docs. Let's set them up from the existing code._

**Review**
> _Review the changes I just made to the auth module._

**Planning phased work**
> _Let's create a plan. I want to break the remaining work into phases — authentication first, then the API layer, then the CLI._

**Refreshing living docs**
> _Refresh the living docs. I've done a few sessions of work and PLAN.md is out of date._

**Tier upgrade**
> _This project has grown. Let's upgrade from light to standard._

### Advanced Examples

For longer, multi-phase tasks, use the ready-made prompts in `examples/`:

- [**Start a new project from scratch**](examples/greenfield-project-prompt.md) — full bootstrap with tier selection, architecture docs, schemas, and initial tests
- [**Rework an existing project**](examples/brownfield-rework-prompt.md) — restructure docs and contracts for a project that already has working code
- [**Full project health review**](examples/review-prompt.md) — periodic check on architecture accuracy, contract health, tier compliance, and complexity
