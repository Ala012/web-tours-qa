# Plan d'exécution Xray – WebTours QA

## 1. Objectif

Organiser, exécuter et tracer les 14 tests manuels dans Jira/Xray, puis produire
un rapport d'exécution et les anomalies associées.

## 2. Préparation du projet Jira

1. Se connecter à <https://alaachaabouni09.atlassian.net/>.
2. Créer un projet **WebTours QA** (clé `WTQA`).
3. Ajouter l'application **Xray** (Essai gratuit ou licence).
4. Vérifier que les types de tickets **Test**, **Test Plan**, **Test Execution**
   et **Precondition** sont disponibles.

## 3. Import des user stories

1. **Issues → Import issues from CSV**.
2. Fichier : `jira-xray/WebTours_UserStories.csv`.
3. Projet : `WTQA`.
4. Mapper `Issue Type` → Story, puis les autres colonnes.
5. Importer.

Résultat attendu : 6 stories `WT-US-01` à `WT-US-06`.

## 4. Import des tests dans Xray

### 4.1 Méthode recommandée : Test Case Importer

1. Ouvrir **Xray → Test Repository**.
2. Cliquer sur **Create → Import** (ou **Test Case Importer**).
3. Choisir **CSV**.
4. Fichier : `jira-xray/WebTours_Xray_Import.csv`.
5. Vérifier le mapping :

| Colonne CSV | Champ Xray |
|---|---|
| Issue Type | Type de ticket = **Test** |
| Summary | Summary |
| Description | Description |
| Test Type | Manual |
| Precondition | Precondition |
| Steps | Steps |
| Expected Result | Expected Result |
| Priority | Priority |
| Labels | Labels |
| Folder | Test Repository Folder |

6. Lancer l'import.

### 4.2 Arborescence attendue dans le Test Repository

```text
WebTours
├─ RSVA - Authentification
│  ├─ FT - Functional Testing      (1 test)
│  ├─ ET - Error Testing           (1 test)
│  ├─ BT - Boundary Testing        (1 test)
│  └─ PT - Permission Testing      (2 tests)
├─ RSVF - Flight
│  ├─ FT - Functional Testing      (2 tests)
│  ├─ ET - Error Testing           (1 test)
│  └─ PT - Permission Testing      (2 tests)
└─ RSVI - Itinerary
   ├─ FT - Functional Testing      (1 test)
   └─ PT - Permission Testing      (3 tests)
```

> Si le champ `Folder` n'est pas mappé, les tests seront importés à la racine.
> Il suffit ensuite de les déplacer dans les dossiers (glisser-déposer).

### 4.3 Vérification

- 14 tickets de type **Test**.
- Chaque test possède ses préconditions, étapes et résultats attendus.
- Les labels contiennent `WebTours`, le module (`RSVA`/`RSVF`/`RSVI`), le type
  (`FT`/`ET`/`BT`/`PT`) et l'identifiant du test.

## 5. Création du Test Plan

1. **Xray → Test Plans → Create**.
2. Nom : **Plan de test WebTours – Sprint 1**.
3. Description : campagne manuelle + automatique.
4. Ajouter les 14 tests :
   - **Add Tests** → sélectionner le dossier `WebTours` ;
   - ou utiliser la recherche JQL : `project = WTQA AND issuetype = Test`.
5. Enregistrer.

## 6. Création du Test Execution

1. **Xray → Test Executions → Create**.
2. Nom : **Exécution manuelle – Sprint 1**.
3. Environnement : `Windows11-Chrome-WebTours-local`.
4. Ajouter les tests du Test Plan.
5. Démarrer l'exécution.

## 7. Exécution des tests

Pour chaque test :

1. Ouvrir le ticket.
2. Lire les préconditions et les étapes.
3. Exécuter le scénario dans le navigateur.
4. Mettre le statut :
   - **PASS** : résultat conforme ;
   - **FAIL** : résultat non conforme → créer un bug ;
   - **TODO** : non exécuté ;
   - **BLOCKED** : impossible à exécuter.
5. Ajouter un commentaire avec la preuve (capture d'écran, message d'erreur,
   extrait de log).
6. Pour un FAIL, lier le bug au test (champ **Defects**).

### 7.1 Résultats attendus

| Statut | Nombre | Commentaire |
|---|---|---|
| PASS | 5 | Non-régression : login, erreur de mot de passe, recherches, itinéraire |
| FAIL | 9 | Scénarios réels en échec (sécurité et crash) |
| TODO | 0 | Tous exécutés |
| BLOCKED | 0 | Aucun |

### 7.2 Import automatisé réalisé

L'exécution a été créée et alimentée par API dans le projet **`WTQA` – WEB_TOURS QA**
(<https://alaachaabouni09.atlassian.net/jira/software/projects/WTQA/boards>).

| Élément | Quantité | Clé(s) Jira |
|---|---|---|
| User stories | 6 | `WTQA-1` à `WTQA-6` |
| Bugs | 15 | `WTQA-7` à `WTQA-21` |
| Tests manuels | 14 | `WTQA-22` à `WTQA-37` |
| Test Plan | 1 | `WTQA-31` – 14 tests |
| Test Execution | 1 | `WTQA-32` – 5 PASSED / 9 FAILED |

- Environnement d'exécution : `Windows11-Chrome-WebTours-local`.
- Les 14 statuts Xray sont **5 PASSED** et **9 FAILED**.
- Traçabilité : 9 liens **bug → test** et 19 liens **test → user story**.
- Les 14 tests possèdent leurs étapes Xray (0 test sans étape).
- L'exécution `WTQA-32` est **associée au plan `WTQA-31`** (panneau
  *Test Executions* du plan alimenté).
- Arborescence Test Repository : `WebTours > module > type`.

Vérification reproductible :

```bat
cd /d "D:\web tours\Mini-Projet"
python scripts\jira_verify.py
```

Le détail des clés et la sortie de vérification sont dans
`jira-xray/RESULTATS_IMPORT.md`.

## 8. Création des anomalies

Deux options :

### Option A – Import CSV

1. **Issues → Import issues from CSV**.
2. Fichier : `jira-xray/WebTours_Bugs.csv`.
3. Projet : `WTQA`.
4. Mapper `Issue Type` → **Bug**, `Summary`, `Priority`, `Labels`,
   `Description`, `Expected Result`, `Actual Result`.
5. Importer, puis lier chaque bug au test concerné.

### Option B – Saisie manuelle

Créer un ticket **Bug** pour chaque ligne du tableau de
`docs/04_Bugs_Detectes.md` avec :

- **Summary** : `BUG-xx – titre`
- **Priority** : Critical/High/Medium
- **Labels** : `WebTours`, module, `BUG`
- **Description** : préconditions, étapes, résultat attendu, résultat obtenu,
  environnement, preuve.
- **Linked issues** : lien vers le test Xray.

## 9. Rapport d'exécution

Xray génère automatiquement :

- le **Test Execution Report** (statuts, durée, defects) ;
- le **Test Plan Report** (couverture, progression) ;
- le **Requirement Coverage** (couverture des user stories).

Exporter le rapport en PDF/CSV et l'archiver dans le dépôt ou dans Jira.

Un export local des statuts est disponible :
`jira-xray/WebTours_Resultats_Execution.csv` (14 lignes, 5 PASS / 9 FAIL),
régénérable avec `python scripts/export_results.py`.

### 9.1 JQL utiles

```jql
project = WTQA AND issuetype = Test ORDER BY key ASC
project = WTQA AND issuetype = Test AND labels = PT
project = WTQA AND issuetype = Bug AND priority in (Critical, High)
project = WTQA AND issuetype = Test AND "Test Status" = FAIL
```

## 10. Définition de terminé

- [ ] 14 tests importés et rangés dans les bons dossiers.
- [ ] Test Plan créé et complété.
- [ ] Test Execution créé et exécuté à 100 %.
- [ ] 15 bugs créés et liés aux tests.
- [ ] Rapport d'exécution exporté.
- [ ] Couverture des 6 user stories vérifiée.
