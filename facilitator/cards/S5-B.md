# S5-B: Version on the health check

**Ops** · Stage 5 · XS · about 10 min

Release at the start of Stage 5: `python scripts/new_task.py S5-B --mode SCRUM_MASTER --push`. Then hands off.

## Wish card

Operations want the health check to also say which version of the app is running. Today that is version 1.0.

## Why this card

Safe for a hands-off run: one more field in an existing response, no new input, and the card answers its own questions. Any open question in Stage 5 costs two extra turns (a `BLOCKED` report and a `PRODUCT_OWNER` decision). It has a trap: `test_health` checks the whole `/health` body, so the Developer must update that test and say so.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- `GET /health` returns `{"status": "ok", "version": "1.0"}`.
- `test_health` is updated, not deleted or skipped. Red flag: a hand-over with a failing test suite.
- Size check: a reference solution adds or changes 1 line in `app/server.py` and 1 line in `tests/test_api.py`, and passes the full test suite. Without its test updates, it breaks `test_health`: the Developer must update them openly.

## Follow-up from Business

None. Don't add a follow-up during a hands-off run.
