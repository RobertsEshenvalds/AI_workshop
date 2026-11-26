# S3-E: Stop people scanning too often

**Feature** · Stage 3 · S · about 15 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-E --mode SCRUM_MASTER --push`. Leaves out a product decision on purpose.

## Wish card

Some people press scan again and again, and every scan costs us money on the real scanner. Stop people from scanning the same repository too often.

## Why this card

"Too often" is a product decision. The error to return is an Architect decision.

## Turn budget (minutes)

| BA | PO decision | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 1.5 | 2 | 2.5 | 3 | 1 | 3 | about 15 |

## What good looks like

- The limit is a Product Owner decision, for example once a minute per repository.
- Two scans in a row: the second is refused with a clear message (for example 429). Another repository can still be scanned.
- Size check: a reference solution with a one-minute limit adds or changes 5 lines in `app/service.py`, and passes the full test suite.

## Follow-up from Business

The owners of payments-api need to be able to scan it whenever they want.
