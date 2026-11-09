# RSVF-BT-03 – Recherche avec un nombre de passagers très élevé (999)

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | BT – Boundary Testing |
| Priorité | Medium |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_bt_03_999_passagers` |
| Tags | WebTours, RSVF, BT, RSVF-BT-03 |

**Statut : Échoué – BUG-08** — voir `docs/04_Bugs_Detectes.md#bug-08`

## Préconditions

- Le formulaire Find Flight est affiché.

## Données de test

- `numPassengers = 999`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Saisir 999 passagers. | La valeur est saisie. |
| 2 | Cliquer sur Next (findFlights). | La recherche doit être refusée au-delà du maximum autorisé. |

## Résultat obtenu

Les vols sont affichés normalement ; aucune limite haute n'est appliquée.

> **Anomalie :** BUG-08. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
