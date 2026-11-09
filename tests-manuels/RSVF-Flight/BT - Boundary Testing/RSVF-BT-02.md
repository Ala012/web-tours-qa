# RSVF-BT-02 – Recherche avec zéro passager

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | BT – Boundary Testing |
| Priorité | High |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_bt_02_zero_passager` |
| Tags | WebTours, RSVF, BT, RSVF-BT-02 |

**Statut : Échoué – BUG-08** — voir `docs/04_Bugs_Detectes.md#bug-08`

## Préconditions

- Le formulaire Find Flight est affiché.

## Données de test

- `numPassengers = 0`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Saisir 0 dans No. of Passengers. | La valeur 0 est saisie. |
| 2 | Cliquer sur Next (findFlights). | La recherche doit être refusée : le nombre de passagers doit être supérieur ou égal à 1. |

## Résultat obtenu

Les vols sont affichés normalement, sans validation.

> **Anomalie :** BUG-08. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
