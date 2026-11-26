"""Facilitators: release a task card from facilitator/cards/ as a new task.

It creates tasks/TASK-NNN/ with task.md (the card's wish text, word for word),
status.yaml and events.jsonl, stamped with the current UTC time. That way the
watchers pick it up at once, and the Scrum Master's stuck-task rule doesn't fire
on an old timestamp.

Examples:
    python scripts/new_task.py --list
    python scripts/new_task.py S1 --show        # print the Stage 1 paper wish cards
    python scripts/new_task.py S2-A --push
    python scripts/new_task.py S3-A --mode SCRUM_MASTER --push
    python scripts/new_task.py --follow-up TASK-003 S3-A --push

Routing mode:
    SELF_ROUTING   (Stages 1 and 2) the task starts as READY_FOR_BA, assigned to PRODUCT_BA.
    SCRUM_MASTER   (Stage 3 on)    the task starts as NEW, assigned to SCRUM_MASTER, and the
                                   Scrum Master's watcher routes it to PRODUCT_BA in seconds.
    Without --mode, the script uses SCRUM_MASTER if any task already has it, otherwise
    SELF_ROUTING. From Stage 3 on, pass --mode SCRUM_MASTER to be sure.

With --push it pulls first (so the task number is the next free one), then commits
and pushes only the new task folder. Without --push it only writes the files.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = ROOT / "facilitator" / "cards"
QUIET_ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0")
MODES = ("SELF_ROUTING", "SCRUM_MASTER")


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args, root=ROOT):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, env=QUIET_ENV)


# --- Cards ---------------------------------------------------------------------------


def find_card(name, cards_dir=CARDS_DIR):
    """A card by code (S2-A) or by file path."""
    path = Path(name)
    if path.is_file():
        return path
    for candidate in sorted(cards_dir.glob("*.md")):
        if candidate.stem.upper() == name.upper():
            return candidate
    known = ", ".join(card.stem for card in sorted(cards_dir.glob("*.md")) if card.stem != "README")
    raise SystemExit(f"No card '{name}'. Known cards: {known or 'none'}")


def card_section(path, heading):
    """The text under '## <heading>' in a card, up to the next '## ' heading."""
    lines, inside = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip().lower() == heading.lower()
            continue
        if inside:
            lines.append(line)
    return "\n".join(lines).strip()


def find_stage(prefix, cards_dir=CARDS_DIR):
    """Every card of one stage, for example S1, for printing."""
    cards = [c for c in sorted(cards_dir.glob("*.md")) if c.stem.upper().startswith(prefix.upper() + "-")]
    return cards or [find_card(prefix, cards_dir)]


def card_title(path):
    """The heading, plus the type, stage and size line under it."""
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    title = next((line[2:] for line in lines if line.startswith("# ")), path.stem)
    meta = next((line.replace("**", "") for line in lines if line.startswith("**")), "")
    return f"{title}  ({meta})" if meta else title


# --- Tasks ---------------------------------------------------------------------------


def next_task_id(tasks_dir):
    numbers = [
        int(match.group(1))
        for match in (re.fullmatch(r"TASK-(\d+)", p.name) for p in tasks_dir.glob("TASK-*"))
        if match
    ]
    return f"TASK-{max(numbers, default=0) + 1:03d}"


def current_mode(tasks_dir):
    """SCRUM_MASTER if any task already uses it, otherwise SELF_ROUTING."""
    for status_path in tasks_dir.glob("*/status.yaml"):
        text = status_path.read_text(encoding="utf-8")
        if re.search(r"^routing_mode:\s*SCRUM_MASTER\s*$", text, re.MULTILINE):
            return "SCRUM_MASTER"
    return "SELF_ROUTING"


def create_task(tasks_dir, wish, task_id, mode, timestamp):
    """Write task.md, status.yaml and events.jsonl for a new task. Returns its folder."""
    if not wish:
        raise SystemExit("The card has no text under '## Wish card'.")
    task_dir = tasks_dir / task_id
    if task_dir.exists():
        raise SystemExit(f"{task_id} already exists. Pick another --id.")

    if mode == "SCRUM_MASTER":
        status, assigned = "NEW", "SCRUM_MASTER"
        reason = "New task created, waiting for the Scrum Master to route it"
    else:
        status, assigned = "READY_FOR_BA", "PRODUCT_BA"
        reason = "New task created"

    task_dir.mkdir(parents=True)
    write(task_dir / "task.md", (
        f"# {task_id}\n\n"
        "<!-- Added by a facilitator. Nobody edits this file; a facilitator may add a "
        "\"Follow-up from Business\" below. -->\n\n"
        "## Request from Business\n\n"
        f"{wish}\n"
    ))
    write(task_dir / "status.yaml", (
        f"task: {task_id}\n"
        f"status: {status}\n"
        f"assigned_to: {assigned}\n"
        "attempt: 1\n"
        "updated_by: TRAINER\n"
        f"routing_mode: {mode}\n"
        f"routing_reason: {reason}\n"
        "result:\n"
        "issue:\n"
        "  type:\n"
        "  description:\n"
    ))
    event = {"timestamp": timestamp, "task": task_id, "agent": "TRAINER",
             "event": "TASK_CREATED", "to": assigned, "reason": reason}
    write(task_dir / "events.jsonl", json.dumps(event, separators=(",", ":")) + "\n")
    return task_dir


def add_follow_up(tasks_dir, task_id, text):
    """Add a 'Follow-up from Business' section to an open task's task.md."""
    if not text:
        raise SystemExit("The card has no text under '## Follow-up from Business'.")
    task_md = tasks_dir / task_id / "task.md"
    if not task_md.exists():
        raise SystemExit(f"{task_md.relative_to(tasks_dir.parent)} doesn't exist.")
    status = (tasks_dir / task_id / "status.yaml").read_text(encoding="utf-8")
    if re.search(r"^status:\s*(ACCEPTED|REJECTED)\s*$", status, re.MULTILINE):
        raise SystemExit(f"{task_id} is closed. Add the follow-up to an open task.")
    existing = task_md.read_text(encoding="utf-8").rstrip("\n")
    write(task_md, f"{existing}\n\n## Follow-up from Business\n\n{text}\n")
    return task_md


def write(path, text):
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def commit_and_push(paths, message):
    files = [p.relative_to(ROOT).as_posix() for p in paths]
    if git("add", *files).returncode or git("commit", "-q", "-m", message).returncode:
        raise SystemExit("git commit failed. The files are written; commit and push them yourself.")
    for _ in range(2):
        if git("push", "-q").returncode == 0:
            return
        if git("pull", "--rebase", "-q").returncode:
            git("rebase", "--abort")
            break
    raise SystemExit("git push failed. The commit is local; run git pull --rebase and git push.")


def pull_first():
    if git("status", "--porcelain").stdout.strip():
        raise SystemExit("This folder has uncommitted changes. Commit or undo them first.")
    result = git("pull", "--rebase", "-q")
    if result.returncode:
        git("rebase", "--abort")
        raise SystemExit(f"git pull failed: {result.stderr.strip() or 'unknown error'}")


# --- Command line --------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(description="Release a facilitator task card as a new task.")
    parser.add_argument("card", nargs="?", help="Card code such as S2-A, or a path to a card file.")
    parser.add_argument("--list", action="store_true", help="List the cards and stop.")
    parser.add_argument("--show", action="store_true",
                        help="Print the wish text of a card, or of every card in a stage (S1), and stop.")
    parser.add_argument("--id", help="Task ID to use instead of the next free one, e.g. TASK-010.")
    parser.add_argument("--mode", choices=MODES, help="Routing mode for the new task.")
    parser.add_argument("--follow-up", metavar="TASK", help="Add the card's follow-up to this open task.")
    parser.add_argument("--push", action="store_true", help="Pull first, then commit and push.")
    args = parser.parse_args(argv)
    tasks_dir = ROOT / "tasks"

    if args.list:
        for card in sorted(CARDS_DIR.glob("*.md")):
            if card.stem != "README":
                print(card_title(card))
        return
    if not args.card:
        parser.error("give a card code, for example: python scripts/new_task.py S2-A")
    if args.show:
        for card in find_stage(args.card):
            print(f"{'-' * 72}\n{card.stem}\n\n{card_section(card, 'Wish card')}\n")
        return
    card = find_card(args.card)
    if args.push:
        pull_first()

    if args.follow_up:
        task_md = add_follow_up(tasks_dir, args.follow_up, card_section(card, "Follow-up from Business"))
        print(f"Added the follow-up from {card.stem} to {task_md.relative_to(ROOT).as_posix()}.")
        if args.push:
            commit_and_push([task_md], f"[TRAINER] {args.follow_up}: follow-up from Business")
            print("Committed and pushed.")
        return

    mode = args.mode or current_mode(tasks_dir)
    task_id = args.id or next_task_id(tasks_dir)
    task_dir = create_task(tasks_dir, card_section(card, "Wish card"), task_id, mode, utc_now())
    print(f"Created {task_dir.relative_to(ROOT).as_posix()}/ from card {card.stem} ({mode}).")
    if args.push:
        commit_and_push([task_dir], f"[TRAINER] {task_id}: task created")
        print("Committed and pushed. The watchers pick it up within a few seconds.")
    else:
        print(f"Not pushed. To release it: git add {task_dir.relative_to(ROOT).as_posix()} && "
              f"git commit -m \"[TRAINER] {task_id}: task created\" && git push")


if __name__ == "__main__":
    sys.exit(main())
