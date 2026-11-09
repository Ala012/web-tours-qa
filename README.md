# Mini-Projet QA – Web Tours

Projet de test manuel et automatisé d'une application web de réservation de vols :
**Web Tours** (`http://127.0.0.1:1080/WebTours/index.htm`).

Ce dépôt contient :

- le **plan de test** et les **user stories** ;
- **36 cas de test manuels** organisés par module et par type :
  - `RSVA` – Authentification
  - `RSVF` – Vols
  - `RSVI` – Itinéraire
  - `FT` – Functional Testing, `ET` – Error Testing, `BT` – Boundary Testing, `PT` – Permission Testing ;
- les fichiers d'**import Jira / Xray** (tests, user stories, bugs) ;
- une suite de **tests automatisés Selenium + pytest** ;
- un **Jenkinsfile** pour lancer la suite en CI ;
- le **rapport de bugs** avec les preuves.

---

## 1. Arborescence

```text
Mini-Projet/
├─ README.md
├─ .gitignore
├─ docs/
│  ├─ 01_Plan_de_Test.md
│  ├─ 02_User_Stories_JIRA.md
│  ├─ 03_Plan_Execution_Xray.md
│  ├─ 04_Bugs_Detectes.md
│  ├─ 05_Installation_WebTours.md
│  ├─ 06_Automatisation_Selenium.md
│  └─ evidence/                  # captures des anomalies
├─ tests-manuels/
│  ├─ RSVA-Authentication/
│  │  ├─ FT - Functional Testing/RSVA-FT-01.md ...
│  │  ├─ ET - Error Testing/...
│  │  ├─ BT - Boundary Testing/...
│  │  └─ PT - Permission Testing/...
│  ├─ RSVF-Flight/...
│  └─ RSVI-Itinerary/...
├─ jira-xray/
│  ├─ WebTours_Xray_Import.csv   # import des 36 tests dans Xray
│  ├─ WebTours_UserStories.csv   # import des user stories dans Jira
│  ├─ WebTours_Bugs.csv          # import des anomalies dans Jira
│  └─ README_Import_Xray.md
├─ automation/
│  ├─ requirements.txt
│  ├─ pytest.ini
│  ├─ conftest.py
│  ├─ pages/                     # Page Object Model
│  ├─ tests/                     # tests Selenium + API
│  ├─ utils/                     # client HTTP WebTours
│  ├─ run_tests.bat
│  └─ reports/                   # rapport HTML généré
├─ scripts/
│  ├─ generate_test_cases.py     # régénère les fiches + CSV
│  ├─ start_webtours.bat
│  ├─ stop_webtours.bat
│  └─ capture_evidence.py        # captures d'écran des bugs
└─ ci/
   ├─ Jenkinsfile
   └─ README_Jenkins.md
```

---

## 2. Prérequis

| Outil | Version / remarque |
|---|---|
| Java | **Java 8** (nécessaire au serveur WebTours) |
| Perl | **Strawberry Perl 5.10.1.0** |
| WebTours | installé dans `D:\web tours\WebTours` |
| Python | 3.10+ (testé avec 3.12) |
| Navigateur | Google Chrome ou Microsoft Edge |
| Selenium | 4.x (Selenium Manager télécharge le driver automatiquement) |
| Jenkins | optionnel, pour la CI |

> Le serveur WebTours doit être lancé **avant** les tests.
> Voir `docs/05_Installation_WebTours.md` pour l'installation et le dépannage.

---

## 3. Démarrage rapide

### 3.1 Lancer WebTours

```bat
cd /d "D:\web tours\WebTours"
StartServer.bat
```

Puis ouvrir : <http://127.0.0.1:1080/WebTours/index.htm>

Comptes de démonstration :

| Utilisateur | Mot de passe |
|---|---|
| `jojo` | `bean` |
| `admin` | `admin` |

### 3.2 Lancer les tests automatisés

```bat
cd /d "D:\web tours\Mini-Projet\automation"
python -m pip install -r requirements.txt
python -m pytest
```

Le rapport HTML est généré dans `automation/reports/report.html`.

Pour ne lancer qu'un module :

```bat
python -m pytest tests/test_rsvf_flight.py -v
```

### 3.3 Régénérer les fiches et les CSV

```bat
cd /d "D:\web tours\Mini-Projet"
python scripts/generate_test_cases.py
```

---

## 4. Test manuel et Jira / Xray

1. Créer le projet Jira **WebTours QA** (clé suggérée : `WTQA`).
2. Importer `jira-xray/WebTours_UserStories.csv` (issues de type **Story**).
3. Installer **Xray** sur le projet.
4. Importer `jira-xray/WebTours_Xray_Import.csv` via **Xray → Test Case Importer**.
5. Créer le **Test Plan** « Plan de test WebTours – Sprint 1 » et y ajouter les 36 tests.
6. Créer le **Test Execution** « Exécution manuelle – Sprint 1 ».
7. Exécuter les tests, passer les statuts à **PASS / FAIL / TODO**.
8. Créer les anomalies à partir de `jira-xray/WebTours_Bugs.csv`.

Le mode opératoire détaillé est dans `jira-xray/README_Import_Xray.md` et
`docs/03_Plan_Execution_Xray.md`.

---

## 5. Automatisation

La suite couvre les trois modules avec :

- **Selenium WebDriver** pour les parcours UI (frames, formulaires, navigation) ;
- **requests + BeautifulSoup** pour les tests de sécurité et les requêtes POST
  forgées (prix, flightID, cookie, accès direct) ;
- **pytest** pour l'organisation, les fixtures et les rapports.

Les tests marqués `xfail` correspondent à des **bugs connus et documentés** :
ils échouent volontairement pour prouver l'anomalie sans casser la CI.

```text
automation/tests/
├─ test_rsva_authentication.py   # 12 tests
├─ test_rsvf_flight.py           # 12 tests
├─ test_rsvi_itinerary.py        # 12 tests
└─ conftest.py
```

Voir `docs/06_Automatisation_Selenium.md`.

---

## 6. Jenkins

Le fichier `ci/Jenkinsfile` :

1. installe les dépendances Python ;
2. démarre WebTours ;
3. lance `pytest` ;
4. publie le rapport HTML et archive les résultats ;
5. arrête le serveur.

Créer un job **Pipeline** dans Jenkins, pointer le dépôt Git et le chemin
`ci/Jenkinsfile`. Voir la section Jenkins de
`docs/06_Automatisation_Selenium.md` et `ci/README_Jenkins.md`.

---

## 7. Versionnement Git

Le dépôt est initialisé sur la branche `main`. Le fichier `.gitignore` exclut
les caches Python, les rapports générés et les drivers de navigateur.

```bat
cd /d "D:\web tours\Mini-Projet"
git status
git add .
git commit -m "Mini-projet QA WebTours : tests manuels, Xray, Selenium et CI"
```

Pour publier le dépôt sur GitHub / GitLab :

```bat
git remote add origin <URL_DU_DEPOT>
git push -u origin main
```

Les rapports (`automation/reports/`) sont régénérés à chaque exécution et ne
sont donc pas versionnés ; Jenkins les archive comme artefacts.

---

## 8. Synthèse des anomalies

15 anomalies ont été identifiées, dont 6 critiques :

| ID | Anomalie | Sévérité |
|---|---|---|
| BUG-01 | Recherche de vols accessible sans login | Critical |
| BUG-03 | Page admin accessible sans authentification | Critical |
| BUG-04 | IDOR : itinéraire d'un autre utilisateur via cookie forgé | Critical |
| BUG-09 | Prix manipulable dans le POST | Critical |
| BUG-10 | flightID falsifié / achat direct | Critical |
| BUG-13 | Mots de passe stockés en clair | Critical |
| BUG-02, 05, 06, 07, 08, 12, 14 | Voir le rapport | High |
| BUG-11, 15 | Voir le rapport | Medium |

Détails, preuves et scénarios de reproduction : `docs/04_Bugs_Detectes.md`.

---

## 9. Remarque sur la configuration WebTours

Le dossier d'installation contient un espace (`D:\web tours\WebTours`).
Apache 2.2 interprète mal les chemins relatifs `DocumentRoot "htdocs"` et
`<Directory "htdocs">` dans ce cas (erreur **403 Forbidden**).
Le fichier `WebTours/conf/httpd.conf` a donc été corrigé avec des chemins
absolus :

```apache
ServerName localhost:1080
DocumentRoot "D:/web tours/WebTours/htdocs"
<Directory "D:/web tours/WebTours/htdocs">
ScriptAlias /cgi-bin/ "D:/web tours/WebTours/cgi-bin/"
<Directory "D:/web tours/WebTours/cgi-bin">
```

Cette modification est documentée dans `docs/05_Installation_WebTours.md`.

---

## 10. Auteur / contexte

Mini-projet de test logiciel – application **Web Tours**.
Tests manuels (Jira/Xray) + tests automatisés (Selenium/pytest) + CI Jenkins.
