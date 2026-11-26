"""Workshop watcher: tells your AI tool when it's your turn.

Every few seconds it pulls the repository, reads tasks/*/status.yaml and checks
whether it's your turn (WORKFLOW.md, section 4). When it is, it either starts
your AI tool with the right prompt, or (the default, --tool notify) beeps,
prints the prompt and copies it to your clipboard so you can paste it.

Examples:
    python scripts/watch.py --role DEVELOPER
    python scripts/watch.py --role PRODUCT_BA,PRODUCT_OWNER --tool claude
    python scripts/watch.py --role SCRUM_MASTER --tool claude
    python scripts/watch.py --role QA --check
    python scripts/watch.py --role QA --command "mytool run {prompt}"

Instant routing for the Scrum Master: with --role SCRUM_MASTER, the watcher makes
routine hand-overs itself (NEW, or a READY_FOR_ status with no issue), straight
from the routing table in WORKFLOW.md section 6. It wakes the Scrum Master's AI
only for turns that need judgment: failures, blocks, change requests, stuck tasks.
Add --ai-routes-everything to send every hand-over to the AI instead.

Safety rules built in:
    - it won't pull while there are uncommitted changes, so it never overwrites your work;
    - only one watcher runs per folder (a lock file in .watcher/);
    - it handles each pushed state only once (it remembers what it already handled);
    - it stops an AI run after --run-timeout minutes, and stops itself after --stop-after minutes.
"""

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from collections import namedtuple
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / ".watcher"
LOCK_FILE = STATE_DIR / "lock"
STATE_FILE = STATE_DIR / "state.json"

CLOSED = {"ACCEPTED", "REJECTED"}
HUMANS = {"HUMAN_FACILITATOR", "HUMAN_SUPPORT"}

ROLE_FILES = {
    "PRODUCT_BA": "roles/product-ba.md",
    "PRODUCT_OWNER": "roles/product-ba.md",
    "ARCHITECT": "roles/architect.md",
    "SECURITY": "roles/architect.md",
    "DEVELOPER": "roles/developer.md",
    "QA": "roles/qa.md",
    "SCRUM_MASTER": "roles/scrum-master.md",
}

SEAT_NAMES = {
    "PRODUCT_BA": "the Product Owner / BA",
    "PRODUCT_OWNER": "the Product Owner / BA",
    "ARCHITECT": "the Architect",
    "SECURITY": "the Architect",
    "DEVELOPER": "a Developer",
    "QA": "QA",
    "SCRUM_MASTER": "the Scrum Master",
}

# How each AI tool is started without a human. "{prompt}" is replaced by the prompt.
# Check yours in a dry run before the workshop; use --command if a flag differs.
TOOLS = {
    "claude": [
        "claude", "-p", "{prompt}",
        "--permission-mode", "acceptEdits",
        "--allowedTools",
        "Bash(git *),Bash(python *),Bash(python3 *),Bash(py *),"
        "PowerShell(git *),PowerShell(python *),PowerShell(py *)",
    ],
    "copilot": ["copilot", "-p", "{prompt}", "--allow-all-tools"],
    "cursor": ["agent", "-p", "--force", "{prompt}"],
    "codex": [
        "codex", "exec", "--sandbox", "workspace-write",
        "-c", "sandbox_workspace_write.network_access=true", "{prompt}",
    ],
}
ALTERNATE_NAMES = {"agent": ["cursor-agent"]}

# Git must never stop and wait for a password inside the watcher.
QUIET_ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0")

Turn = namedtuple("Turn", "task role reason key path stuck")

# WORKFLOW.md section 6: a READY_FOR_ status goes to the role it names.
READY_ROLE = {
    "READY_FOR_BA": "PRODUCT_BA",
    "READY_FOR_ARCHITECT": "ARCHITECT",
    "READY_FOR_DEVELOPMENT": "DEVELOPER",
    "READY_FOR_QA": "QA",
    "READY_FOR_PO": "PRODUCT_OWNER",
}


def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", flush=True)


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, env=QUIET_ENV
    )


def is_dirty():
    return bool(git("status", "--porcelain").stdout.strip())


def sync():
    """Pull the latest changes. Return an error message, or None when all is fine."""
    if is_dirty():
        return (
            "There are uncommitted changes in this folder, so the watcher won't pull. "
            "Commit them or undo them, and it carries on."
        )
    result = git("pull", "--rebase", "--quiet")
    if result.returncode != 0:
        git("rebase", "--abort")  # leave the folder as it was
        lines = result.stderr.strip().splitlines() or ["unknown error"]
        return f"git pull failed: {lines[-1]}"
    return None


# --- Reading the task files --------------------------------------------------------


def read_status(path):
    """Read the top-level fields of a status.yaml. Nested fields such as issue.type are skipped."""
    fields = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line[0] in " \t#" or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.split(" #", 1)[0].strip().strip("'\"")
        fields[key.strip()] = value or None
    return fields


def last_event(task_dir):
    path = task_dir / "events.jsonl"
    if not path.exists():
        return None
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return None
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError:
        return None


def parse_time(text):
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def last_commit(path):
    result = git("log", "-1", "--format=%H", "--", path.relative_to(ROOT).as_posix())
    return result.stdout.strip() or "uncommitted"


def find_turns(roles, stuck_minutes):
    """Every open task where it's one of these roles' turn (WORKFLOW.md, section 4)."""
    turns = []
    for status_path in sorted((ROOT / "tasks").glob("*/status.yaml")):
        task_dir = status_path.parent
        try:
            fields = read_status(status_path)
        except (OSError, UnicodeDecodeError):
            continue
        task = fields.get("task") or task_dir.name
        status = fields.get("status")
        assigned = fields.get("assigned_to")
        updated = fields.get("updated_by")
        if status in CLOSED:
            continue

        commit = last_commit(status_path)
        if assigned in roles and updated != assigned:
            reason = f"assigned to {assigned}, last update by {updated}"
            turns.append(Turn(task, assigned, reason, f"{task}:{commit}:{assigned}", status_path, False))
            continue

        if "SCRUM_MASTER" not in roles or fields.get("routing_mode") != "SCRUM_MASTER":
            continue
        if updated != "SCRUM_MASTER":
            reason = f"new report from {updated}"
            key = f"{task}:{commit}:SCRUM_MASTER"
            turns.append(Turn(task, "SCRUM_MASTER", reason, key, status_path, False))
        elif assigned not in HUMANS:
            event = last_event(task_dir)
            when = parse_time(event.get("timestamp")) if event else None
            if when and datetime.now(timezone.utc) - when > timedelta(minutes=stuck_minutes):
                reason = f"no new event for {stuck_minutes:g} minutes, check whether it is stuck"
                key = f"{task}:stuck:{event.get('timestamp')}"
                turns.append(Turn(task, "SCRUM_MASTER", reason, key, status_path, True))
    return turns


# --- Instant routing for routine hand-overs ------------------------------------------


def read_issue_type(path):
    """The value of issue.type in a status.yaml, or None."""
    in_issue = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line and line[0] not in " \t":
            in_issue = line.startswith("issue:")
            continue
        if in_issue and line.strip().startswith("type:"):
            return line.split(":", 1)[1].split(" #", 1)[0].strip().strip("'\"") or None
    return None


def routine_route(turn):
    """The fixed routing-table move for a routine hand-over, or None when it needs judgment."""
    if turn.role != "SCRUM_MASTER" or turn.stuck:
        return None
    fields = read_status(turn.path)
    if read_issue_type(turn.path) or fields.get("result") in ("FAILED", "BLOCKED"):
        return None
    status = fields.get("status")
    if status == "NEW":
        return "READY_FOR_BA", "PRODUCT_BA"
    if status in READY_ROLE:
        return status, READY_ROLE[status]
    return None


def set_status_fields(path, updates):
    """Change top-level fields in a status.yaml and leave every other line as it is."""
    lines = path.read_text(encoding="utf-8").splitlines()
    remaining = dict(updates)
    for index, line in enumerate(lines):
        if line and line[0] not in " \t#" and ":" in line:
            key = line.split(":", 1)[0].strip()
            if key in remaining:
                lines[index] = f"{key}: {remaining.pop(key)}"
    for key, value in remaining.items():
        position = next((i for i, line in enumerate(lines) if line.startswith("result:")), len(lines))
        lines.insert(position, f"{key}: {value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def route_instantly(turn, new_status, role):
    """Make a routine hand-over without the AI: update status.yaml, add the event, commit, push.

    Returns True when it was pushed. On any failure it puts the folder back as it was.
    """
    before = git("rev-parse", "HEAD").stdout.strip()
    fields = read_status(turn.path)
    attempt = fields.get("attempt") or "1"
    reason = f"Routine hand-over from {fields.get('status')} to {role}, routed by the watcher"
    set_status_fields(turn.path, {
        "status": new_status,
        "assigned_to": role,
        "updated_by": "SCRUM_MASTER",
        "routing_reason": reason,
    })
    event = {
        "timestamp": utc_now(), "task": turn.task, "agent": "SCRUM_MASTER", "event": "ROUTED",
        "to": role, "attempt": int(attempt) if attempt.isdigit() else attempt, "reason": reason,
    }
    events_path = turn.path.parent / "events.jsonl"
    existing = events_path.read_text(encoding="utf-8") if events_path.exists() else ""
    prefix = "" if not existing or existing.endswith("\n") else "\n"
    with events_path.open("a", encoding="utf-8") as events:
        events.write(prefix + json.dumps(event, separators=(",", ":")) + "\n")

    files = [p.relative_to(ROOT).as_posix() for p in (turn.path, events_path)]
    message = f"[SCRUM_MASTER] {turn.task}: ROUTED to {role} - routine hand-over"
    if git("add", *files).returncode == 0 and git("commit", "-q", "-m", message).returncode == 0:
        for _ in range(2):
            if git("push", "-q").returncode == 0:
                return True
            if git("pull", "--rebase", "-q").returncode != 0:
                git("rebase", "--abort")
                break
    git("reset", "-q", "--hard", before)
    return False


# --- Telling the AI tool -------------------------------------------------------------


def build_prompt(turn, roles, unattended):
    role_file = ROLE_FILES[turn.role]
    same_seat = [role for role in roles if ROLE_FILES[role] == role_file] or [turn.role]
    label = "role IDs" if len(same_seat) > 1 else "role ID"
    text = (
        f"You are {SEAT_NAMES[turn.role]} on this team, {label} {' and '.join(same_seat)}. "
        f"Read AGENTS.md, WORKFLOW.md and {role_file}. "
        f"It is your turn on {turn.task} as {turn.role}, because of: {turn.reason}. "
        f"Act only as {turn.role} in this turn. "
        "Do your turn, then commit and push as WORKFLOW.md says. "
        f"The current UTC time is about {utc_now()}."
    )
    if unattended:
        text += (
            " You are running unattended, so no human can answer questions. "
            "If something needs a decision, report BLOCKED as WORKFLOW.md says. Do not wait for input."
        )
    return text


def copy_to_clipboard(text):
    if os.name == "nt":
        candidates = [["clip"]]
    else:
        candidates = [["pbcopy"], ["wl-copy"], ["xclip", "-selection", "clipboard"]]
    for command in candidates:
        if shutil.which(command[0]):
            try:
                subprocess.run(command, input=text, text=True, check=True, timeout=5)
                return True
            except (OSError, subprocess.SubprocessError):
                continue
    return False


def notify(prompt):
    print("\a", end="")
    print("\n" + "=" * 72)
    print("  YOUR TURN. Paste this into your AI tool:\n")
    print("  " + prompt)
    print("=" * 72, flush=True)
    if copy_to_clipboard(prompt):
        print("  (It's on your clipboard.)", flush=True)
    print(flush=True)


def split_command(text):
    """Split --command into arguments, keeping Windows paths with backslashes intact."""
    if os.name == "nt":
        return [part.strip('"') for part in shlex.split(text, posix=False)]
    return shlex.split(text)


def resolve_command(template, prompt):
    """The full command to run, or None when the tool isn't installed."""
    args = [part.replace("{prompt}", prompt) for part in template]
    for name in [args[0]] + ALTERNATE_NAMES.get(args[0], []):
        path = shutil.which(name)
        if path:
            return [path] + args[1:]
    return None


def run_tool(command, minutes):
    log(f"Starting {Path(command[0]).name}. It is stopped after {minutes} minutes.")
    try:
        result = subprocess.run(
            command, cwd=ROOT, stdin=subprocess.DEVNULL, env=QUIET_ENV, timeout=minutes * 60
        )
    except subprocess.TimeoutExpired:
        log("The AI run took too long and was stopped.")
        return
    except OSError as error:
        log(f"Couldn't start the AI tool: {error}")
        return
    log(f"The AI run finished (exit code {result.returncode}).")


# --- Lock and memory ---------------------------------------------------------------


def acquire_lock(force):
    STATE_DIR.mkdir(exist_ok=True)
    try:
        with open(LOCK_FILE, "x" if not force else "w", encoding="utf-8") as lock:
            lock.write(f"pid {os.getpid()}, started {utc_now()}\n")
    except FileExistsError:
        holder = LOCK_FILE.read_text(encoding="utf-8").strip()
        sys.exit(
            f"Another watcher seems to be running in this folder ({holder}).\n"
            f"If it isn't, delete {LOCK_FILE} or start again with --force."
        )


def release_lock():
    try:
        LOCK_FILE.unlink()
    except FileNotFoundError:
        pass


def load_state():
    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        state.setdefault("handled", [])
        return state
    except (OSError, ValueError):
        return {"handled": [], "last_commit": None}


def save_state(state):
    state["handled"] = state["handled"][-500:]
    STATE_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


# --- Main --------------------------------------------------------------------------


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Watch the team repository and act when it's your turn.",
    )
    parser.add_argument("--role", required=True,
                        help="Your role ID, or two separated by a comma, e.g. ARCHITECT,SECURITY")
    parser.add_argument("--tool", default="notify", choices=["notify", *TOOLS],
                        help="notify (default): beep and copy the prompt. Others: start that AI tool.")
    parser.add_argument("--command",
                        help='Your own command to start an AI tool. It must contain {prompt}.')
    parser.add_argument("--check", action="store_true",
                        help="Pull once, say whether it's your turn, and exit.")
    parser.add_argument("--interval", type=float, default=10, help="Seconds between checks (default 10).")
    parser.add_argument("--run-timeout", type=float, default=10,
                        help="Minutes before an AI run is stopped (default 10).")
    parser.add_argument("--stop-after", type=float, default=120,
                        help="Minutes before the watcher stops itself (default 120).")
    parser.add_argument("--stuck-minutes", type=float, default=10,
                        help="Scrum Master only: minutes without an event before a task counts as stuck.")
    parser.add_argument("--ai-routes-everything", action="store_true",
                        help="Scrum Master only: wake the AI for routine hand-overs too.")
    parser.add_argument("--force", action="store_true", help="Start even if a lock file exists.")
    args = parser.parse_args(argv)

    args.roles = [role.strip().upper() for role in args.role.split(",") if role.strip()]
    unknown = [role for role in args.roles if role not in ROLE_FILES]
    if not args.roles or unknown:
        parser.error(f"Unknown role {', '.join(unknown) or args.role!r}. Use one of: {', '.join(ROLE_FILES)}")
    if args.command and "{prompt}" not in args.command:
        parser.error("--command must contain {prompt}")
    return args


def main(argv=None):
    args = parse_args(argv)
    roles = args.roles

    if git("rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        sys.exit("This isn't a Git repository. Run the watcher inside your team's repository.")

    if args.check:
        error = sync()
        if error:
            log(error)
        turns = find_turns(roles, args.stuck_minutes)
        if not turns:
            log(f"Not your turn ({', '.join(roles)}).")
        for turn in turns:
            log(f"Your turn: {turn.task} as {turn.role} ({turn.reason}).")
            route = None if args.ai_routes_everything else routine_route(turn)
            if route:
                print(f"  Routine hand-over: the running watcher routes it to {route[1]} itself.", flush=True)
            else:
                print("  Prompt: " + build_prompt(turn, roles, unattended=False), flush=True)
        return

    if args.command:
        template, tool_label = split_command(args.command), "your command"
    elif args.tool == "notify":
        template, tool_label = None, "notify mode (beep and copy the prompt)"
    else:
        template, tool_label = TOOLS[args.tool], args.tool
    if template and resolve_command(template, "") is None:
        sys.exit(
            f"Can't find '{template[0]}' on this computer. "
            "Install it, use --tool notify, or give your own --command."
        )

    acquire_lock(args.force)
    state = load_state()
    deadline = time.monotonic() + args.stop_after * 60
    log(f"Watching as {', '.join(roles)} using {tool_label}. "
        f"Checking every {args.interval:g} seconds. Press Ctrl+C to stop.")
    last_note = None
    try:
        while time.monotonic() < deadline:
            note = None
            error = sync()
            if error:
                note = error
            else:
                head = git("rev-parse", "HEAD").stdout.strip()
                if state.get("last_commit") != head:
                    state["last_commit"] = head
                    save_state(state)
                turns = find_turns(roles, args.stuck_minutes)
                new_turns = [turn for turn in turns if turn.key not in state["handled"]]
                if new_turns:
                    turn = new_turns[0]
                    route = None if args.ai_routes_everything else routine_route(turn)
                    if route:
                        log(f"Routine hand-over on {turn.task}: {route[1]} is next. Routing it now, no AI needed.")
                        if route_instantly(turn, *route):
                            log(f"Routed {turn.task} to {route[1]} and pushed.")
                            last_note = None
                            continue
                        log("Couldn't push the routing, so this turn goes to the AI as usual.")
                    log(f"Your turn: {turn.task} as {turn.role} ({turn.reason}).")
                    state["handled"].append(turn.key)
                    save_state(state)
                    prompt = build_prompt(turn, roles, unattended=template is not None)
                    if template is None:
                        notify(prompt)
                    else:
                        run_tool(resolve_command(template, prompt), args.run_timeout)
                        if is_dirty():
                            log("The AI run left uncommitted changes. Check them, then commit or "
                                "undo them. The watcher waits until the folder is clean.")
                    last_note = None
                    continue  # check again straight away
                if turns and template is None:
                    note = f"Waiting for you to finish {turns[0].task} and push..."
                elif turns:
                    note = (f"Already handled {turns[0].task} in this state. If your AI tool didn't "
                            "finish, tell it yourself: check for work.")
                else:
                    note = "Not your turn. Waiting for the next push..."
            if note != last_note:
                log(note)
                last_note = note
            time.sleep(args.interval)
        log(f"Stopped after {args.stop_after:g} minutes (--stop-after).")
    except KeyboardInterrupt:
        log("Stopped.")
    finally:
        release_lock()


if __name__ == "__main__":
    main()
