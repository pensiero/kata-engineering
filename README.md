# Kata Engineering (型)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A minimal practice for building software with AI agents.*

It gives your projects a small amount of structure:
- Contracts, guardrails, workflows and practices stored in markdown that keep projects coherent while leaving agents free to explore
- **2 simple skills**: [build](./skills/build) and [review](./skills/review)
- **a tiny routing patch** for [AGENTS.md](./AGENTS-patch.md) (or any other file loaded at runtime)

> **Zero footprint.** No install, no dependencies, no external services.
> Just markdown files loaded by your agent at runtime. Boring in the best way.

## How it works

1. `AGENTS.md` routes the agent to the right skill
2. project docs define architecture, contracts, and constraints
3. the agent builds or reviews within those boundaries
4. as the project grows, you can move from **Light** to **Standard** to **Full** tiers

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
 
## Older Than Software

In martial arts, a kata (型) is a sequence of movements practiced until they become instinct — correct form achieved not through supervision, but through deeply internalized principle. Elegance comes from discipline. Nothing is added that doesn't belong.

[Dave Thomas](https://en.wikipedia.org/wiki/Dave_Thomas_%28programmer%29) introduced the [concept of code kata](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer) to help developers practice and refine their craft. Kata Engineering extends that idea to AI agents.

## Works with

![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-2563EB?style=flat&logo=openai&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-000000?style=flat&logo=cursor&logoColor=white)
![OpenClaw](https://img.shields.io/badge/🦞_OpenClaw-FF5A2D?style=flat)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-4285F4?style=flat&logo=google-gemini&logoColor=white)
![Any markdown agent](https://img.shields.io/badge/✨_any_agent_that_reads_text-FFBD16?style=flat)

## Structure

```
kata-engineering/
├── README.md                  # This file
├── AGENTS-md-patch.md         # Routing section to add to workspace AGENTS.md
├── rules/
│   ├── coding.md              # Universal coding practices
│   └── testing.md             # Universal testing practices
├── skills/
│   ├── build/
│   │   ├── SKILL.md           # Build skill (bootstrap + orient + build + verify + close)
│   │   └── templates/         # Per-tier project scaffolding templates
│   │       ├── light.md
│   │       ├── standard.md
│   │       ├── standard-contracts.md
│   │       ├── full.md
│   │       └── full-contracts.md
│   └── review/
│       └── SKILL.md           # Review skill (observe + check + simplify + report)
├── examples/
│   ├── greenfield-project-prompt.md   # Prompt for starting a new project from scratch
│   ├── brownfield-rework-prompt.md    # Prompt for reworking an existing project
│   └── review-prompt.md              # Prompt for a full project health review
```

## Tiers

| | Light | Standard | Full |
|---|:---:|:---:|:---:|
| `ARCHITECTURE.md` | ✓ | ✓ | ✓ |
| `CONTRACTS.md` | | ✓ | ✓ |
| `PLAN.md` | optional | optional | optional |
| Schema definitions | | ✓ | ✓ |
| Coupling guardrail tests | | | ✓ |
| Structural integrity tests | | | ✓ |
| Change governance | | | ✓ |

Use **light** for scripts and personal tools. **Standard** for projects with APIs, persistence, or multiple modules. **Full** for production systems that need governance. Use `PLAN.md` when the project has phased work, sequencing, or deferred scope.

## Deployment

1. Copy `rules/` to your workspace (example if you are using OpenClaw: `~/.openclaw/workspace/rules/`)
2. Copy `skills/build/` and `skills/review/` to workspace skills folder
3. Add the contents of `AGENTS-patch.md` to your workspace `AGENTS.md`
4. Optionally register skills in config for auto-discovery

## Usage

Once deployed, your agent picks up the right skill automatically via AGENTS.md. Just work naturally — no special syntax needed. If a project has no architecture docs yet, the agent will bootstrap them before proceeding — even for small tasks.

The following are sample prompts:

**New project**
> _I want to build a CLI tool that syncs files between two directories. It's a personal utility, keep it light._

**Feature on an existing project**
> _Add pagination to the /users endpoint._

**Existing project with no docs yet**
> _This project has no architecture docs. Let's set them up from the existing code._

**Review**
> _Review the changes I just made to the auth module._

**Planning phased work**
> _Let's create a plan. I want to break the remaining work into phases — authentication first, then the API layer, then the CLI._

**Tier upgrade**
> _This project has grown. Let's upgrade from light to standard._

### Advanced Examples

For longer, multi-phase tasks, use the ready-made prompts in `examples/`:

- [**Start a new project from scratch**](examples/greenfield-project-prompt.md) — full bootstrap with tier selection, architecture docs, schemas, and initial tests
- [**Rework an existing project**](examples/brownfield-rework-prompt.md) — restructure docs and contracts for a project that already has working code
- [**Full project health review**](examples/review-prompt.md) — periodic check on architecture accuracy, contract health, tier compliance, and complexity
