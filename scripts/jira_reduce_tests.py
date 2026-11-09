# -*- coding: utf-8 -*-
"""Supprime les tests Xray existants pour repartir sur la campagne réduite.

Usage :
    python scripts/jira_reduce_tests.py            # diagnostic (liste)
    python scripts/jira_reduce_tests.py --apply    # supprime réellement

Supprime les tickets de type Test, Test Plan et Test Execution du projet
Jira configuré (WTQA par défaut). Les user stories et les bugs sont conservés.

Attention : le droit Jira « Delete Issues » est requis. Sur le plan gratuit,
ce droit ne peut pas être accordé ; il faut alors supprimer/recréer le projet.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_jira_access import load_env_file  # noqa: E402


def search_issues(session: requests.Session, base: str, jql: str) -> list[dict]:
    issues: list[dict] = []
    token = None
    while True:
        body: dict = {"jql": jql, "maxResults": 100, "fields": ["summary"]}
        if token:
            body["nextPageToken"] = token
        response = session.post(f"{base}/rest/api/3/search/jql", json=body, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(
                f"Recherche : HTTP {response.status_code} - {response.text[:300]}"
            )
        data = response.json()
        issues.extend(data.get("issues", []))
        if data.get("isLast"):
            return issues
        token = data.get("nextPageToken")
        if not token:
            return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    load_env_file()
    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    project = os.getenv("JIRA_PROJECT_KEY", "WTQA")
    session = requests.Session()
    session.auth = (os.getenv("JIRA_EMAIL", ""), os.getenv("JIRA_API_TOKEN", ""))
    session.headers.update({"Accept": "application/json"})

    if not (base and session.auth[0] and session.auth[1]):
        print("[ERREUR] Identifiants Jira incomplets dans .env.local.")
        return 2

    total = 0
    for issue_type in ("Test", "Test Plan", "Test Execution"):
        jql = f'project = "{project}" AND issuetype = "{issue_type}"'
        issues = search_issues(session, base, jql)
        total += len(issues)
        print(f"{issue_type:<16} : {len(issues)}")
        for issue in issues:
            summary = issue.get("fields", {}).get("summary", "")
            print(f"  - {issue['key']} | {summary}")
            if args.apply:
                response = session.delete(
                    f"{base}/rest/api/3/issue/{issue['key']}",
                    params={"deleteSubtasks": "true"},
                    timeout=60,
                )
                if response.status_code in (200, 204):
                    print(f"    [OK] supprime")
                else:
                    print(
                        f"    [ERREUR] HTTP {response.status_code} - "
                        f"{response.text[:300]}"
                    )

    if not args.apply:
        print(f"\n[INFO] {total} tickets a supprimer. Relance avec --apply.")
    else:
        print(f"\n[OK] Suppression demandee pour {total} tickets.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as exc:
        print(f"[ERREUR] {exc}")
        sys.exit(1)
