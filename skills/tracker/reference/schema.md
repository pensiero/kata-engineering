# TRACKER.json — the format

One JSON object. It is the record: versioned in git, readable by any agent,
editable by hand. Its page (`TRACKER.html` beside it) is generated from it by
`scripts/tracker.py build`, which validates everything below first.

## Where trackers live

Each tracker's page sits beside it with the same name and an `.html` suffix.

- `TRACKER.json` at the repository root — the project's main, long-lived
  tracker (what used to be the tracking half of `PLAN.md`).
- `trackers/<name>.json` — a short-lived tracker for one effort (a review, a
  migration, an incident). Closed and deleted when the effort ends.
- A tracker holding private material goes wherever the project keeps private
  files (for example a gitignored `personal/trackers/`). The project's own
  routing rules decide, never this skill.
- An item that grows too big for its tracker becomes its own tracker,
  `trackers/<name>.json`; the item keeps `spawned` pointing at it.

## Top level

```json
{
  "schema": 3,
  "title": "Compass · Calculation review",
  "summary": "Every finding from the 5 October review and where it stands. Temporary: deleted once every item is closed.",
  "principles": ["Fix what is wrong before what is untidy."],
  "items": [ … ]
}
```

| Field | Meaning |
|---|---|
| `schema` | `3`. Schema 1 and 2 files had sections (`groups`, and a `group` on each item): `tracker.py` reads them as one list, sections in order, and any write drops them and sets `3`. |
| `title` | `<Project> · <scope>`: `Compass · Plan` for the main tracker, `Compass · Calculation review` for one effort. At most 60 characters. Also the page's title. |
| `summary` | Two sentences, at most 240 characters. First what it holds, then how long it lives ("Long-lived: …" or "Temporary: deleted once every item is closed."). Pointers to other docs belong in the project's `CLAUDE.md`, not here. |
| `principles` | Optional. Rules an agent works by when nobody is there to ask (a `PLAN.md`'s "Prioritization"). For agents: no page shows them. |
| `items` | The work, one list in the order of work: an agent takes the first `todo` nothing blocks. |

## Items

```json
{
  "id": "A2",
  "title": "A short, large round trip dominates a holding's yearly rate",
  "kind": "decision",
  "status": "waiting",
  "for": "agent",
  "context": "What is true now and why it matters, with the evidence.",
  "plan": "What the agent will do, including any assumption it is making.",
  "question": "The one thing the owner needs to answer.",
  "thread": [
    { "by": "agent", "at": "2026-10-05T15:04:42Z", "text": "…" },
    { "by": "owner", "at": "2026-10-05T18:10:03Z", "text": "…" }
  ],
  "decision": "",
  "outcome": "",
  "refs": [],
  "table": [["Bar", "Days shown"], ["1.5×", "206"]],
  "blocked_by": [],
  "spawned": "",
  "created": "2026-10-05",
  "updated": "2026-10-05",
  "closed": ""
}
```

| Field | Required | Meaning |
|---|:-:|---|
| `id` | ✓ | Unique, short, stable. Letters, digits and `_ - . ~ : @ +` only (it heads the owner's copied replies as `[id]`). Never reused. `new` is reserved: the owner's new items arrive as `[new]` and get the id `new-<n>`. |
| `title` | ✓ | What the item is, in the owner's words, not the code's. |
| `kind` | | `task` (default): the agent can just do it. `decision`: needs the owner's view. `check`: needs something only the owner can look at. |
| `status` | ✓ | In the order they are always shown: `draft` (not ready for an agent), `waiting` (needs the owner), `todo`, `doing` (started and not finished, however long it runs), `done`, `dropped` (shown as "Not doing"). |
| `for` | | `agent` (default) or `me`: a to-do of the owner's own, which the agent never works and the owner archives when done. |
| `fresh` | | `true` on an item the owner added, until an agent first works on it. While fresh, the owner may still rewrite or delete it. |
| `unread` | | `true` when the owner wrote something the agent has not processed: a new item, a promoted draft, a reply, a reopening. The agent clears it once processed. |
| `context` | | What is wrong or what is wanted, with the evidence. |
| `plan` | | How it will be done, and any assumption made. For a `decision`, the agent's recommendation. |
| `question` | when `waiting` | The single open question. Clear it once answered. |
| `thread` | | The conversation, oldest first. `at` is a full ISO timestamp. The owner's entries are added by `tracker.py reply`, from text copied off the page or said in chat; the agent's are its follow-ups. Append only. |
| `decision` | | The settled answer, in one or two sentences. This is what stops a question being asked again. |
| `outcome` | when `done` or `dropped` | What was done and where, or why not. |
| `refs` | | Where the outcome lives: commits, files, PRs, docs. |
| `table` | | Optional small data table; first row is the header. |
| `blocked_by` | | Items that must close first: an id in this tracker, or `<project>/<id>` for another registered project. |
| `spawned` | | The tracker this item grew into (`trackers/<name>.json`). The item stays `doing` until that tracker closes. |
| `created`, `updated` | | ISO dates. |
| `closed` | | When it closed: the archive's order, newest first. Written by the hub and by `build`; an item that reopens loses it. |

## Status, and what moves it

Every view shows the same five tabs, in this order, each left out when empty:
**Draft** (`draft`), **Needs you** (`waiting`, and any open `for: me` item),
**To do** (`todo`), **In progress** (`doing`), **Archive** (`done`, `dropped`).

| From | To | When | Who |
|---|---|---|---|
| — | `draft` | The owner notes something not ready for the agent | owner |
| `draft` | `todo` | The owner promotes it | owner |
| `todo` | `draft` | Not ready for an agent after all | owner |
| — | `todo` | An item is added | agent, or the owner (`[new]`, or the hub) |
| `todo` | `doing` | Work starts | agent |
| any open | `waiting` | The agent needs the owner; `question` is set | agent |
| `waiting` | `todo` / `doing` | A reply settles it; `decision` is written, `question` cleared | agent |
| `waiting` | `waiting` | A reply raises a follow-up; the agent adds a thread entry and a new `question` | agent |
| any | `done` | Finished; `outcome` and `refs` written | agent |
| any | `dropped` | Not going to happen; `outcome` says why | agent, after the owner agrees |
| any open | `done` / `dropped` | The owner archives it, with their reason if they give one | owner |
| `done` / `dropped` | `todo` | The owner reopens it, saying why in the thread | owner |

## Who writes what

The owner writes intents; the agent writes the record. The owner's writes
come through the hub (`kata-tracker`), or as replies copied off the page and
added by `tracker.py reply`. They are the functions in `tracker.py`, applied by
`tracker.py act`, which re-reads the file first and refuses, with the reason,
when the action no longer applies:

| The owner may | Limit |
|---|---|
| add an item (`todo` or `draft`, theirs or the agent's) | — |
| rewrite or delete an item they added | only while `fresh`; after that a rewrite becomes a reply |
| promote a draft, or send a to-do back to draft | — |
| move an item before another, or last | — |
| rewrite the tracker's `title` and `summary` | — |
| reply on any item | — |
| rewrite or delete their reply | only while no agent has read it: the item is `unread` and no agent entry follows |
| reopen a closed item | with a reason, unless it is their own to-do |
| archive an open item as done or not doing | — |

Everything else (status, plan, question, decision, outcome, refs, splitting
and spawning) is the agent's. The agent never acts on a `draft` or a
`for: me` item, and it clears `fresh` and `unread` when it works an item.

## Size

A tracker is read whole, by agents and by its page. When closed items grow
too many to read past, retire them: their `decision` and `outcome` go to
`DECISIONS.md` or git history, and the items are deleted.
