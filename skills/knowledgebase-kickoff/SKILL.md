---
name: knowledgebase-kickoff
description: Bootstrap a project knowledge base — folder skeleton, entity-page design, SCHEMA/CLAUDE/README scaffolding, an ingest-sources skill, .gitignore, git init, and initial commit. Use when the user wants to set up a knowledge base or queryable source of truth for a stakeholder-heavy project with meetings, emails, and documents.
---

# Kickoff Knowledge Base Project

Bootstrap a new project following the knowledge-base-per-project pattern: raw sources → LLM-maintained entity pages → queryable, auditable source of truth.

## When to use

Use this skill when the user wants to set up knowledge management for a project that:
- Involves many stakeholders, frequent meetings, and lots of emails/documents.
- Requires supplier or third-party accountability tracking.
- Needs a queryable source of truth maintained incrementally by an AI agent.

## Pre-flight

1. **Determine target directory.** Default: current working directory. If it's non-empty OR already contains any of the scaffolding files (`SCHEMA.md`, `CLAUDE.md`, `AGENTS.md`, `README.md`), STOP and confirm with the user before proceeding.
2. **Gather project values.** Ask the user for (or derive from conversation context):
   - **`PROJECT_NAME`** — human-readable, e.g., "Warehouse Automation Rollout"
   - **`PROJECT_DESCRIPTION_SHORT`** — one sentence, ≤ 30 words. What the project is.
   - **`PROJECT_DESCRIPTION_LONG`** — a paragraph (80–150 words) covering scale, stakeholders, timeline, and what makes this project complex.
   - **`OWNER_NAME`** — project owner's full name.
   - **`OWNER_EMAIL`** — project owner's email.
   - **`TEAM_DETAILS`** — a paragraph describing who's on the user's side, who the delivery partner is, and any other relevant structure.
   
   Confirm the values with the user before writing files.

## What to create

Mirror this skill's `templates/` tree (resolved relative to this SKILL.md) into the target directory, substituting placeholders:

### Folders
```
sources/{emails,transcripts,documents,ingested/{emails,transcripts,documents}}
people/
organizations/
workstreams/
meetings/
.claude/skills/ingest-sources/
```

### Files (from `templates/`)
- `README.md`
- `CLAUDE.md` — copy to `AGENTS.md` as well (identical)
- `SCHEMA.md`
- `LOG.md`
- `PLAN.md` — the PM action checklist
- `SOURCES-CHECKLIST.md` — the data-collection audit
- `.gitignore`
- `.claude/skills/ingest-sources/SKILL.md`

### Placeholders

Template files contain `{{PLACEHOLDER}}` tokens. Substitute with user-provided values before writing to the target:

| Token | Value source |
|---|---|
| `{{PROJECT_NAME}}` | User-provided project name |
| `{{PROJECT_DESCRIPTION_SHORT}}` | User-provided one-line description |
| `{{PROJECT_DESCRIPTION_LONG}}` | User-provided context paragraph |
| `{{OWNER_NAME}}` | User-provided owner name |
| `{{OWNER_EMAIL}}` | User-provided owner email |
| `{{TEAM_DETAILS}}` | User-provided team paragraph |

### Post-creation steps

1. `git init -q` in the target directory.
2. `git add -A` and commit with message `chore: initial knowledge base skeleton` (Co-Authored-By: Claude).
3. Report to the user:
   - What was created.
   - Confirmed owner + project name.
   - Suggested next action: drop the first sources into `sources/{emails,transcripts,documents}/` and invoke the `ingest-sources` skill.

## Maintenance

The `templates/` tree in this skill is the canonical scaffolding — there is no external reference project. When work in a bootstrapped knowledge base improves its scaffolding in a way that generalizes, fold the improvement back into the templates here, re-inserting `{{PLACEHOLDERS}}` where project-specific values were substituted. This is the same compounding loop as the `build` skill's Close phase.

## What this skill does NOT do

- Does not create entity pages speculatively — people, workstreams, organizations emerge from data during ingestion.
- Does not ingest any sources — that is the `ingest-sources` skill's job, invoked after kickoff.
- Does not overwrite existing scaffolding. If any target file already exists, STOP and confirm.
- Does not push to any remote.

## Output to user after kickoff

Report concisely:
- Target directory.
- Files created (brief list).
- Git commit hash.
- Next action: drop sources into `sources/` and invoke `ingest-sources`.
