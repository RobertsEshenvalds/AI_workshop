# S3-C: The health score ignores open findings

**Product bug** · Stage 3 · S · about 15 min

Release once the Scrum Master is online: `python scripts/new_task.py S3-C --mode SCRUM_MASTER --push`. Leaves out a product decision on purpose.

## Wish card

Complaint from a manager: web-portal has 2 open findings and a health score of 59, while payments-api has 9 open findings and scores 79. The health score doesn't seem to care about open findings at all. Make the health score reflect the open findings.

## Why this card

True in the seed data: the analyser derives the score from the URL, not from the findings. The card says what's wrong but not the formula, so the Product Owner must decide it.

## Turn budget (minutes)

| BA | PO decision | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 1.5 | 2 | 2.5 | 3 | 1 | 3 | about 15 |

## What good looks like

- The formula is a Product Owner decision in `requirements.md`, for example 100 minus 5 per open finding, never below 0.
- Afterwards web-portal (2 findings) scores higher than payments-api (9).
- Red flag: the Developer invents a formula.
- Size check: a reference solution with the example formula adds or changes 1 line in `app/analyzer.py`, and passes the full test suite.

## Follow-up from Business

Lines of code should count too: a big repository with a few findings is healthier than a small one with the same number.
