# User Stories – Projet Jira « WebTours QA »

## 1. Création du projet Jira

| Paramètre | Valeur |
|---|---|
| Type de projet | Scrum (ou Kanban) |
| Nom | **WebTours QA** |
| Clé | `WTQA` |
| Modèle | Logiciel / Scrum |
| Application | Web Tours 1.0 |
| URL | http://127.0.0.1:1080/WebTours/index.htm |

> Le fichier `jira-xray/WebTours_UserStories.csv` permet d'importer les stories
> ci-dessous. Il suffit de sélectionner le projet `WTQA` lors de l'import CSV.

## 2. Backlog

### WT-US-01 – Authentification

**En tant que** visiteur,
**je veux** me connecter avec mes identifiants
**afin d'** accéder à mes réservations et à mon espace personnel.

**Critères d'acceptation :**

- [ ] Un utilisateur valide (`jojo` / `bean`) accède à la page d'accueil avec le
      message « Welcome, jojo ».
- [ ] Un mot de passe incorrect affiche une erreur et refuse l'accès.
- [ ] Les champs vides sont refusés.
- [ ] La déconnexion (Sign Off) invalide la session et réaffiche le login.
- [ ] Les pages réservées (vols, itinéraire, admin) ne sont pas accessibles sans
      authentification.

**Priorité :** High
**Tests :** RSVA-FT-01, RSVA-ET-01, RSVA-BT-03, RSVA-PT-01, RSVA-PT-03

---

### WT-US-02 – Inscription

**En tant que** visiteur,
**je veux** créer un compte
**afin de** pouvoir réserver des vols.

**Critères d'acceptation :**

- [ ] Le formulaire d'inscription est accessible depuis « sign up now ».
- [ ] Un username alphanumérique unique est accepté.
- [ ] La confirmation du mot de passe doit correspondre.
- [ ] Un username déjà utilisé est refusé avec un message.
- [ ] Un username contenant des caractères spéciaux est refusé.
- [ ] Une politique minimale de mot de passe est appliquée.

**Priorité :** High
**Tests :** RSVA-FT-01, RSVA-ET-01, RSVA-BT-03

---

### WT-US-03 – Recherche et réservation de vols

**En tant que** client,
**je veux** rechercher et réserver un vol
**afin de** planifier mon voyage.

**Critères d'acceptation :**

- [ ] Une recherche Denver → Paris retourne quatre vols avec horaires et prix.
- [ ] Une recherche aller-retour affiche les vols aller et retour.
- [ ] La sélection d'un vol ouvre la page de paiement avec le total correct.
- [ ] Le paiement génère une facture « Reservation Made! ».
- [ ] Une date vide ou invalide est refusée avec un message explicite.
- [ ] Une date passée est refusée.
- [ ] Une ville de départ identique à la ville d'arrivée est refusée.
- [ ] Le nombre de passagers est compris entre 1 et le maximum autorisé.
- [ ] Le prix et l'identifiant du vol ne peuvent pas être falsifiés dans le POST.
- [ ] L'achat direct sans sélection est refusé.

**Priorité :** High
**Tests :** RSVF-FT-01, RSVF-FT-02, RSVF-ET-01, RSVF-PT-01, RSVF-PT-02

---

### WT-US-04 – Gestion de l'itinéraire

**En tant que** client,
**je veux** consulter et supprimer mes réservations
**afin de** gérer mon voyage.

**Critères d'acceptation :**

- [ ] L'itinéraire affiche les vols réservés, le total et la carte masquée.
- [ ] La suppression d'un vol met à jour l'itinéraire.
- [ ] La suppression de tous les vols vide l'itinéraire.
- [ ] Un identifiant de vol invalide est refusé.
- [ ] Un compte sans réservation affiche « No flights have been reserved ».
- [ ] Un utilisateur ne peut pas consulter ni supprimer l'itinéraire d'un autre.
- [ ] L'itinéraire n'est pas accessible sans session.

**Priorité :** High
**Tests :** RSVI-FT-01, RSVI-PT-01, RSVI-PT-02, RSVI-PT-03

---

### WT-US-05 – Déconnexion

**En tant que** client,
**je veux** me déconnecter
**afin de** protéger mes données personnelles.

**Critères d'acceptation :**

- [ ] Le bouton Sign Off est visible pour un utilisateur connecté.
- [ ] La déconnexion supprime le cookie de session.
- [ ] Les pages protégées redeviennent inaccessibles après déconnexion.

**Priorité :** Medium
**Tests :** – (hors campagne)

---

### WT-US-06 – Sécurité et permissions

**En tant qu'** administrateur,
**je veux** que les pages et les données sensibles soient protégées
**afin d'** éviter les accès non autorisés et les fraudes.

**Critères d'acceptation :**

- [ ] Aucune page métier n'est accessible sans authentification.
- [ ] La page d'administration exige un rôle administrateur.
- [ ] Un cookie forgé ne permet pas d'accéder aux données d'un autre utilisateur.
- [ ] Le prix, le flightID et le parcours de réservation sont validés côté serveur.
- [ ] Les mots de passe ne sont pas stockés en clair.
- [ ] Les formulaires sensibles sont protégés contre le CSRF.

**Priorité :** Critical
**Tests :** RSVA-PT-01, RSVA-PT-03, RSVF-PT-01, RSVF-PT-02,
RSVI-PT-01, RSVI-PT-02, RSVI-PT-03

---

## 3. Définition of Done (DoD)

Une story est terminée lorsque :

- tous ses critères d'acceptation sont couverts par au moins un test Xray ;
- les tests sont exécutés dans un Test Execution ;
- les anomalies Critical/High sont créées dans Jira ;
- le rapport de test est mis à jour ;
- les tests automatisés associés passent (ou sont `xfail` avec un bug lié).

## 4. Import dans Jira

1. Jira → **Issues** → **Import issues from CSV**.
2. Sélectionner `jira-xray/WebTours_UserStories.csv`.
3. Choisir le projet `WTQA`.
4. Mapper :
   - `Issue Type` → **Story**
   - `Summary` → **Summary**
   - `Description` → **Description**
   - `Priority` → **Priority**
   - `Labels` → **Labels**
   - `Acceptance Criteria` → champ personnalisé ou Description.
5. Lancer l'import.

Les tests sont ensuite liés aux stories via Xray (section **Tests** de la story
ou **Requirement Coverage**).
