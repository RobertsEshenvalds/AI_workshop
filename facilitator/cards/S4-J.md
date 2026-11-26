# S4-J: Colleagues may scan, nobody may touch

**Contradiction** · Stage 4 · S · about 15 min

Release at the start of Stage 4: `python scripts/new_task.py S4-J --mode SCRUM_MASTER --push`, only if the team has at most one other open task.

## Wish card

Let colleagues scan each other's repositories, so anyone on the team can refresh an analysis before a meeting. As always, nobody may do anything with a repository they don't own.

## Why this card

The two sentences contradict each other. The drill is spotting it instead of silently picking one.

## Turn budget (minutes)

| BA | PO decision | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 1.5 | 2 | 2.5 | 3 | 1 | 3 | about 15 |

## What good looks like

- The BA reports `REQUIREMENT_AMBIGUITY` or `PRODUCT_DECISION_NEEDED`. If it comes back ambiguous a second time, the Scrum Master escalates it to the Product Owner (`WORKFLOW.md`, section 8).
- Red flag: someone picks one of the two sentences without a decision on record.
- Size check: a reference solution where anyone may scan but only the owner sees the result adds or changes 4 lines in `app/service.py`, and passes the full test suite.

## Follow-up from Business

Colleagues should also be able to see the analysis they asked for.
