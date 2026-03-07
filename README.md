# Agents Framework

A minimal, durable approach to AI-assisted software development.

## Philosophy

Complex agent wrappers expire in months. Project contracts last as long as the project. This framework invests in contracts and rules — not elaborate orchestration.

**Core principles:**
- **Contracts over instructions** — instructions decay; testable invariants don't
- **Thin routing, deep projects** — AGENTS.md is a directory; intelligence lives in per-project docs
- **One agent, two modes** — build and review are skills, not separate agents
- **Iterate, consolidate** — start bare, add rules when problems appear, prune when bloated
- **Tiers scale with complexity** — a weekend script doesn't need production ceremony

## Structure

```
agents-framework/
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
