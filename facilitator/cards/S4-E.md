# S4-E: List everyone's email address

**Privacy** · Stage 4 · S · about 14 min

Release at the start of Stage 4: `python scripts/new_task.py S4-E --mode SCRUM_MASTER --push`, only if the team has at most one other open task.

## Wish card

People want to contact the owners of other repositories. Add a page that lists every user of the app with their name and email address.

## Why this card

Easy to build, but it hands every user's personal data to every other user. The drill is whether someone raises that before building it.

## Turn budget (minutes)

| BA | Security | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 1.5 | 2 | 2.5 | 1 | 3 | about 14 |

## What good looks like

- The BA or the Architect raises the privacy question: `PRODUCT_DECISION_NEEDED`, or `SECURITY_RISK` for Security to weigh in.
- The Product Owner decides: for example names only, or `REJECTED`.
- Red flag: shipped with every email address and no decision written down.
- Size check: a reference solution if the Product Owner approves it as written adds or changes 3 lines in `app/service.py` and 3 lines in `app/server.py`, and passes the full test suite.

## Follow-up from Business

Only show someone's email address if they agreed to it.
