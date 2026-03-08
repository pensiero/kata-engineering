# Zanshin 残心

*A minimal and elegant practice for building software with AI agents.*

In martial arts, zanshin is the awareness that remains after the technique — the mind that doesn't relax, doesn't drift, stays present. A practitioner without zanshin executes correctly once. With zanshin, they remain aligned.

This applies the same idea to agentic AI. A session ends, the context resets, and the agent starts fresh — the alignment gone. The question isn't how to make agents smarter. It's how to make them remain.

Dave Thomas brought the code kata to software. Zanshin is what a good kata produces.

## Why This Exists

After working with AI agents on real projects for a while, a pattern became impossible to ignore. The agent would start strong — exploring alternatives, following the conventions, building with care. Then, gradually, it would drift. Complexity crept in. The point of what was being built got lost. Fragility appeared in random places. Bugs hid inside codebases that looked fine from the outside. Instructions given once — use schemas, enforce invariants, write tests — would be followed for a session or two, then quietly forgotten. The agent would get stuck on the same approach and stop exploring. At the end of each session, the next one started almost from scratch.

The obvious response is to add more — more agents, more orchestration, a more elaborate setup. It's the wrong instinct. Complex systems age badly, break in places you don't expect, and hide what's actually going wrong. The agentic landscape moves fast enough that anything baroque is obsolete within months.

The real problem is simpler. Agents have no durable memory of the system they're building. Every session, the architecture has to be rediscovered — or it isn't, and things drift. The fix isn't more orchestration. It's contracts. Clear, testable, project-specific invariants that live in the codebase and survive every reset.

## Principles

- **Contracts over instructions** — instructions decay; testable invariants don't
- **Thin routing, deep projects** — AGENTS.md is a directory; intelligence lives in per-project docs
- **One agent, two modes** — build and review are skills, not separate agents
- **Iterate, consolidate** — start bare, add rules when problems appear, prune when bloated
- **Tiers scale with complexity** — a weekend script doesn't need production ceremony

## Structure

```
zanshin-agents/
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

1. Copy `rules/` to your workspace (example if you are using OpenClaw: `~/.openclaw/workspace/rules/`)
2. Copy `skills/build/` and `skills/review/` to workspace skills folder
3. Add the contents of `agents-md-patch.md` to your workspace `AGENTS.md`
4. Optionally register skills in config for auto-discovery

## How It Works

### For new projects
The build skill detects no architecture docs and enters bootstrap mode. It asks about project intent, selects a tier (light/standard/full), and scaffolds the foundation — architecture doc, contracts, schemas, initial tests. Then coding begins with guardrails in place.

### For existing projects
The build skill reads the existing architecture and contracts. If none exist, it offers to discover the architecture from code (brownfield bootstrap). From there, all changes are verified against the project's own contracts.

### For ongoing work
Before coding: read project docs. While coding: follow rules. After coding: verify against contracts. If something drifts, the review skill catches it.

### Tier upgrades
Start light, upgrade when complexity warrants it. The build skill reads the current tier from ARCHITECTURE.md frontmatter and can scaffold additional artifacts when upgrading.
