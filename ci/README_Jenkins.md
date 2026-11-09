# CI Jenkins – Mini-Projet QA Web Tours

Ce dossier contient le pipeline `Jenkinsfile` qui exécute la suite
d'automatisation Selenium/pytest et publie les rapports.

- Dépôt GitHub : <https://github.com/Ala012/web-tours-qa>
- Jenkins local (WAR + JDK 21, job `WebTours-QA`) : voir
  [`jenkins/README.md`](jenkins/README.md)

## 1. Prérequis sur l'agent Jenkins

| Élément | Détail |
|---|---|
| OS | Windows (agent avec le label `windows`) |
| Java | Java 21+ pour Jenkins ; Java 8 pour le serveur WebTours |
| Perl | Strawberry Perl 5.10.1.0 |
| Python | 3.10+ dans le `PATH` |
| Navigateur | Google Chrome (Selenium Manager gère le driver) |
| WebTours | installé dans `D:\web tours\WebTours` |
| Plugins Jenkins | **Pipeline**, **Git**, **HTML Publisher**, **JUnit**, **Timestamper** |

## 2. Création du job

1. Jenkins → **New Item** → **Pipeline** → nom : `WebTours-QA`.
2. Section **Pipeline** :
   - **Definition** : `Pipeline script from SCM`
   - **SCM** : `Git`
   - **Repository URL** : `https://github.com/Ala012/web-tours-qa.git`
   - **Branch Specifier** : `*/main`
   - **Script Path** : `ci/Jenkinsfile`
3. Enregistrer puis **Build Now**.

> Le job peut aussi être créé directement depuis
> `ci/jenkins/WebTours-QA.config.xml` (voir `ci/jenkins/README.md`).

## 3. Ce que fait le pipeline

```text
Checkout
  └─ Installation des dependances (pip install -r requirements.txt)
       └─ Demarrage de WebTours (scripts/start_webtours.bat)
            └─ Tests Selenium + pytest (python -m pytest)
                 └─ Publication des rapports (JUnit + HTML)
                      └─ Arret de WebTours (post / always)
```

## 4. Résultats

- Rapport HTML : lien **Rapport WebTours** sur la page du build.
- Résultats JUnit : **Test Result** du build.
- Artefacts archivés : `automation/reports/**`.

**Build #1 : SUCCESS** — 14 tests collectés, **5 passed / 9 xfailed**
(JUnit : `total=14, pass=5, skip=9, fail=0`).

Les tests marqués `xfail` correspondent aux **bugs connus et documentés**.
Ils sont comptés comme `xfailed` et ne rendent pas le build instable.

## 5. Exécution locale (hors Jenkins)

```bat
cd /d "D:\web tours\Mini-Projet"
scripts\start_webtours.bat
cd automation
python -m pytest
cd ..
scripts\stop_webtours.bat
```

## 6. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| `WebTours ne repond pas sur le port 1080` | Java/Perl absent ou port occupé | Vérifier `docs/05_Installation_WebTours.md` |
| `No module named pytest` | dépendances non installées | `python -m pip install -r automation/requirements.txt` |
| `session not created` | Chrome absent ou trop ancien | Installer/mettre à jour Chrome |
| Rapport HTML vide | plugin HTML Publisher manquant | Installer le plugin puis relancer |
