"""Business logic for the repository registry.

Every function takes the store and the current user's username. The HTTP layer
in server.py only turns requests into calls to these functions, so new
features usually start here.
"""

from datetime import datetime, timezone

from . import analyzer


class ServiceError(Exception):
    """Base class for errors the API returns to the caller."""

    status = 400


class Invalid(ServiceError):
    status = 400


class Unauthorized(ServiceError):
    status = 401


class Forbidden(ServiceError):
    status = 403


class NotFound(ServiceError):
    status = 404


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def require_user(store, username):
    user = store.users.get(username)
    if user is None:
        raise Unauthorized(f"Unknown user: {username}")
    return user


def _summary(repo):
    return {"id": repo["id"], "name": repo["name"], "url": repo["url"], "owner": repo["owner"]}


def _get_owned(store, username, repository_id):
    require_user(store, username)
    repo = store.repositories.get(repository_id)
    if repo is None:
        raise NotFound(f"Repository {repository_id} not found")
    if repo["owner"] != username:
        raise Forbidden("You don't have access to this repository")
    return repo


def list_repositories(store, username):
    """The repositories the user owns, oldest first."""
    require_user(store, username)
    return [
        _summary(repo)
        for repo in sorted(store.repositories.values(), key=lambda r: r["id"])
        if repo["owner"] == username
    ]


def get_repository(store, username, repository_id):
    return dict(_get_owned(store, username, repository_id))


def get_analysis(store, username, repository_id):
    _get_owned(store, username, repository_id)
    return dict(store.analyses[repository_id])


def scan_repository(store, username, repository_id):
    """Run the (pretend) analysis again now and return the new result."""
    repo = _get_owned(store, username, repository_id)
    scanned_at = now_utc()
    repo["last_scanned_at"] = scanned_at
    store.analyses[repository_id] = analyzer.analyze(repo, scanned_at)
    return dict(store.analyses[repository_id])
