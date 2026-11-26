# S3-H: Archive a repository

**Feature** · Stage 3 · S · about 15 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-H --mode SCRUM_MASTER --push`. Leaves out a product decision on purpose.

## Wish card

People have old repositories they don't use any more but don't want to delete. Let them archive a repository so it no longer shows up in their list.

## Why this card

"Archived" is a new concept, and the card doesn't say what else it means. Can it still be opened? Scanned? Unarchived?

## Turn budget (minutes)

| BA | PO decision | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 1.5 | 2 | 2.5 | 3 | 1 | 3 | about 15 |

## What good looks like

- The BA lists those questions, and the Product Owner's answers are in `requirements.md`.
- An archived repository is gone from the list. Everything else behaves as decided.
- Size check: a reference solution where archived repositories can still be opened by number adds or changes 5 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

People also need to see their archived repositories, when they ask for them.
