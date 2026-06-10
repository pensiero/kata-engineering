---
name: ingest-sources
description: Process new emails, meeting transcripts, Word documents, presentations, and PDFs dropped into sources/ and distill them into entity pages (people, organizations, workstreams, commitments, decisions, change-requests, risks, assumptions, dependencies, stakeholders, milestones, integrations, budget, meetings). Also updates SOURCES-CHECKLIST.md. Use when the user says "ingest sources", "process new sources", "update the knowledge base", or drops new files into any sources/ subfolder and asks to process them.
---

# Ingest Sources

You are maintaining a structured knowledge base for {{PROJECT_NAME}}. See `SCHEMA.md` for the full contract — this skill implements its ingest workflow.

## Preconditions

1. Read `SCHEMA.md`, the last ~30 lines of `LOG.md`, and `SOURCES-CHECKLIST.md` before processing anything. Skip if already done this session.
2. Identify unprocessed sources across all input folders:
   - `sources/emails/` — `.md`, `.txt`, `.eml`
   - `sources/transcripts/` — `.md`, `.txt`, `.vtt`
   - `sources/documents/` — `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.md`, `.txt`
   - Ignore anything under `sources/ingested/`.
3. If multiple sources are pending, process oldest first (by filename date if present, else mtime).
4. **Tool availability check** (first ingest only, or if tools have never been verified this session): run `which pandoc python3` via Bash. If either is missing AND the pending batch contains `.docx`/`.pptx`/`.xlsx`, stop and tell the user which tool to install (e.g., `brew install pandoc`, `pip install python-docx python-pptx docx2txt pandas openpyxl`). Record the check result in `LOG.md`.

## Document reading (before extraction)

Read the source using the appropriate method:

- **`.md` / `.txt` / `.eml` / `.vtt`**: use the `Read` tool directly.
- **`.pdf`**: use the `Read` tool directly (up to 20 pages per call; for larger PDFs, read in page chunks).
- **`.docx`**: `pandoc <filepath> -t markdown --wrap=none`. Fallback: `python3 -c "import docx2txt; print(docx2txt.process('<filepath>'))"`.
- **`.pptx`**: `pandoc <filepath> -t markdown --wrap=none`. Fallback: `python3 -c "from pptx import Presentation; prs=Presentation('<filepath>'); [print(s.text) for sl in prs.slides for s in sl.shapes if hasattr(s,'text')]"`.
- **`.xlsx`**: `python3 -c "import pandas as pd; print(pd.read_excel('<filepath>').to_markdown())"`.

If all methods fail, log the failure in `LOG.md` and skip the file (do not move it).

## Document classification

Before extracting entities, identify the document type:

| Type | Signals | Primary extractions |
|---|---|---|
| Meeting transcript / minutes | attendees, timestamps, Q&A | people, commitments, risks, decisions, meeting summary |
| Status report | RAG status, workstream updates | workstreams, commitments, risks, milestones |
| Project plan / Gantt | milestones, dates, owners, phases | workstreams, milestones, commitments, dependencies |
| Scope / requirements / SoW | deliverables, in/out of scope, SLAs | workstreams, decisions, risks, commitments, budget |
| Contract / SoW | deliverables, payment terms, penalties | commitments, budget, decisions |
| Proposal / presentation | options, recommendations, open questions | decisions pending, workstreams, risks, assumptions |
| Email thread | conversation, action items | people, commitments, risks, decisions, dependencies |
| Stakeholder analysis / RACI / org chart | roles, responsibilities | stakeholders, organizations, people |
| Integration / architecture doc | systems, data flows | integrations, dependencies, risks |
| Budget / invoice / payment | line items, totals, dates | budget, commitments |
| Change request | scope change, impact, pricing | change-requests, budget, decisions |
| Current-state inventory | lists of projects/spaces/apps | workstreams (one per migration unit), risks |
| Unknown | — | best-effort; classify as "unknown" in LOG.md |

Record the classification in `LOG.md`.

## Per-source extraction

For each unprocessed source, read it **once** through the reading method above, then extract the following. Create folders/files lazily — only if the relevant record exists in this source.

### 1. Organizations
New org mentioned (internal dept, supplier, vendor, third party) → create `organizations/<slug>.md` with frontmatter (`type: organization`, `name`, `role` e.g. "delivery partner" / "internal team", `first_seen`).

### 2. People (activity log)
Named individual → resolve org first → write to `people/<org-slug>/<person-slug>.md`:
- Append dated entry under `## Activity` with citation. Update frontmatter `last_updated`; fill in role/email/etc. if new.
- **Do NOT merge similar names.** Ambiguity (e.g., "M. Rossi" vs "Marco Rossi") → flag in LOG.md and ask the user.

### 3. Commitments
Explicit promise with an owner → `commitments/register.md` (create on first). Columns: `id | owner | org | commitment | due | status | source`. ID `C-NNNN`. Source = **verbatim quote** (≤ 25 words) + filename. **Dedup**: same owner + semantically similar commitment within a 14-day window → append source to existing row; don't duplicate.

### 4. Decisions
Explicit decision made OR formally pending → `decisions/NNNN-<slug>.md` (ADR format: Context, Options, Decision, Consequences, Status). Embed a **verbatim quote** showing who decided what.

### 5. Change requests
Formal CR (scope change from baseline SoW) → `change-requests/CR-NNNN-<slug>.md`. Sections: Context (what changed), Scope impact, Cost / time impact, Raised by, Approved by, Status (raised / approved / rejected / implemented), Source with verbatim quote.

### 6. Risks
Anything that could cause slippage → `risks/register.md`. Columns: `id | risk | likelihood | impact | owner | mitigation | source`. ID `R-NNNN`. Likelihood/impact `low`/`medium`/`high`. Dedup same as commitments.

### 7. Assumptions
Any "we assume X" / "we rely on Y being true" statement → `assumptions/register.md`. Columns: `id | assumption | risk_if_broken | owner | status | source`. ID `A-NNNN`. Status `holds` / `broken` / `validated`. Dedup.

### 8. Dependencies
Any "we need X from Y by Z" statement, internal or external → `dependencies/register.md`. Columns: `id | dependency | provider_owner | needed_by | blocks | status | source`. ID `D-NNNN`. Status `pending` / `at_risk` / `resolved` / `blocked`. Dedup.

### 9. Workstreams
Create `workstreams/<slug>.md` when EITHER:
- the topic is explicitly named as a workstream/phase/area (SoW section header, project plan row, status report column), OR
- the topic has now appeared in 2+ sources.

Otherwise note in LOG.md under "candidate workstreams". When a workstream file exists, append activity: dated entry + citation + status/blockers.

### 10. Milestones
Project plan, Gantt, or dated deliverable list → `milestones.md` (single file). Columns: `milestone | owner | target_date | status | depends_on | source`. Status `on_track` / `at_risk` / `slipped` / `done`. Sort by target_date.

### 11. Integrations
System-to-system connections mentioned (SSO, CI/CD, Slack, ServiceNow, bots, webhooks, custom APIs) → `integrations/register.md`. Columns: `id | name | type | current_state | target_state | migration_owner | complexity | source`. ID `I-NNNN`. For complex integrations that need more detail, create `integrations/<slug>.md`.

### 12. Budget
Financial line items (baseline, invoices, commitments with cost, penalties) → `budget/register.md`. Suggested structure: a `## Baseline` table, an `## Invoices` table, a `## Changes` table. Each line with verbatim quote + source.

### 13. Stakeholder analysis
RACI matrices, steering committee rosters, explicit stakeholder analysis → `stakeholders/register.md`. Columns: `workstream | stakeholder | org | role (R/A/C/I) | power | interest | comm_preference | source`. Power/interest `low`/`med`/`high`. This is **analysis** — distinct from `people/` which is activity.

### 14. Meeting summary (transcripts only)
Write `meetings/<YYYY-MM-DD>-<slug>.md`. **First-class entity page** — read during queries.
- Frontmatter: `type: meeting`, `date`, `series` (`daily-supplier-standup`, `governance`, `steerco`, `ad-hoc`), `attendees`.
- Sections: **Topics discussed**, **Decisions** (by id), **Commitments** (by id), **Open questions**, **Follow-ups**.
- Under ~400 words. Raw transcript stays under `sources/ingested/transcripts/` for verbatim fallback.

## SOURCES-CHECKLIST.md update

After extraction, map the document's classification + content to checklist items in `SOURCES-CHECKLIST.md`. Examples:

| If the document is… | Tick these items |
|---|---|
| A signed SoW/contract | "Statement of Work / contract"; feed into budget if it has figures |
| Supplier's Gantt | "Supplier's project plan / Gantt" |
| A Jira/Confluence/JSM export listing projects/spaces/queues | "Current-state inventory: …" (the relevant one) |
| A plugin inventory | "Apps & plugins inventory" |
| A RACI matrix | "Stakeholder register with RACI" |
| A security / legal sign-off | "Security review sign-off" / "Compliance requirements" |
| An invoice | "Invoice / payment schedule" |
| Executive sponsor appointment letter / email | "Executive sponsor identification" |

When you tick `[x]`, append `— [src: <source filename>]` to the line so the ingest trail is visible. For partial coverage mark `[/]` and note what's still missing.

If the document doesn't match any checklist item, skip — it's still useful data, just not on the checklist.

## Sensitive data handling

Apply this filter **before writing any entity page**. Assume the KB can be read by any employee in the company.

### Always remove or redact

| Pattern | How to handle |
|---|---|
| Verbatim quotes expressing negative opinions about a named partner or vendor (past failures, near-terminations, quality criticism) | State the factual outcome only (e.g. "partner relationship ended; new partner selected") — no quotes |
| Quotes revealing the client's negotiation position, commercial leverage, or pricing threshold that won a vendor selection | Remove the quote; reference the source file only |
| Any statement about *why* a named individual is unavailable (health, personal, disciplinary) | Record the fact of unavailability and the dates only |
| Personal grievances, HR-sensitive content, or performance criticism about any named individual | Omit entirely; note "HR-sensitive content omitted" in LOG.md |
| Specific PO numbers attributed to a named individual | Record PO numbers separately from names; use role title (e.g. "Category Manager") not the person's name in the same field |
| Phone numbers | Record email addresses only; remove phone numbers |
| Verbatim quotes framing internal contract weaknesses as specific attack vectors (e.g. what a vendor "could" claim) | Replace with a neutral description of the gap and the mitigation required |

### Reframe to neutral facts — examples

| Raw / sensitive | Reframed |
|---|---|
| "Partner X failed / we were on the verge of terminating" | "Prior partner relationship ended; new partner selected" |
| "It's not a vacation" (re: someone's absence) | "Currently unavailable; coverage arranged" |
| "You are right, this is embarrassing" | "Concern acknowledged; corrected" |
| "They could claim the MDs are exhausted and ask for 500 more" | "Deliverables gap identified in T&M contract; mitigation: deliverables-based addendum required" |

### Always retain

- Budget totals and approved amounts (project accountability record)
- Vendor comparison pricing (internal procurement record — keep in budget/register.md and decision ADRs)
- Risk descriptions phrased as project risks, not as attack instructions
- Decisions and their factual rationale
- Obvious secrets (passwords, tokens, API keys) → redact as `<redacted:credential>`; flag in LOG.md

### Logging

Flag every content item removed or reframed under this rule with `[SENSITIVITY-FILTER]` in the LOG.md entry for that source.

Never paste source content into third-party services.

## Post-processing per source

1. **Move the source**: preserve subfolder structure under `sources/ingested/`.
   - `sources/emails/foo.md` → `sources/ingested/emails/foo.md`
   - `sources/documents/plan.docx` → `sources/ingested/documents/plan.docx`
2. **Append to LOG.md**: document type, counts per entity type (e.g. "3 commitments, 2 risks, 1 decision, 4 assumptions"), new files created, checklist items ticked, flags/ambiguities, sensitive-data notes.
3. **Update `SOURCES-CHECKLIST.md`** per mapping above.

## Guardrails

- **Default read scope**: never routinely re-open files under `sources/ingested/`. Re-read only on explicit user request, for verbatim quotes, or when extracted pages are demonstrably insufficient.
- **No speculation**: if a source doesn't state a date, owner, or status, write `unknown` or omit.
- **Same-name ambiguity**: STOP and ask the user. Log the ambiguity.
- **Batch size**: if more than 10 unprocessed sources exist, process 10, report progress, ask to continue.
- **Idempotency check**: before processing, confirm the source filename isn't already listed in `LOG.md`. If it is, skip and warn.

## What this skill does NOT do

- Does not answer user questions or generate dashboards — separate flows.
- Does not pre-create register files without evidence.
- Does not merge people, organizations, or workstreams without explicit user confirmation.
- Does not paste source content into external tools.
- Does not edit `PLAN.md` — that file belongs to the project owner.

## Output to user after each run

Report concisely:
- Number of sources processed and their classifications.
- New entity pages / registers created.
- Counts added per entity type (commitments, risks, assumptions, etc. with ids).
- `SOURCES-CHECKLIST.md` items ticked (`[x]`) or partially ticked (`[/]`).
- Open flags/ambiguities needing user input.
- Sensitive-data flags, if any.
- Suggested next action.
