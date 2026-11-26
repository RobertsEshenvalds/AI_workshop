"""In-memory data for the sample app.

Everything lives in memory: restarting the app resets it to the seed data
below. There is no database on purpose, so the workshop needs no installs.
"""

from copy import deepcopy

from . import analyzer

SEED_USERS = {
    "alice": {"username": "alice", "name": "Alice", "email": "alice@example.com"},
    "bob": {"username": "bob", "name": "Bob", "email": "bob@example.com"},
    "chen": {"username": "chen", "name": "Chen", "email": "chen@example.com"},
}

SEED_REPOSITORIES = [
    {
        "id": 1,
        "name": "payments-api",
        "url": "https://github.com/example-org/payments-api",
        "description": "Card payment service",
        "owner": "alice",
        "registered_at": "2026-10-01T09:00:00Z",
        "last_scanned_at": "2026-11-20T08:00:00Z",
    },
    {
        "id": 2,
        "name": "web-portal",
        "url": "https://gitlab.com/example-org/web-portal",
        "description": "Customer self-service website",
        "owner": "alice",
        "registered_at": "2026-10-03T14:30:00Z",
        "last_scanned_at": "2026-11-21T08:00:00Z",
    },
    {
        "id": 3,
        "name": "data-pipeline",
        "url": "https://github.com/example-org/data-pipeline",
        "description": "Nightly reporting jobs",
        "owner": "bob",
        "registered_at": "2026-10-10T11:15:00Z",
        "last_scanned_at": "2026-11-22T08:00:00Z",
    },
    {
        "id": 4,
        "name": "mobile-app",
        "url": "https://bitbucket.org/example-org/mobile-app",
        "description": "iOS and Android app",
        "owner": "chen",
        "registered_at": "2026-10-15T16:45:00Z",
        "last_scanned_at": "2026-11-23T08:00:00Z",
    },
]


class Store:
    """All app data. Call reset() to go back to the seed data."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.users = deepcopy(SEED_USERS)
        self.repositories = {repo["id"]: deepcopy(repo) for repo in SEED_REPOSITORIES}
        self.analyses = {
            repo_id: analyzer.analyze(repo, repo["last_scanned_at"])
            for repo_id, repo in self.repositories.items()
        }
        self.next_id = max(self.repositories) + 1
