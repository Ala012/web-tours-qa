# RSVI-BT-03 – Suppression du dernier vol de l'itinéraire

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | BT – Boundary Testing |
| Priorité | Medium |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_bt_03_dernier_vol` |
| Tags | WebTours, RSVI, BT, RSVI-BT-03 |

**Statut : Passé**

## Préconditions

- L'utilisateur possède exactement une réservation.

## Données de test

- Aucune donnée spécifique.

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir l'itinéraire. | Un vol est affiché. |
| 2 | Cocher le vol et cliquer sur Cancel Reservation. | L'itinéraire devient vide sans erreur. |

## Résultat obtenu

Dernier vol supprimé, itinéraire vide.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
