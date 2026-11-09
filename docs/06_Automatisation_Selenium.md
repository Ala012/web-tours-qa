# Automatisation Selenium + pytest

## 1. Objectif

Automatiser les parcours critiques de WebTours et les tests de sécurité,
exécuter la suite localement et en intégration continue (Jenkins), et produire
un rapport HTML exploitable.

## 2. Architecture

```text
automation/
├─ conftest.py              # fixtures : driver, login, utilisateurs, API
├─ pytest.ini               # configuration, markers, rapport HTML
├─ requirements.txt
├─ pages/                   # Page Object Model
│  ├─ base_page.py          # navigation dans les frames
│  ├─ login_page.py         # login / inscription
│  ├─ navbar.py             # menu Flights / Itinerary / Home / SignOff
│  ├─ flight_page.py        # recherche, sélection, paiement
│  └─ itinerary_page.py     # affichage / suppression
├─ tests/
│  ├─ test_rsva_authentication.py   # 5 tests
│  ├─ test_rsvf_flight.py           # 4 tests
│  └─ test_rsvi_itinerary.py        # 4 tests
├─ utils/
│  └─ webtours_api.py       # client requests pour les POST forgés
└─ reports/
   └─ report.html           # rapport généré
```

### 2.1 Selenium vs requests

| Besoin | Outil |
|---|---|
| Parcours utilisateur, frames, formulaires | Selenium WebDriver |
| Requêtes POST forgées (prix, flightID, buyFlights) | `requests` |
| Cookie forgé (IDOR), accès direct sans session | `requests` |
| Création rapide d'un compte de test | `requests` |
| Assertions visuelles / textuelles | Selenium + `body.text` |

### 2.2 Gestion des frames

WebTours utilise des frames imbriquées :

```text
index.htm
├─ header
└─ body (welcome.pl)
   ├─ navbar (nav.pl)
   └─ info   (home.html / reservations.pl / itinerary.pl / error.pl)
```

`BasePage` fournit :

- `switch_to_body()`
- `switch_to_navbar()`
- `switch_to_info()`
- `switch_to_default()`

Chaque méthode réessaie si la frame est en cours de rechargement
(`StaleElementReferenceException`, `TimeoutException`).

## 3. Prérequis

```bat
cd /d "D:\web tours\Mini-Projet\automation"
python -m pip install -r requirements.txt
```

- Python 3.10+
- Google Chrome (ou Edge avec adaptation du driver)
- WebTours démarré sur le port 1080
- Selenium Manager télécharge automatiquement le chromedriver

## 4. Exécution

### Suite complète

```bat
cd /d "D:\web tours\Mini-Projet\automation"
python -m pytest
```

### Par module

```bat
python -m pytest tests/test_rsva_authentication.py -v
python -m pytest tests/test_rsvf_flight.py -v
python -m pytest tests/test_rsvi_itinerary.py -v
```

### Par type

```bat
python -m pytest -m ft -v
python -m pytest -m et -v
python -m pytest -m bt -v
python -m pytest -m pt -v
```

### Un test précis

```bat
python -m pytest tests/test_rsva_authentication.py::test_rsva_pt_01_reservations_sans_login -v
```

### Rapport HTML

Le rapport est généré automatiquement dans `reports/report.html` grâce à
`pytest-html`. Il contient le détail des PASS, FAIL et XFAIL.

## 5. Résultats de référence

Exécution du 09/11/2026 :

```text
collected 14 items
tests\test_rsva_authentication.py ..xxx
tests\test_rsvf_flight.py ..xxx
tests\test_rsvi_itinerary.py .xxx
=================== 5 passed, 9 xfailed in 67.85s (0:01:07) ===================
```

- **5 PASS** : non-régression (login valide, mot de passe incorrect, recherche
  aller simple et aller-retour, affichage de l'itinéraire).
- **9 XFAIL** : scénarios réels en échec (sécurité et crash), voir
  `docs/04_Bugs_Detectes.md`.

> Les `xfail` sont volontaires : ils prouvent l'anomalie sans casser la CI.
> Lorsqu'un bug est corrigé, le test correspondant devient `XPASS` ; il faut
> alors retirer le décorateur `xfail`.

## 6. Correspondance tests / anomalies

| Test | Résultat |
|---|---|
| `test_rsva_ft_01_login_valide` | PASS |
| `test_rsva_et_01_mot_de_passe_incorrect` | PASS |
| `test_rsvf_ft_01_recherche_aller_simple` | PASS |
| `test_rsvf_ft_02_recherche_aller_retour` | PASS |
| `test_rsvi_ft_01_affichage_apres_reservation` | PASS |
| `test_rsva_bt_03_username_caracteres_speciaux` | BUG-12 |
| `test_rsva_pt_01_reservations_sans_login` | BUG-01 |
| `test_rsva_pt_03_admin_sans_login` | BUG-03 |
| `test_rsvf_et_01_date_vide` | BUG-05 |
| `test_rsvf_pt_01_prix_modifie_post` | BUG-09 |
| `test_rsvf_pt_02_flightid_falsifie` | BUG-10 |
| `test_rsvi_pt_01_idor` | BUG-04 |
| `test_rsvi_pt_02_acces_sans_session` | BUG-02 |
| `test_rsvi_pt_03_suppression_sans_session` | BUG-02 |

Les autres anomalies (BUG-06, BUG-07, BUG-08, BUG-11, BUG-13, BUG-14, BUG-15)
restent documentées dans `docs/04_Bugs_Detectes.md` mais ne font pas partie de
la campagne.

## 7. Données et isolation

- Les tests UI qui réservent des vols utilisent un **compte neuf**
  (`qa<uuid>`) créé via `WebToursAPI.signup`.
- Le fichier utilisateur est supprimé à la fin du test
  (`cgi-bin/users/<username>`).
- Les tests de recherche en lecture seule utilisent `jojo` / `bean`.
- Les tests de sécurité utilisent `api_noauth` (aucune session) ou un compte
  neuf.
- Les dates sont calculées dynamiquement (`demain`) pour éviter les effets de
  bord.

Variables d'environnement :

| Variable | Défaut | Rôle |
|---|---|---|
| `WEBTOURS_URL` | `http://127.0.0.1:1080` | URL de l'application |
| `WEBTOURS_USERS_DIR` | `D:/web tours/WebTours/cgi-bin/users` | Nettoyage des comptes de test |

## 8. Jenkins

### 8.1 Dépôt GitHub

Le projet est publié sur GitHub :
<https://github.com/Ala012/web-tours-qa> (branche `main`).

### 8.2 Installation locale (réalisée)

Jenkins est lancé **sans installation** (WAR + JDK 21 local) :

```powershell
cd "D:\web tours\Mini-Projet"
powershell -ExecutionPolicy Bypass -File ci\jenkins\run-jenkins.ps1
```

| Élément | Valeur |
|---|---|
| URL | <http://127.0.0.1:8080> |
| Utilisateur | `admin` |
| Mot de passe | `D:\web tours\jenkins\admin-password.txt` (hors dépôt) |
| Jenkins | LTS (WAR), Java 21 (Temurin) |
| Job | `WebTours-QA` |
| Definition | Pipeline script from SCM |
| SCM | `https://github.com/Ala012/web-tours-qa.git` |
| Branche | `*/main` |
| Script Path | `ci/Jenkinsfile` |
| Label de l'agent | `windows` |

Plugins installés : **workflow-aggregator**, **git**, **junit**,
**htmlpublisher**, **timestamper**, **ws-cleanup**.

Le job est défini dans `ci/jenkins/WebTours-QA.config.xml` et peut être recréé
par CLI :

```powershell
java -jar jenkins-cli.jar -s http://127.0.0.1:8080/ -auth "admin:<motdepasse>" `
  create-job WebTours-QA < ci\jenkins\WebTours-QA.config.xml
```

### 8.3 Pipeline

Le `Jenkinsfile` :

1. vérifie l'environnement Python ;
2. installe les dépendances ;
3. démarre WebTours (`scripts/start_webtours.bat`) ;
4. attend le port 1080 ;
5. lance `pytest` (les échecs rendent le build *UNSTABLE* sans masquer les rapports) ;
6. publie `automation/reports/report.html` (HTML Publisher) ;
7. publie `automation/reports/junit.xml` (JUnit) ;
8. archive `automation/reports/**` ;
9. arrête WebTours dans `post { always { ... } }`.

### 8.4 Résultat du build

**Build #1 : SUCCESS** (déclenché manuellement).

```text
collected 14 items
5 passed, 9 xfailed
JUnit : total=14, pass=5, skip=9, fail=0
```

- Rapport HTML : <http://127.0.0.1:8080/job/WebTours-QA/lastBuild/Rapport_20WebTours/>
- Résultats JUnit : page **Test Result** du build.

> Le pipeline étant sur `127.0.0.1`, le webhook GitHub → Jenkins n'est pas
> disponible. Les builds sont déclenchés manuellement (interface ou CLI).

### 8.5 Exécution locale du pipeline

```bat
cd /d "D:\web tours\Mini-Projet"
scripts\start_webtours.bat
cd automation
python -m pytest
```

## 9. Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| `TimeoutException: Frame 'navbar' introuvable` | Page non chargée / mauvais frame | Vérifier que WebTours répond ; augmenter `timeout`. |
| `Unable to locate element` | Formulaire dans une autre frame | Utiliser `switch_to_info()` / `switch_to_navbar()`. |
| `WebDriverException: chrome not reachable` | Chrome absent / driver incompatible | Installer Chrome ; laisser Selenium Manager télécharger le driver. |
| `Connection refused` | WebTours arrêté | Lancer `StartServer.bat`. |
| `xfail` inattendu | Bug corrigé | Retirer le décorateur `xfail` et vérifier le test. |
| Comptes de test résiduels | Nettoyage impossible (fichier verrouillé) | Supprimer manuellement `cgi-bin/users/qa*`. |

## 10. Ajouter un test

1. Ajouter la fiche manuelle dans `tests-manuels/...`.
2. Ajouter le test dans le fichier correspondant.
3. Utiliser les fixtures existantes (`login_page`, `fresh_logged_in`,
   `fresh_user_api`, `api_noauth`).
4. Marquer le type (`@pytest.mark.ft/et/bt/pt`).
5. Si le test révèle un bug, ajouter `@pytest.mark.xfail(reason="BUG-xx ...")`.
6. Régénérer les fiches/CSV : `python scripts/generate_test_cases.py`.
