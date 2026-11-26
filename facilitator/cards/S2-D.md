# S2-D: The Server header reveals the Python version

**Security** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-D --push`. No product decision needed.

## Wish card

Finding from the security scan: every response from the API carries a header like "Server: RepoRegistry/1.0 Python/3.12.4". Telling the world the exact Python version makes attacks easier. Keep the app name and version, drop the Python part.

## Why this card

A real finding: `BaseHTTPRequestHandler` adds `Python/x.y.z` to the `Server` header. Check with `curl -i http://localhost:8000/health`.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- Every response, including errors, has `Server: RepoRegistry/1.0` and nothing about Python.
- Size check: a reference solution adds or changes 2 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

The security scan also wants the header "X-Content-Type-Options: nosniff" on every response.
