# Multi-agent workshop: team repository

Your team is a small software delivery team. Each of you runs your own AI coding session (Claude Code, GitHub Copilot, Cursor, or whatever you already use), and each session plays one role. You hand work to each other through the files in this repository, not through chat.

## Get your team's repository

Each team works in its own copy, not in this repository.

1. One person per team clicks **Use this template** → **Create a new repository** at the top of this page on GitHub.
2. In the new repository, they open **Settings → Collaborators** and add their teammates and the facilitators by GitHub username.
3. Everyone clones the **team's** repository and opens it in their AI tool.

## Seats

| Seat | Role | Role file |
|---|---|---|
| 1 | Product Owner / BA. No coding needed. | `roles/product-ba.md` |
| 2 | Architect, who also covers security | `roles/architect.md` |
| 3 | Developer | `roles/developer.md` |
| 4 | QA | `roles/qa.md` |
| 5–6 | Extra Developer. In Stage 3, one Developer becomes the Scrum Master. | `roles/developer.md`, then `roles/scrum-master.md` |

## Before you start

- [ ] You have cloned this repository and opened the folder in your AI tool.
- [ ] `git pull` works without asking for your password every time.
- [ ] Your AI tool can read files and run commands in this folder. To test it, ask: "Read AGENTS.md and tell me in one sentence what this repository is for."

## Start your session

Paste the line for your seat into your AI tool:

| Seat | Paste this |
|---|---|
| 1, Product Owner / BA | You are the Product Owner / BA on this team (role IDs PRODUCT_BA and PRODUCT_OWNER). Read AGENTS.md, WORKFLOW.md and roles/product-ba.md, then check for work. |
| 2, Architect | You are the Architect on this team (role IDs ARCHITECT and SECURITY). Read AGENTS.md, WORKFLOW.md and roles/architect.md, then check for work. |
| 3, 5, 6, Developer | You are a DEVELOPER on this team. Read AGENTS.md, WORKFLOW.md and roles/developer.md, then check for work. |
| 4, QA | You are QA on this team. Read AGENTS.md, WORKFLOW.md and roles/qa.md, then check for work. |

After that, whenever someone pushes, tell your AI tool: **"Check for work."** If it's your turn, it does your role's work, updates `status.yaml` and `events.jsonl`, commits and pushes. If it isn't, it says so.

## Stage by stage

From Stage 2 on, a facilitator may add more small tasks (`TASK-002`, `TASK-003`, …). The watchers check every task folder, so nothing changes for you: your role may just have turns waiting on more than one task.

**Stage 1: manual hand-off (10 minutes).** A facilitator gives your Product Owner a paper wish card. The Product Owner tells their AI tool:

> Here is our wish card from Business: "...". Put it in tasks/TASK-001/task.md word for word, commit and push it. Then do your PRODUCT_BA turn.

That push starts your team's clock. Nobody is in charge of routing yet: whoever finishes a step picks the next role (`WORKFLOW.md`, section 5). Say out loud when you've pushed.

**Stage 2: automation on (10 minutes).** Each person starts the watcher in a terminal in this folder. It pulls every few seconds and checks whether it's your turn.

```
python scripts/watch.py --role DEVELOPER
```

- Seat 1 uses `--role PRODUCT_BA,PRODUCT_OWNER`. Seat 2 uses `--role ARCHITECT,SECURITY`.
- On Windows, if `python` isn't found, use `py` instead.
- By default the watcher beeps when it's your turn and copies the right prompt to your clipboard. Paste it into your AI tool.
- To let the watcher start your AI tool by itself, add `--tool claude`, `--tool copilot`, `--tool cursor` or `--tool codex`. Stage 5 needs this to run hands-off. If your tool needs different flags, use `--command "yourtool ... {prompt}"`.
- To check once whether it's your turn: `python scripts/watch.py --role QA --check`.

**Stage 3: Scrum Master online (20 minutes).** Your team picks one Developer to become the Scrum Master. That person tells their AI tool:

> You are now the SCRUM_MASTER on this team. Read AGENTS.md, WORKFLOW.md and roles/scrum-master.md, and switch the team to Scrum Master mode.

The Scrum Master then stops their watcher (Ctrl+C) and starts it again with `--role SCRUM_MASTER`. From then on, the watcher makes routine hand-overs itself in a second, and wakes the Scrum Master's AI only when something needs judgment: a failure, a block, a change request or a stuck task.

From then on, only the Scrum Master decides who works next. Everyone else reports their result and stops. The remaining Developer ships a small or stub version, so QA has something real to check.

**Stage 4: resilience (15 minutes).** A facilitator changes something in your repository. Keep working as normal, and watch whether your Scrum Master routes it correctly.

**Stage 5: hands off (12 minutes).** A facilitator adds a small new task. Take your hands off the keyboard and let the watchers and the Scrum Master run it from start to finish. If your AI tool can't be started by the watcher, paste the prompt when it beeps, and do nothing else.

To watch it happen: `python scripts/events.py --follow`.

## What's in this repository

| Path | What it is |
|---|---|
| `AGENTS.md` | Instructions every AI tool reads first |
| `WORKFLOW.md` | Whose turn it is, who owns which file, how work is routed |
| `roles/` | One instruction file per role |
| `templates/` | Starting points for the artifacts each role writes |
| `tasks/` | One folder per task, starting with `TASK-001/`: `task.md`, `status.yaml`, `events.jsonl`, and the artifacts as you write them |
| `app/` | The sample app: a small repository registry API |
| `tests/` | The app's tests |
| `docs/api.md` | What the app does today, and how to add an endpoint |
| `scripts/watch.py` | The watcher (Stage 2 on) |
| `scripts/events.py` | Shows the task status and event timeline |
| `scripts/new_task.py` | Facilitators only: releases a task card as a new task |
| `facilitator/` | Facilitators only: the run sheet and the extra task cards |

## Run the app and tests

The app uses only the Python standard library, so there's nothing to install.

```
python -m unittest
python -m app.server
```

The second command starts the API on http://localhost:8000. Try http://localhost:8000/repositories in a browser. See `docs/api.md` for the endpoints.
