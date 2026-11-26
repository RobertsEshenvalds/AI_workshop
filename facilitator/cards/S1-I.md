# S1-I: Hand a repository over to a colleague

**Feature** · Stage 1 · S · about 14 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-I --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

When someone moves to another team, they need to hand their repositories over to a colleague. Let an owner hand one of their repositories over to another known user. After that, only the new owner can see it.

## Why this card

Changes ownership, so the access rules matter: QA must check the old owner loses access.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 2.5 | 2 | 3 | 3 | 1 | 2.5 | about 14 |

## What good looks like

- For example `POST /repositories/{id}/transfer` with `{"to": "bob"}`. Afterwards Bob sees it and Alice gets 403.
- An unknown new owner gives 400, not 401: the caller is fine, the input isn't.
- Open question the BA should list: must the new owner agree first?
- Size check: a reference solution adds or changes 7 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

The new owner must accept the hand-over before it happens.
