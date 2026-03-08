# Kata

*A practiced form for building software with AI agents.*

In martial arts, a kata is a sequence of movements practiced until they become instinct — correct form achieved not through constant supervision, but through deeply internalized principle. This is the same idea applied to AI-assisted development. Not instructions handed to an agent at the start of each session and quietly forgotten. Contracts that live in the codebase, survive every context reset, and keep agents building in the right direction without anyone watching.

## Why This Exists

After working with AI agents on real projects for a while, a pattern became impossible to ignore. The agent would start strong — exploring alternatives, following the conventions, building with care. Then, gradually, it would drift. Complexity crept in. The point of what was being built got lost. Fragility appeared in random places. Bugs hid inside codebases that looked fine from the outside. Instructions given once — use schemas, enforce invariants, write tests — would be followed for a session or two, then quietly forgotten. The agent would get stuck on the same approach and stop exploring. At the end of each session, the next one started almost from scratch.

The instinctive response is to add more: more agents, more orchestration, more elaborate frameworks. But that instinct is wrong. Complex wrappers are the problem dressed up as a solution — they age fast, they break in surprising ways, and they obscure what's actually happening. The agentic AI landscape moves so fast that anything baroque is obsolete in months.

The real problem is not that agents are dumb. It's that they have no durable memory of the system they're building. Every session, the agent has to rediscover the architecture, the decisions, the boundaries — or it doesn't, and it drifts. The fix isn't more orchestration. It's contracts. Clear, testable, project-specific contracts that live in the codebase and survive context resets.

Simplicity is not a constraint here. It is the goal. A system with fewer moving parts is easier to understand, easier to maintain, and easier to hand to an agent without watching it unravel. The most elegant solution is the one that couldn't reasonably be simpler — and tends to be the one that lasts.

## Principles

- **Contracts over instructions** — instructions decay; testable invariants don't
- **Thin routing, deep projects** — AGENTS.md is a directory; intelligence lives in per-project docs
- **One agent, two modes** — build and review are skills, not separate agents
- **Iterate, consolidate** — start bare, add rules when problems appear, prune when bloated
- **Tiers scale with complexity** — a weekend script doesn't need production ceremony

## Structure

```
kata-agents/
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
│   │       ├── standard-architecture.md
│   │       ├── standard-contracts.md
│   │       ├── full-architecture.md
│   │       └── full-contracts.md
│   └── review/
│       └── SKILL.md           # Review skill (observe + check + simplify + report)
```

## Deployment

1. Copy `rules/` to your OpenClaw workspace (`~/.openclaw/workspace/rules/`)
2. Copy `skills/build/` and `skills/review/` to workspace skills folder
3. Add the contents of `agents-md-patch.md` to your workspace `AGENTS.md`
4. Optionally register skills in OpenClaw config for auto-discovery

## How It Works

### For new projects
The build skill detects no architecture docs and enters bootstrap mode. It asks about project intent, selects a tier (light/standard/full), and scaffolds the foundation — architecture doc, contracts, schemas, initial tests. Then coding begins with guardrails in place.

### For existing projects
The build skill reads the existing architecture and contracts. If none exist, it offers to discover the architecture from code (brownfield bootstrap). From there, all changes are verified against the project's own contracts.

### For ongoing work
Before coding: read project docs. While coding: follow rules. After coding: verify against contracts. If something drifts, the review skill catches it.

### Tier upgrades
Start light, upgrade when complexity warrants it. The build skill reads the current tier from ARCHITECTURE.md frontmatter and can scaffold additional artifacts when upgrading.
