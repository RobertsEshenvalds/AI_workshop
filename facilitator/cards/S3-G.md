# S3-G: Weakest repositories first

**Feature** · Stage 3 · XS · about 10 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-G --mode SCRUM_MASTER --push`. Routine path: the watcher routes every hand-over.

## Wish card

Managers want to deal with their weakest repositories first. When they ask for it, sort their list by health score, lowest first. The normal order should stay as it is.

## Why this card

Routine path, and a regression check on the default order.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- For example `GET /repositories?sort=health` gives Alice `web-portal` (59) before `payments-api` (79).
- Without the option the order is unchanged.
- Size check: a reference solution adds or changes 4 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

When two repositories have the same score, the one with more open findings should come first.
