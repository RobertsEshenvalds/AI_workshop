"""Checks for the facilitator's release script, scripts/new_task.py."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


new_task = load("new_task")
watch = load("watch")

# Facilitators may remove facilitator/ from the team template. Then skip, don't fail.
needs_cards = unittest.skipUnless(new_task.CARDS_DIR.is_dir(), "facilitator/cards/ is not in this copy")


class NewTaskTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.tasks = self.root / "tasks"
        self.tasks.mkdir()
        self.old_root = watch.ROOT
        watch.ROOT = self.root

    def tearDown(self):
        watch.ROOT = self.old_root
        self.tmp.cleanup()

    def release(self, mode):
        task_id = new_task.next_task_id(self.tasks)
        return new_task.create_task(self.tasks, "Wish text.", task_id, mode, new_task.utc_now())

    @needs_cards
    def test_every_card_has_a_wish(self):
        cards = sorted(new_task.CARDS_DIR.glob("*.md"))
        self.assertTrue(cards)
        for card in cards:
            with self.subTest(card=card.name):
                self.assertTrue(new_task.card_section(card, "Wish card"))

    @needs_cards
    def test_ten_cards_per_stage(self):
        for stage in range(1, 6):
            with self.subTest(stage=stage):
                cards = new_task.find_stage(f"S{stage}")
                self.assertEqual(len(cards), 10)
                for card in cards:
                    self.assertIn(f"Stage {stage}", new_task.card_title(card))
                    self.assertTrue(new_task.card_section(card, "Follow-up from Business"))

    @needs_cards
    def test_task_md_has_only_the_wish_text(self):
        card = new_task.find_card("S2-A")
        wish = new_task.card_section(card, "Wish card")
        task_dir = new_task.create_task(self.tasks, wish, "TASK-002", "SELF_ROUTING", "2026-11-26T10:00:00Z")
        text = (task_dir / "task.md").read_text(encoding="utf-8")
        self.assertIn(wish, text)
        self.assertNotIn("What good looks like", text)

    def test_task_numbers_continue(self):
        (self.tasks / "TASK-001").mkdir()
        (self.tasks / "TASK-007").mkdir()
        self.assertEqual(new_task.next_task_id(self.tasks), "TASK-008")

    def test_self_routing_goes_straight_to_the_ba(self):
        task_dir = self.release("SELF_ROUTING")
        turns = watch.find_turns({"PRODUCT_BA", "PRODUCT_OWNER"}, 10)
        self.assertEqual([turn.task for turn in turns], [task_dir.name])
        event = json.loads((task_dir / "events.jsonl").read_text(encoding="utf-8"))
        self.assertEqual((event["event"], event["to"]), ("TASK_CREATED", "PRODUCT_BA"))

    def test_scrum_master_mode_waits_for_routing(self):
        self.release("SCRUM_MASTER")
        self.assertEqual(watch.find_turns({"PRODUCT_BA", "PRODUCT_OWNER"}, 10), [])
        [turn] = watch.find_turns({"SCRUM_MASTER"}, 10)
        self.assertFalse(turn.stuck)
        self.assertEqual(watch.routine_route(turn), ("READY_FOR_BA", "PRODUCT_BA"))

    def test_mode_follows_existing_tasks(self):
        self.release("SELF_ROUTING")
        self.assertEqual(new_task.current_mode(self.tasks), "SELF_ROUTING")
        self.release("SCRUM_MASTER")
        self.assertEqual(new_task.current_mode(self.tasks), "SCRUM_MASTER")

    def test_follow_up_is_added_to_open_tasks_only(self):
        task_dir = self.release("SELF_ROUTING")
        new_task.add_follow_up(self.tasks, task_dir.name, "Also this.")
        self.assertIn("## Follow-up from Business\n\nAlso this.", (task_dir / "task.md").read_text(encoding="utf-8"))

        status = task_dir / "status.yaml"
        status.write_text(status.read_text(encoding="utf-8").replace("READY_FOR_BA", "ACCEPTED"), encoding="utf-8")
        with self.assertRaises(SystemExit):
            new_task.add_follow_up(self.tasks, task_dir.name, "Too late.")


if __name__ == "__main__":
    unittest.main()
