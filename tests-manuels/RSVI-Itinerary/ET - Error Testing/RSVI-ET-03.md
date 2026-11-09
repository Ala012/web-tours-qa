# RSVI-ET-03 – Double suppression de tous les vols

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | ET – Error Testing |
| Priorité | Low |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_et_03_double_suppression` |
| Tags | WebTours, RSVI, ET, RSVI-ET-03 |

**Statut : Passé**

## Préconditions

- L'utilisateur possède une réservation.

## Données de test

- Aucune donnée spécifique.

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Cliquer une première fois sur Cancel All Reservations. | L'itinéraire est vidé. |
| 2 | Cliquer une seconde fois sur Cancel All Reservations. | Le système reste stable et affiche un itinéraire vide. |

## Résultat obtenu

Aucune erreur, itinéraire vide.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
