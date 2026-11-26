# S3-D: Mark repositories with old scans

**Feature** · Stage 3 · S · about 15 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-D --mode SCRUM_MASTER --push`. Leaves out a product decision on purpose.

## Wish card

Some repositories haven't been scanned for a long time, and nobody notices. In the list, mark the repositories whose last scan is too old.

## Why this card

"Too old" is not defined: a product decision. The seed scans are from 20 to 23 November 2026, so whether they count as old depends on the threshold and on the day you run the workshop.

## Turn budget (minutes)

| BA | PO decision | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 1.5 | 2 | 2.5 | 3 | 1 | 3 | about 15 |

## What good looks like

- The threshold is a Product Owner decision, for example 7 days.
- QA checks both sides: a fresh scan is not marked, an old date is.
- Size check: a reference solution with a 7-day threshold adds or changes 5 lines in `app/service.py`, and passes the full test suite.

## Follow-up from Business

Repositories with old scans should also come first in the list.
