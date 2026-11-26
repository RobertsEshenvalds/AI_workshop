# S3-J: The web portal can't call the API from the browser

**Feature** · Stage 3 · S · about 15 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-J --mode SCRUM_MASTER --push`. Leaves out a product decision on purpose.

## Wish card

The web-portal team is building a page that calls this API straight from the browser. The browser blocks every call, because the API doesn't say which websites may call it. Let the web portal call the API.

## Why this card

A CORS task. The card doesn't give the portal's address, so which origins are allowed is a decision, and Security should weigh in.

## Turn budget (minutes)

| BA | PO decision | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 1.5 | 2 | 2.5 | 3 | 1 | 3 | about 15 |

## What good looks like

- The allowed origin is decided and written down, for example `http://localhost:3000`.
- That origin gets `Access-Control-Allow-Origin` and the browser preflight (`OPTIONS`) works with the `X-User` header. Other origins get nothing.
- Red flag: `Access-Control-Allow-Origin: *`.
- Size check: a reference solution with `http://localhost:3000` as the only allowed origin adds or changes 6 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

The portal will also run at https://portal.example.com.
