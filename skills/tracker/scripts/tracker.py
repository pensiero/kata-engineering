#!/usr/bin/env python3
"""Keep a TRACKER.json honest, and build the page that shows it.

Standard library only, Python 3.9+. The file format is specified in
../reference/schema.md; this script is a convenience over it, not the only way
to read or write it — any agent can edit the JSON by hand and run `check`.

    tracker.py new     PATH --title T --summary S
    tracker.py check   PATH
    tracker.py build   PATH                  # check, date what closed, then write PATH's page
    tracker.py brief   [PATH]                # what needs the agent, in a few lines; refreshes a stale page
    tracker.py show    PATH ID               # one item in full
    tracker.py render  PATH [--status todo]
    tracker.py reply   PATH ID TEXT          # one owner reply
    tracker.py reply   PATH --from FILE      # replies copied from the page ('-' = stdin)

A reply addressed to "new" ("[new] …") is a new item from the owner: it is
added as a `todo`, last, for the agent to title and place.
`brief` without a PATH reads TRACKER.json and trackers/*.json in the current
directory.

The owner's actions (add, edit, delete, promote, demote, archive, move, reply,
edit_reply, delete_reply, reopen, edit_tracker) are functions here too, for the
hub that writes them; `act` applies one to a file. Each refuses, with a reason,
when it no longer applies to the file.

The page is PATH with an .html suffix, written next to it: a static file with
the tracker embedded, opened from disk. `new`, `build` and `reply` rewrite it,
so it always matches the file it sits beside.
"""
import argparse
import html
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

SCHEMA = 4
SCHEMAS = (1, 2, 3, 4)   # older files: `load` brings them up to date, and any write sets 4
STATUSES = ("draft", "todo", "doing", "done", "dropped")   # the order they are always shown in
CLOSED = ("done", "dropped")
KINDS = ("task", "decision", "check")
FOR = ("agent", "me")
AUTHORS = ("owner", "agent")
MAX_TITLE = 60        # "<Project> · <scope>"
MAX_SUMMARY = 240     # two sentences: what it holds, how long it lives

# Item ids are short and safe in a file name, a URL fragment and the page's
# "[id] reply" lines: letters, digits and _ - . ~ : @ + only.
ID_RE = re.compile(r"^[A-Za-z0-9_\-.~:@+]{1,64}$")
REPLY_RE = re.compile(r"^\[([A-Za-z0-9_\-.~:@+]{1,64})\]\s?(.*)$")
NEW = "new"           # the reply id the page uses for a new item; never an item's id
MAX_NEW_TITLE = 80
SENTENCE = re.compile(r"(.+?[.!?])\s+(?=[A-Z0-9(\"'*`])")   # a first sentence, not "e.g. this"
ASSETS = Path(__file__).resolve().parent.parent / "assets"
TEMPLATE = ASSETS / "page.html"
STYLE = ASSETS / "style.css"      # shared with the Kata hub
MARKDOWN = ASSETS / "markdown.js" # shared with the Kata hub

STATUS_LABEL = {"draft": "Draft", "todo": "To do", "doing": "In progress", "done": "Done", "dropped": "Not doing"}
BRIEF_LIST = 5        # items per list in `brief`
BRIEF_TEXT = 90       # characters per line in `brief`


class Refused(Exception):
    """An owner action that no longer applies to the file, with the reason."""


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(path):
    with open(path, encoding="utf-8") as f:
        return up_to_date(json.load(f))


def up_to_date(t):
    """Older trackers had sections, and a status `waiting`; an agent may still
    write either out of habit. Sections become the one list they add up to,
    keeping their order, and `waiting` becomes `todo`: its question is what
    says it needs the owner. Nothing past this point knows about either."""
    if not isinstance(t, dict) or not isinstance(t.get("items"), list):
        return t
    groups = t.pop("groups", None)
    if isinstance(groups, list):
        order = {g.get("id"): n for n, g in enumerate(groups) if isinstance(g, dict)}
        t["items"].sort(key=lambda i: order.get(i.get("group"), len(order)) if isinstance(i, dict) else len(order))
    for i in t["items"]:
        if isinstance(i, dict):
            i.pop("group", None)
            if i.get("status") == "waiting":
                i["status"] = "todo"
    return t


def save(path, tracker):
    """Write atomically: a reader (the hub, an agent) never sees half a file."""
    text = json.dumps(tracker, indent=2, ensure_ascii=False) + "\n"
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix="." + path.name + ".")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise


# ---------------------------------------------------------------- check

def problems(t):
    """Every way `t` breaks the schema, as plain sentences. Empty = valid."""
    out = []
    if not isinstance(t, dict):
        return ["The tracker must be a JSON object."]
    if t.get("schema") not in SCHEMAS:
        out.append(f"'schema' must be {SCHEMA}.")
    title, summary = str(t.get("title") or "").strip(), str(t.get("summary") or "").strip()
    if not title:
        out.append("'title' is missing.")
    elif len(title) > MAX_TITLE:
        out.append(f"'title' is over {MAX_TITLE} characters: name the project and the scope, nothing more.")
    if not summary:
        out.append("'summary' is missing: say what the tracker holds and how long it lives.")
    elif len(summary) > MAX_SUMMARY:
        out.append(f"'summary' is over {MAX_SUMMARY} characters: two sentences, what it holds and how long it lives.")
    items = t.get("items")
    if not isinstance(items, list):
        return out + ["'items' must be a list."]
    seen = set()
    all_ids = {i.get("id") for i in items if isinstance(i, dict)}
    for n, it in enumerate(items):
        where = f"Item {it.get('id') or '#' + str(n + 1)}" if isinstance(it, dict) else f"Item #{n + 1}"
        if not isinstance(it, dict):
            out.append(f"{where} must be an object.")
            continue
        iid = it.get("id")
        if not isinstance(iid, str) or not iid.strip():
            out.append(f"{where} needs a string 'id'.")
        elif not ID_RE.match(iid) or iid in (".", ".."):
            out.append(f"{where}: ids may use letters, digits and _ - . ~ : @ + only.")
        elif iid == NEW:
            out.append(f"{where}: '{NEW}' is reserved for the owner's new items; pick another id.")
        elif iid in seen:
            out.append(f"{where}: the id is used twice.")
        seen.add(iid)
        if not str(it.get("title") or "").strip():
            out.append(f"{where} needs a 'title'.")
        status = it.get("status")
        if status not in STATUSES:
            out.append(f"{where}: status must be one of {', '.join(STATUSES)}.")
        if it.get("kind", "task") not in KINDS:
            out.append(f"{where}: kind must be one of {', '.join(KINDS)}.")
        if it.get("for", "agent") not in FOR:
            out.append(f"{where}: 'for' must be agent or me.")
        for flag in ("fresh", "unread"):
            if not isinstance(it.get(flag, False), bool):
                out.append(f"{where}: '{flag}' must be true or false.")
        if not isinstance(it.get("spawned", ""), str):
            out.append(f"{where}: 'spawned' must be the path of the tracker it grew into.")
        blocked = it.get("blocked_by", [])
        if not (isinstance(blocked, list) and all(isinstance(b, str) and b for b in blocked)):
            out.append(f"{where}: 'blocked_by' must be a list of item ids.")
        else:
            for b in blocked:
                if "/" not in b and b not in all_ids:
                    out.append(f"{where}: blocked by '{b}', which is not an item here "
                               "(an item in another project is '<project>/<id>').")
        if status in ("done", "dropped") and not str(it.get("outcome") or "").strip():
            out.append(f"{where} is {status} but has no 'outcome' saying what happened.")
        thread = it.get("thread", [])
        if not isinstance(thread, list):
            out.append(f"{where}: 'thread' must be a list.")
            thread = []
        for m in thread:
            if not (isinstance(m, dict) and m.get("by") in AUTHORS
                    and str(m.get("text") or "").strip() and m.get("at")):
                out.append(f"{where}: every thread entry needs 'by' (owner|agent), 'at' and 'text'.")
                break
        if not isinstance(it.get("refs", []), list):
            out.append(f"{where}: 'refs' must be a list.")
        table = it.get("table")
        if table is not None and not (isinstance(table, list) and all(isinstance(r, list) for r in table)):
            out.append(f"{where}: 'table' must be a list of rows, the first being the header.")
    return out


# ---------------------------------------------------------------- render

def closed_at(it):
    """When an item closed, for the archive's order: newest first."""
    return it.get("closed") or it.get("updated") or it.get("created") or ""


def render(t, status=None):
    """Plain Markdown, for reading in a terminal or by an agent without a page."""
    items = t["items"]
    counts = {s: sum(1 for i in items if i["status"] == s) for s in STATUSES}
    lines = [f"# {t['title']}", ""]
    if t.get("summary"):
        lines += [t["summary"], ""]
    needs = sum(1 for i in items if needs_you(i))
    lines.append(" · ".join(([f"Needs you: {needs}"] if needs else []) + [f"{STATUS_LABEL[s]}: {counts[s]}" for s in STATUSES if counts[s]]))
    lines.append("")
    for s in STATUSES:
        rows = [i for i in items if i["status"] == s and (not status or s == status)]
        if not rows:
            continue
        if s in CLOSED:
            rows.sort(key=closed_at, reverse=True)
        lines += [f"## {STATUS_LABEL[s]}", ""]
        for i in rows:
            lines.append(f"- **{i['id']}** {i['title']}" + (" (needs you)" if needs_you(i) else ""))
            if needs_you(i) and i.get("question"):
                lines.append(f"  - Question: {i['question']}")
            if i.get("decision"):
                lines.append(f"  - Decided: {i['decision']}")
            if s in CLOSED:
                lines.append(f"  - {STATUS_LABEL[s]}: {i['outcome']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------- page

def page_path(path):
    return Path(path).with_suffix(".html")


def build_page(t, source):
    """The page for tracker `t`: the template with the tracker embedded.
    Deterministic, so rebuilding an unchanged tracker leaves git clean."""
    data = json.dumps({"source": source, "tracker": t}, ensure_ascii=False, indent=1)
    data = data.replace("<", "\\u003c")     # "<" only occurs inside strings; keeps </script> out
    return (TEMPLATE.read_text(encoding="utf-8")
            .replace("/*__TRACKER_STYLE__*/", STYLE.read_text(encoding="utf-8"))
            .replace("/*__TRACKER_MARKDOWN__*/", MARKDOWN.read_text(encoding="utf-8"))
            .replace("__TRACKER_TITLE__", html.escape(t["title"]))
            .replace("__TRACKER_DATA__", data))


def repo_relative(path):
    """The tracker's path inside its repository, as the page names it in the
    replies it copies. Never absolute: the page is committed."""
    p = Path(path).resolve()
    for root in p.parents:
        if (root / ".git").exists():
            return p.relative_to(root).as_posix()
    return p.name


def write_page(path, t):
    out = page_path(path)
    out.write_text(build_page(t, repo_relative(path)), encoding="utf-8")
    return out


def refresh_page(path, t):
    """Rebuild the page if it is missing or no longer what `build` would
    write (the tracker was edited by hand, or the template changed).
    Returns the page's path when it was rewritten."""
    out = page_path(path)
    try:
        if out.read_text(encoding="utf-8") == build_page(t, repo_relative(path)):
            return None
    except OSError:
        pass
    return write_page(path, t)


# ---------------------------------------------------------------- replies

def parse_replies(text):
    """The text the page's "Copy for the agent" button produces: a header line
    ("/tracker Replies to <title> (<path>):"), then one "[id] reply" block per item, continuation lines included.
    Returns [(item_id, text)]."""
    out = []
    for line in text.splitlines():
        m = REPLY_RE.match(line)
        if m:
            out.append([m.group(1), [m.group(2)]])
        elif out:
            out[-1][1].append(line)
    return [(iid, "\n".join(lines).strip()) for iid, lines in out if "\n".join(lines).strip()]


def free_id(t):
    taken = {i["id"] for i in t["items"]}
    n = 1
    while f"{NEW}-{n}" in taken:
        n += 1
    return f"{NEW}-{n}"


def owner_words(text):
    """The owner's text as (title, context), with nothing said in both: the
    first line is a provisional title and the lines after it the context. A
    first line too long for a title gives its first sentence, when that is
    short enough, and the rest of the line opens the context; failing that,
    the title is the line cut short and the context the whole text."""
    text = text.strip()
    first, _, rest = text.partition("\n")
    first, rest = first.strip(), rest.strip()
    if len(first) <= MAX_NEW_TITLE:
        return first, rest
    m = SENTENCE.match(first)
    if m and len(m.group(1)) <= MAX_NEW_TITLE:
        return m.group(1), (first[m.end():] + "\n" + rest).strip()
    cut = first[:MAX_NEW_TITLE - 1]
    cut = cut.rsplit(" ", 1)[0] if " " in cut[MAX_NEW_TITLE // 2:] else cut
    return cut.rstrip(" ,;:-") + "…", text


def said(it):
    """What the owner wrote for an item of theirs: the title, then the context.
    An item whose title was cut short, or one added before the two were
    split, holds the whole text in its context. Compare it with `even`: the
    title and context may have been split after a sentence."""
    title, context = it["title"].strip(), str(it.get("context") or "").strip()
    if not context:
        return title
    if context == title or context.startswith(title + "\n") or (title.endswith("…") and context.startswith(title[:-1])):
        return context
    return f"{title}\n\n{context}"


def even(text):
    """Text with its spaces and line breaks evened out, for comparing."""
    return " ".join(text.split())


def needs_you(it):
    """Whether an item is waiting for the owner: a to-do of theirs, or a question,
    they have not replied to since (`unread`). A tag on a to-do or an item in
    progress, whatever its stage; a draft is theirs anyway, and nothing is
    expected of a closed one."""
    if it["status"] not in ("todo", "doing") or it.get("unread"):
        return False
    return it.get("for") == "me" or bool(str(it.get("question") or "").strip())


def pending(it):
    """Whether the item holds something from the owner the agent has not
    processed yet (`unread`). Drafts are never the agent's to act on."""
    return bool(it.get("unread")) and it["status"] != "draft"


def mark_unread(it):
    """Flag what the owner wrote for the agent to read. Not on a draft, nor on
    a to-do the owner added for themselves that no agent has touched (`fresh`):
    no agent works either. A reply on a `for: me` item an agent left them is
    read, and takes it off Needs you until the agent has."""
    if it["status"] != "draft" and not (it.get("for") == "me" and it.get("fresh")):
        it["unread"] = True



# ---------------------------------------------------------------- owner actions
# What the owner may write (reference/schema.md, "Who writes what"). An item
# the owner added stays theirs to edit or delete while it is `fresh`, that is
# until an agent first works on it and clears the flag. Every owner write the
# agent should look at sets `unread`; the agent clears it once processed.

def find(t, iid):
    for it in t["items"]:
        if it["id"] == iid:
            return it
    raise Refused(f"There is no item '{iid}' any more; it may have been removed or renamed.")


def touch(it):
    it["updated"] = date.today().isoformat()


def add(t, text, status="todo", for_me=False):
    """A new item from the owner, last: `todo` (the agent may take it) or
    `draft` (not yet), `fresh` until an agent works on it."""
    if not text.strip():
        raise Refused("An item needs some text.")
    if status not in ("todo", "draft"):
        raise Refused("A new item is either a draft or a to-do.")
    title, context = owner_words(text)
    today = date.today().isoformat()
    item = {"id": free_id(t), "title": title, "kind": "task",
            "status": status, "context": context, "fresh": True, "created": today, "updated": today}
    if for_me:
        item["for"] = "me"
    mark_unread(item)
    t["items"].append(item)
    return item


def edit(t, iid, text):
    """Rewrite an item of the owner's. Once an agent has worked on it the item
    is the agent's record, so the new text becomes a reply instead.
    Returns "edited" or "replied"."""
    it = find(t, iid)
    if not text.strip():
        raise Refused("An item needs some text; delete it instead.")
    if not it.get("fresh"):
        reply(t, iid, text)
        return "replied"
    it["title"], it["context"] = owner_words(text)
    touch(it)
    return "edited"


def delete(t, iid):
    it = find(t, iid)
    if not it.get("fresh"):
        raise Refused(f"An agent has already worked on '{iid}'. Reply to ask for it to be dropped.")
    t["items"].remove(it)
    return it


def promote(t, iid):
    it = find(t, iid)
    if it["status"] != "draft":
        raise Refused(f"'{iid}' is not a draft any more.")
    it["status"] = "todo"
    mark_unread(it)
    touch(it)


def demote(t, iid):
    """A to-do back to draft: not ready for an agent after all."""
    it = find(t, iid)
    if it["status"] != "todo":
        raise Refused(f"'{iid}' is not a to-do any more.")
    it["status"] = "draft"
    it.pop("unread", None)
    touch(it)


def archive(t, iid, how="done", reason=""):
    """Close an open item, whoever's it is: `done`, or `dropped` (not doing it).
    The outcome is the owner's reason, else what the item already says. Nothing
    is left for an agent to read on it."""
    it = find(t, iid)
    if how not in CLOSED:
        raise Refused(f"An item is archived as {' or '.join(CLOSED)}.")
    if it["status"] in CLOSED:
        raise Refused(f"'{iid}' is already in the archive.")
    it["status"] = how
    it["outcome"] = reason.strip() or it.get("outcome") or ("Done, the owner says." if how == "done" else "Not doing it, the owner's call.")
    it.pop("unread", None)
    touch(it)


def move(t, iid, before=None):
    """Put the item just before item `before`, or last."""
    it = find(t, iid)
    if before == iid:
        return
    items = [i for i in t["items"] if i is not it]
    at = len(items) if before is None else next((n for n, i in enumerate(items) if i["id"] == before), None)
    if at is None:
        raise Refused(f"'{before}' is not there any more; reload and try again.")
    items.insert(at, it)
    t["items"] = items


def reply(t, iid, text):
    """One reply typed in the hub. Unlike pasted replies it is never skipped as
    a duplicate: the owner may well say "yes" twice."""
    it = find(t, iid)
    if not text.strip():
        raise Refused("A reply needs some text.")
    it.setdefault("thread", []).append({"by": "owner", "at": now_iso(), "text": text.strip()})
    mark_unread(it)
    touch(it)


def own_reply(t, iid, n, at):
    """Thread entry `n` of an item, if it is an owner reply no agent has read
    yet: the item is `unread` and no agent entry follows it. `at` must match,
    so a thread that changed meanwhile is never edited in the wrong place."""
    it = find(t, iid)
    thread = it.get("thread") or []
    if not (isinstance(n, int) and 0 <= n < len(thread)) or thread[n].get("at") != at or thread[n].get("by") != "owner":
        raise Refused("That reply is not there any more; reload and try again.")
    if not it.get("unread") or any(m.get("by") != "owner" for m in thread[n + 1:]):
        raise Refused("An agent has already read that reply. Send a new one instead.")
    return it, thread


def edit_reply(t, iid, n, at, text):
    it, thread = own_reply(t, iid, n, at)
    if not text.strip():
        raise Refused("A reply needs some text; delete it instead.")
    thread[n]["text"] = text.strip()
    touch(it)


def delete_reply(t, iid, n, at):
    """Delete an unread reply. When nothing of the owner's is left unseen (an
    item of theirs still `fresh` always is), the item is no longer `unread`,
    so a question it had answered needs them again."""
    it, thread = own_reply(t, iid, n, at)
    del thread[n]
    last_agent = max((k for k, m in enumerate(thread) if m.get("by") != "owner"), default=-1)
    if not it.get("fresh") and not any(m.get("by") == "owner" for m in thread[last_agent + 1:]):
        it.pop("unread", None)
    touch(it)


def reopen(t, iid, reason=""):
    """A closed item back to `todo`, the owner's reason in its thread."""
    it = find(t, iid)
    if it["status"] not in CLOSED:
        raise Refused(f"'{iid}' is not closed.")
    if not reason.strip() and it.get("for") != "me":
        raise Refused("Say why it is reopened, so the agent knows what is still wrong.")
    it["status"] = "todo"
    if reason.strip():
        reply(t, iid, reason)
    touch(it)


def edit_tracker(t, title=None, summary=None):
    """What the tracker is called, and what it holds (`summary`)."""
    if title is not None:
        if not title.strip():
            raise Refused("A tracker needs a title.")
        t["title"] = " ".join(title.split())
    if summary is not None:
        if not summary.strip():
            raise Refused("A tracker needs a summary: what it holds, and how long it lives.")
        t["summary"] = " ".join(summary.split())


def stamp(t):
    """Date every item that closed, for the archive's order, and forget the
    date of one that reopened. An agent closing by hand leaves only `updated`:
    a past date is taken as it is, today's gets the time."""
    today = date.today().isoformat()
    for it in t["items"]:
        if it["status"] not in CLOSED:
            it.pop("closed", None)
        elif not it.get("closed"):
            it["closed"] = it["updated"] if it.get("updated") not in (None, "", today) else now_iso()


def finish(path, t):
    """Write a valid tracker and its page."""
    stamp(t)
    t["schema"] = SCHEMA
    save(path, t)
    return write_page(path, t)


def act(path, action, *args, **kwargs):
    """Apply one owner action to the tracker at `path`, reading it fresh, and
    write it and its page back. Refuses rather than write over a file that is
    unreadable or invalid (an agent may be halfway through an edit)."""
    try:
        t = load(path)
    except (OSError, ValueError) as e:
        raise Refused(f"{path} cannot be read right now ({e}).")
    if problems(t):
        raise Refused(f"{path} is not valid right now: {problems(t)[0]}")
    result = action(t, *args, **kwargs)
    issues = problems(t)
    if issues:
        raise Refused(issues[0])
    finish(path, t)
    return result


def add_replies(t, replies, at=None):
    """Append each reply to its item's thread as an owner entry; a reply to
    "new" becomes a new item. A reply already in the thread word for word (for
    a new item: among the owner's unseen items) is skipped, so pasting the
    same text twice is harmless. A reply answers the item's question, so it no
    longer needs the owner; its status does not move, and deciding what the reply
    means is the agent's job. Returns (added [(id, text)], unknown ids)."""
    by_id = {i["id"]: i for i in t["items"]}
    added, unknown = [], []
    for iid, text in replies:
        if iid == NEW:
            if not any(even(said(i)) == even(text) for i in t["items"] if i.get("fresh")):
                added.append((add(t, text)["id"], text))
            continue
        item = by_id.get(iid)
        if item is None:
            unknown.append(iid)
            continue
        thread = item.setdefault("thread", [])
        if any(m.get("by") == "owner" and m.get("text", "").strip() == text for m in thread):
            continue
        thread.append({"by": "owner", "at": at or now_iso(), "text": text})
        mark_unread(item)
        item["updated"] = date.today().isoformat()
        added.append((iid, text))
    return added, unknown


# ---------------------------------------------------------------- brief, show

def clip(text, n=BRIEF_TEXT):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n - 1].rstrip() + "…"


def brief(t, source):
    """What an agent needs at the start of a session, in a few lines whatever
    the tracker's size: what the owner added or said, what waits on them,
    what is in progress and what comes next. `show` gives an item in full."""
    items = t["items"]
    mine = [i for i in items if i.get("for") == "me" and i["status"] not in CLOSED and not pending(i)]
    agents = [i for i in items if i.get("for") != "me"]
    new = [i for i in items if pending(i)]
    lists = [
        ("From the owner, not yet seen", new, 10,
         lambda i: "new: " + clip(said(i)) if i.get("fresh") or not i.get("thread")
         else clip(i["title"], 40) + f" · {i['thread'][-1]['by']}: " + clip(i["thread"][-1]["text"], 50)),
        ("Waiting on the owner", [i for i in agents if needs_you(i)], BRIEF_LIST,
         lambda i: clip(i.get("question") or i["title"])),
        ("Next to do", [i for i in agents if i["status"] == "todo" and not pending(i) and not needs_you(i)], BRIEF_LIST,
         lambda i: clip(i["title"]) + (" · blocked by " + ", ".join(i["blocked_by"]) if i.get("blocked_by") else "")),
        ("In progress", [i for i in agents if i["status"] == "doing" and not pending(i) and not needs_you(i)], BRIEF_LIST,
         lambda i: clip(i["title"])),
    ]
    count = lambda s: sum(1 for i in agents if i["status"] == s)
    waiting = sum(1 for i in agents if needs_you(i))
    tally = [f"drafts {count('draft')} (not yet for you)"] if count("draft") else []
    tally += [f"needs the owner {waiting}"] if waiting else []
    tally += [f"{STATUS_LABEL[s].lower()} {count(s)}" for s in ("todo", "doing") if count(s)]
    tally += [f"archive {count('done') + count('dropped')}"] if count("done") + count("dropped") else []
    tally += [f"owner's own to-dos {len(mine)}"] if mine else []
    lines = [f"{t['title']} ({source}): " + (", ".join(tally) or "empty")]
    for head, rows, cap, fmt in lists:
        if not rows:
            continue
        lines.append(f"{head}:")
        lines += [f"  [{i['id']}] {fmt(i)}" for i in rows[:cap]]
        if len(rows) > cap:
            lines.append(f"  … and {len(rows) - cap} more")
    if new:
        lines.append(f"Read one in full: tracker.py show {source} <id>")
    return "\n".join(lines) + "\n"


def show(t, iid):
    return json.dumps(find(t, iid), indent=2, ensure_ascii=False) + "\n"


def found_trackers(root="."):
    """The trackers of the repository at `root`: its main one, then its efforts."""
    root = Path(root)
    return [p for p in [root / "TRACKER.json"] + sorted((root / "trackers").glob("*.json")) if p.is_file()]


# ---------------------------------------------------------------- new

def new_tracker(title, summary=""):
    return {"schema": SCHEMA, "title": title, "summary": summary, "items": []}


# ---------------------------------------------------------------- cli

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("new");    a.add_argument("path"); a.add_argument("--title", required=True)
    a.add_argument("--summary", required=True)
    a = sub.add_parser("check");  a.add_argument("path")
    a = sub.add_parser("build");  a.add_argument("path")
    a = sub.add_parser("brief");  a.add_argument("path", nargs="?")
    a = sub.add_parser("show");   a.add_argument("path"); a.add_argument("id")
    a = sub.add_parser("render"); a.add_argument("path"); a.add_argument("--status")
    a = sub.add_parser("reply");  a.add_argument("path"); a.add_argument("id", nargs="?"); a.add_argument("text", nargs="?")
    a.add_argument("--from", dest="source")
    args = p.parse_args(argv)

    if args.cmd == "new":
        if Path(args.path).exists():
            print(f"{args.path} already exists; not overwriting it.", file=sys.stderr)
            return 1
        t = new_tracker(args.title, args.summary)
        save(args.path, t)
        print(f"Created {args.path} and {write_page(args.path, t)}.")
        return 0

    if args.cmd == "brief" and not args.path:
        paths = found_trackers()
        if not paths:
            print("No TRACKER.json or trackers/*.json here.")
            return 0
        return max(main(["brief", str(p)]) for p in paths)

    t = load(args.path)
    issues = problems(t)
    if args.cmd == "check" or issues:
        for msg in issues:
            print(f"- {msg}", file=sys.stderr)
        if issues:
            print(f"{args.path}: {len(issues)} problem(s).", file=sys.stderr)
            return 1
        print(f"{args.path}: valid, {len(t['items'])} items.")
        return 0

    if args.cmd == "build":
        print(f"{args.path}: valid, {len(t['items'])} items. Wrote {finish(args.path, t)}.")
        return 0
    if args.cmd == "render":
        sys.stdout.write(render(t, args.status))
        return 0
    if args.cmd == "brief":
        sys.stdout.write(brief(t, args.path))
        rebuilt = refresh_page(args.path, t)
        if rebuilt:
            print(f"(Rebuilt {rebuilt}: it was out of date. Commit it with your work.)")
        return 0
    if args.cmd == "show":
        try:
            sys.stdout.write(show(t, args.id))
        except Refused as e:
            print(e, file=sys.stderr)
            return 1
        return 0
    if args.cmd == "reply":
        if args.source:
            text = sys.stdin.read() if args.source == "-" else Path(args.source).read_text(encoding="utf-8")
            replies = parse_replies(text)
        elif args.id and args.text and args.text.strip():
            replies = [(args.id, args.text.strip())]
        else:
            print("Give an item id and the reply, or --from a file of copied replies.", file=sys.stderr)
            return 2
        added, unknown = add_replies(t, replies)
        for iid in unknown:
            print(f"No item '{iid}': reply not added.", file=sys.stderr)
        if added:
            save(args.path, t)
            write_page(args.path, t)
        for iid, text in added:
            print(f"{iid}: {text}")
        if not added:
            print("No new replies.")
        return 1 if unknown else 0
    return 2

if __name__ == "__main__":
    sys.exit(main())
