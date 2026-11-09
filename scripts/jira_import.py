# -*- coding: utf-8 -*-
"""Import du mini-projet WebTours dans Jira Cloud + Xray Cloud.

Phases :
    meta       : 6 user stories + 15 bugs (API REST Jira)
    tests      : 36 tests manuels avec etapes (API GraphQL Xray)
    execution  : Test Plan, Test Execution, resultats 20 PASS / 16 FAIL, liens

Exemples :
    python scripts/jira_import.py --phase meta --limit 1
    python scripts/jira_import.py --phase tests --limit 1
    python scripts/jira_import.py --phase all

Le script est idempotent : un ticket dont le resume existe deja est reutilise.
Les secrets sont lus dans .env.local et ne sont jamais affiches.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_jira_access import load_env_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
JIRA_DIR = ROOT / "jira-xray"
PRIORITY_MAP = {
    "Critical": "Highest",
    "High": "High",
    "Medium": "Medium",
    "Low": "Low",
    "Lowest": "Lowest",
}
PLAN_SUMMARY = "Plan de test WebTours – Sprint 1"
EXEC_SUMMARY = "Exécution manuelle – Sprint 1"
ENVIRONMENT = "Windows11-Chrome-WebTours-local"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def adf(text: str) -> dict:
    """Convertit du texte brut en Atlassian Document Format."""
    paragraphs = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        paragraphs.append(
            {"type": "paragraph", "content": [{"type": "text", "text": line}]}
        )
    if not paragraphs:
        paragraphs = [{"type": "paragraph", "content": []}]
    return {"type": "doc", "version": 1, "content": paragraphs}


def labels(value: str) -> list[str]:
    return [item for item in re.split(r"\s+", (value or "").strip()) if item]


def priority(value: str) -> dict:
    return {"name": PRIORITY_MAP.get((value or "").strip(), "Medium")}


def read_csv(name: str) -> list[dict]:
    path = JIRA_DIR / name
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_steps(steps_text: str, expected_text: str) -> list[dict]:
    def numbered(text: str) -> list[str]:
        items = []
        for line in (text or "").splitlines():
            match = re.match(r"^\s*\d+[.)]\s*(.+)$", line)
            if match:
                items.append(match.group(1).strip())
        return items

    actions = numbered(steps_text)
    results = numbered(expected_text)
    if not actions:
        if not (steps_text or "").strip():
            return []
        return [
            {
                "action": steps_text.strip(),
                "data": "",
                "result": expected_text.strip(),
            }
        ]
    return [
        {
            "action": action,
            "data": "",
            "result": results[index] if index < len(results) else "",
        }
        for index, action in enumerate(actions)
    ]


def story_ids(description: str) -> list[str]:
    return re.findall(r"WT-US-\d+", description or "")


# ---------------------------------------------------------------------------
# Jira REST
# ---------------------------------------------------------------------------
class Jira:
    def __init__(self, base: str, email: str, token: str, project: str):
        self.base = base.rstrip("/")
        self.project = project
        self.session = requests.Session()
        self.session.auth = (email, token)
        self.session.headers.update({"Accept": "application/json"})

    def _error(self, action: str, response: requests.Response) -> None:
        raise RuntimeError(
            f"{action} : HTTP {response.status_code} - {response.text[:500]}"
        )

    def create_issue(self, fields: dict) -> dict:
        response = self.session.post(
            f"{self.base}/rest/api/3/issue", json={"fields": fields}, timeout=60
        )
        if response.status_code not in (200, 201):
            self._error("Creation issue", response)
        data = response.json()
        return {"key": data["key"], "id": data["id"]}

    def update_description(self, key: str, text: str) -> None:
        response = self.session.put(
            f"{self.base}/rest/api/3/issue/{key}",
            json={"fields": {"description": adf(text)}},
            timeout=60,
        )
        if response.status_code not in (200, 204):
            self._error(f"Mise a jour description {key}", response)

    def existing(self, issue_type: str) -> dict[str, dict]:
        jql = f'project = "{self.project}" AND issuetype = "{issue_type}"'
        found: dict[str, dict] = {}
        token = None
        while True:
            body: dict = {
                "jql": jql,
                "maxResults": 100,
                "fields": ["summary"],
            }
            if token:
                body["nextPageToken"] = token
            response = self.session.post(
                f"{self.base}/rest/api/3/search/jql", json=body, timeout=60
            )
            if response.status_code != 200:
                self._error(f"Recherche {issue_type}", response)
            data = response.json()
            for issue in data.get("issues", []):
                summary = issue.get("fields", {}).get("summary", "")
                found[summary] = {"key": issue["key"], "id": issue["id"]}
            if data.get("isLast"):
                break
            token = data.get("nextPageToken")
            if not token:
                break
        return found

    def link_types(self) -> list[str]:
        response = self.session.get(
            f"{self.base}/rest/api/3/issueLinkType", timeout=30
        )
        if response.status_code != 200:
            return []
        return [item.get("name") for item in response.json().get("issueLinkTypes", [])]

    def link(self, link_type: str, first: str, second: str) -> bool:
        response = self.session.post(
            f"{self.base}/rest/api/3/issueLink",
            json={
                "type": {"name": link_type},
                "inwardIssue": {"key": first},
                "outwardIssue": {"key": second},
            },
            timeout=60,
        )
        if response.status_code in (200, 201, 204):
            return True
        # 400 : lien deja existant
        if response.status_code == 400 and "already exists" in response.text.lower():
            return False
        print(
            f"[ATTENTION] Lien {first} <-> {second} : HTTP "
            f"{response.status_code} - {response.text[:200]}"
        )
        return False


# ---------------------------------------------------------------------------
# Xray GraphQL
# ---------------------------------------------------------------------------
class Xray:
    def __init__(self, client_id: str, client_secret: str, base: str):
        self.base = base.rstrip("/")
        response = requests.post(
            f"{self.base}/api/v2/authenticate",
            json={"client_id": client_id, "client_secret": client_secret},
            timeout=30,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Authentification Xray : HTTP {response.status_code} - "
                f"{response.text[:300]}"
            )
        self.token = response.json()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def graphql(self, query: str, variables: dict | None = None) -> dict:
        response = requests.post(
            f"{self.base}/api/v2/graphql",
            headers=self.headers,
            json={"query": query, "variables": variables or {}},
            timeout=90,
        )
        try:
            payload = response.json()
        except ValueError:
            raise RuntimeError(f"Xray GraphQL : reponse non JSON ({response.status_code})")
        if "errors" in payload:
            raise RuntimeError(
                "Xray GraphQL : " + json.dumps(payload["errors"], ensure_ascii=False)[:800]
            )
        if response.status_code != 200:
            raise RuntimeError(
                f"Xray GraphQL : HTTP {response.status_code} - {response.text[:300]}"
            )
        return payload.get("data", {})

    def create_test(self, summary: str, steps: list[dict], jira_fields: dict) -> dict:
        query = """
        mutation CreateTest($steps: [CreateStepInput], $jira: JSON!) {
          createTest(testType: { name: "Manual" }, steps: $steps, jira: $jira) {
            test { issueId jira(fields: ["key"]) }
            warnings
          }
        }
        """
        data = self.graphql(
            query,
            {
                "steps": steps,
                "jira": {"fields": jira_fields},
            },
        )
        test = data["createTest"]["test"]
        return {
            "key": test["jira"]["key"],
            "id": test["issueId"],
            "warnings": data["createTest"].get("warnings", []),
        }

    def create_plan(self, test_ids: list[str], fields: dict) -> dict:
        query = """
        mutation CreatePlan($tests: [String], $jira: JSON!) {
          createTestPlan(testIssueIds: $tests, jira: $jira) {
            testPlan { issueId jira(fields: ["key"]) }
            warnings
          }
        }
        """
        data = self.graphql(
            query, {"tests": test_ids, "jira": {"fields": fields}}
        )
        plan = data["createTestPlan"]["testPlan"]
        return {"key": plan["jira"]["key"], "id": plan["issueId"]}

    def create_execution(self, test_ids: list[str], fields: dict) -> dict:
        query = """
        mutation CreateExecution($tests: [String], $envs: [String], $jira: JSON!) {
          createTestExecution(
            testIssueIds: $tests
            testEnvironments: $envs
            jira: $jira
          ) {
            testExecution { issueId jira(fields: ["key"]) }
            warnings
            createdTestEnvironments
          }
        }
        """
        data = self.graphql(
            query,
            {
                "tests": test_ids,
                "envs": [ENVIRONMENT],
                "jira": {"fields": fields},
            },
        )
        execution = data["createTestExecution"]["testExecution"]
        return {"key": execution["jira"]["key"], "id": execution["issueId"]}

    def import_results(self, execution_key: str, results: list[dict]) -> dict:
        response = requests.post(
            f"{self.base}/api/v2/import/execution",
            headers=self.headers,
            json={"testExecutionKey": execution_key, "tests": results},
            timeout=120,
        )
        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Import resultats : HTTP {response.status_code} - "
                f"{response.text[:500]}"
            )
        return response.json()


# ---------------------------------------------------------------------------
# Phases
# ---------------------------------------------------------------------------
def create_meta(jira: Jira, limit: int, dry_run: bool) -> dict[str, dict]:
    created: dict[str, dict] = {}
    stories = read_csv("WebTours_UserStories.csv")
    bugs = read_csv("WebTours_Bugs.csv")
    if limit:
        stories = stories[:limit]
        bugs = bugs[:limit]

    for issue_type, rows in (("Story", stories), ("Bug", bugs)):
        existing = jira.existing(issue_type)
        for row in rows:
            summary = row["Summary"]
            if summary in existing:
                created[summary] = existing[summary]
                print(f"[SKIP] {issue_type} deja present : {summary}")
                continue
            if issue_type == "Story":
                description = (
                    f"{row['Description']}\n\n"
                    f"Critères d'acceptation : {row.get('Acceptance Criteria', '')}"
                )
            else:
                description = (
                    f"{row['Description']}\n\n"
                    f"Résultat attendu : {row.get('Expected Result', '')}\n"
                    f"Résultat obtenu : {row.get('Actual Result', '')}"
                )
            fields = {
                "project": {"key": jira.project},
                "issuetype": {"name": issue_type},
                "summary": summary,
                "description": adf(description),
                "labels": labels(row.get("Labels", "")),
                "priority": priority(row.get("Priority", "")),
            }
            if dry_run:
                print(f"[DRY] {issue_type} : {summary}")
                continue
            issue = jira.create_issue(fields)
            created[summary] = issue
            print(f"[OK] {issue_type} {issue['key']} : {summary}")
    return created


def create_tests(jira: Jira, xray: Xray, limit: int, dry_run: bool) -> dict[str, dict]:
    rows = read_csv("WebTours_Xray_Import.csv")
    if limit:
        rows = rows[:limit]
    existing = jira.existing("Test")
    created: dict[str, dict] = {}

    for row in rows:
        summary = row["Summary"]
        if summary in existing:
            created[summary] = existing[summary]
            print(f"[SKIP] Test deja present : {summary}")
            continue
        steps = parse_steps(row.get("Steps", ""), row.get("Expected Result", ""))
        description = (
            f"{row.get('Description', '')}\n\n"
            f"Précondition :\n{row.get('Precondition', '')}\n\n"
            f"Résultat attendu :\n{row.get('Expected Result', '')}"
        )
        jira_fields = {
            "project": {"key": jira.project},
            "summary": summary,
            "labels": labels(row.get("Labels", "")),
            "priority": priority(row.get("Priority", "")),
        }
        if dry_run:
            print(f"[DRY] Test : {summary} ({len(steps)} etapes)")
            continue
        test = xray.create_test(summary, steps, jira_fields)
        jira.update_description(test["key"], description)
        created[summary] = {"key": test["key"], "id": test["id"]}
        warning = f" | warnings: {test['warnings']}" if test.get("warnings") else ""
        print(
            f"[OK] Test {test['key']} : {summary} "
            f"({len(steps)} etapes){warning}"
        )
    return created


def create_execution_phase(
    jira: Jira,
    xray: Xray,
    test_map: dict[str, dict],
    meta_map: dict[str, dict],
    dry_run: bool,
) -> None:
    test_ids = [item["id"] for item in test_map.values()]
    if not test_ids:
        print("[ERREUR] Aucun test disponible pour l'execution.")
        return

    plans = jira.existing("Test Plan")
    plan = plans.get(PLAN_SUMMARY)
    if plan:
        print(f"[SKIP] Test Plan deja present : {plan['key']}")
    elif dry_run:
        print(f"[DRY] Test Plan : {PLAN_SUMMARY}")
        plan = None
    else:
        plan = xray.create_plan(
            test_ids,
            {
                "project": {"key": jira.project},
                "summary": PLAN_SUMMARY,
                "description": "Campagne manuelle + automatique du mini-projet WebTours.",
            },
        )
        print(f"[OK] Test Plan {plan['key']} : {PLAN_SUMMARY}")

    executions = jira.existing("Test Execution")
    execution = executions.get(EXEC_SUMMARY)
    if execution:
        print(f"[SKIP] Test Execution deja presente : {execution['key']}")
    elif dry_run:
        print(f"[DRY] Test Execution : {EXEC_SUMMARY}")
        execution = None
    else:
        execution = xray.create_execution(
            test_ids,
            {
                "project": {"key": jira.project},
                "summary": EXEC_SUMMARY,
                "description": "Execution des 36 tests manuels WebTours (Sprint 1).",
            },
        )
        print(f"[OK] Test Execution {execution['key']} : {EXEC_SUMMARY}")

    if dry_run or not execution:
        return

    results_rows = read_csv("WebTours_Resultats_Execution.csv")
    results = []
    for row in results_rows:
        test = test_map.get(
            next(
                (
                    summary
                    for summary in test_map
                    if summary.startswith(row["Test ID"] + " ")
                    or summary.startswith(row["Test ID"] + " –")
                ),
                "",
            )
        )
        if not test:
            print(f"[ATTENTION] Test introuvable pour {row['Test ID']}")
            continue
        results.append(
            {
                "testKey": test["key"],
                "status": "PASSED" if row["Statut"] == "PASS" else "FAILED",
                "comment": (
                    f"Statut manuel : {row['Statut']}"
                    + (f" | Anomalie : {row['Bug lié']}" if row.get("Bug lié") else "")
                ),
            }
        )
    imported = xray.import_results(execution["key"], results)
    print(
        f"[OK] Resultats importes dans {execution['key']} : "
        f"{len(results)} tests ({imported})"
    )

    # Liens bug -> test
    bug_keys = {
        summary.split(" – ")[0]: item["key"]
        for summary, item in meta_map.items()
        if summary.startswith("BUG-")
    }
    link_types = jira.link_types()
    link_type = "Relates" if "Relates" in link_types else (link_types[0] if link_types else "Relates")
    linked = 0
    for row in results_rows:
        bug_id = row.get("Bug lié", "").strip()
        if not bug_id or bug_id not in bug_keys:
            continue
        summary = next(
            (
                item
                for item in test_map
                if item.startswith(row["Test ID"] + " ")
                or item.startswith(row["Test ID"] + " –")
            ),
            None,
        )
        if not summary:
            continue
        if jira.link(link_type, bug_keys[bug_id], test_map[summary]["key"]):
            linked += 1
    print(f"[OK] Liens bug/test crees : {linked}")

    # Liens test -> user story (les identifiants sont dans la description CSV)
    descriptions = {
        row["Summary"]: row.get("Description", "")
        for row in read_csv("WebTours_Xray_Import.csv")
    }
    story_keys = {
        summary.split(" – ")[0]: item["key"]
        for summary, item in meta_map.items()
        if summary.startswith("WT-US-")
    }
    story_links = 0
    for summary, test in test_map.items():
        for story_id in story_ids(descriptions.get(summary, "")):
            if story_id in story_keys:
                if jira.link(link_type, story_keys[story_id], test["key"]):
                    story_links += 1
    print(f"[OK] Liens test/story crees : {story_links}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["meta", "tests", "execution", "all"], default="all")
    parser.add_argument("--limit", type=int, default=0, help="Limite par categorie (mode pilote)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_env_file()
    base = os.getenv("JIRA_BASE_URL", "").rstrip("/")
    email = os.getenv("JIRA_EMAIL", "")
    token = os.getenv("JIRA_API_TOKEN", "")
    project = os.getenv("JIRA_PROJECT_KEY", "WTQA")
    client_id = os.getenv("XRAY_CLIENT_ID", "")
    client_secret = os.getenv("XRAY_CLIENT_SECRET", "")
    xray_base = os.getenv("XRAY_BASE_URL", "https://xray.cloud.getxray.app")

    if not (base and email and token):
        print("[ERREUR] Identifiants Jira incomplets.")
        return 2

    jira = Jira(base, email, token, project)
    meta_map: dict[str, dict] = {}
    test_map: dict[str, dict] = {}

    if args.phase in ("meta", "all"):
        meta_map.update(create_meta(jira, args.limit, args.dry_run))

    if args.phase in ("tests", "all"):
        if not (client_id and client_secret):
            print("[ERREUR] Identifiants Xray incomplets.")
            return 2
        xray = Xray(client_id, client_secret, xray_base)
        test_map.update(create_tests(jira, xray, args.limit, args.dry_run))

    if args.phase == "execution":
        if not (client_id and client_secret):
            print("[ERREUR] Identifiants Xray incomplets.")
            return 2
        xray = Xray(client_id, client_secret, xray_base)
        # Recharge les tests existants pour l'execution.
        for summary, issue in jira.existing("Test").items():
            test_map[summary] = issue
        for summary, issue in jira.existing("Story").items():
            meta_map[summary] = issue
        for summary, issue in jira.existing("Bug").items():
            meta_map[summary] = issue
        create_execution_phase(jira, xray, test_map, meta_map, args.dry_run)

    if args.phase == "all" and not args.dry_run:
        xray = Xray(client_id, client_secret, xray_base)
        create_execution_phase(jira, xray, test_map, meta_map, False)

    print("\nTermine.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as exc:
        print(f"[ERREUR] {exc}")
        sys.exit(1)
