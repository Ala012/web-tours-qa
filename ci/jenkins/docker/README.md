# Jenkins dans Docker – WebTours QA

Jenkins, Python et Google Chrome tournent dans un conteneur Linux.
WebTours reste sur l'hôte Windows et est joignable depuis le conteneur via
`http://host.docker.internal:1080`.

## 1. Démarrage

```powershell
cd "D:\web tours\Mini-Projet"
powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\start.ps1
```

Le script :

1. génère `ci/jenkins/docker/.env` avec un mot de passe admin aléatoire
   (fichier ignoré par git) ;
2. démarre WebTours sur l'hôte s'il est arrêté ;
3. construit l'image `webtours-jenkins:lts` et démarre le conteneur ;
   si le mot de passe de `.env` a changé, supprime le compte admin existant
   et recrée le conteneur pour appliquer la rotation ;
4. attend Jenkins puis affiche l'URL et l'utilisateur (le mot de passe reste
   dans `.env`, il n'est jamais affiché).

| Élément | Valeur |
|---|---|
| URL | <http://127.0.0.1:8080> |
| Utilisateur | `admin` |
| Mot de passe | `ci/jenkins/docker/.env` |
| Conteneur | `webtours-jenkins` |
| Job | `WebTours-QA` |
| Script Path | `ci/Jenkinsfile.docker` |
| Déclencheur | polling SCM `H/5 * * * *` + build manuel |

## 2. Ce que contient l'image

- `jenkins/jenkins:lts-jdk21` ;
- Python 3 + environnement virtuel `/opt/venv` avec
  `automation/requirements.txt` ;
- Google Chrome stable (Selenium Manager télécharge le driver) ;
- plugins : `workflow-aggregator`, `git`, `junit`, `htmlpublisher`,
  `timestamper`, `ws-cleanup`.

Le job et le compte admin sont créés au démarrage par les scripts
`init.groovy.d/`.

## 3. Commandes utiles

```powershell
# Logs
docker logs -f webtours-jenkins

# Etat
docker compose -f ci\jenkins\docker\docker-compose.yml ps

# Build manuel
$pw = (Select-String -Path ci\jenkins\docker\.env -Pattern '^JENKINS_ADMIN_PASSWORD=').Line `
    -replace '^JENKINS_ADMIN_PASSWORD=', ''
curl.exe -u "admin:$pw" -X POST "http://127.0.0.1:8080/job/WebTours-QA/build"

# Rapports
# http://127.0.0.1:8080/job/WebTours-QA/lastBuild/Rapport_20WebTours/

# Arret (donnees conservees)
powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\stop.ps1

# Reset complet (supprime le volume Jenkins)
powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\stop.ps1 -RemoveVolume
```

## 4. Résultat des builds Docker

| Build | Contexte | Résultat |
|---|---|---|
| #2 | premier build Docker valide | **SUCCESS** — 5 passed / 9 xfailed (222,56 s) |
| #3 | après rotation du mot de passe admin | **SUCCESS** — 5 passed / 9 xfailed (223,46 s) |

```text
collected 14 items
5 passed, 9 xfailed in 223.46s (0:03:43)
JUnit : pass=5, skip=9, fail=0
```

Les 9 `xfail` correspondent aux bugs documentés : le build reste **SUCCESS**.

> Le build #1 a échoué car `ci/Jenkinsfile.docker` n'était pas encore poussé
> sur GitHub.

## 5. Rotation du mot de passe admin

Le mot de passe est transmis au conteneur à sa **création**. Pour le changer :

1. écrire le nouveau secret dans `ci/jenkins/docker/.env` ;
2. relancer `start.ps1`.

Le script détecte l'écart avec l'environnement du conteneur, supprime
`/var/jenkins_home/users/admin_*` dans le volume puis recrée le conteneur :
`init.groovy.d/01-admin.groovy` régénère le compte `admin` avec le nouveau
mot de passe. Les builds et la configuration du job sont conservés.

## 6. Remarques

- WebTours doit être démarré sur l'hôte avant un build (le pipeline le
  vérifie et échoue proprement sinon).
- Le conteneur n'a pas besoin de port 1080 : il consomme WebTours via
  `host.docker.internal`.
- `ci/jenkins/docker/.env` n'est jamais versionné ; seul `env.example` l'est.
- Sur Linux, `host.docker.internal` est fourni par
  `extra_hosts: host-gateway` (déjà configuré).
