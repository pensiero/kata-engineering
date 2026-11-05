---
name: tracker
description: Track a project's work items, the questions waiting on the owner, and what was done, in a versioned TRACKER.json with a static HTML page beside it that the owner opens from disk and replies on. Use when asked to track work or progress, keep a backlog or to-do list, list findings to fix one by one, collect the owner's answers, check whether the owner replied, work an item the owner launched ("/tracker work …"), or turn a PLAN.md into a tracker. Use it unasked whenever many things need the owner's check or decision together — a review's findings, a before/after list of changes, several open questions — instead of a long list in chat. Also use at the start of a session in a repository that has a TRACKER.json, and whenever the owner pastes replies copied from a tracker page.
---

# Tracker

A tracker is the tracking half of a `PLAN.md`, made exact: every item has a
status, a plan, the question it is waiting on and what was finally done. It
lives in the repository as `TRACKER.json` and is versioned like code. Beside
it sits `TRACKER.html`: a static page built from the file, which the owner
opens straight from disk (no server, nothing loaded from the network, nothing
uploaded) to read the tracker and type replies. The owner may also use the
Kata hub (`kata-tracker`), a local app over every project's trackers that
writes their intents straight into the files.

NOT for: why a decision was made (`DECISIONS.md`), what the system is
(`ARCHITECTURE.md`), hand-off instructions or design write-ups (ordinary docs).
A tracker item links to those; it does not contain them.

**Files.** Resolve this skill directory's real path (it is usually symlinked
into the agent's global skills directory). Everything below is relative to it:

- `reference/schema.md`: the file format, the statuses and who moves them,
  the page's database layout. Read it before writing a tracker.
- `scripts/tracker.py`: Python 3 standard library only. `new`, `check`,
  `build`, `brief`, `show`, `render`, `reply`. Run `build` after every hand
  edit: it checks the file, then rewrites its page.
- `assets/page.html` and `assets/style.css`: the template every tracker's page
  is built from, and the look it shares with the hub. Never edit a built page
  or the template per project; everything a page shows comes from its tracker.

---

## The rules that make it work

1. **The file is the record.** Edit `TRACKER.json`, then run `build`. The page
   is generated: never edit it, and if it disagrees with the file, rebuild it.
2. **The owner writes intents, the agent writes the record.** The owner adds
   items and drafts, rewrites their own items until you first work them,
   promotes drafts and sends to-dos back to draft, reorders items, rewrites
   the title and summary, replies (and rewrites a reply until you read it),
   archives any open item as done or not doing, and reopens
   (`reference/schema.md`, "Who writes what"). Every other status change,
   decision and outcome is yours, in the file. Never act on a `draft` or a
   `for: me` item.
3. **Everything stays local.** Never publish a tracker or its page anywhere
   (no artifacts, no gists, no hosted pages). It is shared the way the
   repository is shared, and a private tracker not at all.
4. **A question only when it is the owner's call.** A plain bug gets a plan and
   no question: say what you will do and do it. Ask when there is a real choice
   (a rule change, a trade-off, a preference) or when you are undecided, and put
   your recommendation in `plan` so the owner can answer "yes".
5. **Write for the owner.** Titles and context in the owner's words, with the
   evidence, and numbers when there are numbers. Follow the project's register
   and privacy rules: a tracker holding private data goes where the project
   keeps private files.
6. **Closing means saying what happened.** `done` needs an `outcome` and,
   where possible, `refs` (commit, file, PR). `dropped` needs the reason, and
   the owner's agreement. A settled question keeps its `decision`, so it is
   never asked again. `build` dates what closed, for the archive's order.
7. **Commit the tracker and its page with the work** that moved them, following the project's
   own commit rules. Git history is the tracker's history.

---

## Start a tracker

1. Pick the file: `TRACKER.json` for the project's main tracker,
   `trackers/<name>.json` for one effort (see `reference/schema.md`, "Where
   trackers live").
2. `python3 scripts/tracker.py new <file> --title "<Project> · <scope>" --summary "<what it holds>. <how long it lives>."`.
   A tracker is one list in the order of work, the same in every project:
   there are no sections, and where an item stands is its status. Every tracker
   follows the same title and summary shape (`reference/schema.md`), so two
   trackers' pages read alike. `new` writes the page too.
3. Write the items, first to do first, and `principles` if an agent needs rules
   to work by. What must happen first is `blocked_by`; what is not ready for an
   agent (an idea to argue, something to check again on a date or a condition)
   is a `draft`, saying what it waits for. Run `build`.
4. Tell the owner, in a line or two, what is in it, which items are waiting on
   them, and the page to open (`file://` + the page's absolute path).

## The page

`tracker.py build <file>` writes `<file>` with an `.html` suffix beside it
(`TRACKER.json` → `TRACKER.html`) with the tracker embedded. The owner opens it
from disk in any browser and reloads it after the agent rebuilds.

- Items sit in five tabs, always in this order, each left out when empty:
  Draft, Needs you, To do, In progress, Archive. The hub has the same five.
  The archive is by date, newest first; the others keep the list's order.
- Each waiting item has a reply box; other items take replies inside their
  conversation. Below the list, "Something new?" takes new items, one per
  paragraph. What the owner types is kept in that browser only.
- **Copy for the agent** copies every pending reply as text:

  ```text
  /tracker Replies to Compass · Plan (TRACKER.json):

  [paper-trial] Not running yet. Start it.

  [new] Add a weekly summary of what moved.
  ```

  It starts with `/tracker`, so pasting it into the chat invokes this skill,
  and the path in brackets is the tracker's file inside the repository.

  A reply disappears from the page's pending list once the rebuilt page shows
  it in the item's conversation.

The page is generated, deterministic and committed beside its tracker (a
private tracker's page stays private with it).

## Take the owner's replies

The owner pastes the copied text into the chat (it arrives as this skill's
arguments, starting "Replies to …"), or answers in chat directly.

1. Take the tracker's path from the first line. Save the pasted text to a scratch file outside the repository and run
   `python3 scripts/tracker.py reply <file> --from <scratch file>`. For an
   answer given in chat, `python3 scripts/tracker.py reply <file> <id> "<their words>"`.
   Each reply is appended to its item's `thread` as an `owner` entry, the page
   is rebuilt, and a reply already there word for word is skipped. A `[new]`
   reply becomes a new item: `todo`, last, id `new-<n>`, the
   owner's words as its title and context, `fresh` and `unread`. Nothing else
   changes.
2. Process them (below).

## Process the owner's replies

For each new reply, decide what it means and write it into the item:

- **It settles the question.** Write `decision` in one or two sentences,
  clear `question`, move the item to `todo` (or straight to `doing`).
- **It needs a follow-up.** Add an agent entry to `thread` explaining what is
  still unclear, set a new `question`, keep it `waiting`.
- **It asks for something new.** Add a new item; reference it in a thread
  entry.
- **It is a new item** (`new-<n>`). Give it a real title, its kind and its
  place in the list, and a plan, or a question if it is the owner's call.
- **It drops the item.** Move it to `dropped` with the reason as `outcome`.

Clear `unread` (and `fresh`) on every item you processed, so neither you nor
the owner sees it as unseen again. Then run `build`, and tell the owner in chat what you understood from each
reply and what happens next. If a reply contradicts the project's own rules,
say so rather than following it silently.

## Work an item

- Starting: `doing`, and clear `fresh` and `unread`. Finishing: `done`,
  `outcome`, `refs`, `updated`. `doing` says the work has started and is not
  finished, not that an agent is at it now: a 12-month paper test stays `doing`
  while it runs.
- Take the first `todo` nothing blocks; a `draft` waits for the owner.
- Size it yourself, and pick the smallest shape that fits:
  1. do it directly;
  2. split it into items in the same tracker;
  3. grow it into its own tracker, `trackers/<name>.json`: the item stays
     `doing` with `spawned` set to that path, and closes when that tracker does;
  4. an inbox item (`~/.kata/INBOX.json`) that is a project of its own: move
     it there with `project-kickoff`, and register the new project
     (`kata register <path>`, when the `kata` command exists).
- Discovered on the way: a new item, never a silent fix outside the tracker.
- Blocked on the owner: `waiting` with a `question` and your recommendation.
- Something only the owner can do: a `for: me` item, with what they need.
- Run `build` after every change, so the page never lags the file.

When invoked as `/tracker work <file> <id>` (the hub's Launch button), run
`tracker.py show <file> <id>` and work that item as above.

## At the start of a session

If the repository has `TRACKER.json` or `trackers/*.json`, run
`tracker.py brief` from the repository root: a few lines per tracker, with
what the owner added or said that you have not processed yet. Read the whole
file only when you edit it, and an item with `show`. Mention the owner's news
and the `waiting` items when they bear on the task. `brief` also rebuilds a
page that is missing or out of date; commit it with your work.

## Close a tracker

When every item is `done` or `dropped`:

1. Move anything with lasting value out: durable decisions to `DECISIONS.md`,
   what changed to the main tracker or the project's changelog.
2. Ask the owner before deleting anything. Then delete the file and its page
   in one commit that says where their content went. Git history keeps the
   tracker.

## Turn a PLAN.md into a tracker

Never in one step, never without the owner. First propose, then migrate.

1. Read the whole `PLAN.md` and sort each section:

   | What the section holds | Where it goes |
   |---|---|
   | Work with a status (checkboxes, workstreams, "small items") | Items |
   | Questions for the owner ("open questions", "the owner's call") | Items, `kind: "decision"`, `waiting` |
   | Order and gates (Now → Next → Later, "don't start before…") | The items' order, `blocked_by` |
   | What was done ("completed", execution logs) | `done` items with `outcome` and `refs`, or left to git history |
   | Deferred ("not now, because…") | `draft` items, the reason in `context` |
   | Refused or settled ("refused", "answered") | `dropped` or `done` items that keep their `decision` |
   | Prioritization rules | `principles` |
   | Reasoning, design notes, hand-off instructions, snippets | Stays a document (`DECISIONS.md`, `ARCHITECTURE.md`, the existing doc) |

2. Show the owner the mapping and what would remain of `PLAN.md`.
3. On their yes: write the tracker, run `build`, and reduce `PLAN.md` to what
   stays a document, or delete it if nothing does. Update any doc that points
   at it (the project's `CLAUDE.md`, `AGENTS.md`, `README`). One commit.
