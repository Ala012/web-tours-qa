# CI Jenkins – Mini-Projet QA Web Tours

Deux pipelines sont disponibles :

| Fichier | Environnement | WebTours |
|---|---|---|
| `ci/Jenkinsfile` | agent Jenkins Windows (local) | hôte Windows |
| `ci/Jenkinsfile.docker` | conteneur Jenkins Linux | hôte Windows via `host.docker.internal:1080` |

- Dépôt GitHub : <https://github.com/Ala012/web-tours-qa>
- Jenkins dans Docker (recommandé) : [`jenkins/docker/README.md`](jenkins/docker/README.md)
- Jenkins local (WAR + JDK 21) : [`jenkins/README.md`](jenkins/README.md)

## 1. Jenkins dans Docker (recommandé)

```powershell
cd "D:\web tours\Mini-Projet"
powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\start.ps1
```

| Élément | Valeur |
|---|---|
| URL | <http://127.0.0.1:8080> |
| Utilisateur | `admin` |
| Mot de passe | `ci/jenkins/docker/.env` (généré, ignoré par git) |
| Job | `WebTours-QA` |
| Script Path | `ci/Jenkinsfile.docker` |
| Image | `webtours-jenkins:lts` (Jenkins LTS + Python + Chrome) |
| Déclencheur | polling SCM `H/5 * * * *` + build manuel |

L'image contient Jenkins, Python 3, Google Chrome et les plugins
(`workflow-aggregator`, `git`, `junit`, `htmlpublisher`, `timestamper`,
`ws-cleanup`). Le compte admin et le job sont créés au démarrage par
`ci/jenkins/docker/init.groovy.d/`.

## 2. Jenkins local (agent Windows)

Prérequis : Windows, Java 21+ pour Jenkins, Java 8 + Strawberry Perl pour
WebTours, Python 3.10+, Google Chrome.

1. Lancer `powershell -ExecutionPolicy Bypass -File ci\jenkins\run-jenkins.ps1`.
2. Créer le job **Pipeline** `WebTours-QA` :
   - **Definition** : `Pipeline script from SCM`
   - **SCM** : `Git`
   - **Repository URL** : `https://github.com/Ala012/web-tours-qa.git`
   - **Branch Specifier** : `*/main`
   - **Script Path** : `ci/Jenkinsfile`
3. Enregistrer puis **Build Now**.

## 3. Ce que fait le pipeline

```text
Checkout
  └─ Verification de WebTours
       └─ Installation des dependances (pip install -r requirements.txt)
            └─ Tests Selenium + pytest (python -m pytest)
                 └─ Publication des rapports (JUnit + HTML)
                      └─ Archivage des artefacts
```

- Pipeline Docker : vérifie `host.docker.internal:1080`, ne démarre/arrête pas
  WebTours.
- Pipeline local : démarre WebTours (`scripts/start_webtours.bat`) et l'arrête
  dans `post { always { ... } }`.

## 4. Résultats

- Rapport HTML : lien **Rapport WebTours** sur la page du build.
- Résultats JUnit : **Test Result** du build.
- Artefacts archivés : `automation/reports/**`.

Résultat attendu : **14 tests collectés, 5 passed / 9 xfailed**
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
| Docker : `host.docker.internal` injoignable | WebTours arrêté ou pare-feu | Démarrer WebTours ; vérifier `extra_hosts` |
| Docker : port 8080 occupé | Jenkins local déjà lancé | Arrêter le WAR local ou changer le port |
