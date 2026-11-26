# S1-H: Most recently scanned first

**Feature** · Stage 1 · XS · about 10 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-H --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

People want to see the repositories they scanned most recently at the top of their list, when they ask for that. The normal order should stay as it is.

## Why this card

A small query option with a built-in regression check: the default order must not change.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- For example `GET /repositories?sort=recent` gives Alice `web-portal` before `payments-api`.
- Without the option the list is in the same order as before.
- Size check: a reference solution adds or changes 4 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Repositories that were never scanned should come last.
