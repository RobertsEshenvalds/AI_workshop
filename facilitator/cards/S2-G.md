# S2-G: Show where each repository is hosted

**Feature** · Stage 2 · XS · about 10 min

Release at the start of Stage 2: `python scripts/new_task.py S2-G --push`. No product decision needed.

## Wish card

People keep repositories on GitHub, GitLab and Bitbucket. In the list of repositories, show where each one is hosted, for example github.com.

## Why this card

A derived field: the host comes from the URL. Small, and QA can check all three hosts in the seed data.

## Turn budget (minutes)

| BA | Architect | Developer | QA | PO | Hand-offs | Total |
|---|---|---|---|---|---|---|
| 1.5 | 1 | 1.5 | 2.5 | 1 | 2.5 | about 10 |

## What good looks like

- Every list item has the host of its URL: `github.com`, `gitlab.com` or `bitbucket.org`.
- Size check: a reference solution adds or changes 2 lines in `app/service.py`, and passes the full test suite.

## Follow-up from Business

Let people show only the repositories on one host.
