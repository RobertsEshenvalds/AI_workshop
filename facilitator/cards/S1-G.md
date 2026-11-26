# S1-G: Scan all my repositories at once

**Feature** · Stage 1 · S · about 13 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-G --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

Before the weekly review, people scan each of their repositories one by one. Let them scan all of their own repositories at once.

## Why this card

Reuses the existing scan, but QA must prove that other users' repositories are not touched.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 2 | 1.5 | 2.5 | 3 | 1 | 2.5 | about 13 |

## What good looks like

- For example `POST /repositories/scan` returns the new analyses of the caller's repositories only.
- Bob's `last_scanned_at` doesn't change when Alice scans all of hers.
- Size check: a reference solution adds or changes 2 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

The result should also say how many repositories were scanned.
