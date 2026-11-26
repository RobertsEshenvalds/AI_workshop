# S1-A: Register a repository

**Feature** · Stage 1 · S · about 14 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-A --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

Today only the four demo repositories exist, and nobody can add their own. Let people register a new repository by giving its name and its URL, and optionally a short description. The new repository belongs to whoever registered it, and it should have an analysis straight away.

## Why this card

The biggest gap in the product: `Store.next_id` exists, but nothing creates repositories. It has real open questions for the BA to list rather than answer.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 2.5 | 2 | 3 | 3 | 1 | 2.5 | about 14 |

## What good looks like

- For example `POST /repositories` returns 201 with the new repository, owned by the caller, and its analysis exists at once.
- Missing name or URL gives 400.
- Open questions the BA should list, not decide: can the same URL be registered twice? Must the URL look like a Git host?
- Size check: a reference solution adds or changes 12 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Registering the same URL twice should not be possible.
