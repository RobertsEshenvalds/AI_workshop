# S1-D: 405 response has no Allow header

**Bug** · Stage 1 · XS · about 10 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-D --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

Bug report from the integration team: when our client calls an endpoint with the wrong method, the API answers 405, which is right. But the response has no Allow header, so our client library can't tell us which method to use, and it crashes. Please add the header.

## Why this card

A real defect: `app/server.py` sends 405 without `Allow`, which HTTP requires. Reproduce with `curl -i -X PUT http://localhost:8000/health`.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- Every 405 carries `Allow`, for example `PUT /health` gives `Allow: GET` and `GET /repositories/1/scan` gives `Allow: POST`.
- The JSON error message stays as it is.
- Size check: a reference solution adds or changes 5 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

The Allow header should list the methods in alphabetical order, the same as the error message. (It already does if the Developer reused the sorted list: QA and the PO should notice that it's already met.)
