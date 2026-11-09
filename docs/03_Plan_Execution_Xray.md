# Plan d'exécution Xray – WebTours QA

## 1. Objectif

Organiser, exécuter et tracer les 36 tests manuels dans Jira/Xray, puis produire
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
├─ RSVA - Authentication
│  ├─ FT - Functional Testing      (3 tests)
│  ├─ ET - Error Testing           (3 tests)
│  ├─ BT - Boundary Testing        (3 tests)
│  └─ PT - Permission Testing      (3 tests)
├─ RSVF - Flight
│  ├─ FT - Functional Testing      (3 tests)
│  ├─ ET - Error Testing           (3 tests)
│  ├─ BT - Boundary Testing        (3 tests)
│  └─ PT - Permission Testing      (3 tests)
└─ RSVI - Itinerary
   ├─ FT - Functional Testing      (3 tests)
   ├─ ET - Error Testing           (3 tests)
   ├─ BT - Boundary Testing        (3 tests)
   └─ PT - Permission Testing      (3 tests)
```

> Si le champ `Folder` n'est pas mappé, les tests seront importés à la racine.
> Il suffit ensuite de les déplacer dans les dossiers (glisser-déposer).

### 4.3 Vérification

- 36 tickets de type **Test**.
- Chaque test possède ses préconditions, étapes et résultats attendus.
- Les labels contiennent `WebTours`, le module (`RSVA`/`RSVF`/`RSVI`), le type
  (`FT`/`ET`/`BT`/`PT`) et l'identifiant du test.

## 5. Création du Test Plan

1. **Xray → Test Plans → Create**.
2. Nom : **Plan de test WebTours – Sprint 1**.
3. Description : campagne manuelle + automatique.
4. Ajouter les 36 tests :
   - **Add Tests** → sélectionner le dossier `WebTours` ;
   - ou utiliser la recherche JQL : `project = WTQA AND issuetype = Test`.
5. Enregistrer.

## 6. Création du Test Execution

1. **Xray → Test Executions → Create**.
2. Nom : **Exécution manuelle – Sprint 1**.
3. Environnement : `Windows 10 – Chrome – WebTours local`.
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
| PASS | 20 | Parcours nominaux et validations existantes |
| FAIL | 16 | Anomalies BUG-01 à BUG-15 (certaines couvrent plusieurs tests) |
| TODO | 0 | Tous exécutés |
| BLOCKED | 0 | Aucun |

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

### 9.1 JQL utiles

```jql
project = WTQA AND issuetype = Test ORDER BY key ASC
project = WTQA AND issuetype = Test AND labels = PT
project = WTQA AND issuetype = Bug AND priority in (Critical, High)
project = WTQA AND issuetype = Test AND "Test Status" = FAIL
```

## 10. Définition de terminé

- [ ] 36 tests importés et rangés dans les bons dossiers.
- [ ] Test Plan créé et complété.
- [ ] Test Execution créé et exécuté à 100 %.
- [ ] 15 bugs créés et liés aux tests.
- [ ] Rapport d'exécution exporté.
- [ ] Couverture des 6 user stories vérifiée.
