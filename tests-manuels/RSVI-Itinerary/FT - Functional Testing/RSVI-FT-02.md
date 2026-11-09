# RSVI-FT-02 – Suppression d'un vol de l'itinéraire

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | FT – Functional Testing |
| Priorité | High |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_ft_02_suppression_un_vol` |
| Tags | WebTours, RSVI, FT, RSVI-FT-02 |

**Statut : Passé**

## Préconditions

- L'utilisateur possède au moins deux réservations.

## Données de test

- `Cocher le premier vol`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Ouvrir l'itinéraire. | Les vols réservés sont listés. |
| 2 | Cocher le premier vol et cliquer sur Cancel Reservation. | Le vol est supprimé et les autres vols restent affichés. |

## Résultat obtenu

Suppression effectuée, itinéraire mis à jour.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
