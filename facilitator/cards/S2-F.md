# S2-F: A broken Content-Length gives a misleading error

**Bug** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-F --push`. No product decision needed.

## Wish card

Bug report from the integration team: when our client sends a broken Content-Length header, the API says "Body is not valid JSON: invalid literal for int() with base 10". That's a Python error message, and it sends us looking at the body, which is fine. Please give a clear 400 error that names the Content-Length header.

## Why this card

A real defect in `_read_json` in `app/server.py`. QA needs a raw HTTP client (for example `http.client`), because curl and urllib set the header themselves.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- `Content-Length: abc` or `-1` gives 400 with a message that names Content-Length.
- A valid body still works, and invalid JSON still gets its own message.
- Size check: a reference solution adds or changes 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

A request that announces a body bigger than 1 MB should be refused straight away.
