# SOURCES CHECKLIST

Canonical list of information {{PROJECT_NAME}} needs. As documents are ingested, tick items off. This file answers the question **"what are we missing?"** and is the completeness audit for the KB.

The `ingest-sources` skill updates this automatically when a source satisfies an item. Manual updates are welcome for items the skill can't detect (e.g., "stakeholder register agreed with the sponsor").

## Status legend
- `[ ]` not yet sourced
- `[/]` partially sourced — some data in, more expected
- `[x]` sourced and ingested — note the source file
- `[N/A]` not applicable to this project

---

## Tier 1 — critical (need in week 1)

### Commercial & strategic
- [ ] **Statement of Work / contract** — scope, deliverables, SLAs, penalties, change-control terms.
- [ ] **Business case / project charter** — strategic driver, success criteria, budget approval.
- [ ] **Executive sponsor identification** — who is ultimately accountable on the internal side.
- [ ] **Delivery partner organization profile** — who they are, reference clients, team they're assigning.

### Plan & governance
- [ ] **Delivery partner's project plan / Gantt** — milestones, critical path, resource allocation.
- [ ] **Governance structure** — steering committee, decision rights, escalation matrix.
- [ ] **Stakeholder register with RACI** — who decides, consulted, informed, per workstream.

### Current-state inventory (what's being changed / migrated / replaced)
- [ ] Customize this section for this project — list each discrete area that needs a before-state inventory.

### Technical ecosystem (what connects to it)
- [ ] **Integration inventory** — every system that interacts with what's being changed.
- [ ] **Identity / SSO current state** — federation, MFA, group management.
- [ ] **Network / access considerations** — if relevant.

---

## Tier 2 — first month

### Commercial & control
- [ ] **Budget baseline** — total approved, contingency, payment milestones.
- [ ] **Invoice / payment schedule** — milestones triggering payment.
- [ ] **Change-request process** — who raises, approves, prices CRs.
- [ ] **Delivery partner SLAs and penalty clauses** — extracted from SoW.

### Operational readiness
- [ ] **Communication plan** — stakeholder reporting cadence + format; end-user comms plan.
- [ ] **Training & change management plan** — adoption support.
- [ ] **Acceptance criteria per deliverable** — sign-off definitions.
- [ ] **Rollback / fallback plan** — what happens if a major transition fails.
- [ ] **Performance baseline + targets** — current and expected post-change.

### Compliance & legal
- [ ] **Data residency requirements**.
- [ ] **GDPR / privacy compliance sign-off** — DPIA if needed.
- [ ] **Audit / retention policy**.
- [ ] **Security review sign-off**.

### Internal coordination
- [ ] **Internal dependency map** — which internal teams owe what, when.
- [ ] **Key-person risk** — who (on either side) is irreplaceable; what's the mitigation.

---

## Tier 3 — ongoing (populated over the project life)

- [ ] Delivery partner weekly status reports (ingest each week).
- [ ] Governance meeting transcripts (ingest each week).
- [ ] Ad-hoc meeting transcripts (ingest as they occur).
- [ ] Change requests (one document per CR).
- [ ] Invoice / payment events (each invoice ingested).
- [ ] Post-change adoption metrics.
- [ ] User feedback during / after any major transition.

---

## How the ingest skill updates this file

On each source ingested:
1. The skill classifies the document.
2. Maps the classification to one or more checklist items.
3. Marks `[x]` and appends the source path: `- [x] **Statement of Work / contract** — [src: sources/ingested/documents/2026-04-22-sow.pdf]`.
4. For partial satisfaction, marks `[/]` and notes what's still missing.

Items requiring human judgment (e.g., "executive sponsor identified") can be manually ticked when the condition is met.
