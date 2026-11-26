# S5-E: Owner's name in the details

**Feature** · Stage 5 · XS · about 10 min

Release at the start of Stage 5: `python scripts/new_task.py S5-E --mode SCRUM_MASTER --push`. Then hands off.

## Wish card

In the repository details, also show the owner's name the way the app knows it, for example Alice, next to the username.

## Why this card

Safe for a hands-off run: one more field in an existing response, no new input, and the card answers its own questions. Any open question in Stage 5 costs two extra turns (a `BLOCKED` report and a `PRODUCT_OWNER` decision).

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- `GET /repositories/4` as chen shows `owner_name: Chen`.
- The username field is unchanged.
- Size check: a reference solution adds or changes 2 lines in `app/service.py`, and passes the full test suite.

## Follow-up from Business

None. Don't add a follow-up during a hands-off run.
