# S5-G: Main language in the analysis

**Feature** · Stage 5 · XS · about 10 min

Release at the start of Stage 5: `python scripts/new_task.py S5-G --mode SCRUM_MASTER --push`. Then hands off.

## Wish card

In the analysis, also show the repository's main language: the language with the biggest share.

## Why this card

Safe for a hands-off run: one more field in an existing response, no new input, and the card answers its own questions. Any open question in Stage 5 costs two extra turns (a `BLOCKED` report and a `PRODUCT_OWNER` decision). Ties can't happen: the main language always has at least 55%.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- web-portal shows `TypeScript`, payments-api shows `C#`.
- The analysis stays the same for the same URL.
- Size check: a reference solution adds or changes 1 line in `app/analyzer.py`, and passes the full test suite.

## Follow-up from Business

None. Don't add a follow-up during a hands-off run.
