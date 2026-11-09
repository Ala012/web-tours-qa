# Résultats de l'import Jira / Xray

Import réalisé par API dans le projet **`WTQA` – WEB_TOURS QA**
(<https://alaachaabouni09.atlassian.net/jira/software/projects/WTQA/boards>).

## 1. Tickets créés

| Élément | Quantité | Clés Jira |
|---|---|---|
| User stories | 6 | `WTQA-2` à `WTQA-7` (`WT-US-01` à `WT-US-06`) |
| Bugs | 15 | `WTQA-8` à `WTQA-22` (`BUG-01` à `BUG-15`) |
| Tests manuels | 36 | `WTQA-1`, puis `WTQA-23` à `WTQA-57` |
| Test Plan | 1 | `WTQA-58` – Plan de test WebTours – Sprint 1 |
| Test Execution | 1 | `WTQA-59` – Exécution manuelle – Sprint 1 |

## 2. Contenu des tests

- Type : **Manual**.
- Chaque test possède ses **étapes** (action + résultat attendu) dans Xray.
- Précondition, résultat attendu et test automatisé associé sont dans la
  description Jira.
- Priorité et labels (`WebTours`, module, type, identifiant) sont renseignés.

## 3. Exécution

| Statut | Nombre |
|---|---|
| PASSED | 20 |
| FAILED | 16 |
| **Total** | **36** |

Le Test Plan `WTQA-58` contient les **36 tests**.

## 4. Traçabilité

- **16 liens bug → test** : chaque test en échec est lié à son anomalie.
- **48 liens test → user story** : couverture des 6 user stories.
- Type de lien Jira utilisé : `relates to` (aucun doublon constaté).

## 5. Vérification

```bat
cd /d "D:\web tours\Mini-Projet"
python scripts\jira_verify.py
```

Résultat attendu :

```text
Projet WTQA :
  - Story            : 6
  - Bug              : 15
  - Test             : 36
  - Test Plan        : 1
  - Test Execution   : 1

Test Execution : WTQA-59 - Exécution manuelle – Sprint 1
  Test runs : 36
  - FAILED       : 16
  - PASSED       : 20
[OK] Statuts conformes : 20 PASS / 16 FAIL.

Test Plan : WTQA-58 - Plan de test WebTours – Sprint 1 | 36 tests

Tests Xray : 36 | avec etapes : 36 | sans etapes : 0
```

## 6. Scripts utilisés

| Script | Rôle |
|---|---|
| `scripts/check_jira_access.py` | Vérifie les identifiants Jira/Xray sans afficher les secrets |
| `scripts/jira_discover.py` | Liste les projets et types de tickets disponibles |
| `scripts/jira_create_project.py` | Crée le projet `WTQA` |
| `scripts/jira_xray_setup.py` | Ajoute `Test`, `Test Plan`, `Test Execution`, `Precondition` au projet |
| `scripts/jira_import.py` | Crée stories, bugs, tests, plan, exécution et liens |
| `scripts/jira_verify.py` | Vérifie les compteurs, statuts et étapes |
| `scripts/jira_show_issue.py` | Affiche un ticket et ses étapes Xray |

## 7. Relancer l'import

L'import est **idempotent** : un ticket dont le résumé existe déjà est réutilisé.

```bat
python scripts\jira_import.py --phase meta
python scripts\jira_import.py --phase tests
python scripts\jira_import.py --phase execution
```

Les identifiants sont lus dans `.env.local` (ignoré par Git). Ne jamais
commiter ce fichier ni coller les tokens dans un ticket ou une conversation.
