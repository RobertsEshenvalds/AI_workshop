# S3-B: Letter grade

**Feature** · Stage 3 · S · about 15 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-B --mode SCRUM_MASTER --push`. Leaves out a product decision on purpose.

## Wish card

Managers don't want to read health scores from 0 to 100. Next to the health score in the analysis, show a simple letter grade: A, B or C.

## Why this card

The card leaves out where A ends and B starts. A good BA lists that as an open question; unattended, it becomes `PRODUCT_DECISION_NEEDED` and the Scrum Master routes it to the Product Owner.

## Turn budget (minutes)

| BA | PO decision | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 1.5 | 2 | 2.5 | 3 | 1 | 3 | about 15 |

## What good looks like

- The thresholds are under "Decisions" in `requirements.md`, marked as the Product Owner's, before anyone designs or builds. Any thresholds are fine, for example A from 85, B from 70.
- Red flag: the BA, Architect or Developer picks the thresholds themselves.
- The analysis and the scan result gain `grade`.
- Size check: a reference solution with the example thresholds adds or changes 3 lines in `app/analyzer.py`, and passes the full test suite.

## Follow-up from Business

Managers asked for a fourth grade, D, for the repositories that need urgent attention.
