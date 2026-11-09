# RSVI-BT-01 – Itinéraire avec un seul passager

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | BT – Boundary Testing |
| Priorité | Medium |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_bt_01_un_passager` |
| Tags | WebTours, RSVI, BT, RSVI-BT-01 |

**Statut : Passé**

## Préconditions

- L'utilisateur est connecté.

## Données de test

- `numPassengers = 1`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Réserver un vol pour 1 passager. | La réservation est enregistrée. |
| 2 | Ouvrir l'itinéraire. | Un seul billet est affiché et le total correspond à 1 passager. |

## Résultat obtenu

Un billet affiché.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
