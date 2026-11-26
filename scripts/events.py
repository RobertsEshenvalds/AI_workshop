"""Show what happened in the team repository, as a timeline.

    python scripts/events.py              # print once
    python scripts/events.py --follow     # pull and refresh every 5 seconds (for the projector)
"""

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUIET_ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0")


def read_status(path):
    fields = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line[0] in " \t#" or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.split(" #", 1)[0].strip().strip("'\"") or "-"
    return fields


def load_events():
    events = []
    for path in sorted((ROOT / "tasks").glob("*/events.jsonl")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                events.append({
                    "timestamp": "?", "task": path.parent.name, "agent": "?",
                    "event": "UNREADABLE_LINE", "reason": f"line {number} is not valid JSON",
                })
    return sorted(events, key=lambda event: str(event.get("timestamp", "")))


def render(last):
    lines = ["TASKS"]
    for path in sorted((ROOT / "tasks").glob("*/status.yaml")):
        s = read_status(path)
        lines.append(
            f"  {s.get('task', path.parent.name):<10} {s.get('status', '-'):<22} "
            f"next: {s.get('assigned_to', '-'):<18} attempt {s.get('attempt', '-')}   "
            f"mode {s.get('routing_mode', '-')}"
        )
    lines += ["", f"EVENTS (latest {last})"]
    for event in load_events()[-last:]:
        stamp = str(event.get("timestamp", "?"))
        clock = stamp[11:19] if len(stamp) >= 19 else stamp
        to = f"-> {event['to']}" if event.get("to") else ""
        detail = " ".join(str(part) for part in (event.get("type"), event.get("reason")) if part)
        lines.append(
            f"  {clock:<8}  {str(event.get('task', '?')):<9} {str(event.get('agent', '?')):<14} "
            f"{str(event.get('event', '?')):<22} {to:<20} {detail}"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Show the team's task status and event timeline.")
    parser.add_argument("--follow", action="store_true", help="Pull and refresh every few seconds.")
    parser.add_argument("--every", type=float, default=5, help="Seconds between refreshes (default 5).")
    parser.add_argument("--last", type=int, default=25, help="How many events to show (default 25).")
    args = parser.parse_args()

    if not args.follow:
        print(render(args.last))
        return
    try:
        while True:
            status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                                    capture_output=True, text=True, env=QUIET_ENV)
            if not status.stdout.strip():
                subprocess.run(["git", "pull", "--rebase", "--quiet"], cwd=ROOT,
                               capture_output=True, text=True, env=QUIET_ENV)
            os.system("cls" if os.name == "nt" else "clear")
            print(render(args.last))
            print(f"\n(refreshing every {args.every:g} seconds, Ctrl+C to stop)", flush=True)
            time.sleep(args.every)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
