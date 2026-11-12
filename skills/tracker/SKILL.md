---
name: tracker
description: Track a project's work items, the questions waiting on the owner, and what was done, in a versioned TRACKER.json with a static HTML page beside it that the owner opens from disk and replies on. Use when asked to track work or progress, keep a backlog or to-do list, list findings to fix one by one, collect the owner's answers, check whether the owner replied, work through a tracker the owner launched ("/tracker work …"), or turn a PLAN.md into a tracker. Use it unasked whenever many things need the owner's check or decision together — a review's findings, a before/after list of changes, several open questions — instead of a long list in chat. Also use at the start of a session in a repository that has a TRACKER.json, and whenever the owner pastes replies copied from a tracker page.
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
- `assets/page.html`, `assets/style.css` and `assets/markdown.js`: the
  template every tracker's page is built from, and the look and the Markdown
  drawing it shares with the hub. Never edit a built page or the template per
  project; everything a page shows comes from its tracker.

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
   `for: me` item, beyond reading a reply on it.
3. **Everything stays local.** Never publish a tracker or its page anywhere
   (no artifacts, no gists, no hosted pages). It is shared the way the
   repository is shared, and a private tracker not at all.
4. **A question only when it is the owner's call, and always when it is.** A
   plain bug gets a plan and no question: say what you will do and do it. Ask
   when there is a real choice (a rule change, a trade-off, a preference), when
   you are undecided, or when you want the owner to review something, and put
   your recommendation in `plan` so the owner can answer "yes". `question` is
   the only thing that reaches them: it puts a "Needs you" tag on the item. A
   line in a thread or a plan such as "reply here if you want changes" reaches
   nobody.
5. **Each field says one thing, once.** `context` is what is wanted, `findings`
   what you found out, `plan` what you will do and why, `question` the choice
   left to the owner in one line ("Keep the old export, or drop it? I'd drop
   it."), never the plan again. Your thread entries are news (what you tried,
   what changed after a reply), never the question, the plan or the findings
   restated. The page shows every field, so what is written twice is read twice.
6. **Write for the owner.** Titles and context in the owner's words, with the
   evidence, and numbers when there are numbers. Text fields and thread
   entries are Markdown: a list for a list, bold for what matters most, `code`
   for a file or command; titles stay plain. Follow the project's register
   and privacy rules: a tracker holding private data goes where the project
   keeps private files.
7. **Closing means saying what happened.** `done` needs an `outcome` and,
   where possible, `refs` (commit, file, PR). `dropped` needs the reason, and
   the owner's agreement. A settled question keeps its `decision`, so it is
   never asked again. `build` dates what closed, for the archive's order.
8. **Commit the tracker and its page with the work** that moved them, following the project's
   own commit rules. Git history is the tracker's history.

---

## Start a tracker

1. Pick the file: `TRACKER.json` for the project's main tracker,
   `trackers/<name>.json` for one effort (see `reference/schema.md`, "Where
   trackers live").
2. `python3 scripts/tracker.py new <file> --title "<Project> · <scope>" --summary "<what it holds>. <how long it lives>."`.
   A tracker is one list in the order of work, the same in every project:
   there are no sections, groups or gates, and where an item stands is its
   status: `draft`, `todo`, `doing`, `done` or `dropped`. `check` refuses any
   other, and `build` flattens sections left in a file. Every tracker
   follows the same title and summary shape (`reference/schema.md`), so two
   trackers' pages read alike. `new` writes the page too.
3. Write the items, first to do first, and `principles` if an agent needs rules
   to work by. What must happen first is `blocked_by`; what is not ready for an
   agent (an idea to argue, something to check again on a date or a condition)
   is a `draft`, saying what it waits for. Run `build`.
4. Tell the owner, in a line or two, what is in it, which items need them, and
   the page to open (`file://` + the page's absolute path).

## The page

`tracker.py build <file>` writes `<file>` with an `.html` suffix beside it
(`TRACKER.json` → `TRACKER.html`) with the tracker embedded. The owner opens it
from disk in any browser and reloads it after the agent rebuilds.

- Items sit in four stages, always in this order: Draft, To do, In progress,
  Archive. Needs you stands apart before them, a filter over To do and In
  progress, and those items carry a tag in their stage. The hub has the same
  tabs, and empty ones are left out. The archive is by date, newest first; the
  others keep the list's order.
- Each item that needs the owner has a reply box; other items take replies inside their
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
   owner's first line (or first sentence) as its title and the rest as its context, `fresh` and `unread`. A reply marks
   its item `unread`, which answers a question, or reports on a `for: me` item
   you left them, and takes the tag off; the status does not move.
2. Process them (below).

## Process the owner's replies

For each new reply, decide what it means and write it into the item:

An answered item keeps its stage and its `question`, so you can see what was
asked.

- **It settles the question.** Write `decision` in one or two sentences and
  clear `question`. The stage moves only if the work did.
- **It needs a follow-up.** Rewrite `plan` (and `findings`) to what you know
  now, and set a new `question`. Clearing `unread` is what puts the tag back.
- **It asks for something new.** Add a new item; reference it in a thread
  entry.
- **It is a new item** (`new-<n>`). Give it a real title, its kind and its
  place in the list, then work it as "An item the owner wrote" says. Its
  title is the owner's first line (or first sentence) and is not repeated in
  `context`: when you rewrite the title, put their line at the top of
  `context`, so their words stay on the item.
- **It drops the item.** Move it to `dropped` with the reason as `outcome`.
- **It is on a `for: me` item you left them.** If they did it, remove `for`
  and carry on with the work it unblocks, or close the item `done`. If it is
  still theirs, leave `for: me`: clearing `unread` puts the tag back.

Clear `unread` (and `fresh`) on every item you processed, so neither you nor
the owner sees it as unseen again. Then run `build`, and tell the owner in chat what you understood from each
reply and what happens next. If a reply contradicts the project's own rules,
say so rather than following it silently.

## Work an item

- Starting: `doing`, and clear `fresh` and `unread`. Finishing: `done`,
  `outcome`, `refs`, `updated`. `doing` says the work itself has started and is
  not finished, not that an agent is at it now: a 12-month paper test stays
  `doing` while it runs. Discussing or designing something not yet being built
  leaves it `todo`.
- Take the first `todo` that nothing blocks and that does not need the owner; a
  `draft` waits for them.
- Size it yourself, and pick the smallest shape that fits:
  1. do it directly;
  2. split it into items in the same tracker;
  3. grow it into its own tracker, `trackers/<name>.json`: the item stays
     `doing` with `spawned` set to that path, and closes when that tracker does;
  4. an inbox item (`~/.kata/INBOX.json`) that is a project of its own: move
     it there with `project-kickoff`, and register the new project
     (`kata register <path>`, when the `kata` command exists).
- Discovered on the way: a new item, never a silent fix outside the tracker.
- An item the owner wrote (`fresh`, or a `new-<n>`): read what they want from
  it first (below).
- Blocked on the owner, or wanting their review: set `question`, with your
  recommendation. The item stays in its stage, `todo` or `doing`, tagged.
- Something only the owner can do: a `for: me` item, with what they need.
- Run `build` after every change, so the page never lags the file.

### An item the owner wrote

A to-do the owner wrote is one of three things, and their words say which:

- **Do it** ("Add…", "Fix…", "Make…"): they are convinced, and the item is the
  go-ahead. Plan it, build it, close it with an `outcome`. Ask only at a fork
  their words leave open, and ask for a review after the work, not leave to
  start it.
- **Find out** (a question, "look into…", "why does…"): the answer is the
  work. Write it in `findings`, with the evidence. When it settles the matter,
  close the item `done`, its `outcome` saying what came of it ("Answered;
  nothing to change"). When it leads to work, put what you recommend in
  `plan` and ask, or split the work into new items and name them in `outcome`.
- **Plan it first** ("think about…", "plan…", "should we…"): they are not
  convinced yet. Explore, write `findings` if there are any and the `plan`,
  and ask whether to build it ("Build it as planned, or …?"). When the plan
  is several pieces of work, list them in `plan` and, on the owner's yes, add
  them as new items.

When the words leave it open, something small and easy to undo is "do it",
and anything large, costly or touching the project's rules is "plan it first".

## Work a tracker

`/tracker work <file>` (the hub's Launch agent, one per tracker) means: work
through this tracker. Run `tracker.py brief <file>`, then, in this order:

1. **What the owner said.** Everything `unread`, as in "Process the owner's
   replies". Most of the time this is the point of the launch.
2. **To do.** Each `todo` from the top that nothing blocks.
3. **In progress.** Carry on with what can move now. Leave a long-running item
   (a paper test, a ledger) alone until its next date or step comes.

Never a `draft`, a `for: me` item, or an item that needs the owner: when you
need them, set the question and go on with the next item. When there is more than one
session's work, take the top of it and tell the owner what is left.

With an id, `/tracker work <file> <id>`: run `tracker.py show <file> <id>` and
work that item only.

## At the start of a session

If the repository has `TRACKER.json` or `trackers/*.json`, run
`tracker.py brief` from the repository root: a few lines per tracker, with
what the owner added or said that you have not processed yet. Read the whole
file only when you edit it, and an item with `show`. Mention the owner's news
and what is waiting on them when they bear on the task. `brief` also rebuilds a
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
   | Questions for the owner ("open questions", "the owner's call") | Items, `kind: "decision"`, with a `question` |
   | Order and gates (Now → Next → Later, "don't start before…") | The items' order, `blocked_by` |
   | What was done ("completed", execution logs) | `done` items with `outcome` and `refs`, or left to git history |
   | Deferred ("not now, because…") | `draft` items, the reason in `context` |
   | Refused or settled ("refused", "answered") | `dropped` or `done` items that keep their `decision` |
   | Prioritization rules | `principles` |
   | Reasoning, design notes, hand-off instructions, snippets | Stays a document (`DECISIONS.md`, `ARCHITECTURE.md`, the existing doc) |

2. Show the owner the mapping and what would remain of `PLAN.md`.
3. On their yes: write the tracker, keeping the plan's lists, emphasis and
   links as Markdown in the items' fields, run `build`, and reduce `PLAN.md` to what
   stays a document, or delete it if nothing does. Update any doc that points
   at it (the project's `CLAUDE.md`, `AGENTS.md`, `README`). One commit.
