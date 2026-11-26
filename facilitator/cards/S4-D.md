# S4-D: Rescanning never changes the numbers

**Not a bug** · Stage 4 · S · about 13 min

Release at the start of Stage 4: `python scripts/new_task.py S4-D --mode SCRUM_MASTER --push`, only if the team has at most one other open task.

## Wish card

Bug report from a user: I fixed three findings in payments-api and scanned it again, but the analysis shows exactly the same numbers as before. Scanning seems to be broken.

## Why this card

Works as designed: `app/analyzer.py` is a pretend analyser that derives stable numbers from the URL and never downloads code. The drill is whether the team investigates and classifies before it "fixes" anything.

## Turn budget (minutes)

| BA | Architect | PO decision | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 1.5 | 1.5 | 2 | 1 | 3 | about 13 |

## What good looks like

- The BA or the Architect finds the analyser's docstring and says it's by design.
- The Product Owner decides: `REJECTED` (works as designed), or a short note in `docs/api.md` that the analysis is simulated.
- Red flag: the Developer makes the numbers random, which breaks `test_analysis_is_stable_for_the_same_url`.
- Size check: no code change is expected. The documentation note, if the Product Owner wants one, is a line or two in `docs/api.md`.

## Follow-up from Business

Then the documentation should say clearly that the analysis is simulated.
