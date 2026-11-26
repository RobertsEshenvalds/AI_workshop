# S1-E: Health check rejects requests with a body

**Bug** · Stage 1 · XS · about 10 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-E --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

Bug report from Operations: our monitoring tool checks GET /health every minute, and it always sends a small body with the request. The API answers 400 "Body is not valid JSON", so the monitor thinks the app is down. A GET request shouldn't care about a body.

## Why this card

A real defect: the server parses the body for every method. Reproduce with `curl -X GET -d ping http://localhost:8000/health`.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- A GET with any body gets its normal answer.
- A POST with invalid JSON still gets 400 (QA's "worked before" check).
- Size check: a reference solution adds or changes 1 line in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Operations also want the 400 message for a bad body to say which endpoint was called.
