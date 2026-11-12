# Kata Engineering (型)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A minimal practice for building software with AI agents.*

It gives your projects a small amount of structure:
- Contracts, guardrails, workflows and practices stored in markdown that keep projects coherent while leaving agents free to explore
- **6 workflow skills**: [project-kickoff](./skills/project-kickoff) · [build](./skills/build) · [review](./skills/review) · [harmonize](./skills/harmonize) · [knowledgebase-kickoff](./skills/knowledgebase-kickoff) · [tracker](./skills/tracker)
- **1 setup skill**: [kata-init](./skills/kata-init)
- **no instruction-file patching** — skills route themselves through their descriptions and point to the central rules

> **Zero footprint.** No install, no dependencies, no external services.
> Markdown files loaded by your agent at runtime, plus one optional
> standard-library Python script in `tracker`. Boring in the best way.

## How it works

1. skill descriptions route the agent to the right skill; each skill reads the central rules
2. project docs define architecture, contracts, and constraints
3. the agent builds or reviews within those boundaries
4. as the project grows, you can move from **Light** to **Standard** to **Full** tiers
5. living docs (`PLAN.md`, `DECISIONS.md`) capture state that evolves — refreshed as you work, or in one pass via the review skill's Refresh mode

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

This repository is itself a light-tier Kata project — docs, plus one optional standard-library Python script in the `tracker` skill. This README serves as its architecture doc.

```
kata-engineering/
├── README.md                          # This file — also the repo's architecture doc
├── INITIAL_PROMPT.md                  # Origin story: the prompt that started this project
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
│   │       └── decisions.md
│   ├── review/
│   │   └── SKILL.md                   # Review skill (focused + health + tier + refresh)
│   ├── harmonize/
│   │   └── SKILL.md                   # Harmonize filenames and folder layout for product-readability
│   ├── knowledgebase-kickoff/
│   │   ├── SKILL.md                   # Bootstrap a knowledge base for stakeholder-heavy projects
│   │   └── templates/                 # KB scaffolding (SCHEMA, AGENTS, PLAN, ingest-sources skill, …)
│   └── tracker/
│       ├── SKILL.md                   # Track work, owner questions and outcomes in TRACKER.json
│       ├── reference/schema.md        # The file format and who moves each status
│       ├── scripts/tracker.py         # new / check / build / brief / show / render / reply, owner actions (stdlib only) + tests
│       ├── assets/page.html           # The template every tracker's page is built from
│       ├── assets/markdown.js         # Draws the text fields as Markdown, on the page and in the hub
│       └── assets/style.css           # The look shared by the pages and the Kata hub
```

## Skills

There are six workflow skills. The first four are used in sequence for new projects, and independently for ongoing work; `knowledgebase-kickoff` bootstraps knowledge bases rather than codebases; `tracker` keeps a project's work and open questions. The separate `kata-init` skill is only for installing or refreshing the global Codex/Claude setup.

### `project-kickoff` — optional starting point

Use this before `build` when the idea is fuzzy. It interrogates the concept, challenges weak assumptions, and produces a brief, a phased project shape and the first actions — plus research and an execution plan when the idea needs them. The outcome lands in `PLAN.md`, with a refined prompt ready to hand to the build skill.

Skip it when the idea is already clear.

### `build` — the implementation loop

The core skill. Covers the full lifecycle of a coding task:

- **Bootstrap** (when starting or restructuring a project) — pick a tier, scaffold architecture docs and living docs
- **Orient** — read project context, understand scope
- **Build** — implement the change
- **Verify** — run tests, check contracts, simplicity check
- **Close** — update affected docs, capture lessons, commit

The agent determines which phase to start from automatically, and scales each phase to the change: a one-line fix runs through them in minutes. A new project starts at Bootstrap; everything else starts at Orient. The agent commits each finished chunk of work on its own — code, tests and docs together.

Close runs the **compounding loop**: corrections received during the task are routed into the project's docs (project-specific lessons) or proposed as additions to the central rules (universal lessons), so the practice improves with every session instead of repeating mistakes.

### `review` — three modes

| Mode | When | Edits files? |
|---|---|:---:|
| **Focused** | After a change, before merge | No |
| **Health** | Periodic, when something feels off, after a tier upgrade, before a handoff | No |
| **Refresh** | When living docs have drifted from reality | Yes — living docs only |

Focused and Health are diagnostic: they produce findings, not edits — in a tracker when many need your decision. Health includes tier compliance. Refresh is the only mode that writes, and it writes only to living docs (`PLAN.md` or `TRACKER.json`, `DECISIONS.md`).

### `harmonize` — three modes

| Mode | When | Edits files? |
|---|---|:---:|
| **Propose** | First pass — surface rename candidates without touching anything | No |
| **Apply** | Execute approved renames, update imports + doc refs, run tests | Yes |
| **Review** | Fresh-eyes pass over a plan or applied diff produced by another agent | No |

Use when filenames and folder layout no longer match the product vocabulary — names that mislead, undersell what a file owns, or reflect historical accidents. The skill insists on building independent assumptions before reading any prior plan, so the fresh-eyes signal stays honest.

### `knowledgebase-kickoff` — knowledge bases, not codebases

Bootstraps a project whose deliverable is current knowledge rather than code: raw sources (emails, transcripts, documents) flow into LLM-maintained entity pages, forming a queryable, auditable source of truth. Scaffolds the folder skeleton, `SCHEMA`/`CLAUDE`/`README` docs, and an `ingest-sources` skill for the new project. Use it for stakeholder-heavy projects — many meetings, suppliers to hold accountable, decisions to trace.

### `tracker` — work, questions and outcomes, one item at a time

Keeps the tracking half of `PLAN.md` exact, in a versioned `TRACKER.json`: one list in the order of work, where every item has a stage (draft, to do, in progress, done, not doing) and, when it waits for the owner, a Needs you tag, the plan, the question it is waiting on, the conversation, the decision taken and what was finally done, with commit references. Several trackers per project: `TRACKER.json` for the long-lived one, `trackers/<name>.json` for one effort. The agent sizes each item itself: it does it, splits it, or grows it into a tracker of its own.

Beside each tracker sits a generated page (`TRACKER.html`): a static file the owner opens from disk, with no server and nothing uploaded. It shows the items in the same tabs as the hub (Needs you, then Draft, To do, In progress, Archive), takes replies item by item and new items from the owner; a "Copy for the agent" button hands them over, and the agent writes them into the file and rebuilds the page. The file stays the record and both are committed together. It can also propose turning an existing `PLAN.md` into a tracker, leaving the reasoning in the docs where it belongs.

The owner writes intents (new items and drafts, order, replies, archiving, reopening); the agent writes the record. A reply takes the Needs you tag off. Those writes can also come from the Kata hub (`kata-tracker`), a local app over every registered project's trackers, which applies them through the same script.

The skill ships a small Python script (standard library only) that validates the file, builds the page, takes the owner's replies and gives an agent a short `brief` of what needs it, so every project works the same way. The format is specified in plain markdown, so an agent can work the file by hand.

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
| `TRACKER.json` (the tracking half of `PLAN.md`) | living | optional | optional | optional |

Use **light** for scripts and personal tools. **Standard** for projects with APIs, persistence, or multiple modules. **Full** for production systems that need governance.

## Global setup

Setup is symlinks only. Clone this
repository once, then run the **`kata-init`** skill from the repository root —
or ask your agent to follow
[`skills/kata-init/SKILL.md`](./skills/kata-init/SKILL.md). It symlinks the
skills into each agent's global skills directory (`~/.claude/skills`,
`~/.codex/skills`). Skills route themselves: the agent picks them by their
descriptions, and each skill points to the central `rules/` in this repository.
Edits to this repository are picked up by all projects automatically.

Project-level `AGENTS.md` or `CLAUDE.md` files stay focused on
project-specific constraints.

### Agent bootstrap prompt

If you want an agent to initialize a computer from GitHub, use a prompt like:

> Clone `https://github.com/pensiero/kata-engineering` into a sensible local
> projects directory, then follow `skills/kata-init/SKILL.md` from the cloned
> repository to configure the agents installed on this machine.

### Other agents

For agents that support the SKILL.md format, symlink `skills/` into their
skills directory the same way. For agents that don't, copy or reference
`rules/` and the relevant SKILL.md files from the agent's configuration —
the skills are plain markdown and work anywhere text is read.

## Maintaining the framework

Rules encode preferences and practices. They grow through the build skill's
lesson capture at Close, and they shrink through periodic consolidation.
Every few weeks — or when agent performance degrades:

- Review rules for contradictions or bloat; merge overlapping rules; remove rules that no longer apply
- Promote recurring lesson entries (captured in project docs by `build` Close) into rules; drop the originals
- Verify the skills still match your workflow

When editing any rule or skill:

- Write instructions, not descriptions — tell the agent what to do, don't restate what the code already shows
- Refer to artifacts by descriptive name (e.g. "the architecture doc"), not by exact path — paths churn, names survive
- Add new rule files as needed; reference them from the skills that should read them

## Usage

Once deployed, your agent picks up the right skill automatically from the skill descriptions. Just work naturally — no special syntax needed. When you start a new project, or ask for it, the agent bootstraps the architecture docs first; small changes in an undocumented repo just get made.

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

**Project health check**
> _Run a health check on this project: does the architecture doc still match the code, are the contracts tested, is complexity creeping in?_

**Planning phased work**
> _Let's create a plan. I want to break the remaining work into phases — authentication first, then the API layer, then the CLI._

**Refreshing living docs**
> _Refresh the living docs. I've done a few sessions of work and PLAN.md is out of date._

**Tier upgrade**
> _This project has grown. Let's upgrade from light to standard._
