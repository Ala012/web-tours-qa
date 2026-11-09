# Installation et démarrage de Web Tours

## 1. Prérequis

| Logiciel | Version | Rôle |
|---|---|---|
| Java | **Java 8** (JRE ou JDK) | Applets/classes Java de WebTours |
| Perl | **Strawberry Perl 5.10.1.0** | Scripts CGI (`*.pl`) |
| WebTours | 1.0 | Application de réservation de vols |
| Navigateur | Chrome / Edge / Firefox | Accès à l'interface |

> WebTours est une application ancienne (Apache 2.2, Perl 5.10, applets Java).
> Utiliser Java 8 et Strawberry Perl 5.10.1.0 évite la plupart des problèmes.

## 2. Installation de Java 8

1. Télécharger Java 8 depuis le site Oracle :
   <https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html>
2. Installer le JRE/JDK 8 (par défaut : `C:\Program Files\Java\jre1.8.0_xxx`).
3. Vérifier :

```bat
java -version
```

Résultat attendu : `java version "1.8.0_xxx"`.

> Si Java 17/21 est déjà installé, il peut rester présent : WebTours n'utilise
> Java que pour les applets de calendrier. Le serveur Apache/Perl fonctionne
> indépendamment. Pour forcer Java 8, ajuster `JAVA_HOME` et le `PATH`.

## 3. Installation de Strawberry Perl 5.10.1.0

1. Télécharger l'installeur :
   <https://strawberryperl.com/download/5.10.1.0/strawberry-perl-5.10.1.0.msi>
2. Installer dans `C:\strawberry` (par défaut).
3. Vérifier :

```bat
perl -v
```

Résultat attendu : `This is perl, v5.10.1 (*) built for MSWin32-x86-multi-thread`.

## 4. Installation de WebTours

1. Copier le dossier `WebTours` dans `D:\web tours\WebTours`.
2. Vérifier la présence de :

```text
D:\web tours\WebTours\
├─ bin\httpd.exe
├─ cgi-bin\
├─ conf\httpd.conf
├─ htdocs\WebTours\index.htm
├─ logs\
└─ StartServer.bat
```

## 5. Correction de la configuration Apache (important)

Le chemin contient un **espace** (`D:\web tours`). Apache 2.2 interprète mal
les directives relatives `DocumentRoot "htdocs"` et `<Directory "htdocs">` :
les requêtes retournent **403 Forbidden**.

Ouvrir `D:\web tours\WebTours\conf\httpd.conf` et remplacer :

```apache
#ServerName localhost:1080
DocumentRoot "htdocs"
<Directory "htdocs">
ScriptAlias /cgi-bin/ "cgi-bin/"
<Directory "cgi-bin">
```

par :

```apache
ServerName localhost:1080
DocumentRoot "D:/web tours/WebTours/htdocs"
<Directory "D:/web tours/WebTours/htdocs">
ScriptAlias /cgi-bin/ "D:/web tours/WebTours/cgi-bin/"
<Directory "D:/web tours/WebTours/cgi-bin">
```

> Utiliser des **slashes** `/` et des chemins absolus entre guillemets.
> Redémarrer Apache après modification.

## 6. Démarrage du serveur

### Méthode 1 – Script fourni

```bat
cd /d "D:\web tours\WebTours"
StartServer.bat
```

Laisser la fenêtre ouverte. Le serveur écoute sur le port **1080**.

### Méthode 2 – Ligne de commande

```bat
cd /d "D:\web tours\WebTours"
bin\httpd.exe -d "D:\web tours\WebTours"
```

### Vérification

```bat
curl http://127.0.0.1:1080/WebTours/index.htm
```

Ou ouvrir dans le navigateur :
<http://127.0.0.1:1080/WebTours/index.htm>

## 7. Comptes de démonstration

| Utilisateur | Mot de passe | Rôle |
|---|---|---|
| `jojo` | `bean` | Client |
| `admin` | `admin` | Administrateur |
| `karino01` | `karino` | Client (optionnel) |

## 8. Arrêt du serveur

- Fermer la fenêtre `StartServer.bat`, ou
- `Ctrl+C` dans la console, ou
- `taskkill /IM httpd.exe /F`.

## 9. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| **403 Forbidden** | Chemins relatifs + espace dans le chemin | Appliquer la section 5 (chemins absolus). |
| **Port 1080 déjà utilisé** | Ancien processus Apache | `netstat -ano \| findstr :1080` puis `taskkill /PID <pid> /F`. |
| **500 Internal Server Error** | Perl absent ou mauvais chemin | Vérifier `perl -v`, réinstaller Strawberry Perl 5.10.1.0. |
| **Page blanche sur les dates** | Bug applicatif (BUG-05) | Saisir une date valide `MM/DD/YYYY` ; voir le rapport de bugs. |
| **Applets de calendrier invisibles** | Applets non supportés par Chrome/Edge | Saisir la date manuellement. |
| **Les scripts CGI ne trouvent pas les utilisateurs** | Le dossier `MTData` est absent | Comportement connu : les scripts utilisent `cgi-bin/users` en repli. Ne pas supprimer ce dossier. |
| **Erreur `Month '-1' out of range`** | Date vide/invalide (BUG-05) | Utiliser une date valide ; correction côté code nécessaire. |

## 10. Journaux

| Fichier | Contenu |
|---|---|
| `logs\error.log` | Erreurs Apache/Perl (ex. `Month '-1' out of range`) |
| `logs\access.log` | Requêtes HTTP |

Consulter `logs\error.log` après chaque campagne de tests.

## 11. Scripts fournis dans le projet

| Script | Rôle |
|---|---|
| `scripts\start_webtours.bat` | Démarre Apache en arrière-plan. |
| `scripts\stop_webtours.bat` | Arrête Apache. |
| `scripts\capture_evidence.py` | Génère les captures des anomalies. |
| `scripts\generate_test_cases.py` | Régénère les fiches et les CSV. |
