# RSVA-PT-02 – Accès direct à itinerary.pl sans être connecté

| Champ | Valeur |
|---|---|
| Module | RSVA – Authentification |
| Type | PT – Permission Testing |
| Priorité | High |
| User Story | WT-US-01 / WT-US-02 |
| Test automatisé | `test_rsva_authentication.py::test_rsva_pt_02_itinerary_sans_login` |
| Tags | WebTours, RSVA, PT, RSVA-PT-02 |

**Statut : Échoué – BUG-02** — voir `docs/04_Bugs_Detectes.md#bug-02`

## Préconditions

- Aucune session utilisateur n'est ouverte.

## Données de test

- `URL = /cgi-bin/itinerary.pl`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir directement l'URL de l'itinéraire. | L'application doit rediriger vers la page de connexion. |
| 2 | Vérifier le contenu affiché. | Aucune donnée d'itinéraire ne doit être accessible. |

## Résultat obtenu

La page Itinerary est affichée avec le message « No flights have been reserved ».

> **Anomalie :** BUG-02. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
