# -*- coding: utf-8 -*-
"""Verifie le contenu du projet Jira/Xray apres import.

Usage :
    python scripts/jira_verify.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_jira_access import load_env_file  # noqa: E402


def count_jira(session: requests.Session, base: str, project: str, issue_type: str) -> int:
    jql = f'project = "{project}" AND issuetype = "{issue_type}"'
    total = 0
    token = None
    while True:
        body: dict = {"jql": jql, "maxResults": 100, "fields": ["key"]}
        if token:
            body["nextPageToken"] = token
        response = session.post(f"{base}/rest/api/3/search/jql", json=body, timeout=30)
        if response.status_code != 200:
            return -1
        data = response.json()
        total += len(data.get("issues", []))
        if data.get("isLast"):
            return total
        token = data.get("nextPageToken")
        if not token:
            return total


def main() -> int:
    load_env_file()
    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    project = os.getenv("JIRA_PROJECT_KEY", "WTQA")
    session = requests.Session()
    session.auth = (os.getenv("JIRA_EMAIL", ""), os.getenv("JIRA_API_TOKEN", ""))
    session.headers.update({"Accept": "application/json"})

    print(f"Projet {project} :")
    for issue_type in ("Story", "Bug", "Test", "Test Plan", "Test Execution"):
        print(f"  - {issue_type:<16} : {count_jira(session, base, project, issue_type)}")

    jql = f'project = "{project}" AND issuetype = "Test Execution"'
    response = session.post(
        f"{base}/rest/api/3/search/jql",
        json={"jql": jql, "maxResults": 10, "fields": ["summary"]},
        timeout=30,
    )
    executions = response.json().get("issues", [])
    if not executions:
        print("[ATTENTION] Aucune Test Execution trouvee.")
        return 0

    execution = executions[0]
    execution_id = execution["id"]
    print(f"\nTest Execution : {execution['key']} - {execution['fields']['summary']}")

    client_id = os.getenv("XRAY_CLIENT_ID", "")
    client_secret = os.getenv("XRAY_CLIENT_SECRET", "")
    xray_base = os.getenv("XRAY_BASE_URL", "https://xray.cloud.getxray.app").rstrip("/")
    token = requests.post(
        f"{xray_base}/api/v2/authenticate",
        json={"client_id": client_id, "client_secret": client_secret},
        timeout=30,
    ).json()

    query = """
    query Execution($id: String!) {
      getTestExecution(issueId: $id) {
        issueId
        jira(fields: ["key", "summary"])
        testRuns(limit: 100) {
          total
          results {
            status { name }
            test { issueId jira(fields: ["key"]) }
          }
        }
      }
    }
    """
    response = requests.post(
        f"{xray_base}/api/v2/graphql",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"query": query, "variables": {"id": execution_id}},
        timeout=60,
    )
    payload = response.json()
    if "errors" in payload:
        print("[ERREUR] GraphQL : " + json.dumps(payload["errors"], ensure_ascii=False)[:800])
        return 1

    data = payload["data"]["getTestExecution"]
    runs = data.get("testRuns", {}).get("results", [])
    statuses = Counter((run.get("status") or {}).get("name") for run in runs)
    print(f"  Test runs : {data.get('testRuns', {}).get('total')}")
    for name, count in sorted(statuses.items(), key=lambda item: str(item[0])):
        print(f"  - {name:<12} : {count}")

    expected = {"FAILED": 9}
    actual = {str(name).upper(): count for name, count in statuses.items()}
    if actual == expected:
        print("[OK] Statuts conformes : 9 FAILED (campagne réduite).")
    else:
        print(f"[ATTENTION] Statuts inattendus : {actual}")

    # Verification du Test Plan
    jql_plan = f'project = "{project}" AND issuetype = "Test Plan"'
    plans = session.post(
        f"{base}/rest/api/3/search/jql",
        json={"jql": jql_plan, "maxResults": 10, "fields": ["summary"]},
        timeout=30,
    ).json().get("issues", [])
    if plans:
        plan = plans[0]
        plan_query = """
        query Plan($id: String!) {
          getTestPlan(issueId: $id) {
            issueId
            jira(fields: ["key", "summary"])
            tests(limit: 100) { total }
            testExecutions(limit: 100) { total }
          }
        }
        """
        plan_response = requests.post(
            f"{xray_base}/api/v2/graphql",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={"query": plan_query, "variables": {"id": plan["id"]}},
            timeout=60,
        ).json()
        if "errors" not in plan_response:
            plan_data = plan_response["data"]["getTestPlan"]
            print(
                f"\nTest Plan : {plan['key']} - {plan['fields']['summary']} "
                f"| {plan_data.get('tests', {}).get('total')} tests "
                f"| {plan_data.get('testExecutions', {}).get('total')} execution(s)"
            )
        else:
            print("[ATTENTION] Verification du Test Plan impossible.")

    # Verification des etapes des 9 tests
    test_query = """
    query AllTests($jql: String!) {
      getTests(jql: $jql, limit: 100) {
        total
        results {
          issueId
          jira(fields: ["key"])
          testType { name }
          steps { action }
        }
      }
    }
    """
    test_response = requests.post(
        f"{xray_base}/api/v2/graphql",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"query": test_query, "variables": {"jql": f'project = "{project}"'}},
        timeout=60,
    ).json()
    if "errors" not in test_response:
        tests = test_response["data"]["getTests"]
        no_steps = [
            test["jira"]["key"]
            for test in tests.get("results", [])
            if not test.get("steps")
        ]
        print(
            f"\nTests Xray : {tests.get('total')} | "
            f"avec etapes : {tests.get('total', 0) - len(no_steps)} | "
            f"sans etapes : {len(no_steps)}"
        )
        if no_steps:
            print("  Sans etapes : " + ", ".join(no_steps))
    else:
        print("[ATTENTION] Verification des etapes impossible.")

    # Verification des dossiers du Test Repository
    project_info = session.get(
        f"{base}/rest/api/3/project/{project}", timeout=30
    ).json()
    project_id = str(project_info.get("id", ""))
    csv_path = (
        Path(__file__).resolve().parent.parent
        / "jira-xray"
        / "WebTours_Xray_Import.csv"
    )
    folders: list[str] = []
    if csv_path.exists():
        with csv_path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                folder = (row.get("Folder") or "").strip()
                if folder and folder not in folders:
                    folders.append(folder)

    folder_query = """
    query Folder($projectId: String!, $path: String!) {
      getFolder(projectId: $projectId, path: $path) {
        name
        path
        testsCount
      }
    }
    """
    print("\nDossiers Xray :")
    for folder in folders:
        payload = requests.post(
            f"{xray_base}/api/v2/graphql",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "query": folder_query,
                "variables": {"projectId": project_id, "path": folder},
            },
            timeout=60,
        ).json()
        if "errors" in payload:
            message = payload["errors"][0].get("message", "")
            print(f"  - {folder} : [ERREUR] {message[:120]}")
            continue
        data = payload.get("data", {}).get("getFolder")
        if data:
            print(f"  - {data.get('path')} : {data.get('testsCount')} tests")
        else:
            print(f"  - {folder} : [ABSENT]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
