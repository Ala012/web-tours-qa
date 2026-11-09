# RSVF-ET-01 – Recherche avec une date de départ vide

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | ET – Error Testing |
| Priorité | High |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_et_01_date_vide` |
| Tags | WebTours, RSVF, ET, RSVF-ET-01 |

**Statut : Échoué – BUG-05** — voir `docs/04_Bugs_Detectes.md#bug-05`

## Préconditions

- L'utilisateur jojo est connecté.
- Le formulaire Find Flight est affiché.

## Données de test

- `departDate = (vide)`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Vider le champ Departure Date. | Le champ est vide. |
| 2 | Cliquer sur Next (findFlights). | Un message de validation doit s'afficher et le formulaire doit rester utilisable. |

## Résultat obtenu

La page se limite au titre « Find Flight » : formulaire absent, aucun message d'erreur. Le log Apache contient « Month '-1' out of range ».

> **Anomalie :** BUG-05. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
