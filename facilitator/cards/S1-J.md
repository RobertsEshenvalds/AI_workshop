# S1-J: HEAD and OPTIONS return an HTML error page

**Bug** · Stage 1 · XS · about 10 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-J --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

Bug report from Operations: our uptime monitor sends HEAD /health, and the API answers with an HTML error page (501 Unsupported method) instead of a normal answer. Other unsupported methods, like OPTIONS, also get HTML, while everything else in the API is JSON. HEAD /health should work, and errors should always be JSON.

## Why this card

A real defect: `BaseHTTPRequestHandler` answers unknown methods with its own HTML page. Reproduce with `curl -I http://localhost:8000/health`.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- `HEAD /health` gives 200 with no body.
- `OPTIONS /repositories` gives a JSON error. Which status (405 or 501) is the Architect's call.
- Size check: a reference solution adds or changes 7 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

HEAD should work for every GET endpoint, not only /health.
