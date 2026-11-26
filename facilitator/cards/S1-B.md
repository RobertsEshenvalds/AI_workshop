# S1-B: Remove a repository

**Feature** · Stage 1 · S · about 13 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-B --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

People registered repositories by mistake and want to remove them. Let owners remove one of their own repositories. Once removed, it should be gone everywhere, including its analysis.

## Why this card

A destructive action with a clear access rule, so QA must check both the happy path and that nobody can remove someone else's repository.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 2 | 1.5 | 2.5 | 3 | 1 | 2.5 | about 13 |

## What good looks like

- For example `DELETE /repositories/{id}` returns 204. Afterwards the details and the analysis give 404.
- Someone else's repository gives 403 (or 404, if the team already did S4-B), and it stays.
- Open question the BA should list: can a removal be undone?
- Size check: a reference solution adds or changes 4 lines in `app/service.py` and 4 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Business wants removed repositories to be recoverable for a while instead of gone for good.
