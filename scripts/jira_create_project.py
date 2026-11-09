# -*- coding: utf-8 -*-
"""Cree un projet Jira Cloud pour le mini-projet WebTours.

Usage :
    python scripts/jira_create_project.py
    python scripts/jira_create_project.py --key WTQA --name "WEB_TOURS QA"

Nécessite un token Jira avec le droit de créer des projets
(scope manage:jira-project ou compte administrateur).
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_jira_access import load_env_file  # noqa: E402

DEFAULT_TEMPLATE = "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic"
FALLBACK_TEMPLATES = (
    "com.pyxis.greenhopper.jira:gh-simplified-kanban-classic",
    "com.pyxis.greenhopper.jira:gh-simplified-basic",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", default="WTQA")
    parser.add_argument("--name", default="WEB_TOURS QA")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE)
    parser.add_argument("--description", default="Mini-projet QA WebTours : tests manuels, Xray, Selenium et CI Jenkins.")
    args = parser.parse_args()

    load_env_file()
    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")
    if not (base and email and token):
        print("[ERREUR] Identifiants Jira incomplets dans .env.local.")
        return 2

    session = requests.Session()
    session.auth = (email, token)
    session.headers.update({"Accept": "application/json"})

    me = session.get(f"{base}/rest/api/3/myself", timeout=20)
    if me.status_code != 200:
        print(f"[ERREUR] Authentification Jira : HTTP {me.status_code}")
        return 1
    account_id = me.json().get("accountId")
    print(f"[OK] Connecte comme {me.json().get('displayName')} ({account_id})")

    existing = session.get(f"{base}/rest/api/3/project/{args.key}", timeout=20)
    if existing.status_code == 200:
        data = existing.json()
        print(
            f"[INFO] Le projet {args.key} existe deja : "
            f"{data.get('name')} (id {data.get('id')})"
        )
        return 0
    if existing.status_code not in (400, 404):
        print(f"[ATTENTION] Verification du projet : HTTP {existing.status_code}")

    payload = {
        "key": args.key,
        "name": args.name,
        "projectTypeKey": "software",
        "projectTemplateKey": args.template,
        "description": args.description,
        "leadAccountId": account_id,
        "assigneeType": "PROJECT_LEAD",
    }

    templates = (args.template,) + tuple(
        t for t in FALLBACK_TEMPLATES if t != args.template
    )
    for template in templates:
        payload["projectTemplateKey"] = template
        response = session.post(
            f"{base}/rest/api/3/project", json=payload, timeout=60
        )
        if response.status_code in (200, 201):
            data = response.json()
            print(
                f"[OK] Projet cree : {data.get('key')} - {data.get('name')} "
                f"(id {data.get('id')}, template {template})"
            )
            return 0
        print(
            f"[ATTENTION] Template {template} refuse : "
            f"HTTP {response.status_code} - {response.text[:300]}"
        )
        if response.status_code in (401, 403):
            break

    print(
        "[ERREUR] Creation impossible. Verifie que le token a le scope "
        "manage:jira-project et que la cle n'est pas deja utilisee."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
