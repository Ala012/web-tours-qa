# Jenkins – WebTours QA

Deux méthodes sont disponibles :

| Méthode | Jenkins | Tests | WebTours |
|---|---|---|---|
| **Docker (recommandé)** | conteneur Linux | conteneur (Python + Chrome) | hôte Windows |
| Local (WAR) | Windows | hôte Windows | hôte Windows |

## 1. Docker (recommandé)

```powershell
cd "D:\web tours\Mini-Projet"
powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\start.ps1
```

Le script génère `ci/jenkins/docker/.env` (mot de passe admin, ignoré par git),
démarre WebTours si besoin, construit l'image et lance le conteneur.

| Élément | Valeur |
|---|---|
| URL | <http://127.0.0.1:8080> |
| Utilisateur | `admin` |
| Mot de passe | `ci/jenkins/docker/.env` |
| Conteneur | `webtours-jenkins` |
| Job | `WebTours-QA` |
| Script Path | `ci/Jenkinsfile.docker` |
| Déclencheur | polling SCM `H/5 * * * *` + build manuel |

Détails, commandes et dépannage : [`docker/README.md`](docker/README.md).

```powershell
# Logs / état
docker logs -f webtours-jenkins
docker compose -f ci\jenkins\docker\docker-compose.yml ps

# Arrêt (volume conservé) / reset complet
powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\stop.ps1
powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\stop.ps1 -RemoveVolume
```

## 2. Local (WAR + JDK 21)

```powershell
cd "D:\web tours\Mini-Projet"
powershell -ExecutionPolicy Bypass -File ci\jenkins\run-jenkins.ps1
```

Le script télécharge `jenkins.war` dans `D:\web tours\jenkins`, génère le mot de
passe admin dans `D:\web tours\jenkins\admin-password.txt` et démarre Jenkins
sur <http://127.0.0.1:8080>.

> Jenkins LTS récent exige **Java 21+** ; le script utilise le JDK 21 local.
> Java 17 reste utilisé par WebTours.

### 2.1 Job Pipeline (local)

Le job **WebTours-QA** se crée depuis `WebTours-QA.config.xml` :

```powershell
$pw = Get-Content "D:\web tours\jenkins\admin-password.txt" -Raw
curl.exe -u "admin:$pw" -X POST "http://127.0.0.1:8080/createItem?name=WebTours-QA" `
  -H "Content-Type: application/xml" --data-binary "@ci\jenkins\WebTours-QA.config.xml"
```

Configuration :

| Paramètre | Valeur |
|---|---|
| Type | Pipeline |
| Definition | Pipeline script from SCM |
| SCM | Git |
| Repository | `https://github.com/Ala012/web-tours-qa.git` |
| Branche | `*/main` |
| Script Path | `ci/Jenkinsfile` |
| Label de l'agent | `windows` |

### 2.2 Plugins requis

```text
workflow-aggregator, git, junit, htmlpublisher, timestamper, ws-cleanup
```

## 3. Lancer un build

```powershell
# Docker
$pw = ((Get-Content ci\jenkins\docker\.env) -replace '^JENKINS_ADMIN_PASSWORD=', '')
curl.exe -u "admin:$pw" -X POST "http://127.0.0.1:8080/job/WebTours-QA/build"

# Local
$pw = Get-Content "D:\web tours\jenkins\admin-password.txt" -Raw
curl.exe -u "admin:$pw" -X POST "http://127.0.0.1:8080/job/WebTours-QA/build"
```

Résultats :

- rapport HTML : `http://127.0.0.1:8080/job/WebTours-QA/lastBuild/Rapport_20WebTours/`
- résultats JUnit : page **Test Result** du build
- artefacts : `automation/reports/**`

## 4. Remarques

- En Docker, le pipeline **ne démarre/arrête pas** WebTours : il vérifie qu'il
  répond sur `host.docker.internal:1080`. Le script `start.ps1` le démarre.
- En local, le pipeline démarre puis arrête WebTours ; relancer le serveur
  après le build si besoin.
- Aucun secret n'est versionné : `.env` et `D:\web tours\jenkins` restent
  hors du dépôt.
- Le build est vert tant que les 9 `xfail` restent des échecs connus ; un
  `XPASS` signifie qu'un bug est corrigé (mettre à jour Xray et retirer le
  `xfail`).
