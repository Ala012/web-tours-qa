# -*- coding: utf-8 -*-
"""Genere le rapport d'execution local (CSV) a partir des fiches manuelles.

Sortie : jira-xray/WebTours_Resultats_Execution.csv
"""
from __future__ import annotations

import csv
import glob
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "tests-manuels"
OUTPUT = ROOT / "jira-xray" / "WebTours_Resultats_Execution.csv"


def parse_sheet(path: str) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    test_id = os.path.splitext(os.path.basename(path))[0]

    title = re.search(
        r"^#\s+" + re.escape(test_id) + r"\s*[\u2013-]\s*(.+)$", text, re.M
    ).group(1).strip()
    module = re.search(r"\| Module \| (.+?) \|", text).group(1).strip()
    test_type = re.search(r"\| Type \| (.+?) \|", text).group(1).strip()
    automated = re.search(r"\| Test automatisé \| `(.+?)` \|", text)

    status_match = re.search(r"^\*\*Statut : (.+?)\*\*(.*)$", text, re.M)
    status_raw = (status_match.group(1) + status_match.group(2)).strip()

    if status_raw.startswith("Passé"):
        status, bug = "PASS", ""
    else:
        status = "FAIL"
        bug_match = re.search(r"BUG-\d+", status_raw)
        bug = bug_match.group(0) if bug_match else ""

    return [
        test_id,
        module,
        test_type,
        title,
        status,
        bug,
        automated.group(1) if automated else "",
        f"docs/04_Bugs_Detectes.md#{bug.lower()}" if bug else "",
    ]


def main() -> None:
    rows = [
        parse_sheet(path)
        for path in sorted(glob.glob(str(TESTS_DIR / "**" / "*.md"), recursive=True))
    ]
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_ALL)
        writer.writerow(
            [
                "Test ID",
                "Module",
                "Type",
                "Summary",
                "Statut",
                "Bug lié",
                "Test automatisé",
                "Preuve",
            ]
        )
        writer.writerows(rows)

    passed = sum(row[4] == "PASS" for row in rows)
    print(f"{OUTPUT.relative_to(ROOT)} : {len(rows)} lignes")
    print(f"PASS : {passed} | FAIL : {len(rows) - passed}")


if __name__ == "__main__":
    main()
