# S3-I: One stuck client freezes the whole API

**Bug** · Stage 3 · XS · about 10 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-I --mode SCRUM_MASTER --push`. Routine path: the watcher routes every hand-over.

## Wish card

Incident report from Operations: yesterday the whole API stopped answering for minutes. We found one client that had opened a connection and sent its request very slowly. While it was connected, nobody else got an answer, not even GET /health. One slow or broken client must never block everyone else.

## Why this card

A real defect: `RegistryServer` is a single-threaded `HTTPServer`, so one connection that doesn't finish its request blocks every other request. Architect-heavy, but no product decision.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- The Architect names the cause, and the design picks a fix: for example a threading server, a socket timeout, or both.
- QA's check opens a raw connection that sends half a request, then shows `GET /health` still answers within a second or two.
- Size check: a reference solution adds or changes 2 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

A connection that sends nothing at all should be closed after 10 seconds.
