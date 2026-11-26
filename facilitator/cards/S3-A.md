# S3-A: Find a repository by name

**Feature** · Stage 3 · S · about 13 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-A --mode SCRUM_MASTER --push`. Routine path: the watcher routes every hand-over.

## Wish card

People with many repositories want to find one quickly by typing part of its name. Capital letters shouldn't matter. They should still only ever see their own repositories.

## Why this card

A clean task for the Scrum Master's first minutes: every hand-over is routine, so the watcher routes it in seconds.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 2 | 1.5 | 2.5 | 3 | 1 | 2.5 | about 13 |

## What good looks like

- For example `GET /repositories?name=pay`; `PAY`, `pay` and `Pay` give the same result.
- Alice searching for `pipeline` gets an empty list, not Bob's repository.
- No filter gives the same list as before.
- Size check: a reference solution adds or changes 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

People also want to find a repository by a word in its description, not only by its name.
