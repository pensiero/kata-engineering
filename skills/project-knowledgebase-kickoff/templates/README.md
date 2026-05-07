# {{PROJECT_NAME}} — Knowledge Base

## What this is

This repository is the **single source of truth** for {{PROJECT_DESCRIPTION_SHORT}}.

{{PROJECT_DESCRIPTION_LONG}}

This is not a code repository. It is a structured knowledge base, maintained incrementally by AI agents that ingest raw communication artefacts (emails, meeting transcripts, documents, presentations) and distill them into queryable, structured entity pages.

## Why this exists

A project of this scale involves many people, frequent meetings, cascading decisions, commitments from internal and external parties, and non-negotiable deadlines. Information typically gets scattered across emails, shared drives, tickets, and chat. Without a system to consolidate it, things fall through the cracks: a commitment made in one meeting gets forgotten days later; a risk flagged in an email never makes it to the steering committee; a new stakeholder joins and has no way to quickly understand the landscape.

This knowledge base solves that by being the place where everything lands and is organized. It is queryable — by a human asking an AI, or directly by reading the structured entity pages. It is updateable — new sources are ingested and the relevant pages updated, without re-reading everything from scratch. And it is auditable — every fact cites the source it came from.

## How it is organized

The structure is deliberately minimal and grows with the project:

- **`sources/`** — raw inputs (emails, transcripts, documents). Once ingested, they move to `sources/ingested/` and are read only on demand.
- **`people/`** — one file per named individual, organized by organization.
- **`organizations/`** — one file per organization (internal teams, suppliers, vendors).
- **`workstreams/`** — one file per topic/area of work.
- **`commitments/`** — a register of every commitment. The accountability tool.
- **`risks/`** — a risk register.
- **`decisions/`** — formal decisions recorded in ADR format.
- **`meetings/`** — first-class meeting summary pages.

The full technical specification — naming conventions, frontmatter, citation format, workflows — lives in `SCHEMA.md`.

## How to use it

**As a human**: ask an AI agent a question. Examples:
- *"What has the supplier committed to this month?"*
- *"Who should I invite to a meeting about topic X?"*
- *"What are the top three open risks right now?"*
- *"Draft an agenda for tomorrow's governance call."*

**As an agent**: read `CLAUDE.md` (or `AGENTS.md`) first. It tells you what your role is, what to read, and how to behave.

## Who owns this

{{TEAM_DETAILS}}

Project owner: {{OWNER_NAME}} ({{OWNER_EMAIL}}).
