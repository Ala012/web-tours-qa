# -*- coding: utf-8 -*-
"""Affiche un ticket Jira et, si c'est un Test, ses etapes Xray.

Usage :
    python scripts/jira_show_issue.py WTQA-1
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_jira_access import load_env_file  # noqa: E402


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage : python scripts/jira_show_issue.py <CLE>")
        return 2
    key = sys.argv[1].strip().upper()

    load_env_file()
    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    session = requests.Session()
    session.auth = (os.getenv("JIRA_EMAIL", ""), os.getenv("JIRA_API_TOKEN", ""))
    session.headers.update({"Accept": "application/json"})

    issue = session.get(
        f"{base}/rest/api/3/issue/{key}",
        params={"fields": "summary,issuetype,status,priority,labels,description,issuelinks"},
        timeout=30,
    )
    if issue.status_code != 200:
        print(f"[ERREUR] {key} : HTTP {issue.status_code}")
        return 1
    data = issue.json()
    fields = data["fields"]
    print(f"{key} | {fields['issuetype']['name']} | {fields.get('status', {}).get('name')}")
    print(f"Resume : {fields.get('summary')}")
    print(f"Priorite : {(fields.get('priority') or {}).get('name')}")
    print(f"Labels : {', '.join(fields.get('labels', []))}")
    description = fields.get("description")
    if description:
        texts = []

        def walk(node):
            if isinstance(node, dict):
                if node.get("type") == "text":
                    texts.append(node.get("text", ""))
                for child in node.get("content", []):
                    walk(child)

        walk(description)
        print("Description : " + " ".join(texts)[:500])

    links = fields.get("issuelinks", [])
    print(f"Liens : {len(links)}")
    for link in links:
        link_type = link.get("type", {})
        if "outwardIssue" in link:
            print(
                f"  - {link_type.get('outward')} "
                f"{link['outwardIssue']['key']}"
            )
        if "inwardIssue" in link:
            print(
                f"  - {link_type.get('inward')} "
                f"{link['inwardIssue']['key']}"
            )

    if fields["issuetype"]["name"] != "Test":
        return 0

    client_id = os.getenv("XRAY_CLIENT_ID", "")
    client_secret = os.getenv("XRAY_CLIENT_SECRET", "")
    xray_base = os.getenv("XRAY_BASE_URL", "https://xray.cloud.getxray.app").rstrip("/")
    if not (client_id and client_secret):
        print("[INFO] Identifiants Xray absents : etapes non affichees.")
        return 0

    token = requests.post(
        f"{xray_base}/api/v2/authenticate",
        json={"client_id": client_id, "client_secret": client_secret},
        timeout=30,
    ).json()
    query = """
    query ShowTest($id: String!) {
      getTest(issueId: $id) {
        issueId
        testType { name }
        steps { action data result }
      }
    }
    """
    response = requests.post(
        f"{xray_base}/api/v2/graphql",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"query": query, "variables": {"id": data["id"]}},
        timeout=30,
    )
    payload = response.json()
    print("\nXray :")
    print(json.dumps(payload, ensure_ascii=False, indent=2)[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
