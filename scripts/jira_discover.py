# -*- coding: utf-8 -*-
"""Diagnostic Jira / Xray : projets accessibles et types de tickets.

Usage :
    python scripts/jira_discover.py [PROJECT_KEY]
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_jira_access import load_env_file  # noqa: E402


def jira_session(base: str, email: str, token: str) -> requests.Session:
    session = requests.Session()
    session.auth = (email, token)
    session.headers.update({"Accept": "application/json"})
    response = session.get(f"{base}/rest/api/3/myself", timeout=20)
    if response.status_code == 200:
        return session
    session.auth = None
    session.headers["Authorization"] = f"Bearer {token}"
    return session


def count_issues(session: requests.Session, base: str, jql: str) -> str:
    """Compte les tickets via l'API de recherche (ancienne puis nouvelle)."""
    response = session.get(
        f"{base}/rest/api/3/search",
        params={"jql": jql, "maxResults": 0},
        timeout=30,
    )
    if response.status_code == 200:
        return str(response.json().get("total", "?"))

    total = 0
    token = None
    while True:
        body: dict = {"jql": jql, "maxResults": 100, "fields": ["key"]}
        if token:
            body["nextPageToken"] = token
        response = session.post(
            f"{base}/rest/api/3/search/jql", json=body, timeout=30
        )
        if response.status_code != 200:
            return "?"
        data = response.json()
        total += len(data.get("issues", []))
        if data.get("isLast"):
            return str(total)
        token = data.get("nextPageToken")
        if not token:
            return str(total)


def main() -> int:
    load_env_file()
    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")
    wanted = (sys.argv[1] if len(sys.argv) > 1 else os.getenv("JIRA_PROJECT_KEY", "WTQA")).upper()

    if not (base and email and token):
        print("[ERREUR] Identifiants Jira incomplets dans .env.local.")
        return 2

    session = jira_session(base, email, token)

    response = session.get(
        f"{base}/rest/api/3/project/search",
        params={"maxResults": 100, "orderBy": "name"},
        timeout=30,
    )
    if response.status_code != 200:
        print(f"[ERREUR] Liste des projets : HTTP {response.status_code}")
        return 1

    projects = response.json().get("values", [])
    print(f"Projets accessibles ({len(projects)}) :")
    for project in projects:
        print(
            f"  - {project.get('key'):<12} | {project.get('name')} "
            f"| {project.get('projectTypeKey')}"
        )

    match = next((p for p in projects if p.get("key") == wanted), None)
    if not match:
        print(f"\n[ATTENTION] Projet '{wanted}' absent de la liste.")
        print("\nDisponibilite Xray par projet :")
        for project in projects:
            key = project.get("key")
            detail = session.get(f"{base}/rest/api/3/project/{key}", timeout=30)
            if detail.status_code != 200:
                print(f"  - {key:<12} | HTTP {detail.status_code}")
                continue
            types = {t.get("name") for t in detail.json().get("issueTypes", [])}
            required = {"Test", "Test Plan", "Test Execution", "Precondition"}
            ready = required.issubset(types)
            tests = count_issues(session, base, f'project = "{key}" AND issuetype = Test')
            bugs = count_issues(session, base, f'project = "{key}" AND issuetype = Bug')
            stories = count_issues(session, base, f'project = "{key}" AND issuetype = Story')
            print(
                f"  - {key:<12} | Xray {'OK' if ready else 'incomplet'}"
                f" | Tests {tests} | Bugs {bugs} | Stories {stories}"
                + ("" if ready else " | manque : " + ", ".join(sorted(required - types)))
            )
        return 0

    detail = session.get(f"{base}/rest/api/3/project/{wanted}", timeout=30)
    if detail.status_code != 200:
        print(f"[ATTENTION] Detail du projet {wanted} : HTTP {detail.status_code}")
        return 0

    data = detail.json()
    print(f"\nProjet {wanted} : {data.get('name')} (id {data.get('id')})")
    types = [t.get("name") for t in data.get("issueTypes", [])]
    print("Types de tickets : " + ", ".join(sorted(types)))

    required = ["Story", "Bug", "Test", "Test Plan", "Test Execution", "Precondition"]
    missing = [name for name in required if name not in types]
    if missing:
        print("[ATTENTION] Types manquants (Xray installe ?) : " + ", ".join(missing))
    else:
        print("[OK] Tous les types Xray requis sont presents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
