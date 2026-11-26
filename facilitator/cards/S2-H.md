# S2-H: Languages across my repositories

**Feature** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-H --push`. No product decision needed.

## Wish card

Team leads want to know which programming languages their team works in. Give them the list of languages used across all of their own repositories, each language once, in alphabetical order.

## Why this card

A small aggregate with an ordering rule QA can check exactly.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- For example `GET /languages` gives Alice `["C#", "CSS", "PowerShell", "TypeScript"]` and Chen `["Java", "Kotlin"]`.
- Size check: a reference solution adds or changes 3 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

For each language, also show in how many repositories it is used.
