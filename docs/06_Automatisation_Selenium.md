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
│  ├─ test_rsva_authentication.py   # 12 tests
│  ├─ test_rsvf_flight.py           # 12 tests
│  └─ test_rsvi_itinerary.py        # 12 tests
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
python -m pytest tests/test_rsva_authentication.py::test_rsva_ft_01_login_valide -v
```

### Rapport HTML

Le rapport est généré automatiquement dans `reports/report.html` grâce à
`pytest-html`. Il contient le détail des PASS, FAIL et XFAIL.

## 5. Résultats de référence

Exécution du 09/11/2026 :

```text
collected 36 items
tests\test_rsva_authentication.py .......xxxxx
tests\test_rsvf_flight.py ...xxx.xxxxx
tests\test_rsvi_itinerary.py .........xxx
================= 20 passed, 16 xfailed in 426.81s (0:07:06) ==================
```

- **20 PASS** : parcours nominaux et validations existantes.
- **16 XFAIL** : anomalies connues (voir `docs/04_Bugs_Detectes.md`).

> Les `xfail` sont volontaires : ils prouvent l'anomalie sans casser la CI.
> Lorsqu'un bug est corrigé, le test correspondant devient `XPASS` ; il faut
> alors retirer le décorateur `xfail`.

## 6. Correspondance tests / anomalies

| Test | Anomalie |
|---|---|
| `test_rsva_bt_02_mot_de_passe_1_caractere` | BUG-11 |
| `test_rsva_bt_03_username_caracteres_speciaux` | BUG-12 |
| `test_rsva_pt_01_reservations_sans_login` | BUG-01 |
| `test_rsva_pt_02_itinerary_sans_login` | BUG-02 |
| `test_rsva_pt_03_admin_sans_login` | BUG-03 |
| `test_rsvf_et_01_date_vide` | BUG-05 |
| `test_rsvf_et_02_date_invalide` | BUG-05 |
| `test_rsvf_et_03_meme_ville` | BUG-07 |
| `test_rsvf_bt_02_zero_passager` | BUG-08 |
| `test_rsvf_bt_03_999_passagers` | BUG-08 |
| `test_rsvf_pt_01_prix_modifie_post` | BUG-09 |
| `test_rsvf_pt_02_flightid_falsifie` | BUG-10 |
| `test_rsvf_pt_03_buy_direct` | BUG-10 |
| `test_rsvi_pt_01_idor` | BUG-04 |
| `test_rsvi_pt_02_acces_sans_session` | BUG-02 |
| `test_rsvi_pt_03_suppression_sans_session` | BUG-02 |

Les anomalies BUG-06, BUG-13, BUG-14 et BUG-15 sont documentées et vérifiées
manuellement (elles ne font pas l'objet d'un test automatisé dédié).

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

### 8.1 Préparation

1. Installer Jenkins (Windows ou Linux avec agent Windows).
2. Installer les plugins : **Pipeline**, **HTML Publisher**, **JUnit**,
   **Git**.
3. Créer un job **Pipeline**.
4. Dans **Pipeline → Definition**, choisir **Pipeline script from SCM**.
5. SCM : Git, URL du dépôt, branche `main`.
6. Script Path : `ci/Jenkinsfile`.

### 8.2 Pipeline

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

### 8.3 Exécution locale du pipeline

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
