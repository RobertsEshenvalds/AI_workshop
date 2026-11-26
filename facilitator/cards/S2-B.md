# S2-B: Contributors of a repository

**Feature** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-B --push`. No product decision needed.

## Wish card

Team leads want to see who has worked on a repository without reading the whole analysis.

## Why this card

A small read-only endpoint that reuses the existing access rules. A good warm-up for an extra Developer.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- For example `GET /repositories/{id}/contributors` returns the contributors from the latest analysis, with 401, 403 and 404 like the analysis.
- Size check: a reference solution adds or changes 2 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Team leads also want to see how many contributors there are, not only the list.
