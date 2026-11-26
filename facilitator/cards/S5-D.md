# S5-D: Description in the list

**Feature** · Stage 5 · XS · about 10 min

Release at the start of Stage 5: `python scripts/new_task.py S5-D --mode SCRUM_MASTER --push`. Then hands off.

## Wish card

In the list of repositories, also show each repository's description, the same text as in its details.

## Why this card

Safe for a hands-off run: one more field in an existing response, no new input, and the card answers its own questions. Any open question in Stage 5 costs two extra turns (a `BLOCKED` report and a `PRODUCT_OWNER` decision).

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- Alice's list shows `Card payment service` for payments-api.
- Bob's list still shows only his own repository.
- Size check: a reference solution adds or changes 1 line in `app/service.py`, and passes the full test suite.

## Follow-up from Business

None. Don't add a follow-up during a hands-off run.
