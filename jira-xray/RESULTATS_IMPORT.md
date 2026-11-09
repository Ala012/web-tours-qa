# Résultats de l'import Jira / Xray

Import réalisé par API dans le projet **`WTQA` – WEB_TOURS QA**
(<https://alaachaabouni09.atlassian.net/jira/software/projects/WTQA/boards>).

## 1. Tickets créés

| Élément | Quantité | Clés Jira |
|---|---|---|
| User stories | 6 | `WTQA-1` à `WTQA-6` (`WT-US-01` à `WT-US-06`) |
| Bugs | 15 | `WTQA-7` à `WTQA-21` (`BUG-01` à `BUG-15`) |
| Tests manuels | 9 | `WTQA-22` à `WTQA-30` |
| Test Plan | 1 | `WTQA-31` – Plan de test WebTours – Sprint 1 |
| Test Execution | 1 | `WTQA-32` – Exécution manuelle – Sprint 1 |

## 2. Campagne réduite : 3 tests réels par module

| Module | Tests |
|---|---|
| RSVA – Authentification | `RSVA-BT-03`, `RSVA-PT-01`, `RSVA-PT-03` |
| RSVF – Vols | `RSVF-ET-01`, `RSVF-PT-01`, `RSVF-PT-02` |
| RSVI – Itinéraire | `RSVI-PT-01`, `RSVI-PT-02`, `RSVI-PT-03` |

Ces scénarios sont des **échecs réels** : accès sans authentification, IDOR,
page blanche sur date vide, prix et flightID falsifiables, suppression sans
session.

## 3. Arborescence Xray

```text
WebTours
├─ RSVA - Authentification
│  ├─ BT - Boundary Testing        (1 test)
│  └─ PT - Permission Testing      (2 tests)
├─ RSVF - Flight
│  ├─ ET - Error Testing           (1 test)
│  └─ PT - Permission Testing      (2 tests)
└─ RSVI - Itinerary
   └─ PT - Permission Testing      (3 tests)
```

## 4. Exécution

| Statut | Nombre |
|---|---|
| PASSED | 0 |
| FAILED | 9 |
| **Total** | **9** |

Le Test Plan `WTQA-31` contient les **9 tests**.

## 5. Traçabilité

- **9 liens bug → test** : chaque test en échec est lié à son anomalie.
- **12 liens test → user story** : couverture des stories des modules.
- Type de lien Jira utilisé : `relates to` (aucun doublon constaté).

## 6. Vérification

```bat
cd /d "D:\web tours\Mini-Projet"
python scripts\jira_verify.py
```

Résultat attendu :

```text
Projet WTQA :
  - Story            : 6
  - Bug              : 15
  - Test             : 9
  - Test Plan        : 1
  - Test Execution   : 1

Test Execution : WTQA-32 - Exécution manuelle – Sprint 1
  Test runs : 9
  - FAILED       : 9
[OK] Statuts conformes : 9 FAILED (campagne réduite).

Test Plan : WTQA-31 - Plan de test WebTours – Sprint 1 | 9 tests

Tests Xray : 9 | avec etapes : 9 | sans etapes : 0
```

## 7. Scripts utilisés

| Script | Rôle |
|---|---|
| `scripts/check_jira_access.py` | Vérifie les identifiants Jira/Xray sans afficher les secrets |
| `scripts/jira_discover.py` | Liste les projets et types de tickets disponibles |
| `scripts/jira_create_project.py` | Crée le projet `WTQA` |
| `scripts/jira_xray_setup.py` | Ajoute `Test`, `Test Plan`, `Test Execution`, `Precondition` au projet |
| `scripts/jira_import.py` | Crée stories, bugs, tests, dossiers Xray, plan, exécution et liens |
| `scripts/jira_verify.py` | Vérifie les compteurs, statuts, étapes et dossiers |
| `scripts/jira_show_issue.py` | Affiche un ticket et ses étapes Xray |
| `scripts/jira_reduce_tests.py` | Diagnostic/suppression des tests (nécessite le droit *Delete Issues*) |

## 8. Relancer l'import

L'import est **idempotent** : un ticket dont le résumé existe déjà est réutilisé.

```bat
python scripts\jira_import.py --phase meta
python scripts\jira_import.py --phase tests
python scripts\jira_import.py --phase execution
```

Les identifiants sont lus dans `.env.local` (ignoré par Git). Ne jamais
commiter ce fichier ni coller les tokens dans un ticket ou une conversation.

## 9. Note sur la suppression des anciens tests

Le projet Jira est sur le **plan gratuit**, qui ne permet pas de modifier les
schémas de permissions ni de supprimer des tickets individuellement via l'API.
Pour repartir d'une base propre, le projet `WTQA` a été supprimé puis recréé,
puis les 6 stories, 15 bugs et 9 tests ont été réimportés. Les clés ci-dessus
sont celles du projet recréé.
