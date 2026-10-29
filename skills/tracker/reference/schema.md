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

## Top level

```json
{
  "schema": 1,
  "title": "Compass · Calculation review",
  "summary": "Every finding from the 5 October review and where it stands. Temporary: deleted once every item is closed.",
  "principles": ["Fix what is wrong before what is untidy."],
  "groups": [
    { "id": "now",   "title": "Now",   "note": "The one active loop.", "gate": "" },
    { "id": "next",  "title": "Next",  "note": "", "gate": "The Now loop has produced evidence." }
  ],
  "items": [ … ]
}
```

| Field | Meaning |
|---|---|
| `schema` | Always `1`. |
| `title` | `<Project> · <scope>`: `Compass · Plan` for the main tracker, `Compass · Calculation review` for one effort. At most 60 characters. Also the page's title. |
| `summary` | Two sentences, at most 240 characters. First what it holds, then how long it lives ("Long-lived: …" or "Temporary: deleted once every item is closed."). Pointers to other docs belong in the project's `CLAUDE.md`, not here. |
| `principles` | Optional. How to choose what comes next when nobody is there to ask (a `PLAN.md`'s "Prioritization"). The page shows them under "How the next item is chosen". |
| `groups` | Ordered sections. Their order is the order of work. `gate` says what must be true before a group starts; leave it empty when there is none. Typical sets: `now / next / later`, or one group per area for a review. |
| `items` | The work, in display order within each group. |

## Items

```json
{
  "id": "A2",
  "group": "now",
  "title": "A short, large round trip dominates a holding's yearly rate",
  "kind": "decision",
  "status": "waiting",
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
  "created": "2026-10-05",
  "updated": "2026-10-05"
}
```

| Field | Required | Meaning |
|---|:-:|---|
| `id` | ✓ | Unique, short, stable. Letters, digits and `_ - . ~ : @ +` only (it heads the owner's copied replies as `[id]`). Never reused. `new` is reserved: the owner's new items arrive as `[new]` and get the id `new-<n>`. |
| `group` | ✓ | One of the group ids. |
| `title` | ✓ | What the item is, in the owner's words, not the code's. |
| `kind` | | `task` (default): the agent can just do it. `decision`: needs the owner's view. `check`: needs something only the owner can look at. |
| `status` | ✓ | `todo`, `doing`, `waiting` (needs the owner), `done`, `dropped`. |
| `context` | | What is wrong or what is wanted, with the evidence. |
| `plan` | | How it will be done, and any assumption made. For a `decision`, the agent's recommendation. |
| `question` | when `waiting` | The single open question. Clear it once answered. |
| `thread` | | The conversation, oldest first. `at` is a full ISO timestamp. The owner's entries are added by `tracker.py reply`, from text copied off the page or said in chat; the agent's are its follow-ups. Append only. |
| `decision` | | The settled answer, in one or two sentences. This is what stops a question being asked again. |
| `outcome` | when `done` or `dropped` | What was done and where, or why it was dropped. |
| `refs` | | Where the outcome lives: commits, files, PRs, docs. |
| `table` | | Optional small data table; first row is the header. |
| `created`, `updated` | | ISO dates. |

## Status, and what moves it

| From | To | When | Who |
|---|---|---|---|
| — | `todo` | An item is added | agent, or the owner through `[new]` |
| `todo` | `doing` | Work starts | agent |
| any open | `waiting` | The agent needs the owner; `question` is set | agent |
| `waiting` | `todo` / `doing` | A reply settles it; `decision` is written, `question` cleared | agent |
| `waiting` | `waiting` | A reply raises a follow-up; the agent adds a thread entry and a new `question` | agent |
| any | `done` | Finished; `outcome` and `refs` written | agent |
| any | `dropped` | Not going to happen; `outcome` says why | agent, after the owner agrees |

The owner never edits the file: replying is the only thing the page lets them
do, and the agent writes the reply into the file.

## Size

A tracker is read whole, by agents and by its page. When done items crowd out
the open ones, archive them: their `decision` and `outcome` go to
`DECISIONS.md` or git history, and the items are deleted.
