# S5-A: Last scan time in the list

**Feature** · Stage 5 · XS · about 10 min

Release at the start of Stage 5: `python scripts/new_task.py S5-A --mode SCRUM_MASTER --push`. Then hands off.

## Wish card

In the list of repositories, people also want to see when each repository was last scanned, shown the same way the repository details already show it.

## Why this card

Safe for a hands-off run: one more field in an existing response, no new input, and the card answers its own questions. Any open question in Stage 5 costs two extra turns (a `BLOCKED` report and a `PRODUCT_OWNER` decision).

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- Every item in `GET /repositories` gains `last_scanned_at`, in the same UTC format as the details.
- After a scan, the list shows the new time.
- Size check: a reference solution adds or changes 1 line in `app/service.py`, and passes the full test suite.

## Follow-up from Business

None. Don't add a follow-up during a hands-off run.
