"""Tests for tracker.py. Standard library only:

    python3 -m unittest discover -s skills/tracker/scripts
"""
import json
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
        self.assertEqual(item["context"], text)
        self.assertEqual(item["thread"][0]["text"], text)
        self.assertEqual(tracker.problems(t), [])
        self.assertEqual(tracker.add_replies(t, [("new", text)]), ([], []))   # pasted twice
        self.assertEqual(len(t["items"]), 5)

    def test_new_is_not_an_item_id(self):
        t = sample()
        t["items"][0]["id"] = "new"
        self.assertIn("'new' is reserved", " ".join(tracker.problems(t)))

    def test_replies_for_unknown_items_are_reported(self):
        self.assertEqual(tracker.add_replies(sample(), [("GONE", "hi")]), ([], ["GONE"]))


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
