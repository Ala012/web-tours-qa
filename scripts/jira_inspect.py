# -*- coding: utf-8 -*-
"""Compare les tests presents dans chaque projet Jira avec nos 36 tests.

Usage :
    python scripts/jira_inspect.py
"""
from __future__ import annotations

import csv
import glob
import os
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_jira_access import load_env_file  # noqa: E402
from jira_discover import jira_session  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ID_PATTERN = re.compile(r"^([A-Z]+-[A-Z]+-\d+)")


def local_ids() -> set[str]:
    ids = set()
    for path in glob.glob(str(ROOT / "tests-manuels" / "**" / "*.md"), recursive=True):
        match = ID_PATTERN.match(os.path.splitext(os.path.basename(path))[0])
        if match:
            ids.add(match.group(1))
    return ids


def fetch_issues(session: requests.Session, base: str, jql: str) -> list[dict]:
    issues: list[dict] = []
    token = None
    while True:
        body: dict = {
            "jql": jql,
            "maxResults": 100,
            "fields": ["summary", "issuetype", "status"],
        }
        if token:
            body["nextPageToken"] = token
        response = session.post(f"{base}/rest/api/3/search/jql", json=body, timeout=30)
        if response.status_code != 200:
            print(f"[ERREUR] Recherche : HTTP {response.status_code}")
            break
        data = response.json()
        issues.extend(data.get("issues", []))
        if data.get("isLast"):
            break
        token = data.get("nextPageToken")
        if not token:
            break
    return issues


def main() -> int:
    load_env_file()
    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")
    if not (base and email and token):
        print("[ERREUR] Identifiants Jira incomplets.")
        return 2

    ours = local_ids()
    print(f"Tests locaux de reference : {len(ours)}")

    session = jira_session(base, email, token)
    projects = session.get(
        f"{base}/rest/api/3/project/search", params={"maxResults": 100}, timeout=30
    ).json().get("values", [])

    print("\nPresence de nos tests par projet :")
    for project in projects:
        key = project.get("key")
        issues = fetch_issues(
            session, base, f'project = "{key}" AND issuetype = Test'
        )
        found_ids = []
        for issue in issues:
            summary = issue.get("fields", {}).get("summary", "")
            match = ID_PATTERN.match(summary)
            if match and match.group(1) in ours:
                found_ids.append(match.group(1))
        unique = set(found_ids)
        duplicates = len(found_ids) - len(unique)
        print(
            f"  - {key:<12} | {len(unique):>2}/{len(ours)} identifiants "
            f"| {len(issues):>3} tests | doublons {duplicates}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
