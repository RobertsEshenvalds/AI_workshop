# S1-F: The summary says "1 open findings"

**Bug** · Stage 1 · XS · about 10 min

Stage 1 paper card. Print it with `python scripts/new_task.py S1-F --show`, hand it to the Product Owner, who types it into `tasks/TASK-001/task.md`. It also works as a spare later: release it with the script.

## Wish card

Small bug report from a user: the analysis summary of one of our repositories says "1 open findings". It should say "1 open finding". The other numbers read fine.

## Why this card

A real defect in `app/analyzer.py`. None of the seed repositories has exactly one finding, so QA has to find a way to test it, for example by calling the analyser with another URL (`https://github.com/x/r12` gives 1).

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- Exactly 1 gives "1 open finding."; 0 and 2 or more stay plural.
- The analysis stays the same for the same URL (`test_analysis_is_stable_for_the_same_url`).
- Size check: a reference solution adds or changes 1 line in `app/analyzer.py`, and passes the full test suite.

## Follow-up from Business

The same goes for "1 files", if that can ever happen. (It can't: every analysis has at least 40 files. A good Architect says so instead of building it.)
