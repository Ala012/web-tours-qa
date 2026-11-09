# Rapport de bugs – Web Tours

## 1. Contexte

| Élément | Valeur |
|---|---|
| Application | Web Tours 1.0 |
| URL | http://127.0.0.1:1080/WebTours/index.htm |
| Environnement | Windows, Java 8, Strawberry Perl 5.10.1.0, Apache 2.2.21 |
| Navigateur | Google Chrome (headless et graphique) |
| Méthode | Tests manuels + Selenium/pytest + requêtes HTTP forgées |
| Date | 09/11/2026 |

## 2. Synthèse

| Sévérité | Nombre |
|---|---|
| Critical | 6 |
| High | 7 |
| Medium | 2 |
| **Total** | **15** |

| ID | Module | Anomalie | Sévérité | Test(s) |
|---|---|---|---|---|
| BUG-01 | RSVA | Recherche de vols accessible sans login | Critical | RSVA-PT-01 |
| BUG-02 | RSVA/RSVI | Itinéraire accessible sans login | High | RSVA-PT-02, RSVI-PT-02/03 |
| BUG-03 | RSVA | Page admin accessible sans authentification | Critical | RSVA-PT-03 |
| BUG-04 | RSVI | IDOR : itinéraire d'un autre utilisateur via cookie forgé | Critical | RSVI-PT-01 |
| BUG-05 | RSVF | Date vide/invalide : page blanche et erreur Perl | High | RSVF-ET-01/02 |
| BUG-06 | RSVF | Date passée acceptée | High | RSVF-ET-01 (variante) |
| BUG-07 | RSVF | Départ = arrivée accepté, vols à 0 $ | High | RSVF-ET-03 |
| BUG-08 | RSVF | Nombre de passagers non validé (0, négatif, 999) | High | RSVF-BT-02/03 |
| BUG-09 | RSVF | Prix manipulable dans le POST | Critical | RSVF-PT-01 |
| BUG-10 | RSVF | flightID falsifié / achat direct | Critical | RSVF-PT-02/03 |
| BUG-11 | RSVA | Politique de mot de passe absente | Medium | RSVA-BT-02 |
| BUG-12 | RSVA | Normalisation silencieuse du username | High | RSVA-BT-03 |
| BUG-13 | RSVA | Mots de passe stockés en clair | Critical | – (audit) |
| BUG-14 | RSVF | Aucune validation de la carte bancaire | High | RSVF-FT-03 (variante) |
| BUG-15 | Tous | Absence de jetons anti-CSRF | Medium | – (audit) |

---

## BUG-01 – Recherche de vols accessible sans authentification

- **Module :** RSVA – Authentification / permissions
- **Sévérité :** Critical
- **Priorité :** Highest
- **Test :** RSVA-PT-01
- **Automatisé :** `test_rsva_authentication.py::test_rsva_pt_01_reservations_sans_login` (`xfail`)

**Préconditions :** aucune session ouverte.

**Étapes :**

1. Ouvrir directement `http://127.0.0.1:1080/cgi-bin/reservations.pl?page=welcome`.
2. Observer la page.

**Résultat attendu :** redirection vers la page de connexion ; aucun formulaire de
réservation accessible.

**Résultat obtenu :** le formulaire **Find Flight** est affiché, avec les listes
de villes, les dates et le bouton de recherche.

**Impact :** un visiteur non authentifié peut lancer une recherche et tenter une
réservation ; contournement du contrôle d'accès.

**Correctif recommandé :** vérifier côté serveur la présence d'une session
valide (cookie signé ou session serveur) avant d'afficher `reservations.pl`.

---

## BUG-02 – Itinéraire accessible sans authentification

- **Module :** RSVA / RSVI
- **Sévérité :** High
- **Priorité :** High
- **Tests :** RSVA-PT-02, RSVI-PT-02, RSVI-PT-03
- **Automatisé :** `test_rsva_authentication.py::test_rsva_pt_02_itinerary_sans_login` (`xfail`)

**Étapes :**

1. Ouvrir directement `http://127.0.0.1:1080/cgi-bin/itinerary.pl`.
2. Envoyer un POST `removeAllFlights.x=1` sans cookie.

**Résultat attendu :** redirection vers le login ou HTTP 401/403.

**Résultat obtenu :** la page **Itinerary** est affichée avec
« No flights have been reserved ». Le POST est traité et retourne une page vide.

**Impact :** les pages métier ne sont pas protégées ; la logique de suppression
est exécutable sans session.

**Correctif recommandé :** contrôle de session centralisé (middleware) avant
l'exécution des scripts CGI.

---

## BUG-03 – Page d'administration accessible sans authentification

- **Module :** RSVA
- **Sévérité :** Critical
- **Priorité :** Highest
- **Test :** RSVA-PT-03
- **Automatisé :** `test_rsva_authentication.py::test_rsva_pt_03_admin_sans_login` (`xfail`)

**Étapes :**

1. Ouvrir `http://127.0.0.1:1080/cgi-bin/admin.pl` sans être connecté.
2. Observer les options serveur.

**Résultat attendu :** accès refusé ou authentification administrateur requise.

**Résultat obtenu :** la page **Web Tours Admin Page** est affichée. Les options
(`MSO_Comments`, `MSO_JSCalc`, `MSO_JSVerify`, etc.) sont modifiables et
peuvent être enregistrées via `admin.pl?save=Update`.

**Impact :** modification de la configuration serveur, activation d'options
dangereuses, déni de service, altération du comportement de l'application.

**Correctif recommandé :** authentification + rôle admin + jeton CSRF sur le
formulaire d'administration.

---

## BUG-04 – IDOR : itinéraire d'un autre utilisateur via cookie forgé

- **Module :** RSVI
- **Sévérité :** Critical
- **Priorité :** Highest
- **Test :** RSVI-PT-01
- **Automatisé :** `test_rsvi_itinerary.py::test_rsvi_pt_01_idor` (`xfail`)

**Préconditions :** aucune authentification.

**Étapes :**

1. Envoyer une requête `GET /cgi-bin/itinerary.pl` avec le cookie :
   `MTUserInfo=username&admin&hash&78`.
2. Lire la réponse.

**Résultat attendu :** refus ou retour des données de la session authentifiée
uniquement.

**Résultat obtenu :** l'itinéraire complet de `admin` est affiché :

```text
Itinerary admin admin's Flight Transaction Summary
2 First class tickets ... Total Charge: $ 2892 (CC: x-5285)
Flight 100 leaves Frankfurt for Denver ...
```

**Impact :** fuite de données personnelles (nom, adresse, carte masquée,
réservations) et possibilité de supprimer les vols d'un autre utilisateur.

**Cause :** le cookie `MTUserInfo` contient le username et le hash ; le serveur
lui fait confiance sans vérifier la session.

**Correctif recommandé :** session serveur signée (HttpOnly, Secure), identifiant
utilisateur non modifiable côté client, contrôle d'autorisation sur chaque
requête.

---

## BUG-05 – Date vide ou invalide : page blanche et erreur Perl

- **Module :** RSVF
- **Sévérité :** High
- **Priorité :** High
- **Tests :** RSVF-ET-01, RSVF-ET-02
- **Automatisé :** `test_rsvf_flight.py::test_rsvf_et_01_date_vide`, `test_rsvf_et_02_date_invalide` (`xfail`)

**Étapes :**

1. Se connecter et ouvrir **Flights**.
2. Vider le champ **Departure Date** (ou saisir `13/45/2026`).
3. Cliquer sur **Next**.

**Résultat attendu :** message de validation clair, formulaire conservé.

**Résultat obtenu :** la page ne contient plus que le titre « Find Flight » :
le formulaire disparaît, aucun message n'est affiché. Le log Apache contient :

```text
[error] [client 127.0.0.1] Month '-1' out of range 0..11
at .../reservations.pl line 727
```

**Impact :** impasse fonctionnelle, erreur serveur non gérée, mauvaise expérience
utilisateur.

**Correctif recommandé :** valider le format `MM/DD/YYYY` côté serveur, vérifier
les bornes mois/jour/année et afficher un message d'erreur.

---

## BUG-06 – Date passée acceptée

- **Module :** RSVF
- **Sévérité :** High
- **Priorité :** High
- **Test :** RSVF-ET-01 (variante)
- **Automatisé :** couvert par `test_rsvf_et_02_date_invalide` / scénario manuel

**Étapes :**

1. Rechercher un vol avec `departDate = 01/01/2020`.

**Résultat attendu :** refus avec message « la date doit être dans le futur ».

**Résultat obtenu :** quatre vols sont proposés normalement.

**Impact :** réservation incohérente, calcul de remise avancée faussé.

**Correctif recommandé :** comparer la date à la date du jour côté serveur.

---

## BUG-07 – Ville de départ identique à la ville d'arrivée

- **Module :** RSVF
- **Sévérité :** High
- **Priorité :** High
- **Test :** RSVF-ET-03
- **Automatisé :** `test_rsvf_flight.py::test_rsvf_et_03_meme_ville` (`xfail`)

**Étapes :**

1. Sélectionner `Denver` au départ et `Denver` à l'arrivée.
2. Cliquer sur **Next**.

**Résultat attendu :** refus avec message explicite.

**Résultat obtenu :** quatre vols fictifs `Denver → Denver` à **0 $**.

**Impact :** réservations incohérentes, factures à 0 $.

**Correctif recommandé :** validation `depart != arrive`.

---

## BUG-08 – Nombre de passagers non validé

- **Module :** RSVF
- **Sévérité :** High
- **Priorité :** High
- **Tests :** RSVF-BT-02, RSVF-BT-03
- **Automatisé :** `test_rsvf_flight.py::test_rsvf_bt_02_zero_passager`, `test_rsvf_bt_03_999_passagers` (`xfail`)

**Étapes :**

1. Saisir `0`, `-1`, `abc` ou `999` dans **No. of Passengers**.
2. Lancer la recherche.

**Résultat attendu :** refus si la valeur n'est pas un entier entre 1 et le
maximum autorisé.

**Résultat obtenu :** les vols sont affichés dans tous les cas.

**Impact :** totaux à 0 $, nombres de billets incohérents, risque de calcul
négatif.

**Correctif recommandé :** validation entière + bornes min/max côté serveur.

---

## BUG-09 – Prix manipulable dans la requête POST

- **Module :** RSVF
- **Sévérité :** Critical
- **Priorité :** Highest
- **Test :** RSVF-PT-01
- **Automatisé :** `test_rsvf_flight.py::test_rsvf_pt_01_prix_modifie_post` (`xfail`)

**Étapes :**

1. Rechercher `Denver → Paris` (prix 350 $).
2. Intercepter le POST `reserveFlights`.
3. Remplacer `outboundFlight=040;350;11/10/2026` par
   `outboundFlight=040;1;11/10/2026`.
4. Finaliser le paiement.

**Résultat attendu :** le serveur recalcule le prix à partir de sa base ; total
facturé = 350 $.

**Résultat obtenu :** la page de paiement affiche **Total for 1 ticket(s) = 1 $**
et la facture est générée à **1 $**.

**Impact :** fraude financière directe.

**Correctif recommandé :** ne jamais faire confiance au prix envoyé par le
client ; recalculer à partir du flightID et de la classe.

---

## BUG-10 – Falsification du flightID et achat direct

- **Module :** RSVF
- **Sévérité :** Critical
- **Priorité :** Highest
- **Tests :** RSVF-PT-02, RSVF-PT-03
- **Automatisé :** `test_rsvf_flight.py::test_rsvf_pt_02_flightid_falsifie`, `test_rsvf_pt_03_buy_direct` (`xfail`)

**Étapes :**

1. Envoyer un POST `reserveFlights` avec
   `outboundFlight=999;1;01/01/2027` (vol inexistant).
2. Finaliser le paiement.
3. Variante : envoyer directement un POST `buyFlights` sans recherche ni
   sélection.

**Résultat attendu :** refus du vol inexistant et du parcours incomplet.

**Résultat obtenu :** une facture est générée pour un vol **999 Zurich → Zurich**
à **1 $**. L'achat direct crée également une réservation.

**Impact :** création de réservations fictives, fraude, pollution des données.

**Correctif recommandé :** valider le flightID contre la base, vérifier l'état du
panier/session et l'ordre des étapes.

---

## BUG-11 – Politique de mot de passe absente

- **Module :** RSVA
- **Sévérité :** Medium
- **Priorité :** Medium
- **Test :** RSVA-BT-02
- **Automatisé :** `test_rsva_authentication.py::test_rsva_bt_02_mot_de_passe_1_caractere` (`xfail`)

**Étapes :**

1. Créer un compte avec le mot de passe `a`.

**Résultat attendu :** refus (longueur/complexité minimale).

**Résultat obtenu :** le compte est créé et la connexion fonctionne.

**Impact :** comptes vulnérables au brute force.

**Correctif recommandé :** longueur minimale (8+), complexité, blocage après
plusieurs échecs.

---

## BUG-12 – Normalisation silencieuse du nom d'utilisateur

- **Module :** RSVA
- **Sévérité :** High
- **Priorité :** High
- **Test :** RSVA-BT-03
- **Automatisé :** `test_rsva_authentication.py::test_rsva_bt_03_username_caracteres_speciaux` (`xfail`)

**Étapes :**

1. Se connecter avec `jojo!` / `bean`.

**Résultat attendu :** refus, car le username ne correspond pas exactement à un
compte existant.

**Résultat obtenu :** la connexion réussit : `jojo!` est transformé en `jojo`.
La casse est également ignorée sous Windows (`JOJO` fonctionne).

**Impact :** contournement de la correspondance exacte des identifiants,
ambiguïté de comptes, risque d'usurpation.

**Correctif recommandé :** ne pas modifier silencieusement le username ; valider
le format à l'inscription et comparer exactement à la connexion.

---

## BUG-13 – Mots de passe stockés en clair

- **Module :** RSVA
- **Sévérité :** Critical
- **Priorité :** Highest
- **Test :** audit du stockage
- **Automatisé :** non (vérification fichier)

**Constat :** le fichier `cgi-bin/users/jojo` contient :

```text
bean
Jojo;Bean
...
```

Le mot de passe `bean` est stocké en clair, de même que pour les autres comptes.

**Impact :** compromission de tous les comptes en cas d'accès au système de
fichiers ou à une sauvegarde.

**Correctif recommandé :** hachage salé (bcrypt/Argon2), ne jamais stocker le
mot de passe en clair.

---

## BUG-14 – Aucune validation de la carte bancaire

- **Module :** RSVF
- **Sévérité :** High
- **Priorité :** High
- **Test :** RSVF-FT-03 (variante)
- **Automatisé :** scénario API

**Étapes :**

1. Réserver un vol.
2. Laisser les champs **Credit Card** et **Exp Date** vides.
3. Cliquer sur **Next**.

**Résultat attendu :** refus avec message de validation.

**Résultat obtenu :** la facture est générée avec
`Total Charged to Credit Card #` vide.

**Impact :** réservations sans paiement valide, données de facturation
incohérentes.

**Correctif recommandé :** validation du numéro (Luhn), de la date d'expiration
et des champs obligatoires.

---

## BUG-15 – Absence de jetons anti-CSRF

- **Module :** Tous
- **Sévérité :** Medium
- **Priorité :** Medium
- **Test :** audit des formulaires
- **Automatisé :** non

**Constat :** les formulaires de réservation, de suppression d'itinéraire et
d'administration ne contiennent aucun jeton CSRF. Un POST forgé
(`removeAllFlights.x=1`, `buyFlights.x=1`, `admin.pl?save=Update`) est accepté.

**Impact :** un site tiers peut faire effectuer des actions à un utilisateur
connecté (suppression de réservations, achat, modification de configuration).

**Correctif recommandé :** jeton CSRF unique par session/formulaire, vérifié
côté serveur, et cookies `SameSite`.

---

## 3. Preuves

Les captures sont disponibles dans `docs/evidence/` :

| Fichier | Contenu |
|---|---|
| `01_reservations_sans_login.png` | Formulaire de recherche accessible sans login |
| `02_admin_sans_login.png` | Page d'administration accessible sans login |
| `03_idor_admin_itinerary.png` | Itinéraire de admin via cookie forgé |
| `04_prix_modifie.png` | Page de paiement à 1 $ après manipulation du POST |
| `04b_facture_prix_modifie.png` | Facture à 1 $ après manipulation du POST |
| `05_date_invalide.png` | Page incomplète après date invalide |

## 4. Conclusion

L'application Web Tours est fonctionnelle sur les parcours nominaux, mais elle
présente des **failles de sécurité majeures** : absence de contrôle d'accès,
confiance aveugle dans les données client (prix, flightID, cookie), stockage de
mots de passe en clair et absence de protection CSRF. Ces anomalies doivent être
corrigées avant toute mise en production.
