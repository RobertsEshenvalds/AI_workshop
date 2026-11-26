# S2-A: Who am I

**Feature** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-A --push`. No product decision needed.

## Wish card

Users keep asking which account the app thinks they are using. Let them see their own username and name. Only their own, nobody else's.

## Why this card

In Stage 2 the BA and the Architect sit idle while the first task is with the Developer and QA. A tiny card gives them work at once, and the team sees the watchers queue turns across two tasks.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- For example `GET /me` returns the caller's `username` and `name`. An unknown user gets 401.
- No email: the card doesn't ask for it. A BA who lists it as an open question is doing the right thing.
- Size check: a reference solution adds or changes 3 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

People also want to see their email address there.
