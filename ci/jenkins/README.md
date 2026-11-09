# Jenkins local – WebTours QA

Ce dossier permet de lancer **Jenkins sur Windows sans installation** (WAR +
JDK 21) et de créer automatiquement le job **WebTours-QA**.

## 1. Démarrage

```powershell
cd "D:\web tours\Mini-Projet"
powershell -ExecutionPolicy Bypass -File ci\jenkins\run-jenkins.ps1
```

Le script :

1. télécharge `jenkins.war` (LTS) dans `D:\web tours\jenkins` s'il est absent ;
2. génère le mot de passe admin dans `D:\web tours\jenkins\admin-password.txt` ;
3. démarre Jenkins sur <http://127.0.0.1:8080> avec l'utilisateur `admin`.

> Jenkins LTS récent exige **Java 21+**. Le script utilise le JDK 21 présent
> dans `D:\web tours\jenkins\jdk21` (ou `JAVA_HOME` s'il pointe déjà vers 21).
> Java 17 reste utilisé par WebTours.

## 2. Job Pipeline

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

## 3. Plugins requis

```text
workflow-aggregator, git, junit, htmlpublisher, timestamper, ws-cleanup
```

Ils s'installent via **Manage Jenkins → Plugins** ou par l'API/CLI.

## 4. Lancer un build

```powershell
$pw = Get-Content "D:\web tours\jenkins\admin-password.txt" -Raw
curl.exe -u "admin:$pw" -X POST "http://127.0.0.1:8080/job/WebTours-QA/build"
```

Résultats :

- rapport HTML : `http://127.0.0.1:8080/job/WebTours-QA/lastBuild/Rapport_20WebTours/`
- résultats JUnit : page **Test Result** du build
- artefacts : `automation/reports/**`

## 5. Remarques

- Le pipeline démarre puis **arrête** WebTours (`scripts/start_webtours.bat` /
  `scripts/stop_webtours.bat`). Relancer le serveur après le build si besoin.
- Les données Jenkins (`D:\web tours\jenkins`) sont **hors du dépôt** : aucun
  secret n'est versionné.
- Le pipeline est vert tant que les 9 `xfail` restent des échecs connus ; un
  `XPASS` signifie qu'un bug est corrigé (mettre à jour Xray et retirer le
  `xfail`).
