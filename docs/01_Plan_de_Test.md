# Plan de test – Web Tours

## 1. Informations générales

| Élément | Valeur |
|---|---|
| Projet | WebTours QA |
| Application testée | Web Tours – site de réservation de vols |
| URL | http://127.0.0.1:1080/WebTours/index.htm |
| Type de test | Manuel (Jira/Xray) + automatisé (Selenium/pytest) |
| Version | 1.0 |
| Auteur | Équipe QA |
| Date | 09/11/2026 |

## 2. Objectifs

- Vérifier le bon fonctionnement des parcours principaux : authentification,
  recherche/réservation de vols, gestion de l'itinéraire.
- Vérifier la robustesse face aux saisies invalides et aux valeurs limites.
- Vérifier les contrôles d'accès et la sécurité des échanges (prix, identifiants,
  cookies, pages d'administration).
- Détecter et documenter les anomalies.
- Fournir une base de régression automatisée exécutable en CI.

## 3. Périmètre

### 3.1 Inclus

| Module | Fonctionnalités |
|---|---|
| RSVA – Authentification | Login, logout, inscription, validation des identifiants |
| RSVF – Vols | Recherche aller simple / aller-retour, sélection, paiement, facture |
| RSVI – Itinéraire | Affichage, suppression d'un vol, suppression de tous les vols |

### 3.2 Exclu

- Paiement réel (application de démonstration, aucune passerelle bancaire).
- Tests de charge et de performance.
- Tests multi-navigateurs exhaustifs (Chrome/Edge testés).
- Administration avancée du serveur Apache.
- Applets Java de calendrier (non supportés par les navigateurs modernes).

## 4. Stratégie de test

Quatre types de tests sont utilisés :

| Code | Type | Objectif |
|---|---|---|
| **FT** | Functional Testing | Vérifier les parcours nominaux (connexion, recherche, itinéraire). |
| **ET** | Error Testing | Vérifier la gestion des erreurs et des saisies invalides. |
| **BT** | Boundary Testing | Vérifier les valeurs limites (longueur, nombre de passagers, dernier vol). |
| **PT** | Permission Testing | Vérifier les contrôles d'accès, l'authentification et l'intégrité des données. |

La campagne contient **14 tests** :

- **9 tests ciblés** (3 par module) : scénarios **réels qui échouent** ou qui
  font planter l'application (page blanche, erreur serveur, faille d'accès) ;
- **5 tests de non-régression** qui doivent **passer** (connexion valide,
  mot de passe incorrect, recherche aller simple et aller-retour, affichage de
  l'itinéraire après réservation).

Cela donne une exécution **5 PASSED / 9 FAILED**, avec à la fois la preuve des
anomalies et la confirmation que les parcours principaux fonctionnent.

### 4.1 Priorisation

| Priorité | Description |
|---|---|
| Critical | Sécurité ou intégrité financière ; à corriger immédiatement. |
| High | Parcours principal ou anomalie bloquante. |
| Medium | Fonction secondaire ou validation manquante. |
| Low | Confort, message, cas limite peu fréquent. |

## 5. Environnement de test

| Composant | Configuration |
|---|---|
| Système | Windows 10/11 |
| Java | Java 8 (JRE/JDK) |
| Perl | Strawberry Perl 5.10.1.0 |
| Serveur | Apache 2.2.21 + CGI Perl, port 1080 |
| Application | WebTours 1.0 – `D:\web tours\WebTours` |
| Navigateurs | Google Chrome, Microsoft Edge |
| Automatisation | Python 3.12, Selenium 4.51, pytest 9.1, requests, BeautifulSoup |
| CI | Jenkins (Pipeline) |
| Gestion des tests | Jira + Xray |

## 6. Données de test

| Donnée | Valeur |
|---|---|
| Compte existant | `jojo` / `bean` |
| Compte admin | `admin` / `admin` |
| Compte de test | `qa<horodatage>` / `Passw0rd!` (créé et supprimé par les tests) |
| Trajet nominal | Denver → Paris |
| Trajet aller-retour | Denver ↔ Paris |
| Date | Demain (calculée dynamiquement, format MM/DD/YYYY) |
| Carte de test | `4111111111111111`, expiration `12/28` |
| Passagers | 1 (nominal), 0 / 999 (limites), 8 (limite interface) |

## 7. Critères d'entrée

- WebTours démarré et accessible sur le port 1080.
- Comptes `jojo` et `admin` disponibles.
- Jeu de données de test connu.
- Environnement Python et dépendances installés.
- Accès Jira/Xray opérationnel.

## 8. Critères de sortie

- Les 14 tests manuels ont été exécutés et tracés dans Xray.
- Tous les tests Critical/High ont un statut (PASS/FAIL) et une anomalie associée
  en cas d'échec.
- La suite automatisée s'exécute sans erreur d'infrastructure.
- Le rapport de bugs est complet et reproductible.
- Le rapport HTML pytest est archivé.

## 9. Livrables

- Plan de test (ce document).
- User stories Jira.
- 14 fiches de test manuelles.
- Fichiers d'import Xray.
- Rapport d'exécution Xray.
- Rapport de bugs avec preuves.
- Suite de tests automatisés + rapport HTML.
- Jenkinsfile et documentation CI.
- Dépôt Git.

## 10. Risques et mitigation

| Risque | Impact | Mitigation |
|---|---|---|
| Application ancienne (Apache 2.2, Perl 5.10) | Instabilité, incompatibilités | Utiliser Java 8 et Strawberry Perl 5.10.1.0 ; documenter la configuration. |
| Chemins avec espace (`D:\web tours`) | Erreur 403 Apache | Chemins absolus dans `httpd.conf` (voir doc installation). |
| Données persistantes entre exécutions | Tests non idempotents | Comptes uniques + nettoyage des fichiers utilisateurs. |
| Applets Java de calendrier | Non exécutables | Saisie manuelle de la date au format MM/DD/YYYY. |
| Absence de serveur de messagerie | Pas de notification | Non applicable. |
| Bugs de sécurité nombreux | Blocage de la recette | Anomalies Critical documentées et priorisées. |

## 11. Matrice de traçabilité

| User Story | Tests |
|---|---|
| WT-US-01 – Authentification | RSVA-FT-01, RSVA-ET-01, RSVA-BT-03, RSVA-PT-01, RSVA-PT-03 |
| WT-US-02 – Inscription | RSVA-FT-01, RSVA-ET-01, RSVA-BT-03 |
| WT-US-03 – Recherche et réservation | RSVF-FT-01, RSVF-FT-02, RSVF-ET-01, RSVF-PT-01, RSVF-PT-02 |
| WT-US-04 – Itinéraire | RSVI-FT-01, RSVI-PT-01, RSVI-PT-02, RSVI-PT-03 |
| WT-US-05 – Déconnexion | – (hors campagne) |
| WT-US-06 – Sécurité et permissions | RSVA-PT-01, RSVA-PT-03, RSVF-PT-01, RSVF-PT-02, RSVI-PT-01, RSVI-PT-02, RSVI-PT-03 |

## 12. Calendrier indicatif

| Phase | Durée | Activités |
|---|---|---|
| Préparation | 1 jour | Installation, plan de test, user stories, jeu de données |
| Conception | 1 jour | 14 cas de test (9 ciblés + 5 non-régression), import Xray, revue |
| Exécution manuelle | 2 jours | Exécution, captures, anomalies |
| Automatisation | 2 jours | Page Objects, tests, exécution, rapport |
| CI / Git | 0,5 jour | Dépôt, Jenkinsfile, exécution Jenkins |
| Bilan | 0,5 jour | Rapport final, synthèse |

## 13. Résultats attendus

À l'issue de la campagne :

- **9 tests FAIL** couvrant **8 anomalies distinctes**, dont **5 critiques** ;
- **5 tests PASS** prouvant que les parcours principaux fonctionnent ;
- une suite automatisée de 14 tests (9 `xfail` + 5 PASS) couvrant la sécurité,
  les crashs et la non-régression ;
- une exécution Jenkins verte (les bugs connus sont marqués `xfail`).
