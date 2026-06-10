# SCHEMA

Technical specification for the {{PROJECT_NAME}} knowledge base. Defines folder layout, file conventions, citation format, and the ingest/query workflows. Read `README.md` first for project context.

## Design principles

1. **Sources are immutable.** Raw emails, transcripts, and documents in `sources/` are never edited. After ingestion they move to `sources/ingested/`.
2. **Entity pages are primary for queries.** For routine questions, read entity pages. Raw sources are a **fallback** — re-read them when entity pages are insufficient, when the user wants a verbatim quote, or when you suspect an extraction error. The goal is token efficiency, not information hiding.
3. **Meeting summaries are first-class entity pages.** Files under `meetings/` are read during queries like any other entity. Raw transcripts under `sources/ingested/transcripts/` are the archival backup.
4. **Citations are provenance.** Every claim cites its source by filename. For high-stakes facts (commitments, decisions, change requests, budget entries), embed a short verbatim quote.
5. **Structure emerges from data.** Most entity folders are created only when the first record of that type is extracted. The skeleton is deliberately minimal.
6. **No speculation.** Write only what is evidenced. Flag uncertainty in `LOG.md`.
7. **Sensitive data.** This KB is internal-only — never paste source content into third-party tools. Redact obvious secrets in entity pages and flag in `LOG.md`.

## Folder layout

### Top-level files (always present)
```
README.md                  Human narrative overview.
CLAUDE.md / AGENTS.md      Agent behavioral contract (identical).
SCHEMA.md                  This file — technical spec.
LOG.md                     Append-only ingest log + flags.
PLAN.md                    Project-level todo checklist (PM action list).
SOURCES-CHECKLIST.md       Canonical list of information the project needs,
                           ticked off as sources are ingested.
.gitignore
```

### Sources (always present)
```
sources/
  emails/                  .md, .txt, .eml
  transcripts/             .md, .txt, .vtt
  documents/               .pdf, .docx, .pptx, .xlsx, .md, .txt
  ingested/                Moved here after processing. Re-read only on demand.
    emails/
    transcripts/
    documents/
```

### Entity folders (always present — created at kickoff)
```
organizations/             One file per organization.
people/                    people/<org-slug>/<person-slug>.md — activity log per person.
workstreams/               One file per topic/area.
meetings/                  meetings/<YYYY-MM-DD>-<slug>.md — first-class summaries.
```

### Entity folders created on first record (NOT pre-created)
```
commitments/register.md                Supplier/internal promises.
decisions/NNNN-<slug>.md               ADR-format formal decisions.
risks/register.md                      Risk register.
assumptions/register.md                Things we're betting on without proof.
dependencies/register.md               What we need from whom, by when.
stakeholders/register.md               Stakeholder analysis: RACI, power/interest, comm prefs.
milestones.md                          Canonical project timeline (single file).
integrations/register.md               Integration inventory (summary table).
integrations/<slug>.md                 Detailed notes for complex integrations.
budget/register.md                     Financial tracking.
change-requests/CR-NNNN-<slug>.md      One file per formal change request.
dashboards/                            LLM-regenerated rollups. Never hand-edited.
```

## Entity catalog — directory listings are the index

There is no INDEX.md. To enumerate entities:
- `ls people/*/` — all people (two-level).
- `ls workstreams/` — all workstreams.
- `ls organizations/`, `ls meetings/`, etc.
- `find . -name register.md` — all registers.

The agent lists what it needs when it needs it. No index file to keep in sync.

## File conventions

- **Slugs**: lowercase, hyphenated, ASCII-folded.
- **Dates**: ISO `YYYY-MM-DD`. Resolve relative dates to absolute before writing.
- **Frontmatter**: every entity file begins with YAML. Person example:
  ```yaml
  ---
  type: person
  name: Jane Smith
  org: acme-partners
  role: migration lead
  first_seen: 2026-04-15
  last_updated: 2026-04-20
  ---
  ```
- **Register tables**: markdown tables with a monotonic id column (`C-0001`, `R-0001`, `A-0001`, `D-0001`, `I-0001`, etc.). Rows are never deleted; statuses are updated in place.

## Citation format

**Low-stakes facts** (activity notes, topics discussed):
```
- Joined the governance cadence. [src: sources/ingested/transcripts/2026-04-18-governance.md]
```

**High-stakes facts** (commitments, decisions, change requests, budget lines): embed a verbatim quote.
```
| C-0007 | Jane Smith | acme | SSO config delivered by May 3 | 2026-05-03 | open | "We'll have SSO configured and tested by May 3rd" — sources/ingested/transcripts/2026-04-18-governance.md |
```

## Distinction: `people/` vs `stakeholders/register.md`

- **`people/<org>/<person>.md`** — activity log. What this person said, committed to, participated in. Every named individual gets one.
- **`stakeholders/register.md`** — analysis table. RACI per workstream, power/interest rating, communication preferences. Only stakeholders whose influence matters (decision makers, blockers, heavy consumers).

A person can appear in both. People pages are automatic; stakeholder register entries require evidence of their role (org chart, RACI matrix, steering committee list, explicit stakeholder analysis).

## Ingest workflow

New files in `sources/{emails,transcripts,documents}/` → invoke the `ingest-sources` skill. On each ingest, the skill:
1. Reads the source once.
2. Classifies it.
3. Extracts entities across all applicable categories.
4. Updates `SOURCES-CHECKLIST.md` based on what the document satisfies.
5. Moves the source to `sources/ingested/`.
6. Logs to `LOG.md`.

## Query workflow

1. List the relevant entity folders for the question.
2. Read only the entity pages needed — meeting summaries are first-class.
3. If entity pages are insufficient → read the relevant file from `sources/ingested/`.
4. Cite sources by path; embed verbatim quotes for high-stakes claims.

## What agents must NOT do

- Read `sources/ingested/` files *routinely* during queries — only on demand per rule above.
- Pre-create workstreams, decisions, risks, commitments, etc. without evidence.
- Merge two people or organizations with similar names without explicit user confirmation.
- Hand-edit `dashboards/` files — those are regenerated.
- Paste source content into third-party services.
- Invent dates, names, roles, or commitments not in a source.
