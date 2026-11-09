# Automatisation Jira / Xray par API

Ce guide explique comment fournir les identifiants nécessaires pour créer
directement dans Jira/Xray les user stories, les tests, les bugs et
l'exécution, sans passer par les imports CSV manuels.

> **Important** : personne ne peut te « donner » un token Jira ou une clé Xray.
> Ces secrets sont générés dans **ton** compte Atlassian et ne doivent jamais
> être publiés ni collés dans une conversation.

## 1. Deux jeux de clés différents

| Clé | Générée dans | Sert à |
|---|---|---|
| **Jira API token** | <https://id.atlassian.com/manage-profile/security/api-tokens> | API REST Jira : créer projets, stories, bugs, liens |
| **Xray Client ID + Client Secret** | Jira → ⚙️ **Settings → Apps → Xray → API Keys** | API Xray : tests, plans, exécutions, résultats |

Le token Jira ne donne **pas** accès à l'API Xray, et inversement.

## 2. Générer le token Jira

1. Se connecter à <https://id.atlassian.com/manage-profile/security/api-tokens>.
2. Cliquer sur **Create API token** (ou **Create API token with scopes**).
3. Nom : `WebTours-QA`.
4. Expiration : 30 à 90 jours.
5. Pour un token avec scopes :
   - application : **Jira** ;
   - scopes : `read:jira-work`, `write:jira-work`, `read:jira-user` ;
   - ajouter `manage:jira-project` seulement si le projet doit être créé par API.
6. Copier le token immédiatement : il n'est affiché qu'une seule fois.

## 3. Générer la clé Xray Cloud

1. Dans Jira : ⚙️ **Settings → Apps → Xray → API Keys**.
2. Cliquer sur **Create API Key**.
3. Choisir l'utilisateur dont la clé reprend les permissions.
4. Copier **Client ID** et **Client Secret** (le secret n'est affiché qu'une fois).

> Cette page nécessite les droits **administrateur Jira**. Si elle n'apparaît
> pas, demander à un administrateur de créer la clé.
>
> Région : `https://xray.cloud.getxray.app` (US) ou
> `https://eu.xray.cloud.getxray.app` (EU). Le token Xray obtenu expire après
> 24 h ; les clés Client ID/Secret, elles, n'expirent pas.

## 4. Configurer les identifiants en local

```bat
cd /d "D:\web tours\Mini-Projet"
copy .env.local.example .env.local
notepad .env.local
```

Remplir :

```ini
JIRA_BASE_URL=https://alaachaabouni09.atlassian.net
JIRA_EMAIL=ton.email@exemple.com
JIRA_API_TOKEN=...
JIRA_PROJECT_KEY=WTQA
XRAY_CLIENT_ID=...
XRAY_CLIENT_SECRET=...
XRAY_BASE_URL=https://xray.cloud.getxray.app
```

Vérifier que le fichier contenant les secrets est bien ignoré par Git :

```bat
git check-ignore -v .env.local
```

## 5. Vérifier l'accès

```bat
python scripts\check_jira_access.py
```

Résultat attendu :

```text
[OK] Jira (Basic) : connecte comme Prenom Nom <email>
[OK] Projet WTQA : WebTours QA (id 10001)
[OK] Xray : token obtenu (valide 24 h, ...)
[OK] Xray GraphQL : 1 projet(s) visible(s).
```

Codes de sortie :

| Code | Signification |
|---|---|
| `0` | Jira accessible (et Xray si configuré) |
| `1` | Authentification ou projet en erreur |
| `2` | Variables manquantes dans `.env.local` |

## 6. Ce que l'automatisation fera ensuite

Une fois l'accès validé :

1. créer le projet `WTQA` s'il n'existe pas ;
2. créer les 6 user stories (`WT-US-01` à `WT-US-06`) ;
3. créer les 9 tests Xray avec préconditions, étapes et résultat attendu ;
4. créer le **Test Plan** « Plan de test WebTours – Sprint 1 » ;
5. créer le **Test Execution** « Exécution manuelle – Sprint 1 » ;
6. importer les statuts **9 FAILED** ;
7. créer les 15 bugs et les lier aux tests concernés.

## 7. Sécurité

- Ne jamais commiter `.env.local` (déjà dans `.gitignore`).
- Ne pas coller les secrets dans le chat, un ticket ou un dépôt.
- Révoquer le token Jira et la clé Xray après le projet.
- En cas de fuite : révoquer immédiatement et régénérer.

## 8. Solution de repli sans API

Si les droits administrateur ou l'API Xray ne sont pas disponibles, utiliser
les imports CSV décrits dans `jira-xray/README_Import_Xray.md`. Le résultat
fonctionnel est identique, seule la saisie est manuelle.
