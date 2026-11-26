# S2-J: Show when the previous scan was

**Feature** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-J --push`. No product decision needed.

## Wish card

When people rescan a repository, they want to see when it was scanned before, so they know how old the previous result was. Show that in the result of the scan.

## Why this card

A small change to one response, with a clear check against the seed data.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- The first scan of `payments-api` returns `previous_scanned_at: 2026-11-20T08:00:00Z`.
- `GET /repositories/{id}/analysis` is unchanged.
- Size check: a reference solution adds or changes 2 lines in `app/service.py`, and passes the full test suite.

## Follow-up from Business

Show it as how many days ago, not as a date.
