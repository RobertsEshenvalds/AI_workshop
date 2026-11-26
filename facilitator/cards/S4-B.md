# S4-B: 403 versus 404 reveals which repositories exist

**Security** · Stage 4 · S · about 14 min

Release at the start of Stage 4: `python scripts/new_task.py S4-B --mode SCRUM_MASTER --push`, only if the team has at most one other open task.

## Wish card

Finding from the security review: if you ask for someone else's repository, the API answers 403 "You don't have access". If the repository doesn't exist, it answers 404. So anyone can find out which repository numbers exist by trying them one by one. Someone else's repository should look exactly like one that doesn't exist.

## Why this card

A real finding in `_get_owned`. The right fix breaks two existing tests and contradicts `docs/api.md`, so the drill is about changing agreed behaviour openly.

## Turn budget (minutes)

| BA | Security | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 1.5 | 2 | 2.5 | 1 | 3 | about 14 |

## What good looks like

- Someone else's repository gives the same 404 and the same kind of message as a missing one, on every endpoint that takes a repository number.
- The Developer updates the two tests that expected 403, and `docs/api.md`, and says so in `implementation.md`.
- QA's "worked before" check spots the change and confirms it is the intended one.
- Size check: a reference solution adds or changes 1 line in `app/service.py`, 2 lines in `tests/test_api.py` and 1 line in `tests/test_service.py`, and passes the full test suite. Without its test updates, it breaks `test_cannot_open_someone_elses_repository` and `test_other_users_repository_is_forbidden`: the Developer must update them openly.

## Follow-up from Business

The error message shouldn't include the repository number either.
