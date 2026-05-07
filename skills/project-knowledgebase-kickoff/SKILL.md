---
name: project-knowledgebase-kickoff
description: Bootstrap a new project knowledge base with the same structure as the Atlassian Cloud migration project — folder skeleton, entity-page design, SCHEMA/CLAUDE/README scaffolding, the ingest-sources skill, .gitignore, git init, and initial commit. Use when the user says "kickoff a new project", "set up a new knowledge base", "bootstrap a KB project", or wants the same setup replicated for a different project.
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

Mirror the template tree at `~/.claude/skills/kickoff-kb-project/templates/` into the target directory, substituting placeholders:

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

## Maintenance — KEEP THIS SKILL IN SYNC

The templates in this skill are a snapshot of the reference implementation at `/Users/oscar/Projects/atlassian-migration`. **Whenever scaffolding in that reference project changes — `SCHEMA.md`, `CLAUDE.md`, `AGENTS.md`, `README.md`, `PLAN.md`, `SOURCES-CHECKLIST.md`, `LOG.md`, `.gitignore`, or `.claude/skills/ingest-sources/SKILL.md` — the corresponding template in this skill must be updated to match.**

Sync procedure:
1. Edit the scaffolding file in the reference project.
2. Copy the updated content into the corresponding template under `~/.claude/skills/kickoff-kb-project/templates/`.
3. Re-insert `{{PLACEHOLDERS}}` where project-specific values had been substituted.
4. Commit both changes in the reference project (or separately, whichever the user prefers).

When updating scaffolding in the reference project, proactively ask: "Should I also update the kickoff-kb-project skill templates to match?" Do not silently let them drift.

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
