# S5-H: nosniff header on every response

**Security** · Stage 5 · XS · about 10 min

Release at the start of Stage 5: `python scripts/new_task.py S5-H --mode SCRUM_MASTER --push`. Then hands off.

## Wish card

Finding from the security scan: browsers may guess the type of our responses instead of trusting their Content-Type. Add the header "X-Content-Type-Options: nosniff" to every response the API sends, including errors.

## Why this card

Safe for a hands-off run: one more header on every response, no new input, and the card answers its own questions. Any open question in Stage 5 costs two extra turns (a `BLOCKED` report and a `PRODUCT_OWNER` decision).

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- `/health`, an unknown path (404) and a missing repository all carry the header.
- Nothing else in the responses changes.
- Size check: a reference solution adds or changes 1 line in `app/server.py`, and passes the full test suite.

## Follow-up from Business

None. Don't add a follow-up during a hands-off run.
