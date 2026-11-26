# S2-I: The app's home address shows an error

**Bug** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-I --push`. No product decision needed.

## Wish card

When people open the app's address in a browser, http://localhost:8000/, they get "No endpoint for GET /". That looks broken. Show them the list of endpoints the API offers instead.

## Why this card

A real rough edge: there is no route for `/`.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- `GET /` returns the endpoints, for example `"POST /repositories/{id}/scan"`.
- The list comes from the registered routes, so it stays right when endpoints are added. Red flag: a hard-coded list.
- Size check: a reference solution adds or changes 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Each endpoint in the list should have a short description too.
