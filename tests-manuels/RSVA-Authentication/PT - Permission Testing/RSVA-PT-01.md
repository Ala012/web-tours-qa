# RSVA-PT-01 – Accès direct à reservations.pl sans être connecté

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | PT – Permission Testing |
| Priorité | Critical |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_pt_01_reservations_sans_login` |
| Tags | WebTours, RSVA, PT, RSVA-PT-01 |

**Statut : Échoué – BUG-01** — voir `docs/04_Bugs_Detectes.md#bug-01`

## Préconditions

- Aucune session utilisateur n'est ouverte.

## Données de test

- `URL = /cgi-bin/reservations.pl?page=welcome`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir directement l'URL de recherche de vols sans passer par le login. | L'application doit rediriger vers la page de connexion. |
| 2 | Vérifier le contenu affiché. | Aucun formulaire de réservation ne doit être accessible sans authentification. |

## Résultat obtenu

Le formulaire « Find Flight » est affiché sans authentification.

> **Anomalie :** BUG-01. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
