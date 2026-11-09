# RSVF-PT-03 – Accès direct à buyFlights sans sélection de vol

| Champ | Valeur |
|---|---|
| Module | RSVF – Vols |
| Type | PT – Permission Testing |
| Priorité | Critical |
| User Story | WT-US-03 |
| Test automatisé | `test_rsvf_flight.py::test_rsvf_pt_03_buy_direct` |
| Tags | WebTours, RSVF, PT, RSVF-PT-03 |

**Statut : Échoué – BUG-10** — voir `docs/04_Bugs_Detectes.md#bug-10`

## Préconditions

- L'utilisateur est connecté.

## Données de test

- `POST reservations.pl avec buyFlights.x=1 et des champs arbitraires`

## Étapes et résultats attendus

| # | Action | Résultat attendu |
|---|---|---|
| 1 | Envoyer directement une requête POST buyFlights sans passer par la recherche ni la sélection. | Le serveur doit refuser la requête. |
| 2 | Vérifier l'itinéraire. | Aucune réservation ne doit être enregistrée. |

## Résultat obtenu

Une réservation est créée et une facture est affichée.

> **Anomalie :** BUG-10. Voir le rapport de bugs pour les détails et les preuves.

## Statut d'exécution

- [x] Exécuté
- [ ] Passé
- [x] Échoué
- [ ] Bloqué

## Notes

Test exécuté sur l'environnement local WebTours (Windows, Java 8, Strawberry Perl, Apache 2.2, port 1080).
