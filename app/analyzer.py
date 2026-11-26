"""A pretend code analyser.

It never downloads anything. It derives stable, made-up numbers from the
repository URL, so the same URL always gives the same analysis.
"""

import hashlib

LANGUAGE_PAIRS = [
    ("Python", "SQL"),
    ("TypeScript", "CSS"),
    ("Java", "Kotlin"),
    ("Go", "Shell"),
    ("C#", "PowerShell"),
]


def analyze(repository, scanned_at):
    """Return an analysis summary for one repository."""
    digest = hashlib.sha256(repository["url"].encode("utf-8")).digest()

    main_language, second_language = LANGUAGE_PAIRS[digest[0] % len(LANGUAGE_PAIRS)]
    main_share = 55 + digest[1] % 40
    files = 40 + digest[2] * 3
    open_findings = digest[3] % 12
    contributors = sorted({f"dev{1 + digest[i] % 9}@example.com" for i in (4, 5, 6)})

    return {
        "repository_id": repository["id"],
        "scanned_at": scanned_at,
        "languages": {main_language: main_share, second_language: 100 - main_share},
        "files": files,
        "lines_of_code": files * (80 + digest[7]),
        "open_findings": open_findings,
        "health_score": 55 + digest[8] % 45,
        "contributors": contributors,
        "summary": f"{files} files, mostly {main_language}. {open_findings} open findings.",
    }
