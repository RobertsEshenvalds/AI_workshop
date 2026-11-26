# S3-F: Filter by language

**Feature** · Stage 3 · S · about 13 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-F --mode SCRUM_MASTER --push`. Routine path: the watcher routes every hand-over.

## Wish card

Team leads want to see only the repositories that use a given language, for example all their CSS repositories. Capital letters shouldn't matter. They should still only ever see their own repositories.

## Why this card

Routine path, with a cross-check against the analysis data.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 2 | 1.5 | 2.5 | 3 | 1 | 2.5 | about 13 |

## What good looks like

- For example `GET /repositories?language=css` gives Alice only `web-portal`; `language=java` gives her an empty list.
- No filter gives the same list as before.
- Size check: a reference solution adds or changes 5 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Only count a language when it makes up at least half of the repository.
