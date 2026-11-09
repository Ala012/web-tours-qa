# -*- coding: utf-8 -*-
"""Active les types de tickets Xray dans un projet Jira Cloud.

Usage :
    python scripts/jira_xray_setup.py            # diagnostic seulement
    python scripts/jira_xray_setup.py --apply    # ajoute les types manquants
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_jira_access import load_env_file  # noqa: E402

REQUIRED = ("Test", "Test Plan", "Test Execution", "Precondition")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=os.getenv("JIRA_PROJECT_KEY", "WTQA"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    load_env_file()
    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")
    if not (base and email and token):
        print("[ERREUR] Identifiants Jira incomplets.")
        return 2

    session = requests.Session()
    session.auth = (email, token)
    session.headers.update({"Accept": "application/json"})

    project = session.get(f"{base}/rest/api/3/project/{args.project}", timeout=30)
    if project.status_code != 200:
        print(f"[ERREUR] Projet {args.project} : HTTP {project.status_code}")
        return 1
    project_id = project.json().get("id")
    current_names = {t.get("name") for t in project.json().get("issueTypes", [])}
    print(f"Projet {args.project} (id {project_id}) : {', '.join(sorted(current_names))}")

    types = session.get(f"{base}/rest/api/3/issuetype", timeout=30)
    if types.status_code != 200:
        print(f"[ERREUR] Liste des types : HTTP {types.status_code}")
        return 1
    by_name = {t.get("name"): t.get("id") for t in types.json()}
    missing = [name for name in REQUIRED if name not in current_names]
    absent_globally = [name for name in missing if name not in by_name]
    print(f"Types Xray manquants dans le projet : {', '.join(missing) or 'aucun'}")
    if absent_globally:
        print(
            "[ERREUR] Types absents globalement (Xray installe ?) : "
            + ", ".join(absent_globally)
        )
        return 1
    if not missing:
        print("[OK] Tous les types Xray sont deja presents.")
        return 0

    schemes = session.get(
        f"{base}/rest/api/3/issuetypescheme/project",
        params={"projectId": project_id},
        timeout=30,
    )
    if schemes.status_code != 200:
        print(f"[ERREUR] Schema de types : HTTP {schemes.status_code}")
        return 1
    values = schemes.json().get("values", [])
    if not values:
        print("[ERREUR] Aucun schema de types trouve pour ce projet.")
        return 1
    scheme = values[0].get("issueTypeScheme", {})
    scheme_id = scheme.get("id")
    print(f"Schema : {scheme.get('name')} (id {scheme_id})")

    detail = session.get(f"{base}/rest/api/3/issuetypescheme/{scheme_id}", timeout=30)
    if detail.status_code == 200:
        ids = detail.json().get("issueTypeIds", [])
        names = [name for name, tid in by_name.items() if tid in ids]
        print(f"Types du schema : {', '.join(sorted(names))}")

    if not args.apply:
        print(
            "\n[INFO] Mode diagnostic. Relance avec --apply pour ajouter : "
            + ", ".join(missing)
        )
        return 0

    response = session.put(
        f"{base}/rest/api/3/issuetypescheme/{scheme_id}/issuetype",
        json={"issueTypeIds": [by_name[name] for name in missing]},
        timeout=30,
    )
    if response.status_code in (200, 201, 204):
        print("[OK] Types ajoutes : " + ", ".join(missing))
    else:
        print(
            f"[ERREUR] Ajout des types : HTTP {response.status_code} - "
            f"{response.text[:300]}"
        )
        return 1

    verify = session.get(f"{base}/rest/api/3/project/{args.project}", timeout=30)
    final_names = {t.get("name") for t in verify.json().get("issueTypes", [])}
    still_missing = [name for name in REQUIRED if name not in final_names]
    if still_missing:
        print("[ATTENTION] Toujours manquants : " + ", ".join(still_missing))
        return 1
    print("[OK] Types Xray actifs dans le projet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
