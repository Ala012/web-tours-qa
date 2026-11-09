# -*- coding: utf-8 -*-
"""Verifie l'acces a Jira Cloud et Xray Cloud.

Lit les identifiants depuis `.env.local` (non versionne) ou depuis les
variables d'environnement. N'affiche jamais les secrets.

Usage :
    python scripts/check_jira_access.py
"""
from __future__ import annotations

import base64
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env.local"

XRAY_DEFAULT_URL = "https://xray.cloud.getxray.app"


def load_env_file() -> None:
    """Charge .env.local sans ecraser les variables deja definies."""
    if not ENV_FILE.exists():
        return
    for raw_line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def jira_headers(email: str, token: str) -> tuple[dict, str]:
    """Retourne des en-tetes valides (Basic ou Bearer) et le mode retenu."""
    basic = base64.b64encode(f"{email}:{token}".encode("utf-8")).decode("ascii")
    headers = {"Authorization": f"Basic {basic}", "Accept": "application/json"}
    return headers, "Basic"


def check_jira(base: str, email: str, token: str, project: str) -> bool:
    headers, mode = jira_headers(email, token)
    try:
        response = requests.get(
            f"{base}/rest/api/3/myself", headers=headers, timeout=20
        )
    except requests.RequestException as exc:
        print(f"[ERREUR] Connexion Jira impossible : {exc}")
        return False

    # Les tokens recents avec scopes peuvent exiger Bearer.
    if response.status_code in (401, 403):
        bearer = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        retry = requests.get(
            f"{base}/rest/api/3/myself", headers=bearer, timeout=20
        )
        if retry.status_code == 200:
            headers, mode, response = bearer, "Bearer", retry

    if response.status_code != 200:
        print(
            f"[ERREUR] Jira a repondu HTTP {response.status_code}. "
            "Verifie JIRA_EMAIL, JIRA_API_TOKEN et les scopes du token."
        )
        return False

    me = response.json()
    print(
        f"[OK] Jira ({mode}) : connecte comme "
        f"{me.get('displayName', '?')} <{me.get('emailAddress', '?')}>"
    )

    try:
        project_response = requests.get(
            f"{base}/rest/api/3/project/{project}", headers=headers, timeout=20
        )
    except requests.RequestException as exc:
        print(f"[ATTENTION] Verification du projet impossible : {exc}")
        return True

    if project_response.status_code == 200:
        data = project_response.json()
        print(f"[OK] Projet {project} : {data.get('name')} (id {data.get('id')})")
    elif project_response.status_code in (400, 404):
        print(
            f"[ATTENTION] Projet '{project}' introuvable. "
            "Cree-le dans Jira ou modifie JIRA_PROJECT_KEY."
        )
    elif project_response.status_code == 403:
        print(f"[ATTENTION] Le compte n'a pas acces au projet '{project}'.")
    else:
        print(
            f"[ATTENTION] Projet '{project}' : HTTP "
            f"{project_response.status_code}."
        )
    return True


def check_xray(client_id: str, client_secret: str) -> bool:
    base = os.getenv("XRAY_BASE_URL", XRAY_DEFAULT_URL).rstrip("/")
    try:
        response = requests.post(
            f"{base}/api/v2/authenticate",
            json={"client_id": client_id, "client_secret": client_secret},
            timeout=30,
        )
    except requests.RequestException as exc:
        print(f"[ERREUR] Connexion Xray impossible : {exc}")
        return False

    if response.status_code != 200:
        print(
            f"[ERREUR] Xray a repondu HTTP {response.status_code}. "
            "Verifie XRAY_CLIENT_ID / XRAY_CLIENT_SECRET. "
            "Si ton site est en Europe, essaie "
            "XRAY_BASE_URL=https://eu.xray.cloud.getxray.app"
        )
        return False

    token = response.json()
    if isinstance(token, dict):
        token = token.get("token", "")
    print(f"[OK] Xray : token obtenu (valide 24 h, {len(token)} caracteres).")

    try:
        graphql = requests.post(
            f"{base}/api/v2/graphql",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"query": "{ getProjects { total } }"},
            timeout=30,
        )
        payload = graphql.json()
        if graphql.status_code == 200 and "errors" not in payload:
            total = payload.get("data", {}).get("getProjects", {}).get("total", "?")
            print(f"[OK] Xray GraphQL : {total} projet(s) visible(s).")
        else:
            print(
                "[ATTENTION] Authentification Xray OK, mais la verification "
                "GraphQL a echoue (droits ou version d'API)."
            )
    except (requests.RequestException, ValueError) as exc:
        print(f"[ATTENTION] Verification GraphQL Xray impossible : {exc}")

    return True


def main() -> int:
    load_env_file()

    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")
    project = os.getenv("JIRA_PROJECT_KEY", "WTQA")
    client_id = os.getenv("XRAY_CLIENT_ID", "")
    client_secret = os.getenv("XRAY_CLIENT_SECRET", "")

    missing = [
        name
        for name, value in (
            ("JIRA_BASE_URL", base),
            ("JIRA_EMAIL", email),
            ("JIRA_API_TOKEN", token),
        )
        if not value
    ]
    if missing:
        print("[ERREUR] Variables manquantes : " + ", ".join(missing))
        print("Copie .env.local.example en .env.local puis remplis les valeurs.")
        return 2

    jira_ok = check_jira(base, email, token, project)

    if not client_id or not client_secret:
        print(
            "[INFO] Xray non configure : renseigne XRAY_CLIENT_ID et "
            "XRAY_CLIENT_SECRET dans .env.local."
        )
        return 0 if jira_ok else 1

    xray_ok = check_xray(client_id, client_secret)
    return 0 if jira_ok and xray_ok else 1


if __name__ == "__main__":
    sys.exit(main())
