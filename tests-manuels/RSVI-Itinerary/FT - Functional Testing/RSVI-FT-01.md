# RSVI-FT-01 – Affichage de l'itinéraire après une réservation

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_ft_01_affichage_apres_reservation` |
| Tags | WebTours, RSVI, FT, RSVI-FT-01 |

**Statut : Passé**

## Préconditions

- L'utilisateur est connecté.
- Au moins un vol a été réservé.

## Données de test

- `Vol Denver → Paris du lendemain`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Cliquer sur Itinerary dans le menu. | La page Itinerary s'affiche. |
| 2 | Vérifier les informations du vol. | Le vol, la date, le prix et les 4 derniers chiffres de la carte sont affichés. |

## Résultat obtenu

Itinéraire affiché avec les détails de la réservation.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
