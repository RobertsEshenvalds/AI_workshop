# S2-E: The API docs don't mention common errors

**Docs** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-E --push`. No product decision needed.

## Wish card

New developers keep getting surprised by errors that the API documentation doesn't mention: 400 when the body isn't valid JSON, 404 for a path that doesn't exist, and 405 for the wrong method. Please add them to docs/api.md. No code changes.

## Why this card

A documentation task: the Developer edits `docs/api.md`, and QA checks each documented error against the running app.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- `docs/api.md` says when 400, 404 and 405 happen, and the examples match what the app really returns.
- No change under `app/`.
- Size check: a reference solution adds or changes 4 lines in `docs/api.md`, and passes the full test suite.

## Follow-up from Business

Also document that a call without the X-User header counts as alice. (It already is: QA and the PO should notice.)
