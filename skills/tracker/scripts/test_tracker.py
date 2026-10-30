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
    t = tracker.new_tracker("Demo · Plan", ["now", "later"], "What is planned for the demo. Long-lived.")
    t["items"] = [
        {"id": "T1", "group": "now", "title": "Fix the thing", "status": "todo"},
        {"id": "T2", "group": "now", "title": "Pick a colour", "status": "waiting",
         "kind": "decision", "question": "Blue or green?", "thread": []},
        {"id": "T3", "group": "later", "title": "Old idea", "status": "dropped",
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

    def test_unknown_group_duplicate_id_and_bad_status_are_caught(self):
        t = sample()
        t["items"].append({"id": "T1", "group": "someday", "title": "x", "status": "maybe"})
        msgs = " ".join(tracker.problems(t))
        self.assertIn("the id is used twice", msgs)
        self.assertIn("group 'someday' is not in 'groups'", msgs)
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

    def test_replies_are_appended_once_and_never_change_a_status(self):
        t = sample()
        added, unknown = tracker.add_replies(t, [("T2", "Green.")], at="2026-10-05T10:00:00+00:00")
        self.assertEqual((added, unknown), ([("T2", "Green.")], []))
        self.assertEqual(t["items"][1]["thread"][-1],
                         {"by": "owner", "at": "2026-10-05T10:00:00+00:00", "text": "Green."})
        self.assertEqual(t["items"][1]["status"], "waiting")
        # Pasting the same text again changes nothing.
        self.assertEqual(tracker.add_replies(t, [("T2", "Green.")]), ([], []))
        self.assertEqual(len(t["items"][1]["thread"]), 1)

    def test_a_reply_to_new_becomes_a_todo_in_the_first_group_once(self):
        t = sample()
        text = "Add a dark mode.\nOnly for the settings page."
        added, _ = tracker.add_replies(t, [("new", text), ("new", "Ship it")], at="2026-10-05T10:00:00+00:00")
        self.assertEqual([i for i, _ in added], ["new-1", "new-2"])
        item = t["items"][3]
        self.assertEqual((item["group"], item["status"], item["title"]), ("now", "todo", "Add a dark mode."))
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


class OwnerActions(unittest.TestCase):
    def test_add_makes_a_fresh_draft_or_todo_the_owner_can_still_edit(self):
        t = sample()
        d = tracker.add(t, "Try a sidebar\nMaybe on the left.", status="draft")
        m = tracker.add(t, "Renew the domain", for_me=True, group="later")
        self.assertEqual((d["id"], d["status"], d["title"], d["fresh"]), ("new-1", "draft", "Try a sidebar", True))
        self.assertEqual((m["id"], m["for"], m["group"]), ("new-2", "me", "later"))
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

    def test_move_reorders_and_regroups(self):
        t = sample()
        tracker.move(t, "T2", "now", before="T1")
        self.assertEqual([i["id"] for i in t["items"]], ["T2", "T1", "T3"])
        tracker.move(t, "T2", "later")
        self.assertEqual([(i["id"], i["group"]) for i in t["items"]], [("T1", "now"), ("T3", "later"), ("T2", "later")])
        tracker.move(t, "T2", "now")      # last in a group, before the next group's items
        self.assertEqual([i["id"] for i in t["items"]], ["T1", "T2", "T3"])

    def test_a_move_that_no_longer_applies_is_refused_and_changes_nothing(self):
        t = sample()
        before = json.dumps(t)
        for args in [("T1", "now", "GONE"), ("T1", "now", "T3"), ("T1", "someday", None), ("GONE", "now", None)]:
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

    def test_the_owner_ticks_only_their_own_to_dos(self):
        t = sample()
        tracker.add(t, "Renew the domain", for_me=True)
        tracker.tick(t, "new-1")
        self.assertEqual(t["items"][-1]["status"], "done")
        self.assertEqual(tracker.problems(t), [])
        with self.assertRaises(tracker.Refused):
            tracker.tick(t, "T1")

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

    def test_the_owner_renames_adds_reorders_and_removes_empty_sections(self):
        t = sample()
        tracker.rename_group(t, "later", "Someday")
        self.assertEqual(tracker.add_group(t, "Ideas & bets"), "ideas-bets")
        self.assertEqual(tracker.add_group(t, "Ideas & bets"), "ideas-bets-2")
        tracker.move_group(t, "ideas-bets", before="now")
        self.assertEqual([g["id"] for g in t["groups"]], ["ideas-bets", "now", "later", "ideas-bets-2"])
        self.assertEqual(t["groups"][2]["title"], "Someday")
        tracker.delete_group(t, "ideas-bets-2")
        with self.assertRaises(tracker.Refused):          # holds a dropped item
            tracker.delete_group(t, "later")
        with self.assertRaises(tracker.Refused):
            tracker.move_group(t, "now", before="GONE")
        with self.assertRaises(tracker.Refused):
            tracker.rename_group(t, "now", "  ")
        self.assertEqual(tracker.problems(t), [])

    def test_act_writes_the_file_and_its_page_atomically_and_upgrades_the_schema(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "TRACKER.json"
            t = sample()
            t["schema"] = 1
            tracker.save(path, t)
            item = tracker.act(path, tracker.add, "From the hub", status="draft")
            saved = tracker.load(path)
            self.assertEqual((saved["schema"], saved["items"][-1]["id"]), (2, item["id"]))
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
        t["items"].append({"id": f"B{n}", "group": "later", "title": f"Bulk item {n} " + "words " * 30,
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
        self.assertIn("drafts 1 (the owner's, not yet for you)", lines[0])
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
            t["items"].append({"id": "T1", "group": "now", "title": "x", "status": "waiting", "question": "Ok?"})
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
        self.assertIn("Dropped: Not worth it: nobody asked.", md)
        self.assertNotIn("Old idea", tracker.render(sample(), status="waiting"))


if __name__ == "__main__":
    unittest.main()
