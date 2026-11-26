# S4-C: Calls without X-User become alice

**Security** · Stage 4 · S · about 14 min

Release at the start of Stage 4: `python scripts/new_task.py S4-C --mode SCRUM_MASTER --push`, only if the team has at most one other open task.

## Wish card

Finding from the security review: a request without the X-User header is treated as alice. So anyone who forgets the header, or leaves it out on purpose, can see and scan alice's repositories. Requests that don't say who is calling must be refused.

## Why this card

A real finding: `DEFAULT_USER = "alice"` in `app/server.py`. A one-line fix with a wide blast radius: tests, `docs/api.md` and the README's "try it in a browser" all rely on the default.

## Turn budget (minutes)

| BA | Security | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 1.5 | 2 | 2.5 | 1 | 3 | about 14 |

## What good looks like

- A request without `X-User` gets 401 everywhere a user matters. `/health` stays open.
- The Developer updates the tests openly (the test helper, and the test that expected the default) plus the docs and README examples.
- Open question worth raising: the README tells people to open `/repositories` in a browser, which can't send the header.
- Size check: a reference solution adds or changes 1 line in `app/server.py` and 4 lines in `tests/test_api.py`, and passes the full test suite. Without its test updates, it breaks `test_analysis_and_scan` and `test_list_defaults_to_alice` and `test_missing_repository`: the Developer must update them openly.

## Follow-up from Business

Opening http://localhost:8000/repositories in a browser should still work for demos.
