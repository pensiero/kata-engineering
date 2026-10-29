#!/usr/bin/env python3
"""Keep a TRACKER.json honest, and build the page that shows it.

Standard library only, Python 3.9+. The file format is specified in
../reference/schema.md; this script is a convenience over it, not the only way
to read or write it — any agent can edit the JSON by hand and run `check`.

    tracker.py new     PATH --title T --summary S [--groups now,next,later]
    tracker.py check   PATH
    tracker.py build   PATH                  # check, then write PATH's page
    tracker.py render  PATH [--status waiting] [--group G]
    tracker.py reply   PATH ID TEXT          # one owner reply
    tracker.py reply   PATH --from FILE      # replies copied from the page ('-' = stdin)

A reply addressed to "new" ("[new] …") is a new item from the owner: it is
added as a `todo` in the first group, for the agent to title and place.

The page is PATH with an .html suffix, written next to it: a static file with
the tracker embedded, opened from disk. `new`, `build` and `reply` rewrite it,
so it always matches the file it sits beside.
"""
import argparse
import html
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

SCHEMA = 1
STATUSES = ("todo", "doing", "waiting", "done", "dropped")
KINDS = ("task", "decision", "check")
AUTHORS = ("owner", "agent")
MAX_TITLE = 60        # "<Project> · <scope>"
MAX_SUMMARY = 240     # two sentences: what it holds, how long it lives

# Item ids are short and safe in a file name, a URL fragment and the page's
# "[id] reply" lines: letters, digits and _ - . ~ : @ + only.
ID_RE = re.compile(r"^[A-Za-z0-9_\-.~:@+]{1,64}$")
REPLY_RE = re.compile(r"^\[([A-Za-z0-9_\-.~:@+]{1,64})\]\s?(.*)$")
NEW = "new"           # the reply id the page uses for a new item; never an item's id
MAX_NEW_TITLE = 80
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "page.html"

STATUS_LABEL = {"todo": "To do", "doing": "In progress", "waiting": "Needs you",
                "done": "Done", "dropped": "Dropped"}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, tracker):
    text = json.dumps(tracker, indent=2, ensure_ascii=False) + "\n"
    Path(path).write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- check

def problems(t):
    """Every way `t` breaks the schema, as plain sentences. Empty = valid."""
    out = []
    if not isinstance(t, dict):
        return ["The tracker must be a JSON object."]
    if t.get("schema") != SCHEMA:
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
    groups = t.get("groups")
    if not isinstance(groups, list) or not groups:
        out.append("'groups' must be a non-empty list.")
        groups = []
    gids = [g.get("id") for g in groups if isinstance(g, dict)]
    if len(gids) != len(groups) or not all(isinstance(g, str) and g for g in gids):
        out.append("Every group needs a non-empty string 'id'.")
    if len(set(gids)) != len(gids):
        out.append("Group ids must be unique.")
    for g in groups:
        if isinstance(g, dict) and not str(g.get("title") or "").strip():
            out.append(f"Group '{g.get('id')}' needs a 'title'.")
    items = t.get("items")
    if not isinstance(items, list):
        return out + ["'items' must be a list."]
    seen = set()
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
        if it.get("group") not in gids:
            out.append(f"{where}: group '{it.get('group')}' is not in 'groups'.")
        if not str(it.get("title") or "").strip():
            out.append(f"{where} needs a 'title'.")
        status = it.get("status")
        if status not in STATUSES:
            out.append(f"{where}: status must be one of {', '.join(STATUSES)}.")
        if it.get("kind", "task") not in KINDS:
            out.append(f"{where}: kind must be one of {', '.join(KINDS)}.")
        if status == "waiting" and not str(it.get("question") or "").strip():
            out.append(f"{where} is waiting on the owner but has no 'question'.")
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

def render(t, status=None, group=None):
    """Plain Markdown, for reading in a terminal or by an agent without a page."""
    items = t["items"]
    counts = {s: sum(1 for i in items if i["status"] == s) for s in STATUSES}
    lines = [f"# {t['title']}", ""]
    if t.get("summary"):
        lines += [t["summary"], ""]
    lines.append(" · ".join(f"{STATUS_LABEL[s]}: {counts[s]}" for s in STATUSES if counts[s]))
    lines.append("")
    for g in t["groups"]:
        if group and g["id"] != group:
            continue
        rows = [i for i in items if i["group"] == g["id"] and (not status or i["status"] == status)]
        if not rows:
            continue
        lines.append(f"## {g['title']}")
        if g.get("gate"):
            lines.append(f"*Starts when:* {g['gate']}")
        lines.append("")
        for i in rows:
            lines.append(f"- **{i['id']}** [{STATUS_LABEL[i['status']]}] {i['title']}")
            if i["status"] == "waiting":
                lines.append(f"  - Question: {i['question']}")
            if i.get("decision"):
                lines.append(f"  - Decided: {i['decision']}")
            if i["status"] in ("done", "dropped"):
                lines.append(f"  - {STATUS_LABEL[i['status']]}: {i['outcome']}")
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


def new_item(t, text, at):
    """A `todo` in the first group holding the owner's words: the first line as
    a provisional title, the whole text as context and as the thread's first
    entry. The agent gives it its real title, group and kind."""
    taken = {i["id"] for i in t["items"]}
    n = 1
    while f"{NEW}-{n}" in taken:
        n += 1
    first = text.splitlines()[0].strip()
    title = first if len(first) <= MAX_NEW_TITLE else first[:MAX_NEW_TITLE - 1].rstrip() + "…"
    today = date.today().isoformat()
    item = {"id": f"{NEW}-{n}", "group": t["groups"][0]["id"], "title": title, "kind": "task",
            "status": "todo", "context": text if text != title else "",
            "thread": [{"by": "owner", "at": at, "text": text}], "created": today, "updated": today}
    t["items"].append(item)
    return item


def add_replies(t, replies, at=None):
    """Append each reply to its item's thread as an owner entry; a reply to
    "new" becomes a new item. A reply already in the thread word for word (for
    a new item: in any thread) is skipped, so pasting the same text twice is
    harmless. Statuses are NOT changed: deciding what a reply means is the
    agent's job. Returns (added [(id, text)], unknown ids)."""
    by_id = {i["id"]: i for i in t["items"]}
    added, unknown = [], []
    for iid, text in replies:
        if iid == NEW:
            if not any(m.get("by") == "owner" and m.get("text", "").strip() == text
                       for i in t["items"] for m in i.get("thread", [])):
                added.append((new_item(t, text, at or now_iso())["id"], text))
            continue
        item = by_id.get(iid)
        if item is None:
            unknown.append(iid)
            continue
        thread = item.setdefault("thread", [])
        if any(m.get("by") == "owner" and m.get("text", "").strip() == text for m in thread):
            continue
        thread.append({"by": "owner", "at": at or now_iso(), "text": text})
        item["updated"] = date.today().isoformat()
        added.append((iid, text))
    return added, unknown


# ---------------------------------------------------------------- new

def new_tracker(title, groups, summary=""):
    return {
        "schema": SCHEMA,
        "title": title,
        "summary": summary,
        "principles": [],
        "groups": [{"id": g, "title": g.replace("-", " ").capitalize(), "note": "", "gate": ""}
                   for g in groups],
        "items": [],
    }


# ---------------------------------------------------------------- cli

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("new");    a.add_argument("path"); a.add_argument("--title", required=True)
    a.add_argument("--summary", required=True)
    a.add_argument("--groups", default="now,next,later")
    a = sub.add_parser("check");  a.add_argument("path")
    a = sub.add_parser("build");  a.add_argument("path")
    a = sub.add_parser("render"); a.add_argument("path"); a.add_argument("--status"); a.add_argument("--group")
    a = sub.add_parser("reply");  a.add_argument("path"); a.add_argument("id", nargs="?"); a.add_argument("text", nargs="?")
    a.add_argument("--from", dest="source")
    args = p.parse_args(argv)

    if args.cmd == "new":
        if Path(args.path).exists():
            print(f"{args.path} already exists; not overwriting it.", file=sys.stderr)
            return 1
        t = new_tracker(args.title, [g.strip() for g in args.groups.split(",") if g.strip()], args.summary)
        save(args.path, t)
        print(f"Created {args.path} and {write_page(args.path, t)}.")
        return 0

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
        print(f"{args.path}: valid, {len(t['items'])} items. Wrote {write_page(args.path, t)}.")
        return 0
    if args.cmd == "render":
        sys.stdout.write(render(t, args.status, args.group))
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
