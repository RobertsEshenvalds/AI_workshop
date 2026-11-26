# S1-C: Edit a repository's description

**Feature** · Stage 1 · S · about 13 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-C --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

Repository descriptions are out of date. Let owners change the description of their own repositories.

## Why this card

The first endpoint that takes input from a body, so QA gets real wrong-input checks.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 2 | 1.5 | 2.5 | 3 | 1 | 2.5 | about 13 |

## What good looks like

- For example `PATCH /repositories/{id}` with `{"description": "..."}` returns the updated repository, and the details show it.
- A missing or non-text description gives 400. Someone else's repository gives 403.
- Open questions the BA should list: maximum length? Is an empty description allowed?
- Size check: a reference solution adds or changes 7 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Descriptions should be at most 200 characters.
