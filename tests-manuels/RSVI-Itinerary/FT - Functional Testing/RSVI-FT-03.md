# RSVI-FT-03 – Suppression de tous les vols de l'itinéraire

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_ft_03_suppression_tous_vols` |
| Tags | WebTours, RSVI, FT, RSVI-FT-03 |

**Statut : Passé**

## Préconditions

- L'utilisateur possède au moins une réservation.

## Données de test

- Aucune donnée spécifique.

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir l'itinéraire. | Les vols réservés sont listés. |
| 2 | Cliquer sur Cancel All Reservations. | Tous les vols sont supprimés et le message « No flights have been reserved » s'affiche. |

## Résultat obtenu

Itinéraire vidé.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
