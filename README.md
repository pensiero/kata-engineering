# Kata Engineering (型)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A minimal practice for building software with AI agents.*

It gives your projects a small amount of structure:
- Contracts, guardrails, workflows and practices stored in markdown that keep projects coherent while leaving agents free to explore
- **3 workflow skills**: [project-kickoff](./skills/project-kickoff) · [build](./skills/build) · [review](./skills/review)
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
 
## Older Than Software

In martial arts, a kata (型) is a sequence of movements practiced until they become instinct — correct form achieved not through supervision, but through deeply internalized principle. Elegance comes from discipline. Nothing is added that doesn't belong.

[Dave Thomas](https://en.wikipedia.org/wiki/Dave_Thomas_%28programmer%29) introduced the [concept of code kata](https://en.wikipedia.org/wiki/The_Pragmatic_Programmer) to help developers practice and refine their craft. Kata Engineering extends that idea to AI agents.

## Structure

```
kata-engineering/
├── README.md                          # This file
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
│   └── review/
│       └── SKILL.md                   # Review skill (focused + health + tier + refresh)
└── examples/
    ├── greenfield-project-prompt.md   # Prompt for starting a new project from scratch
    ├── brownfield-rework-prompt.md    # Prompt for reworking an existing project
    └── review-prompt.md               # Prompt for a full project health review
```

## Skills

There are three workflow skills. They are used in sequence for new projects, and independently for ongoing work. The separate `kata-init` skill is only for installing or refreshing the global Codex/Claude setup.

### `project-kickoff` — optional starting point

Use this before `build` when the idea is fuzzy. It interrogates the concept, challenges weak assumptions, and produces a Project Brief, Research Brief, and Execution Plan. It ends with a refined prompt ready to hand to the build skill.

Skip it when the idea is already clear.

### `build` — the implementation loop

The core skill. Covers the full lifecycle of a coding task:

- **Bootstrap** (once, on new projects) — pick a tier, scaffold architecture docs and living docs
- **Orient** — read project context, understand scope
- **Build** — implement the change
- **Verify** — run tests, check contracts, simplicity check
- **Close** — update affected docs, commit

The agent determines which phase to start from automatically. On a new project with no docs, it starts at Bootstrap. On an existing project, it starts at Orient.

### `review` — four modes

| Mode | When | Edits files? |
|---|---|:---:|
| **Focused** | After a change, before merge | No |
| **Health** | Periodic, or when something feels off | No |
| **Tier** | After a tier upgrade, before a handoff | No |
| **Refresh** | When living docs have drifted from reality | Yes — living docs only |

Focused, Health, and Tier are diagnostic: they produce findings, not edits. Refresh is the only mode that writes, and it writes only to living docs (`PLAN.md`, `DECISIONS.md`, `RESEARCH.md`).

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
patching every project. Clone this repository once, then symlink its skills into
the agent's global skills directory and include its routing patch from the
agent's global instruction file.

### Codex

Run these commands from the cloned `kata-engineering` repository:

```bash
KATA_ENGINEERING_HOME="$(pwd -P)"
mkdir -p ~/.codex/skills

ln -sfn "$KATA_ENGINEERING_HOME/skills/build" ~/.codex/skills/build
ln -sfn "$KATA_ENGINEERING_HOME/skills/review" ~/.codex/skills/review
ln -sfn "$KATA_ENGINEERING_HOME/skills/project-kickoff" ~/.codex/skills/project-kickoff
ln -sfn "$KATA_ENGINEERING_HOME/skills/kata-init" ~/.codex/skills/kata-init
```

Then ensure `~/.codex/AGENTS.md` includes the central routing patch:

```bash
include="@${KATA_ENGINEERING_HOME}/AGENTS-patch.md"
touch ~/.codex/AGENTS.md
grep -Fxq "$include" ~/.codex/AGENTS.md || printf '\n%s\n' "$include" >> ~/.codex/AGENTS.md
```

### Claude

Run these commands from the cloned `kata-engineering` repository:

```bash
KATA_ENGINEERING_HOME="$(pwd -P)"
mkdir -p ~/.claude/skills

ln -sfn "$KATA_ENGINEERING_HOME/skills/build" ~/.claude/skills/build
ln -sfn "$KATA_ENGINEERING_HOME/skills/review" ~/.claude/skills/review
ln -sfn "$KATA_ENGINEERING_HOME/skills/project-kickoff" ~/.claude/skills/project-kickoff
ln -sfn "$KATA_ENGINEERING_HOME/skills/kata-init" ~/.claude/skills/kata-init
```

Then ensure `~/.claude/CLAUDE.md` includes the central routing patch:

```bash
include="@${KATA_ENGINEERING_HOME}/AGENTS-patch.md"
touch ~/.claude/CLAUDE.md
grep -Fxq "$include" ~/.claude/CLAUDE.md || printf '\n%s\n' "$include" >> ~/.claude/CLAUDE.md
```

Do not duplicate unrelated global instructions that are already present in
the global instruction file. For example, if RTK is already included globally,
leave it as-is and only add the Kata include if it is missing.

With this setup, edits to this repository's skills, rules, or `AGENTS-patch.md`
are picked up by all projects automatically. Project-level `AGENTS.md` or
`CLAUDE.md` files can stay focused on project-specific constraints.

### Agent bootstrap prompt

If you want an agent to initialize a computer from GitHub, use a prompt like:

> Clone `https://github.com/pensiero/kata-engineering` into a sensible local
> projects directory. From the cloned repository, set `KATA_ENGINEERING_HOME` to
> the repository's absolute path, create symlinks from its `skills/kata-init`,
> `skills/build`, `skills/review`, and `skills/project-kickoff` directories into
> the global skills directory for the agent I am using (`~/.codex/skills` for
> Codex, `~/.claude/skills` for Claude), and add
> `@${KATA_ENGINEERING_HOME}/AGENTS-patch.md` to the agent's global instruction
> file if it is not already present (`~/.codex/AGENTS.md` for Codex,
> `~/.claude/CLAUDE.md` for Claude). Do not add duplicate global instructions
> such as RTK if they are already configured.

### Other agents

For agents that do not read Codex global skills, use the same principle:
reference this repository from the agent's global configuration where possible.
Only copy `skills/`, `rules/`, or `AGENTS-patch.md` when the tool has no support
for includes or symlinks.

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
