# RSVI-BT-02 – Itinéraire avec huit passagers (limite de l'interface)

| Champ | Valeur |
|---|---|
| Module | RSVI – Itinéraire |
| Type | BT – Boundary Testing |
| Priorité | Medium |
| User Story | WT-US-04 |
| Test automatisé | `test_rsvi_itinerary.py::test_rsvi_bt_02_8_passagers` |
| Tags | WebTours, RSVI, BT, RSVI-BT-02 |

**Statut : Passé**

## Préconditions

- L'utilisateur est connecté.

## Données de test

- `numPassengers = 8`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Réserver un vol pour 8 passagers. | Huit champs de nom de passager sont affichés. |
| 2 | Ouvrir l'itinéraire. | Le total est multiplié par 8 et les 8 passagers sont enregistrés. |

## Résultat obtenu

Réservation pour 8 passagers affichée.

## Statut d'exécution

- [x] Exécuté
- [x] Passé
- [ ] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
