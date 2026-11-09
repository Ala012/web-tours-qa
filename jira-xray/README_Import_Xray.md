# Import Jira / Xray – WebTours QA

> **État actuel : l'import a déjà été réalisé par API** dans le projet
> `WTQA` – WEB_TOURS QA (14 tests : 9 ciblés + 5 non-régression, 15 bugs, 6 stories, Test Plan `WTQA-31`,
> Test Execution `WTQA-32`). Voir `RESULTATS_IMPORT.md` et
> `README_API_Automatisation.md`.
> Ce document décrit la procédure **manuelle de repli**, utile pour rejouer
> l'import dans un autre projet Jira ou sans les identifiants API.

Ce dossier contient les fichiers prêts à importer dans Jira et Xray.

| Fichier | Contenu | Import |
|---|---|---|
| `WebTours_UserStories.csv` | 6 user stories | Jira → Import issues from CSV |
| `WebTours_Xray_Import.csv` | 14 tests manuels (9 FAIL + 5 PASS) | Xray → Test Case Importer |
| `WebTours_Bugs.csv` | 15 anomalies | Jira → Import issues from CSV |

---

## 1. Créer le projet Jira

1. Se connecter à <https://alaachaabouni09.atlassian.net/>.
2. **Projects → Create project**.
3. Choisir **Scrum** (ou Kanban).
4. Nom : **WebTours QA**.
5. Clé : `WTQA`.
6. Créer.

## 2. Installer Xray

1. **Apps → Explore more apps**.
2. Rechercher **Xray – Test Management for Jira**.
3. Installer (essai gratuit).
4. Vérifier la présence des types **Test**, **Test Plan**, **Test Execution**,
   **Precondition**.

## 3. Importer les user stories

1. **Issues → Import issues from CSV**.
2. Fichier : `WebTours_UserStories.csv`.
3. Projet : `WTQA`.
4. Mapper :

| CSV | Jira |
|---|---|
| Issue Type | Issue Type = **Story** |
| Summary | Summary |
| Description | Description |
| Priority | Priority |
| Labels | Labels |
| Acceptance Criteria | Description ou champ personnalisé |

5. Importer.

Résultat : `WT-US-01` à `WT-US-06`.

## 4. Importer les tests dans Xray

### 4.1 Méthode 1 – Test Case Importer (recommandée)

1. **Xray → Test Repository**.
2. **Create → Import → CSV**.
3. Fichier : `WebTours_Xray_Import.csv`.
4. Projet : `WTQA`.
5. Vérifier le mapping :

| Colonne CSV | Champ Xray |
|---|---|
| Issue Type | Test |
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
7. Vérifier les 14 tests et l'arborescence.

### 4.2 Méthode 2 – Import manuel

Si le champ `Folder` n'est pas disponible dans votre version de Xray :

1. Importer les tests à la racine.
2. Créer les dossiers dans **Test Repository** :
   - `WebTours/RSVA-Authentication/FT - Functional Testing`
   - `WebTours/RSVA-Authentication/ET - Error Testing`
   - `WebTours/RSVA-Authentication/BT - Boundary Testing`
   - `WebTours/RSVA-Authentication/PT - Permission Testing`
   - idem pour `RSVF-Flight` et `RSVI-Itinerary`.
3. Glisser-déposer les tests dans les dossiers.

### 4.3 Arborescence cible

```text
WebTours
├─ RSVA-Authentication
│  ├─ FT - Functional Testing      (RSVA-FT-01..03)
│  ├─ ET - Error Testing           (RSVA-ET-01..03)
│  ├─ BT - Boundary Testing        (RSVA-BT-01..03)
│  └─ PT - Permission Testing      (RSVA-PT-01..03)
├─ RSVF-Flight
│  ├─ FT - Functional Testing      (RSVF-FT-01..03)
│  ├─ ET - Error Testing           (RSVF-ET-01..03)
│  ├─ BT - Boundary Testing        (RSVF-BT-01..03)
│  └─ PT - Permission Testing      (RSVF-PT-01..03)
└─ RSVI-Itinerary
   ├─ FT - Functional Testing      (RSVI-FT-01..03)
   ├─ ET - Error Testing           (RSVI-ET-01..03)
   ├─ BT - Boundary Testing        (RSVI-BT-01..03)
   └─ PT - Permission Testing      (RSVI-PT-01..03)
```

## 5. Créer le Test Plan

1. **Xray → Test Plans → Create**.
2. Nom : **Plan de test WebTours – Sprint 1**.
3. Description : campagne manuelle + automatisée.
4. **Add Tests** :
   - sélectionner le dossier `WebTours` ;
   - ou JQL : `project = WTQA AND issuetype = Test`.
5. Enregistrer.

## 6. Créer le Test Execution

1. **Xray → Test Executions → Create**.
2. Nom : **Exécution manuelle – Sprint 1**.
3. Environnement : `Windows 10 – Chrome – WebTours local`.
4. Ajouter les tests du plan.
5. Démarrer.

## 7. Exécuter et tracer

Pour chaque test :

1. Ouvrir le test.
2. Exécuter les étapes dans le navigateur.
3. Mettre le statut **PASS** ou **FAIL**.
4. En cas de FAIL, créer un bug et le lier au test.
5. Ajouter une capture dans le commentaire.

Résultats attendus :

| Statut | Nombre |
|---|---|
| PASS | 20 |
| FAIL | 16 |
| TODO | 0 |
| BLOCKED | 0 |

## 8. Importer les bugs

1. **Issues → Import issues from CSV**.
2. Fichier : `WebTours_Bugs.csv`.
3. Projet : `WTQA`.
4. Mapper `Issue Type` → **Bug**.
5. Importer.
6. Lier chaque bug au test Xray correspondant.

## 9. Lier les tests aux user stories

Deux méthodes :

### Méthode A – Depuis la story

1. Ouvrir `WT-US-03`.
2. Section **Tests** (Xray) → **Add Tests**.
3. Sélectionner les tests `RSVF-*`.

### Méthode B – Depuis le test

1. Ouvrir un test.
2. Champ **Requirements** / **User Story**.
3. Ajouter la story.

Vérifier ensuite la **Requirement Coverage** dans Xray.

## 10. JQL utiles

```jql
project = WTQA AND issuetype = Test ORDER BY key ASC
project = WTQA AND issuetype = Test AND labels = PT
project = WTQA AND issuetype = Test AND labels = RSVF
project = WTQA AND issuetype = Bug AND priority in (Critical, High)
project = WTQA AND issuetype = Test AND "Test Status" = FAIL
```

## 11. Dépannage

| Problème | Solution |
|---|---|
| Colonne `Folder` non reconnue | Importer à la racine puis déplacer les tests manuellement. |
| `Steps` vides | Vérifier que le champ multiligne est bien mappé ; ouvrir le CSV dans un éditeur UTF-8. |
| Types `Test` absents | Vérifier que Xray est installé et activé sur le projet. |
| User stories non liées | Utiliser la section **Tests** de la story ou le champ **Requirements** du test. |
| Caractères accentués | Importer en UTF-8 (le CSV contient un BOM UTF-8). |
| Statuts Xray différents | Configurer les statuts de test dans **Xray → Settings → Test Statuses**. |
