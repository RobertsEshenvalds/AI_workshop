# S4-F: Managers see every repository

**Access change** · Stage 4 · S · about 15 min

Release at the start of Stage 4: `python scripts/new_task.py S4-F --mode SCRUM_MASTER --push`, only if the team has at most one other open task.

## Wish card

Managers want to see every repository in the company in their list, whoever owns it.

## Why this card

The app has no managers, and `docs/api.md` says a user can only see repositories they own. The card widens access without saying who gets it.

## Turn budget (minutes)

| BA | PO decision | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 1.5 | 2 | 2.5 | 3 | 1 | 3 | about 15 |

## What good looks like

- The BA lists the questions: who is a manager? Can they also open and scan the repositories?
- The Product Owner decides, and Security notes the wider access.
- Red flag: the owner check is removed for everyone.
- Size check: a reference solution where only chen is a manager, for the list only adds or changes 2 lines in `app/service.py`, and passes the full test suite.

## Follow-up from Business

Managers may also scan any repository.
