# Kata Engineering (型)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A minimal practice for building software with AI agents.*

Contracts, guardrails, workflows and practices that keep projects coherent while leaving agents free to explore.
 
## Older Than Software

In martial arts, a kata (型) is a sequence of movements practiced until they become instinct — correct form achieved not through supervision, but through deeply internalized principle. Elegance comes from discipline. Nothing is added that doesn't belong.

[Dave Thomas](https://en.wikipedia.org/wiki/Dave_Thomas_%28programmer%29) introduced the [concept of code kata](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer) to help developers practice and refine their craft. Kata Engineering extends that idea to AI agents.

## Why This Exists

After working with AI agents on real projects for a while, a pattern became clear. The agent would start strong — exploring alternatives, following the conventions, building with care. Then, gradually, it would drift. Complexity crept in. The point of what was being built got lost. Fragility appeared in random places. Bugs hid inside codebases that looked fine from the outside. Instructions like use schemas, enforce invariants, or write tests would be followed for a while, then quietly forgotten. The agent would get stuck on the same approach and stop exploring.

The obvious response is to add more: more agents, more orchestration, more complex setups. In practice this makes things worse. Complex setups age badly, hide problems, and quickly become obsolete in a fast-moving agent ecosystem.

Industry is moving fast:
- Yesterday: you had to carefully design and orchestrate dozens of specialized agents.
- Today: you can ask a model like Claude to generate the instructions for those agents.
- Tomorrow: the model will likely create and run them internally from a single prompt.

If something consistently works, frameworks eventually automate it.
Over-engineering may become obsolete sooner than you think. So, KISS 💋.

What's actually needed is structure — not control. Elegant boundaries, guardrails, and best practices precise enough that the agent knows what the project is, how it's shaped, and what must never change. Simple enough that the agent stays free to explore, try alternatives, push back. The architecture persists. The decisions are recorded. The constraints are testable. The agent works within them, not around them.

## Works with

![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-2563EB?style=flat&logo=openai&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-000000?style=flat&logo=cursor&logoColor=white)
![OpenClaw](https://img.shields.io/badge/🦞_OpenClaw-FF5A2D?style=flat)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-4285F4?style=flat&logo=google-gemini&logoColor=white)
![Any markdown agent](https://img.shields.io/badge/✨_any_agent_that_reads_text-FFBD16?style=flat)

## Principles

- **1 agent, 2 modes** - _build_ and _review_ are skills, not separate agents
- **3 tiers complexity** based on your project - light, standard and full
- AGENTS.md routes, intelligence lives in project docs
- Contracts over instructions

> **Zero footprint.** No install, no dependencies, no external services or API calls. Instructions in markdown files have no external reference. 

## Structure

```
kata-engineering/
├── README.md                  # This file
├── agents-md-patch.md         # Routing section to add to workspace AGENTS.md
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
```

## Tiers

| | Light | Standard | Full |
|---|:---:|:---:|:---:|
| `ARCHITECTURE.md` | ✓ | ✓ | ✓ |
| `CONTRACTS.md` | | ✓ | ✓ |
| Schema definitions | | ✓ | ✓ |
| Coupling guardrail tests | | | ✓ |
| Structural integrity tests | | | ✓ |
| Change governance | | | ✓ |

Use **light** for scripts and personal tools. **Standard** for projects with APIs, persistence, or multiple modules. **Full** for production systems that need governance.

## Deployment

1. Copy `rules/` to your workspace (example if you are using OpenClaw: `~/.openclaw/workspace/rules/`)
2. Copy `skills/build/` and `skills/review/` to workspace skills folder
3. Add the contents of `agents-md-patch.md` to your workspace `AGENTS.md`
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

**Tier upgrade**
> _This project has grown. Let's upgrade from light to standard._
