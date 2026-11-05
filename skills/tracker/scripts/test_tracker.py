"""Tests for tracker.py. Standard library only:

    python3 -m unittest discover -s skills/tracker/scripts
"""
import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

import tracker


def sample():
    t = tracker.new_tracker("Demo · Plan", "What is planned for the demo. Long-lived.")
    t["items"] = [
        {"id": "T1", "title": "Fix the thing", "status": "todo"},
        {"id": "T2", "title": "Pick a colour", "status": "waiting",
         "kind": "decision", "question": "Blue or green?", "thread": []},
        {"id": "T3", "title": "Old idea", "status": "dropped",
         "outcome": "Not worth it: nobody asked."},
    ]
    return t


class Check(unittest.TestCase):
    def test_a_sound_tracker_has_no_problems(self):
        self.assertEqual(tracker.problems(sample()), [])

    def test_title_and_summary_are_required_and_short(self):
        t = sample()
        t["summary"] = ""
        self.assertTrue(any("'summary' is missing" in p for p in tracker.problems(t)))
        t["summary"] = "x" * (tracker.MAX_SUMMARY + 1)
        t["title"] = "x" * (tracker.MAX_TITLE + 1)
        self.assertEqual(len(tracker.problems(t)), 2)

    def test_waiting_needs_a_question_and_closed_needs_an_outcome(self):
        t = sample()
        t["items"][1]["question"] = ""
        t["items"][0]["status"] = "done"
        msgs = " ".join(tracker.problems(t))
        self.assertIn("T2 is waiting on the owner but has no 'question'", msgs)
        self.assertIn("T1 is done but has no 'outcome'", msgs)

    def test_duplicate_id_and_bad_status_are_caught(self):
        t = sample()
        t["items"].append({"id": "T1", "title": "x", "status": "maybe"})
        msgs = " ".join(tracker.problems(t))
        self.assertIn("the id is used twice", msgs)
        self.assertIn("status must be one of", msgs)

    def test_ids_must_be_safe_in_reply_lines(self):
        t = sample()
        t["items"][0]["id"] = "fix/1"
        self.assertIn("ids may use letters", " ".join(tracker.problems(t)))


COPIED = """/tracker Replies to Demo · Plan (TRACKER.json):

[T2] Green.
The darker one, if there are two.

[T1] Go ahead.
"""


class Replies(unittest.TestCase):
    def test_parses_what_the_copy_button_produces(self):
        self.assertEqual(tracker.parse_replies(COPIED), [
            ("T2", "Green.\nThe darker one, if there are two."), ("T1", "Go ahead.")])

    def test_a_reply_moves_a_question_to_todo_for_an_agent_to_read(self):
        t = sample()
        tracker.add_replies(t, [("T2", "Green.")])
        it = t["items"][1]
        self.assertEqual((it["status"], it["question"], it["unread"]), ("todo", "Blue or green?", True))
        self.assertTrue(tracker.pending(it))
        self.assertEqual(tracker.problems(t), [])
        typed = sample()
        tracker.reply(typed, "T2", "Green.")
        self.assertEqual(typed["items"][1]["status"], "todo")
        tracker.reply(typed, "T1", "And quickly.")               # not a question: it stays where it is
        self.assertEqual(typed["items"][0]["status"], "todo")

    def test_a_reply_elsewhere_moves_nothing_and_a_draft_stays_a_draft(self):
        t = sample()
        t["items"].append({"id": "D", "title": "Started", "status": "doing"})
        t["items"].append({"id": "A", "title": "An idea", "status": "draft"})
        tracker.add_replies(t, [("D", "Hurry."), ("A", "Maybe.")])
        self.assertEqual([i["status"] for i in t["items"][-2:]], ["doing", "draft"])

    def test_deleting_the_answer_puts_the_question_back(self):
        t = sample()
        tracker.reply(t, "T2", "Green.")
        tracker.delete_reply(t, "T2", 0, t["items"][1]["thread"][0]["at"])
        self.assertEqual(t["items"][1]["status"], "waiting")
        self.assertFalse(tracker.pending(t["items"][1]))

    def test_a_reply_is_appended_once(self):
        t = sample()
        added, unknown = tracker.add_replies(t, [("T2", "Green.")], at="2026-10-05T10:00:00+00:00")
        self.assertEqual((added, unknown), ([("T2", "Green.")], []))
        self.assertEqual(t["items"][1]["thread"][-1],
                         {"by": "owner", "at": "2026-10-05T10:00:00+00:00", "text": "Green."})
        # Pasting the same text again changes nothing.
        self.assertEqual(tracker.add_replies(t, [("T2", "Green.")]), ([], []))
        self.assertEqual(len(t["items"][1]["thread"]), 1)

    def test_a_reply_to_new_becomes_a_todo_once(self):
        t = sample()
        text = "Add a dark mode.\nOnly for the settings page."
        added, _ = tracker.add_replies(t, [("new", text), ("new", "Ship it")], at="2026-10-05T10:00:00+00:00")
        self.assertEqual([i for i, _ in added], ["new-1", "new-2"])
        item = t["items"][3]
        self.assertEqual((item["status"], item["title"]), ("todo", "Add a dark mode."))
        # The owner's words are the item itself, flagged unseen, so they can still edit it.
        self.assertEqual((item["context"], item["fresh"]), (text, True))
        self.assertEqual(tracker.problems(t), [])
        self.assertEqual(tracker.add_replies(t, [("new", text)]), ([], []))   # pasted twice
        self.assertEqual(len(t["items"]), 5)

    def test_new_is_not_an_item_id(self):
        t = sample()
        t["items"][0]["id"] = "new"
        self.assertIn("'new' is reserved", " ".join(tracker.problems(t)))

    def test_replies_for_unknown_items_are_reported(self):
        self.assertEqual(tracker.add_replies(sample(), [("GONE", "hi")]), ([], ["GONE"]))


class Schema2(unittest.TestCase):
    def test_a_schema_1_file_is_still_valid(self):
        t = sample()
        t["schema"] = 1
        self.assertEqual(tracker.problems(t), [])

    def test_new_fields_are_checked(self):
        t = sample()
        t["items"][0].update({"status": "draft", "for": "me", "fresh": True, "spawned": "trackers/x.json",
                              "blocked_by": ["T2", "takamagahara/php-shared"]})
        self.assertEqual(tracker.problems(t), [])
        t["items"][0].update({"for": "someone", "fresh": "yes", "blocked_by": ["T9"]})
        msgs = " ".join(tracker.problems(t))
        self.assertIn("'for' must be agent or me", msgs)
        self.assertIn("'fresh' must be true or false", msgs)
        self.assertIn("blocked by 'T9', which is not an item here", msgs)


class Order(unittest.TestCase):
    def test_a_file_with_sections_becomes_one_list_in_their_order(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TRACKER.json"
            old = sample()
            old.update(schema=2, groups=[{"id": "now", "title": "Now"}, {"id": "later", "title": "Later"}])
            old["items"] = [dict(old["items"][2], group="later"), dict(old["items"][0], group="now"), dict(old["items"][1], group="now")]
            path.write_text(json.dumps(old))
            t = tracker.load(path)
            self.assertEqual([i["id"] for i in t["items"]], ["T1", "T2", "T3"])
            self.assertNotIn("groups", t)
            self.assertNotIn("group", t["items"][0])
            self.assertEqual(tracker.problems(t), [])
            tracker.act(path, tracker.reply, "T1", "Hi")
            self.assertNotIn("groups", json.loads(path.read_text()))

    def test_sections_left_in_a_new_file_are_flattened_not_kept(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TRACKER.json"
            t = sample()
            t["items"][0]["group"] = "now"                     # an agent's habit, with no sections at all
            path.write_text(json.dumps(t))
            self.assertEqual(tracker.main(["build", str(path)]), 0)
            self.assertNotIn("group", path.read_text())

    def test_a_new_tracker_has_only_what_a_tracker_needs(self):
        self.assertEqual(sorted(tracker.new_tracker("Demo · Plan", "What. Long-lived.")), ["items", "schema", "summary", "title"])

    def test_statuses_always_read_draft_needs_you_to_do_in_progress_then_the_archive(self):
        self.assertEqual([tracker.STATUS_LABEL[s] for s in tracker.STATUSES],
                         ["Draft", "Needs you", "To do", "In progress", "Done", "Not doing"])
        t = sample()
        t["items"] += [{"id": "D", "title": "An idea", "status": "doing"}, {"id": "A", "title": "A thought", "status": "draft"},
                       {"id": "O", "title": "Late", "status": "done", "outcome": "x", "closed": "2026-11-02"},
                       {"id": "N", "title": "Later", "status": "done", "outcome": "x", "closed": "2026-11-03"}]
        text = tracker.render(t)
        heads = [l[3:] for l in text.splitlines() if l.startswith("## ")]
        self.assertEqual(heads, ["Draft", "Needs you", "To do", "In progress", "Done", "Not doing"])
        self.assertLess(text.index("**N**"), text.index("**O**"))     # the archive: newest first

    def test_the_brief_keeps_that_order_too(self):
        t = sample()
        t["items"] += [{"id": "D", "title": "Started", "status": "doing"}, {"id": "A", "title": "A thought", "status": "draft"}]
        text = tracker.brief(t, "TRACKER.json")
        self.assertIn("drafts 1 (not yet for you), needs you 1, to do 1, in progress 1, archive 1", text)
        self.assertLess(text.index("Waiting on the owner"), text.index("Next to do"))
        self.assertLess(text.index("Next to do"), text.index("In progress:"))


class OwnerActions(unittest.TestCase):
    def test_add_makes_a_fresh_draft_or_todo_the_owner_can_still_edit(self):
        t = sample()
        d = tracker.add(t, "Try a sidebar\nMaybe on the left.", status="draft")
        m = tracker.add(t, "Renew the domain", for_me=True)
        self.assertEqual((d["id"], d["status"], d["title"], d["fresh"]), ("new-1", "draft", "Try a sidebar", True))
        self.assertEqual((m["id"], m["for"]), ("new-2", "me"))
        self.assertEqual(tracker.edit(t, "new-1", "Try a top bar"), "edited")
        self.assertEqual((d["title"], d["context"]), ("Try a top bar", ""))
        self.assertEqual(tracker.problems(t), [])
        with self.assertRaises(tracker.Refused):
            tracker.add(t, "x", status="doing")
        with self.assertRaises(tracker.Refused):
            tracker.add(t, "   ")

    def test_once_an_agent_has_worked_on_it_an_edit_becomes_a_reply_and_delete_is_refused(self):
        t = sample()
        self.assertEqual(tracker.edit(t, "T1", "Fix it before Friday"), "replied")
        self.assertEqual(t["items"][0]["title"], "Fix the thing")
        self.assertEqual(t["items"][0]["thread"][-1]["text"], "Fix it before Friday")
        with self.assertRaises(tracker.Refused):
            tracker.delete(t, "T1")
        tracker.add(t, "Scratch that")
        tracker.delete(t, "new-1")
        self.assertNotIn("new-1", [i["id"] for i in t["items"]])

    def test_promote_turns_a_draft_into_a_todo_only(self):
        t = sample()
        tracker.add(t, "Idea", status="draft")
        tracker.promote(t, "new-1")
        self.assertEqual(t["items"][-1]["status"], "todo")
        with self.assertRaises(tracker.Refused):
            tracker.promote(t, "new-1")

    def test_demote_turns_a_todo_back_into_a_draft_only(self):
        t = sample()
        tracker.add(t, "Idea")
        tracker.demote(t, "new-1")
        self.assertEqual(t["items"][-1]["status"], "draft")
        self.assertFalse(tracker.pending(t["items"][-1]))
        with self.assertRaises(tracker.Refused):
            tracker.demote(t, "T2")

    def test_move_puts_an_item_before_another_or_last(self):
        t = sample()
        tracker.move(t, "T2", before="T1")
        self.assertEqual([i["id"] for i in t["items"]], ["T2", "T1", "T3"])
        tracker.move(t, "T2")
        self.assertEqual([i["id"] for i in t["items"]], ["T1", "T3", "T2"])

    def test_a_move_that_no_longer_applies_is_refused_and_changes_nothing(self):
        t = sample()
        before = json.dumps(t)
        for args in [("T1", "GONE"), ("GONE", None)]:
            with self.assertRaises(tracker.Refused):
                tracker.move(t, *args)
        self.assertEqual(json.dumps(t), before)

    def test_a_typed_reply_is_never_skipped_as_a_duplicate(self):
        t = sample()
        tracker.reply(t, "T2", "Yes.")
        tracker.reply(t, "T2", "Yes.")
        self.assertEqual([m["text"] for m in t["items"][1]["thread"]], ["Yes.", "Yes."])
        with self.assertRaises(tracker.Refused):
            tracker.reply(t, "GONE", "Hi")

    def test_reopen_needs_a_reason_and_puts_it_in_the_thread(self):
        t = sample()
        with self.assertRaises(tracker.Refused):
            tracker.reopen(t, "T3")
        tracker.reopen(t, "T3", "Someone asked after all.")
        self.assertEqual(t["items"][2]["status"], "todo")
        self.assertEqual(t["items"][2]["thread"][-1]["text"], "Someone asked after all.")
        with self.assertRaises(tracker.Refused):
            tracker.reopen(t, "T1", "It is open.")

    def test_the_owner_archives_any_open_item_as_done_or_not_doing(self):
        t = sample()
        tracker.add(t, "Renew the domain", for_me=True)
        tracker.archive(t, "new-1")
        tracker.reply(t, "T2", "Forget it.")
        tracker.archive(t, "T2", "dropped", "Nobody will see the difference.")
        tracker.archive(t, "T1", "dropped")
        by_id = {i["id"]: i for i in t["items"]}
        self.assertEqual(by_id["new-1"]["status"], "done")
        self.assertEqual((by_id["T2"]["status"], by_id["T2"]["outcome"]), ("dropped", "Nobody will see the difference."))
        self.assertFalse(tracker.pending(by_id["T2"]))         # nothing is left for an agent to read
        self.assertEqual(tracker.problems(t), [])              # the outcome a closed item needs is there
        with self.assertRaises(tracker.Refused):
            tracker.archive(t, "T1")
        with self.assertRaises(tracker.Refused):
            tracker.archive(sample(), "T1", "maybe")

    def test_archiving_keeps_the_progress_an_item_already_records(self):
        t = sample()
        t["items"][0].update(status="doing", outcome="Half of it is in.")
        tracker.archive(t, "T1")
        self.assertEqual(t["items"][0]["outcome"], "Half of it is in.")

    def test_everything_that_closes_is_dated_and_a_reopened_item_forgets_it(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TRACKER.json"
            t = sample()
            t["items"][2]["updated"] = "2026-10-05"           # closed by an agent, by hand, long ago
            tracker.save(path, t)
            tracker.act(path, tracker.archive, "T1")
            t = tracker.load(path)
            self.assertEqual(t["items"][2]["closed"], "2026-10-05")
            self.assertIn("T", t["items"][0]["closed"])        # today: to the second, so it sorts newest
            self.assertEqual(sorted(t["items"], key=tracker.closed_at, reverse=True)[0]["id"], "T1")
            tracker.act(path, tracker.reopen, "T1", "Not quite.")
            self.assertNotIn("closed", tracker.load(path)["items"][0])

    def test_a_reply_no_agent_has_read_can_be_edited_or_deleted(self):
        t = sample()
        tracker.reply(t, "T2", "Blue.")
        tracker.reply(t, "T2", "No, wait.")
        first, second = t["items"][1]["thread"]
        tracker.edit_reply(t, "T2", 0, first["at"], "Green.")
        tracker.delete_reply(t, "T2", 1, second["at"])
        self.assertEqual([m["text"] for m in t["items"][1]["thread"]], ["Green."])
        with self.assertRaises(tracker.Refused):          # the thread changed under it
            tracker.edit_reply(t, "T2", 1, second["at"], "x")
        tracker.delete_reply(t, "T2", 0, first["at"])
        self.assertFalse(tracker.pending(t["items"][1]))    # nothing unseen is left

    def test_a_reply_the_agent_has_read_or_answered_stays(self):
        t = sample()
        tracker.reply(t, "T2", "Blue.")
        at = t["items"][1]["thread"][0]["at"]
        t["items"][1]["thread"].append({"by": "agent", "at": at, "text": "Blue it is."})
        with self.assertRaises(tracker.Refused):
            tracker.delete_reply(t, "T2", 0, at)
        t["items"][1]["thread"].pop()
        del t["items"][1]["unread"]                         # read, not answered
        with self.assertRaises(tracker.Refused):
            tracker.edit_reply(t, "T2", 0, at, "Green.")

    def test_the_owner_rewrites_the_title_and_the_summary(self):
        t = sample()
        tracker.edit_tracker(t, title="Demo  · Launch", summary="What the demo needs.\nLong-lived.")
        self.assertEqual((t["title"], t["summary"]), ("Demo · Launch", "What the demo needs. Long-lived."))
        for bad in ({"title": " "}, {"summary": " "}):
            with self.assertRaises(tracker.Refused):
                tracker.edit_tracker(t, **bad)

    def test_a_title_past_the_limit_is_refused_and_the_file_keeps_its_own(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TRACKER.json"
            tracker.save(path, sample())
            with self.assertRaises(tracker.Refused):
                tracker.act(path, tracker.edit_tracker, title="x" * (tracker.MAX_TITLE + 1))
            self.assertEqual(tracker.load(path)["title"], "Demo · Plan")

    def test_act_writes_the_file_and_its_page_atomically_and_upgrades_the_schema(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TRACKER.json"
            t = sample()
            t["schema"] = 1
            tracker.save(path, t)
            item = tracker.act(path, tracker.add, "From the hub", status="draft")
            saved = tracker.load(path)
            self.assertEqual((saved["schema"], saved["items"][-1]["id"]), (tracker.SCHEMA, item["id"]))
            self.assertIn("From the hub", (Path(d) / "TRACKER.html").read_text())
            self.assertEqual(sorted(os.listdir(d)), ["TRACKER.html", "TRACKER.json"])   # no temp files left

    def test_act_never_writes_over_a_file_that_is_invalid_or_half_written(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TRACKER.json"
            path.write_text('{"schema": 2, "items": [')
            with self.assertRaises(tracker.Refused):
                tracker.act(path, tracker.add, "x")
            bad = sample()
            bad["items"][1]["question"] = ""
            tracker.save(path, bad)
            with self.assertRaises(tracker.Refused):
                tracker.act(path, tracker.add, "x")
            self.assertEqual(len(tracker.load(path)["items"]), 3)


def big():
    t = sample()
    for n in range(80):
        t["items"].append({"id": f"B{n}", "title": f"Bulk item {n} " + "words " * 30,
                           "status": ("todo", "doing", "done", "waiting")[n % 4],
                           "question": "Ok?", "outcome": "Done."})
    return t


class Brief(unittest.TestCase):
    def test_pending_is_what_the_owner_added_or_said_unread_never_their_drafts_or_own_to_dos(self):
        t = sample()
        tracker.add(t, "New thing")
        tracker.add(t, "Half an idea", status="draft")
        tracker.add(t, "Call the bank", for_me=True)
        tracker.reply(t, "T2", "Green.")
        self.assertEqual([i["id"] for i in t["items"] if tracker.pending(i)], ["T2", "new-1"])
        del t["items"][1]["unread"]          # the agent, once it has processed the reply
        self.assertFalse(tracker.pending(t["items"][1]))
        tracker.promote(t, "new-2")
        self.assertTrue(tracker.pending(t["items"][4]))

    def test_replies_processed_before_unread_existed_are_not_pending(self):
        t = sample()
        t["items"][1]["thread"] = [{"by": "owner", "at": "2026-10-05T10:00:00+00:00", "text": "Green."}]
        self.assertFalse(tracker.pending(t["items"][1]))

    def test_brief_stays_short_whatever_the_size_and_leads_with_the_owners_news(self):
        t = big()
        tracker.add(t, "Add an export")
        tracker.add(t, "Not yet", status="draft")
        tracker.reply(t, "T2", "Green.")
        text = tracker.brief(t, "TRACKER.json")
        lines = text.splitlines()
        self.assertLessEqual(len(lines), 30)
        self.assertTrue(all(len(l) <= 140 for l in lines))
        self.assertIn("From the owner, not yet seen:", lines[1])
        self.assertIn("[new-1] new: Add an export", text)
        self.assertIn("[T2] Pick a colour · owner: Green.", text)
        self.assertIn("drafts 1 (not yet for you)", lines[0])
        self.assertNotIn("Not yet", text)
        self.assertIn("… and", text)

    def test_brief_without_a_path_reads_every_tracker_of_the_repository(self):
        with tempfile.TemporaryDirectory() as d:
            tracker.save(Path(d) / "TRACKER.json", sample())
            (Path(d) / "trackers").mkdir()
            effort = sample()
            effort["title"] = "Demo · Review"
            tracker.save(Path(d) / "trackers" / "review.json", effort)
            out, cwd = io.StringIO(), os.getcwd()
            os.chdir(d)
            try:
                with contextlib.redirect_stdout(out):
                    self.assertEqual(tracker.main(["brief"]), 0)
            finally:
                os.chdir(cwd)
            self.assertIn("Demo · Plan (TRACKER.json)", out.getvalue())
            self.assertIn("Demo · Review (trackers/review.json)", out.getvalue())

    def test_brief_rebuilds_a_missing_or_stale_page_and_leaves_a_current_one(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TRACKER.json"
            tracker.save(path, sample())
            (Path(d) / "TRACKER.html").write_text("<p>an older template</p>")
            with contextlib.redirect_stdout(io.StringIO()) as out:
                tracker.main(["brief", str(path)])
            self.assertIn("Rebuilt", out.getvalue())
            self.assertEqual((Path(d) / "TRACKER.html").read_text(), tracker.build_page(sample(), "TRACKER.json"))
            with contextlib.redirect_stdout(io.StringIO()) as out:
                tracker.main(["brief", str(path)])
            self.assertNotIn("Rebuilt", out.getvalue())

    def test_show_prints_one_item_in_full(self):
        self.assertEqual(json.loads(tracker.show(sample(), "T2"))["question"], "Blue or green?")
        with self.assertRaises(tracker.Refused):
            tracker.show(sample(), "GONE")


class Page(unittest.TestCase):
    def test_the_page_embeds_the_tracker_safely_and_deterministically(self):
        t = sample()
        t["items"][0]["context"] = "Ends with </script><!-- here"
        page = tracker.build_page(t, "TRACKER.json")
        self.assertIn("<title>Demo · Plan</title>", page)
        self.assertNotIn("</script><!--", page)
        data = page.split('id="tracker-data">', 1)[1].split("</script>", 1)[0]
        self.assertEqual(json.loads(data)["tracker"], t)
        self.assertEqual(page, tracker.build_page(t, "TRACKER.json"))
        self.assertNotIn("https://", page)     # nothing loads from the network

    def test_cli_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "TRACKER.json")
            new = ["new", path, "--title", "Demo · Plan", "--summary", "What is planned. Long-lived."]
            self.assertEqual(tracker.main(new), 0)
            self.assertEqual(tracker.main(new), 1)   # never overwrites
            self.assertTrue((Path(d) / "TRACKER.html").exists())
            self.assertEqual(tracker.main(["build", path]), 0)
            t = tracker.load(path)
            t["items"].append({"id": "T1", "title": "x", "status": "waiting", "question": "Ok?"})
            tracker.save(path, t)
            copied = Path(d) / "copied.txt"
            copied.write_text("Replies to Demo:\n\n[T1] Yes.\n")
            self.assertEqual(tracker.main(["reply", path, "--from", str(copied)]), 0)
            self.assertEqual(tracker.load(path)["items"][0]["thread"][0]["text"], "Yes.")
            self.assertIn("Yes.", (Path(d) / "TRACKER.html").read_text())


class Render(unittest.TestCase):
    def test_render_shows_questions_and_outcomes(self):
        md = tracker.render(sample())
        self.assertIn("Question: Blue or green?", md)
        self.assertIn("Not doing: Not worth it: nobody asked.", md)
        self.assertNotIn("Old idea", tracker.render(sample(), status="waiting"))


if __name__ == "__main__":
    unittest.main()
