# S2-C: My totals

**Feature** · Stage 2 · S · about 13 min

Release at the start of Stage 2: `python scripts/new_task.py S2-C --push`. No product decision needed.

## Wish card

People want one place that tells them how many repositories they have and how many open findings there are across all of them.

## Why this card

A small aggregate over data the user already owns. QA has to check that other users' repositories are never counted.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 2 | 1.5 | 2.5 | 3 | 1 | 2.5 | about 13 |

## What good looks like

- For example `GET /summary` returns `{"repositories": 2, "open_findings": 11}` for Alice and `{"repositories": 1, "open_findings": 0}` for Bob.
- An unknown user gets 401.
- Size check: a reference solution adds or changes 4 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Also show the average health score. (Rounding is a product decision.)
