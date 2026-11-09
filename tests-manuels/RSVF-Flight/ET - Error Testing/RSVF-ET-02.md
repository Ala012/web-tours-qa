# RSVF-ET-02 – Recherche avec une date invalide (13/45/2026)

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | ET – Error Testing |
| Priorité | High |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_et_02_date_invalide` |
| Tags | WebTours, RSVF, ET, RSVF-ET-02 |

**Statut : Échoué – BUG-05** — voir `docs/04_Bugs_Detectes.md#bug-05`

## Préconditions

- Le formulaire Find Flight est affiché.

## Données de test

- `departDate = 13/45/2026`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Saisir 13/45/2026 dans Departure Date. | La valeur est saisie. |
| 2 | Cliquer sur Next (findFlights). | Un message d'erreur explicite doit être affiché. |

## Résultat obtenu

Page incomplète sans formulaire ni message d'erreur ; erreur Perl dans le log.

> **Anomalie :** BUG-05. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
