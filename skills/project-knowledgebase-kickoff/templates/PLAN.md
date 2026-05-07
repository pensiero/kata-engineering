# PLAN

Project-level todo checklist for {{PROJECT_NAME}} — the PM action list. Update status as items complete. For *information we need to collect*, see `SOURCES-CHECKLIST.md`. This file is about **what to do**; that file is about **what to gather**.

## Status legend
- `[ ]` todo
- `[/]` in progress
- `[x]` done
- `[~]` deferred (see the Deferred section)

---

## This week

- [ ] Obtain the Statement of Work / contract from procurement and drop it into `sources/documents/`.
- [ ] Request the delivery partner's detailed project plan / Gantt.
- [ ] Identify and contact the executive sponsor — confirm success criteria, budget, decision rights.
- [ ] Establish the governance cadence with the delivery partner (day, format, attendees, agenda template).
- [ ] Schedule stakeholder interviews with key internal leads. Transcripts go into `sources/transcripts/`.
- [ ] Produce a first-pass current-state inventory of what's being changed / migrated / replaced.
- [ ] Identify internal dependency owners (per workstream).

## First month

- [ ] Resolve any major open strategic decisions — schedule decision forums with the sponsor + delivery partner.
- [ ] Build the stakeholder register with RACI per workstream (`stakeholders/register.md`).
- [ ] Define acceptance criteria per major deliverable.
- [ ] Draft the rollback / fallback plan for any high-risk transitions.
- [ ] Confirm compliance / legal / data-residency requirements. Record in `decisions/` or `assumptions/`.
- [ ] Secure budget baseline; set up burn tracking (`budget/register.md`).
- [ ] Agree the reporting rhythm to the steering committee (format, frequency, audience).
- [ ] Establish the change-request process with the delivery partner.
- [ ] Complete any required security / architecture sign-offs.

## Ongoing

- [ ] Ingest delivery partner's weekly status reports as they arrive.
- [ ] Ingest all governance and standup transcripts.
- [ ] Track every commitment; escalate slippages within 48h.
- [ ] Update `SOURCES-CHECKLIST.md` and `PLAN.md` after each ingest batch.
- [ ] Review `risks/register.md` and `assumptions/register.md` weekly — revalidate or promote to issues.
- [ ] Present workstream status to stakeholders on a regular cadence.

---

## Deferred — not now, but don't forget

These are identified needs deliberately deferred until current-week and first-month items are underway. When ready, pick up in this order:

- [~] **Stakeholder interview script** — draft 8–10 standardized questions to ask key people in week 1 (executive sponsor, delivery-partner PM, identity / security / ops / support / training leads). Keeps interview content comparable across conversations. Store as `sources/documents/interview-script.md` or as a skill under `.claude/skills/`.
- [~] **Project charter template** — questions the sponsor must answer: why this project, success criteria, budget ceiling, escalation path, decision rights. Fill in from a conversation with the exec sponsor and drop as `sources/documents/project-charter.md`.
- [~] **Dashboards generation skill** — LLM-regenerated rollup (status by workstream, open commitments, top risks, next milestones) written to `dashboards/`. Read from entity pages; never hand-edited. Becomes the stakeholder-facing view.

---

## Completed
_(none yet)_
